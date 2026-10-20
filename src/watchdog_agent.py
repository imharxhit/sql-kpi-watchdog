#!/usr/bin/env python3
"""Automated SQL KPI Watchdog Agent with deterministic drill-down tools."""
import argparse
import json
from dataclasses import dataclass
from typing import Dict


@dataclass
class AnomalyEvent:
    metric_date: str
    region: str
    channel: str
    actual_conv_pct: float
    baseline_conv_pct: float
    z_score: float
    gmv_impact_inr: float


def inspect_gateway_failures(region: str, metric_date: str) -> Dict[str, object]:
    return {
        "dimension": "payment_gateway",
        "region": region,
        "date": metric_date,
        "top_failing_provider": "UPI_Provider_B",
        "failure_rate_pct": 28.4,
        "baseline_failure_rate_pct": 4.1,
        "failed_transactions": 1420,
    }


def inspect_sku_stockouts(region: str, metric_date: str) -> Dict[str, object]:
    return {
        "dimension": "sku_inventory",
        "region": region,
        "date": metric_date,
        "top_stockout_category": "Beverages_ColdBrew_Pack",
        "out_of_stock_views": 310,
        "estimated_lost_orders": 28,
    }


def synthesize_root_cause_brief(anomaly: AnomalyEvent) -> Dict[str, object]:
    gw = inspect_gateway_failures(anomaly.region, anomaly.metric_date)
    sku = inspect_sku_stockouts(anomaly.region, anomaly.metric_date)
    return {
        "alert_header": f"[{anomaly.metric_date}] {anomaly.region} ({anomaly.channel}) Conversion {anomaly.actual_conv_pct}% vs {anomaly.baseline_conv_pct}% (z = {anomaly.z_score})",
        "primary_root_cause": f"Payment gateway '{gw['top_failing_provider']}' failure rate surged to {gw['failure_rate_pct']}% (vs {gw['baseline_failure_rate_pct']}% baseline), accounting for {gw['failed_transactions']} dropped checkouts.",
        "secondary_factor": f"SKU category '{sku['top_stockout_category']}' recorded {sku['out_of_stock_views']} OOS product views.",
        "estimated_gmv_at_risk_inr": anomaly.gmv_impact_inr,
        "recommended_action": "Enable automatic UPI gateway failover when 5-min error rate > 8%.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SQL KPI Watchdog")
    parser.add_argument("--run-date", default="2026-04-15")
    args = parser.parse_args()
    sample_anomaly = AnomalyEvent(
        metric_date=args.run_date,
        region="West_Indore_Cluster",
        channel="Mobile_App",
        actual_conv_pct=3.12,
        baseline_conv_pct=4.45,
        z_score=-2.41,
        gmv_impact_inr=482000.0,
    )
    print(json.dumps(synthesize_root_cause_brief(sample_anomaly), indent=2))
