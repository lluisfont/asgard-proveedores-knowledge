# Graphify iterative audit pass 3

Target: `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61`

Date: 2026-09-14

Scope: new iteration after the Brownfield and API-auditor passes. This pass
intentionally used different techniques: Graphify query over the existing graph,
CLI/documentation drift checks, Windows-focused install/uninstall tests, XML
negative probes, import-cycle analysis, generated-artifact validation, pyright,
vulture, packaging, graph health diagnostics, and targeted pytest slices.

Stop criterion: after the last new finding, two consecutive closure iterations
added no new findings:

- Closure 1: `compileall`, configured `ruff check`, `test_skillgen.py`, and
  `test_wheel_packaging.py` were clean.
- Closure 2: pytest collection, `pip check`, and `graphify diagnose multigraph`
  were clean or unchanged.

Graphify note: queries used the existing `graphify-out/graph.json` with 13,712
nodes. No graph rebuild or LLM extraction was performed in this pass.

## New findings in this pass

### P1 - POM manifest parsing expands internal XML entities

`graphify/manifest_ingest.py` parses `pom.xml` with the standard ElementTree
path. A negative probe showed that `graphify.extract._project_xml_is_safe`
correctly rejects a POM containing a `DOCTYPE`, but
`extract_package_manifest()` still accepts the same content and expands internal
entities into package labels.

Evidence:

- `graphify/manifest_ingest.py:80` exposes `extract_package_manifest()`.
- `tests/test_manifest_ingest.py:67` covers normal POM parsing, but not unsafe
  XML constructs.
- Probe result: internal entity label became `g:EXPANDED`; a small
  entity-expansion payload produced a 300-character expanded label.

Risk: a crafted `pom.xml` can produce unexpected entity-expanded data in the
graph. External entities errored in this environment, but relying on default XML
parser behavior is fragile.

Recommended fix: reuse `_project_xml_is_safe` before parsing POM files or switch
this parser path to `defusedxml`.

### P1 - `collect_files()` drops absolute paths located under `.graphify`

When `collect_files()` receives an absolute target inside a path that contains a
`.graphify` component, it returns no files because it checks every component of
`target.parts` against `_is_noise_dir()`.

Evidence:

- `graphify/extract.py:7784` defines `collect_files()`.
- `graphify/extract.py:7792` returns `[]` when any component is a noise dir.
- `graphify/detect.py:846` lists `.graphify` as a noise dir.
- Reproduction in this checkout:
  - `collect_files(Path("tests/fixtures"))` -> 109 files.
  - `collect_files(Path("tests/fixtures").resolve())` -> 0 files.
- Reproduced failing test:
  - `tests/test_extract.py::test_collect_files_from_dir`

Risk: Graphify-managed clones under `~/.graphify/repos/...` can become
self-hostile when callers pass absolute paths. Skills and tooling often operate
with absolute paths, so this can silently create empty extraction inputs.

Recommended fix: only apply noise-dir pruning to path components below the
scan root, not to ancestor directories outside the target tree.

### P1 - Windows atomic writes can clobber read-only destinations

The Windows-specific atomic-write contract says a read-only destination should
not be silently overwritten. The focused test fails: `graph.json` is replaced
with new content even though the test expected `PermissionError` and preservation
of the original content.

Evidence:

- `graphify/paths.py:88` defines `_atomic_replace()`.
- `graphify/paths.py:155` exposes `write_text_atomic()`.
- `tests/test_atomic_writes.py:58` documents the Windows read-only contract.
- Reproduced failing test:
  - `tests/test_atomic_writes.py::test_write_text_atomic_refuses_a_readonly_destination_without_leaking_a_temp`
  - Actual content became `replaced` instead of `original`.

Risk: user-marked read-only graph/report files can be overwritten on Windows,
contradicting the repository's own regression test and comments.

