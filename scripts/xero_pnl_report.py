#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "PyYAML",
#     "xero-python",
# ]
# ///
"""
Xero Profit and Loss Report Generator

This script fetches and displays the Profit and Loss report from Xero for a specified date range.

Usage:
    ./xero_pnl_report.py [options]

Options:
    --start-date YYYY-MM-DD  Start date for the report (default: 2025-01-01)
    --end-date YYYY-MM-DD    End date for the report (default: 2025-12-31)

Examples:
    ./xero_pnl_report.py
    ./xero_pnl_report.py --start-date 2024-01-01 --end-date 2024-12-31
"""
import argparse
import os
import json
import yaml
import sys
from datetime import date, datetime
from xero_python.api_client import ApiClient
from xero_python.api_client.configuration import Configuration
from xero_python.api_client.oauth2 import OAuth2Token
from xero_python.identity import IdentityApi
from xero_python.accounting import AccountingApi


def load_config(config_file="xero_config.yaml"):
    with open(config_file, "r") as f:
        return yaml.safe_load(f)


def load_token(token_file=".token.json"):
    if not os.path.exists(token_file):
        print("Token file not found. Please run xero_connect.py first.")
        return None
    with open(token_file, "r") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Generate Xero Profit and Loss Report")
    # Default to current year
    current_year = date.today().year
    default_start = f"{current_year}-01-01"
    default_end = f"{current_year}-12-31"

    parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD) (default: {default_start})",
        default=default_start,
    )
    parser.add_argument(
        "--end-date",
        help=f"End date (YYYY-MM-DD) (default: {default_end})",
        default=default_end,
    )
    args = parser.parse_args()

    try:
        from_date = datetime.strptime(args.start_date, "%Y-%m-%d").date()
        to_date = datetime.strptime(args.end_date, "%Y-%m-%d").date()
    except ValueError:
        print("Error: Dates must be in YYYY-MM-DD format")
        sys.exit(1)

    config = load_config()
    token_data = load_token()

    if not token_data:
        return

    # Create the token object first
    oauth2_token = OAuth2Token(
        client_id=config["CLIENT_ID"], client_secret=config["CLIENT_SECRET"]
    )
    oauth2_token.update_token(**token_data)

    api_client = ApiClient(
        Configuration(debug=False, oauth2_token=oauth2_token),
        pool_threads=1,
    )

    @api_client.oauth2_token_getter
    def obtain_xero_oauth2_token():
        return token_data

    # 1. Get Tenant ID
    identity_api = IdentityApi(api_client)
    connections = identity_api.get_connections()

    if not connections:
        print("No connections found.")
        return

    tenant_id = connections[0].tenant_id
    print(f"Using Tenant: {connections[0].tenant_name}")

    # 2. Get Profit and Loss Report
    accounting_api = AccountingApi(api_client)

    print(f"Fetching P&L from {from_date} to {to_date}...")

    try:
        report = accounting_api.get_report_profit_and_loss(
            tenant_id, from_date=from_date, to_date=to_date
        )

        # The response is a ReportWithRows object
        # We need to traverse it to print nicely

        if report.reports:
            r = report.reports[0]
            print(f"\nReport: {r.report_name}")
            print(f"Title: {r.report_titles[0] if r.report_titles else ''}")
            print(f"Date: {r.report_date}")
            print("-" * 60)

            if not r.rows:
                print("No rows returned in the report.")
            else:
                print(f"Found {len(r.rows)} rows.")

            for row in r.rows:
                row_type_str = str(row.row_type)

                if row_type_str == "RowType.HEADER":
                    # Print headers
                    cells = [c.value for c in row.cells]
                    print(f"{' | '.join(cells)}")
                    print("-" * 60)
                elif row_type_str == "RowType.SECTION":
                    print(f"\n--- {row.title} ---")
                    if row.rows:
                        for sub_row in row.rows:
                            sub_row_type_str = str(sub_row.row_type)
                            if sub_row_type_str == "RowType.ROW":
                                cells = [c.value for c in sub_row.cells]
                                # Format: Label ... Value
                                label = cells[0]
                                values = cells[1:]
                                print(f"{label:<40} {', '.join(values)}")
                            elif sub_row_type_str == "RowType.SUMMARYROW":
                                cells = [c.value for c in sub_row.cells]
                                label = cells[0]
                                values = cells[1:]
                                print(f"{label:<40} {', '.join(values)}")
                elif row_type_str == "RowType.ROW":
                    cells = [c.value for c in row.cells]
                    label = cells[0]
                    values = cells[1:]
                    print(f"{label:<40} {', '.join(values)}")
                elif row_type_str == "RowType.SUMMARYROW":
                    cells = [c.value for c in row.cells]
                    label = cells[0]
                    values = cells[1:]
                    print(f"TOTAL: {label:<33} {', '.join(values)}")

    except Exception as e:
        print(f"Error fetching report: {e}")


if __name__ == "__main__":
    main()
