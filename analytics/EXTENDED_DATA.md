# Extended synthetic incident dataset

Generate **600 deterministic, synthetic incidents** with:

```bash
python analytics/generate_data.py
```

This creates `data/incidents_extended.csv` locally. To change the sample:

```bash
python analytics/generate_data.py --count 1000 --seed 2026
```

The generator includes ticket ID, issue, team, priority, status, resolution hours, SLA flag, creation and resolution timestamps, category, and SLA target hours. Targets are illustrative: Critical 4h, High 8h, Medium 24h, Low 72h. They are **not** an employer's real service agreement.

## Data assumptions
- Synthetic data only; no real users, employers, or customer records.
- Tickets are created approximately every 12 hours from January 2025.
- A fixed seed makes datasets reproducible.
- Open and Pending tickets have blank resolution outcomes; do not treat these as resolved.
- Resolution duration follows a synthetic log-normal distribution; no inference about real service desk performance is valid.
- Existing dashboard and `analytics/analyze.py` still use the original 10-record sample. The extended dataset is a **foundation for the next visualization and analytics iteration**, not yet connected to the deployed dashboard.
- SLA is modeled as a simple resolution-hours threshold; real SLAs may use business hours, pauses, escalation rules, and different priority definitions.

## Next tasks
1. Add time-series and team-level analytics for the extended schema.
2. Wire a CSV-driven dashboard to the extended data, with robust loading/error states.
3. Add browser-level tests and verify the live deployment.
4. Produce Power BI assets and a case-study narrative with defensible findings.
