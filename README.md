# IT Service Desk Analytics & Operations Dashboard

[Live dashboard](https://natinaelaberashi.github.io/cloud-desk-it-support/) · [Source code](https://github.com/natinaelaberashi/cloud-desk-it-support) · [CI results](https://github.com/natinaelaberashi/cloud-desk-it-support/actions)

A portfolio case study demonstrating **data analysis, operational reporting, incident management, SQL, Python, JavaScript, testing and continuous deployment**. All records are **synthetic**, and findings are illustrative rather than real business results.

## Business problem
Service desk managers need to understand incoming workload, unresolved incidents, resolution time and SLA outcomes, then identify where operational attention is needed.

## Dashboard features
- 600 synthetic tickets with creation and resolution timestamps, team, priority, status and SLA targets
- Interactive filters for priority, status and team
- Total tickets, unresolved backlog, **resolved-only** SLA compliance and average resolution hours
- Monthly ticket volume, priority distribution, team performance and recent incidents
- Responsive static website; no backend, user accounts or private data

## Data definitions
**Resolved SLA compliance** = resolved tickets flagged within target / all resolved tickets. **Average resolution time** = mean resolution hours among resolved tickets. Unresolved cases are excluded from both denominators. The sample SLA targets (Critical 4h, High 8h, Medium 24h, Low 72h) are hypothetical and not employer commitments.

## Run locally
Serve the site over HTTP because the browser loads CSV using `fetch`:

```bash
python -m http.server 8765
# open http://localhost:8765
```

Rebuild the committed synthetic dataset deterministically:

```bash
python analytics/generate_data.py
python -m unittest discover -s analytics -p 'test_*.py' -v
python analytics/analyze.py
```

The original `analytics/analyze.py` and `sql/service_desk_analysis.sql` operate on the small 10-ticket learning sample. The browser dashboard uses `data/incidents_extended.csv`. Do not mix their reported KPIs. For SQL examples, see `sql/service_desk_analysis.sql`.

## Automated quality checks
GitHub Actions checks Python tests, JavaScript syntax, 600-row CSV integrity, deterministic regeneration, and a headless Chromium test that exercises loading, filtering and reset behavior. The Pages workflow publishes `main`, then checks that the **public** site serves the expected HTML, JavaScript and 600-record CSV. [See workflow runs](https://github.com/natinaelaberashi/cloud-desk-it-support/actions).

To run the browser test locally:

```bash
pip install playwright==1.58.0
python -m playwright install chromium
python -m http.server 8765 &
python analytics/browser_test.py
```

## Findings and interpretation
This project is a demonstration of how to investigate SLA misses, backlog by priority, and team workload. Because the data is artificially generated, no performance figures should be represented as actual company outcomes. A production-ready extension would incorporate business-hour calendars, SLA pause logic, data freshness indicators, incident aging and audit trails.

## Project structure
- `index.html`, `style.css`, `app.js`: browser dashboard
- `data/incidents_extended.csv`: synthetic dashboard dataset
- `analytics/generate_data.py`: reproducible dataset generator
- `analytics/test_*.py`: validation and dashboard smoke tests
- `analytics/browser_test.py`: Chromium integration test
- `analytics/verify_live.py`: public deployment verification
- `sql/service_desk_analysis.sql`: illustrative SQL queries
- `ANALYTICS.md`, `analytics/EXTENDED_DATA.md`: assumptions, analysis and limitations

## Portfolio context
Demonstrates skills relevant to junior **Data Analyst, BI Analyst, IT Support, and Python** roles. Built as a static GitHub Pages project to make it easy for recruiters to inspect and run.
