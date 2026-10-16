# Service Desk Analytics — Analyst Case Study

## Business question
Which teams and priorities contribute to support workload, and how efficiently are resolved incidents handled?

## Data and scope
The sample is **10 synthetic incidents**, not production records. It is too small for statistical inference, forecasting, or claims about real employers. The dataset contains no timestamps, so monthly trends and time-to-SLA cannot be inferred.

## Reproduce
Requires Python 3.10+; no third-party Python packages.

```bash
python analytics/analyze.py
python analytics/analyze.py --output metrics.json
python -m unittest discover -s analytics -p 'test_*.py' -v
```

SQL examples are in `sql/service_desk_analysis.sql`. Import `data/incidents.csv` into a SQLite table named `incidents` (columns matching CSV headers); then execute the queries.

## Definitions
- **Ticket volume**: all records.
- **Backlog**: Open + Pending.
- **Resolved SLA compliance**: resolved records with `sla_met=true` divided by all resolved records. Unresolved cases are excluded rather than automatically counted as successes or failures.
- **Average resolution hours**: mean `resolution_hours` across resolved records only.
- **Team workload**: count of records assigned to each team.

## Findings from the supplied sample
- 10 tickets total; 7 resolved and 3 open/pending.
- 6 of 7 resolved tickets are flagged as meeting SLA (85.71%).
- Mean resolved duration is approximately 3.19 hours.
- These are descriptive observations of synthetic records, not real-world performance benchmarks.

## Recommendations
1. Triage the three unresolved tickets; prioritize the critical pending application incident.
2. Investigate the resolved high-priority network incident marked as an SLA miss.
3. Add timestamps, actual SLA targets, and a larger representative dataset before attempting time-series analysis or reliable service-level comparisons.

## Limitations
The source CSV includes `resolution_hours` and `sla_met` values even for unresolved tickets. These are **not** treated as final resolution outcomes in the Python and SQL calculations. SLA flags are taken as provided, not independently recalculated from timestamps. This case study deliberately avoids implying otherwise.

## Deployment
The existing static dashboard is intended for GitHub Pages. This analytics extension uses Python only during local/CI analysis; it requires no production backend and does not expose sensitive data. Verify Pages settings and workflow status before describing a live deployment as successful.
