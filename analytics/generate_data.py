"""Generate the exact committed 600-row synthetic dashboard CSV, with no dependencies."""
import argparse
import csv
import math
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
TARGETS = PRIORITY_TARGETS

class LCG:
    def __init__(self, seed):
        self.state = seed & 0xffffffff

    def random(self):
        self.state = (self.state * 1664525 + 1013904223) & 0xffffffff
        return self.state / 4294967296

def iso_js(dt):
    return dt.isoformat(timespec="milliseconds").replace("+00:00","Z")

def generate(count=600, seed=2026):
    if count < 1:
        raise ValueError("count must be positive")
    rng = LCG(seed)
    start = datetime(2025,1,1,8,tzinfo=timezone.utc)
    teams = list(CATEGORIES)
    priorities = list(TARGETS)
    rows = []
    for i in range(count):
        team = teams[int(rng.random()*4)]
        issue = CATEGORIES[team][int(rng.random()*4)]
        priority = priorities[int(rng.random()*4)]
        first_status = rng.random()
        if first_status < .8:
            status = "Resolved"
        else:
            status = "Open" if rng.random() < .55 else "Pending"
        target = TARGETS[priority]
        hours = max(.25, -math.log(max(.0001, 1-rng.random()))*target*.6)
        hours = float(f"{hours:.2f}")
        created = start + timedelta(hours=i*12 + int(rng.random()*12))
        resolved = created + timedelta(milliseconds=round(hours*3600000)) if status == "Resolved" else None
        rows.append({
            "id":f"INC-{10000+i}", "issue":issue,"priority":priority,"team":team,
            "status":status,"resolution_hours":f"{hours:.2f}" if resolved else "",
            "sla_met":str(hours <= target).lower() if resolved else "",
            "created_at":iso_js(created),"resolved_at":iso_js(resolved) if resolved else "",
            "category":team,"sla_target_hours":target
        })
    return rows

def write_csv(rows, path):
    with open(path,"w",newline="",encoding="utf-8") as stream:
        writer=csv.DictWriter(stream,fieldnames=FIELDS,lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count",type=int,default=600)
    parser.add_argument("--seed",type=int,default=2026)
    parser.add_argument("--output",type=Path,default=Path(__file__).resolve().parents[1]/"data"/"incidents_extended.csv")
    args=parser.parse_args()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    write_csv(generate(args.count,args.seed),args.output)
    print(f"Wrote {args.count} synthetic incidents to {args.output}")

if __name__=="__main__":
    main()
