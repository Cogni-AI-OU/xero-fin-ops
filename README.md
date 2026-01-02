# Xero FinOps

CLI tools to manage Xero accounting data, automate journal entries, and generate financial reports via the Xero API.

## Setup

To use these scripts, you need to create a Xero App to get your API credentials (`CLIENT_ID` and `CLIENT_SECRET`).

1.  Go to [Xero Developer Portal](https://developer.xero.com/app/manage/) and create a new app.
2.  Select "Web app" as the integration type.
3.  Set the Redirect URI to `http://localhost:8888/callback`.
4.  Copy `xero_config.example.yaml` to `xero_config.yaml` and fill in your credentials.

## Scripts

### `xero_journal_manager.py`
Manage Xero Manual Journals via the API.
- **View**: List journals with powerful filtering (e.g., by AccountCode, Amount, Date).
- **Edit**: Fix incorrect journal entries (e.g., reassigning Account Codes for loan repayments).

### `xero_coa_manager.py`
Manage the Xero Chart of Accounts.
- **View**: List all accounts in the ledger.
- **Filter**: Search for specific accounts by code, name, or class.

### `xero_pnl_report.py`
Generate financial reports directly from the CLI.
- **Profit & Loss**: Fetch P&L for any custom date range.

### `xero_balance_sheet_report.py`
Generate Balance Sheet reports.
- **Balance Sheet**: Fetch Balance Sheet for any specific date.

### `xero_connect.py`
Handle authentication with the Xero API.
- **Connect**: Authenticate and generate the `.token.json` file required by other scripts.