Recommended fix: explicitly detect the Windows read-only attribute before the
replace path, or update the documented/tested contract if overwrite is now
intended.

### P1 - Pyright is configured but currently reports 579 errors

`pyright` is in the dev dependencies and configured in `pyproject.toml`, but the
current run fails heavily.

Evidence:

- `pyproject.toml:121` includes `pyright>=1.1.409`.
- `pyproject.toml:172` configures `include = ["graphify", "tests"]`.
- `python -m pyright --outputjson` result:
  - 367 files analyzed.
  - 579 errors.
  - Top files: `extract.py` 107, `serve.py` 72, `callflow_html.py` 42,
    `test_dart.py` 34, `engine.py` 32, `resolution.py` 29.
  - Top rules: `reportArgumentType` 241,
    `reportAttributeAccessIssue` 85, `reportOptionalSubscript` 69.
- `.github/workflows/ci.yml` does not run pyright.

Risk: type checking exists as a declared tool but has no enforceable baseline,
so regressions can accumulate unnoticed.

Recommended fix: either add pyright to CI with an explicit baseline/suppression
plan, or remove/de-scope the config so it is not a misleading signal.

### P2 - Gemini uninstall no longer removes global skill in two documented paths

Two uninstall-scope tests fail for Gemini. The tests plant a global
`.gemini/skills/graphify/SKILL.md`, call the uninstall API, and the global skill
remains.

Evidence:

- `graphify/install.py:856` defines `gemini_uninstall()`.
- `tests/test_uninstall_scope.py:63` expects bare calls to remove the global
  skill.
- `tests/test_uninstall_scope.py:76` expects `remove_user_skill=True` to remove
  the global skill.
- Reproduced failing tests:
  - `test_bare_call_still_removes_global[gemini]`
  - `test_remove_user_skill_opt_in_with_project_dir[gemini]`
- Captured output: `No GEMINI.md found in current directory - nothing to do`.

Risk: Gemini uninstall can leave orphaned progressive-disclosure skill files,
which is exactly the behavior the regression tests claim to prevent.

Recommended fix: compare `gemini_uninstall()` with `claude_uninstall()` and make
global skill removal independent of whether local `GEMINI.md` exists.

### P2 - Hermes install roundtrip test uses the wrong Windows user-scope assumption

The full install roundtrip slice fails for `user-hermes`. The test asserts that
the destination starts with `Path.home()`, while the implementation intentionally
uses `%LOCALAPPDATA%\hermes\skills` on Windows.

Evidence:

- `graphify/install.py:95` special-cases Hermes.
- `graphify/install.py:98` says Windows Hermes scans `%LOCALAPPDATA%`.
- `tests/test_install_roundtrip.py:70` asserts user-scope destinations start
  with `home`.
- Reproduced failing test:
  - `tests/test_install_roundtrip.py::test_skill_roundtrip_at_real_destination[user-hermes]`

Risk: Windows CI or local Windows runs fail for a platform-specific behavior the
implementation already documents.

Recommended fix: update the test invariant to allow `%LOCALAPPDATA%` for
Hermes, while still ensuring it stays inside the sandboxed test environment.

### P2 - C include cache write can fail near Windows path limits

The C include portability test fails on the second checkout name with a
`FileNotFoundError` from `tempfile.mkstemp()`. The directory path is 200
characters; the generated temp file path is 278 characters.

Evidence:

- `graphify/cache.py:1126` calls `tempfile.mkstemp()` in the cache directory.
- `tests/test_extract.py:1487` creates a deliberately long checkout name.
- Reproduced failing test:
  - `tests/test_extract.py::test_c_include_out_of_root_target_id_is_deterministic_across_checkout_paths`
- Measured path length for the failed temp file: 278 characters.

Risk: cache writes can fail on Windows in deeply nested checkouts despite the
cache temp name being hash based.

Recommended fix: add a Windows long-path guard/fallback for cache temp creation,
or route cache writes through the already-tested bounded atomic path helpers.

