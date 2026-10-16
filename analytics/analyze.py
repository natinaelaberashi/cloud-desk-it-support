"""Reproducible service desk metrics from synthetic incident CSV."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

REQUIRED = {"id", "issue", "priority", "team", "status", "resolution_hours", "sla_met"}
STATUSES = {"Resolved", "Open", "Pending"}
PRIORITIES = {"Critical", "High", "Medium", "Low"}


def load_tickets(path):
    with open(path, newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            raise ValueError(f"Missing required CSV columns: {sorted(REQUIRED - set(reader.fieldnames or []))}")
        tickets = []
        ids = set()
        for row in reader:
            ticket_id = row["id"].strip()
            if not ticket_id or ticket_id in ids:
                raise ValueError("Ticket IDs must be nonempty and unique")
            ids.add(ticket_id)
            if row["status"] not in STATUSES or row["priority"] not in PRIORITIES:
                raise ValueError(f"Invalid status or priority for {ticket_id}")
            try:
                hours = float(row["resolution_hours"])
            except (ValueError, TypeError) as exc:
                raise ValueError(f"Invalid hours for {ticket_id}") from exc
            if not 0 <= hours < float("inf"):
                raise ValueError(f"Invalid hours for {ticket_id}")
            if row["sla_met"].lower() not in {"true", "false"}:
                raise ValueError(f"Invalid SLA flag for {ticket_id}")
            row["resolution_hours"] = hours
            row["sla_met"] = row["sla_met"].lower() == "true"
            tickets.append(row)
    return tickets


def summarize(tickets):
    if not tickets:
        raise ValueError("Cannot summarize an empty dataset")
    resolved = [t for t in tickets if t["status"] == "Resolved"]
    # SLA compliance is measured on resolved tickets only; unresolved cases are excluded.
    return {
        "total_tickets": len(tickets),
        "resolved_tickets": len(resolved),
        "open_or_pending": len(tickets) - len(resolved),
        "sla_compliance_pct_resolved": round(100 * sum(t["sla_met"] for t in resolved) / len(resolved), 2) if resolved else None,
        "avg_resolution_hours_resolved": round(sum(t["resolution_hours"] for t in resolved) / len(resolved), 2) if resolved else None,
        "by_priority": dict(sorted(Counter(t["priority"] for t in tickets).items())),
        "by_team": dict(sorted(Counter(t["team"] for t in tickets).items())),
        "by_status": dict(sorted(Counter(t["status"] for t in tickets).items())),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path(__file__).resolve().parents[1] / "data/incidents.csv")
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()
    result = json.dumps(summarize(load_tickets(args.input)), indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result + "\n", encoding="utf-8")
    else:
        print(result)


if __name__ == "__main__":
    main()
