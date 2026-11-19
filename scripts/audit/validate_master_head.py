"""Validate the dated master-head delta and its explicit submodule boundary."""

import csv
import json


def validate(root):
    def read(path):
        return json.loads((root / path).read_text(encoding="utf-8-sig"))

    prefix = "knowledge/reviews/master-head-20261119/"
    accepted = read(prefix + "accepted-deltas.json")
    ledger = read(prefix + "iterations.json")
    summary = read("source-audits/master/2026-11-19/audit-summary.json")
    tree = read("source-audits/master/2026-11-19/tree-comparison.json")
    boundary = read("source-audits/master/2026-11-19/submodule-boundary.json")
    head = "a44f4ed69470f1bc00c800e592eadfce1bac6053"
    previous = "a8ce2c23dead8552d2c4699e4a9b9134f7a18707"

    if {accepted["master_head"], ledger["master_head"], summary["reviewed_head_commit"]} != {head}:
        raise ValueError("Unexpected master-head audit pin")
    if {accepted["previous_master"], ledger["previous_master"], summary["previous_audited_commit"]} != {previous}:
        raise ValueError("Unexpected previous master pin")
    if tree["counts"] != {"old_entries": 10629, "new_entries": 10629,
                           "identical_non_changed_entries": 10628, "changed_entries": 1}:
        raise ValueError("Unexpected master-head tree counts")
    manifest = tree["non_changed_entry_manifest"]
    if not manifest["equal"] or manifest["old"] != manifest["new"]:
        raise ValueError("Parent tree carry-forward is not proven")
    change = tree["changes"]
    if len(change) != 1 or change[0]["path"] != "index_archivos/intercambioDocumental":
        raise ValueError("Unexpected master-head changed path")
    if change[0]["old_oid"] != boundary["old_commit"] or change[0]["new_oid"] != boundary["new_commit"]:
        raise ValueError("Submodule pins disagree")
    if boundary["content_diff_executed"] or boundary["new_object_available_locally"]:
        raise ValueError("Submodule boundary overstates executed coverage")
    with (root / "source-audits/master/2026-11-19/consumers.csv").open(encoding="utf-8", newline="") as handle:
        if len(list(csv.DictReader(handle))) != 8:
            raise ValueError("Unexpected submodule consumer inventory")
    records = accepted["deltas"]
    counts = {"new_findings": sum(r["classification"] == "new_finding" for r in records),
              "improvements": sum(r["classification"] == "improvement" for r in records)}
    if counts != accepted["counts"] or len({r["id"] for r in records}) != len(records):
        raise ValueError("Master-head delta classification/count mismatch")
    streak = 0
    for version, iteration in enumerate(ledger["iterations"], 1):
        if iteration["version"] != version or iteration["status"] != "completed":
            raise ValueError("Invalid master-head iteration receipt")
        if not iteration["new_findings"] and not iteration["improvements"]:
            streak += 1
        else:
            streak = 0
    if not ledger["converged"] or streak != ledger["consecutive_zero_delta_passes"] or streak < 2:
        raise ValueError("Master-head convergence criterion not reached")
    return {**counts, "master_head": head, "completed_passes": len(ledger["iterations"]),
            "consecutive_zero_delta_passes": streak, "parent_scope": "CLOSED",
            "submodule_content": "NOT_AUDITED", "coverage": "PARTIAL"}