### P2 - Security tests are not hermetic because `validate_url()` performs real DNS

The security suite has six failures in this environment because `validate_url`
calls `socket.getaddrinfo()` for `example.com`. Several tests mock the opener
but not DNS, so fetch behavior is hidden behind network availability.

Evidence:

- `graphify/security.py:129` uses `socket.getaddrinfo()`.
- `tests/test_security.py:36` calls `validate_url("https://example.com/...")`.
- `tests/test_security.py:83` and related fetch tests mock response handling,
  but `safe_fetch()` still validates DNS first.
- Reproduced result: `tests/test_security.py` -> 6 failed, 54 passed.

Risk: CI or offline developer machines can fail on environment DNS rather than
on the behavior under test.

Recommended fix: mock `socket.getaddrinfo()` in these tests or use a URL
validation bypass for safe-fetch unit tests focused on response handling.

### P2 - Installation/documentation drift around `kimi`, `skills`, and extras

There are multiple small but user-visible drifts:

- Top-level `graphify --help` omits `kimi` and the `skills` alias from the
  `install --platform` list.
- `graphify install --help` includes `kimi` but still omits the `skills` alias.
- README documents `graphify install --platform kimi` and the `skills` alias.
- README optional extras list omits `kimi` and `watch`, although both exist in
  `pyproject.toml`.

Evidence:

- `graphify/__main__.py:536` prints the stale top-level platform list.
- `README.md:228` documents Kimi Code install.
- `README.md:230` documents `agents` with alias `skills`.
- `pyproject.toml:64` defines `watch = ["watchdog"]`.
- `pyproject.toml:77` defines `kimi = ["openai", "tiktoken"]`.
- `README.md:246` starts the optional extras table, which lacks both.

Risk: users can believe a supported platform or extra does not exist, while the
commands actually work.

Recommended fix: centralize platform/help rendering from `_PLATFORM_CONFIG` and
add README rows for `kimi` and `watch`.

### P2 - Multilingual docs still reference old repo and old capability counts

The translated docs lag behind the main README and still mention the old
repository identity and older language counts.

Evidence:

- `README.md:853` still shows `git clone https://github.com/safishamsi/graphify.git`.
- `graphify/wiki.py:268` still emits a footer for `github.com/safishamsi/graphify`.
- Many translated READMEs reference `safishamsi/graphify`, old branches, or
  older counts such as 25 languages while the main README says 37 grammars.

Risk: non-English users get stale installation and capability guidance, and
generated wiki output points at the former upstream identity.

Recommended fix: refresh translations from the current README source and update
the wiki footer to `Graphify-Labs/graphify`.

### P3 - Current graph input is polluted by root audit JSON artifacts

The current `graphify-out/manifest.json` includes generated audit files in the
repo root because they are not ignored by `.gitignore` or `.graphifyignore`.

Evidence:

- Manifest includes `bandit_v0961.json`, `pip_audit_v0961.json`, and
  `pyright_v0961.json`.
- Graph contains three nodes and two edges from `pip_audit_v0961.json`.
- `.gitignore` ignores `.graphify_*.json`, `graphify-out`, caches, dist/build,
  but not root-level `*_audit*.json`.

Risk: subsequent Graphify queries can treat audit outputs as source facts,
creating feedback noise in future audits.

Recommended fix: write audit outputs outside the target repo or add a
project-local `.graphifyignore` for audit/generated JSON.

### P3 - Four internal import cycles remain

AST import-cycle analysis over `graphify/*.py` found four cycles:

- `graphify.build -> graphify.dedup -> graphify.llm -> graphify.build`
- `graphify.__main__ <-> graphify.cli`
- `graphify.extract <-> graphify.extractors.markdown`
- `graphify.paths <-> graphify.security`

Evidence examples:

