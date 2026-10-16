"""Generate a reproducible synthetic IT incident dataset (no real customer data)."""
import argparse
import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

FIELDS = ["id","issue","priority","team","status","resolution_hours","sla_met","created_at","resolved_at","category","sla_target_hours"]
CATEGORIES = {
    "Network": ["VPN connection failure","Network latency","Wi-Fi outage","DNS issue"],
    "Access": ["Password reset / MFA","Account locked","SSO sign-in issue","Permission request"],
    "Applications": ["CRM application issue","Checkout application error","Application crash","API timeout"],
    "Service Desk": ["Laptop performance","Software installation","Printer unavailable","Device setup"],
}
PRIORITY_TARGETS = {"Critical":4,"High":8,"Medium":24,"Low":72}

def generate(count=600, seed=2026):
    if count < 1:
        raise ValueError("count must be positive")
    rng = random.Random(seed)
    start = datetime(2025, 1, 1, 8, tzinfo=timezone.utc)
    rows = []
    for i in range(count):
        team = rng.choice(list(CATEGORIES))
        priority = rng.choices(list(PRIORITY_TARGETS), weights=[8,22,45,25])[0]
        target = PRIORITY_TARGETS[priority]
        created = start + timedelta(hours=i * 12 + rng.randrange(12))
        status = rng.choices(["Resolved","Open","Pending"], weights=[80,12,8])[0]
        hours = round(max(0.25, rng.lognormvariate(0.0, 0.75) * target * 0.48), 2)
        resolved = created + timedelta(hours=hours) if status == "Resolved" else None
        rows.append({
            "id": f"INC-{10000+i}", "issue":rng.choice(CATEGORIES[team]),
            "priority":priority, "team":team, "status":status,
            "resolution_hours": hours if resolved else "",
            "sla_met": str(hours <= target).lower() if resolved else "",
            "created_at":created.isoformat(timespec="seconds"),
            "resolved_at":resolved.isoformat(timespec="seconds") if resolved else "",
            "category":team, "sla_target_hours":target
        })
    return rows

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count",type=int,default=600)
    parser.add_argument("--seed",type=int,default=2026)
    parser.add_argument("--output",type=Path,default=Path(__file__).resolve().parents[1]/"data"/"incidents_extended.csv")
    args=parser.parse_args()
    rows=generate(args.count,args.seed)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("w",newline="",encoding="utf-8") as stream:
        writer=csv.DictWriter(stream,fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} synthetic incidents to {args.output}")

if __name__=="__main__":
    main()
