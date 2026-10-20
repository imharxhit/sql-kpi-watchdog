# sql-kpi-watchdog

Automated daily revenue, checkout conversion, and cohort retention anomaly detector built for Business & Product Analytics teams.

Instead of manually running ad-hoc SQL queries across regional outlets and payment gateways every morning, `sql-kpi-watchdog` runs scheduled PostgreSQL/MySQL window-function diagnostics, flags any metric deviating by `>1.8σ` from its 28-day rolling baseline, executes a deterministic drill-down across SKU category and payment method logs, and posts a plain-English root-cause brief (with the exact SQL evidence) to Slack while refreshing the Power BI source table.

## Architecture
1. **Rolling Baseline Engine (`sql/cohort_baseline.sql`)**: Computes 28-day rolling mean and standard deviation (`STDDEV_SAMP`) partitioned by `region`, `channel`, and `day_of_week`.
2. **Diagnostic Agent (`src/watchdog_agent.py`)**: Orchestrates multi-step root-cause isolation using structured tool-calling (`inspect_gateway_failures`, `inspect_sku_stockouts`).
3. **Power BI & Slack Dispatcher**: Writes verified anomaly records for Power BI DAX cards and sends a structured alert to Slack.