- `graphify/llm.py:1014` imports `_coerce_hyperedge_member_refs` from build.
- `graphify/build.py:1424` imports `deduplicate_entities`.
- `graphify/dedup.py:1098` imports backend helpers from llm.
- `graphify/cli.py:1060` imports `main` from `__main__`.
- `graphify/security.py:18` imports path constants from `paths`.
- `graphify/paths.py:492` lazily imports `check_graph_file_size_cap`.

Risk: currently importable, but these cycles make startup, typing, and
refactoring brittle.

Recommended fix: extract small shared helpers into leaf modules, starting with
the build/dedup/llm cycle.

### P3 - Vulture reports production/tool dead code

`vulture graphify tools --min-confidence 80` reported unused imports and one
unused variable in production/tool code.

Evidence:

- `graphify/cli.py:2494` unused import `_Opt`.
- `graphify/cli.py:2931` unused import `_bfj`.
- `graphify/cli.py:4349` unused import `_build_from_json`.
- `graphify/detect.py:563` unused import `qn`.
- `graphify/install.py:23` unused import `NoReturn`.
- `graphify/llm.py:15` unused import `Iterator`.
- `graphify/reflect.py:742` unused variable `fallback_outcome`.

Risk: low direct runtime risk, but useful cleanup and signal-to-noise reduction.

Recommended fix: remove confirmed-unused imports/variables or add explicit
allowlist comments if they are intentional dynamic hooks.

### P3 - Ruff formatter baseline is not clean if formatting is expected

`ruff check graphify tools tests` passes with the repository's conservative lint
selection, but `ruff format --check graphify tools tests` reports 347 files that
would be reformatted.

Evidence:

- `pyproject.toml:166` configures Ruff.
- `pyproject.toml:169` limits linting to fatal syntax/import-style rules.
- `python -m ruff format --check graphify tools tests` reports 347 files would
  be reformatted.

Risk: only relevant if the project expects Ruff formatting. As written, CI does
not enforce it, so this is a baseline/expectation issue rather than a failing
quality gate.

Recommended fix: either add formatter enforcement after a one-time format pass,
or document that Ruff is lint-only for now.

## Clean or unchanged checks

- `python -m pip check`: no broken requirements.
- `python -m compileall -q graphify tools tests`: passed.
- `python -m ruff check graphify tools tests`: passed.
- `python -m tools.skillgen --check`: 134 artifacts match.
- `python -m tools.skillgen --audit-coverage`: passed.
- `python -m tools.skillgen --schema-singleton`: passed.
- `python -m tools.skillgen --monolith-roundtrip`: passed.
- `python -m tools.skillgen --always-on-roundtrip`: passed.
- `python -m build --wheel --sdist --outdir dist_audit_pass3`: succeeded.
- `python -m pytest tests/test_wheel_packaging.py -q`: 133 passed.
- `python -m pytest tests/test_skillgen.py tests/test_wheel_packaging.py -q`:
  198 passed.
- `python -m pytest tests/test_backend_extras.py tests/test_llm_backends.py tests/test_backend_env_isolation.py -q`:
  116 passed.
- `python -m pytest --collect-only -q`: 5,569 tests collected.
- `graphify diagnose multigraph --graph graphify-out\graph.json --json`: no
  missing endpoints, dangling endpoints, self-loops, duplicate edges, or
  relation/source variants. It did report 12 producer-suppression sites as
  heuristic source evidence, unchanged from the diagnostic output.

## Environmental notes

- `pip-audit --strict` could not complete because this local Python environment
  contains `asgard-api-auditor 0.8.0`, which is not on PyPI. I did not count
  that as a Graphify finding.
- The cleanup command for temporary directories was rejected by the host policy.
  The verified temporary directories left in the repo are `dist_audit_pass3`,
  `tmp_audit_home_agents`, `tmp_audit_home_kimi`, `tmp_audit_home_skills`, and
  `build`. They are audit artifacts from this pass.
