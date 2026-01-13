#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "PyYAML",
#     "xero-python",
# ]
# ///
"""
Xero Balance Sheet Report Generator

This script fetches and displays the Balance Sheet report from Xero for a specified date.

Usage:
    ./xero_balance_sheet_report.py [options]

Options:
    --date YYYY-MM-DD        Date for the report (default: 2025-12-31)

Examples:
    ./xero_balance_sheet_report.py
    ./xero_balance_sheet_report.py --date 2024-12-31
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


def load_token(token_file=".xero_token.json"):
    if not os.path.exists(token_file):
        print("Token file not found. Please run xero_connect.py first.")
        return None
    with open(token_file, "r") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Generate Xero Balance Sheet Report")
    # Default to end of current year if not specified
    current_year = date.today().year
    default_date = f"{current_year}-12-31"
    parser.add_argument(
        "--date",
        help=f"Report date (YYYY-MM-DD) (default: {default_date})",
        default=default_date,
    )
    args = parser.parse_args()

    try:
        report_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    except ValueError:
        print("Error: Date must be in YYYY-MM-DD format")
        sys.exit(1)

    config = load_config()
    token_data = load_token()

    if not token_data:
        return

    # Create the token object first
    oauth2_token = OAuth2Token(client_id=config["CLIENT_ID"], client_secret=config["CLIENT_SECRET"])
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

    # 2. Get Balance Sheet Report
    accounting_api = AccountingApi(api_client)

    print(f"Fetching Balance Sheet as of {report_date}...")

    try:
        report = accounting_api.get_report_balance_sheet(tenant_id, date=report_date)

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
                        for section_row in row.rows:
                            cells = [c.value for c in section_row.cells]
                            # Format: Description ........... Value
                            if len(cells) >= 2:
                                print(f"{cells[0]:<40} {cells[1]:>15}")
                elif row_type_str == "RowType.ROW":
                    cells = [c.value for c in row.cells]
                    if len(cells) >= 2:
                        print(f"{cells[0]:<40} {cells[1]:>15}")
                elif row_type_str == "RowType.SUMMARYROW":
                    cells = [c.value for c in row.cells]
                    if len(cells) >= 2:
                        print("-" * 60)
                        print(f"{cells[0]:<40} {cells[1]:>15}")

    except Exception as e:
        print(f"Error fetching report: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
