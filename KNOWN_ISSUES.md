# Known Issues

## Koinly loan repayment mapping bug

- **What happens:** The Koinly → Xero sync misclassifies loan repayments, creating manual journals that debit the
  configured realized P&L account instead of a liability account, overstating losses/expenses. (Ref:
  https://feedback.koinly.io/bug-reports-public/p/xero-integration-loan-repayments-incorrectly-booked-as-realized-losses-pl-debit)
- **Why it matters:** Profit & Loss reports show large artificial losses while liabilities remain unchanged, causing a
  balance-sheet/P&L mismatch.
- **Scope observed:** A small set of draft manual journals produced by the Koinly-to-Xero integration exhibit this
  mapping error.
- **Workarounds:**
  - Manually reclassify the draft journals to a liability account before approving them.
  - If possible, update the integration mapping so loan repayments post to a liability account rather than P&L.
