# Test Plan
1. Valid demo login opens dashboard.
2. Unique SKU product can be added.
3. Duplicate SKU is rejected.
4. Positive inward quantity increases stock.
5. Outward quantity within stock decreases stock.
6. Outward quantity above available stock is rejected.
7. Zero/negative quantities are rejected.
8. Quantity at/below minimum appears in low-stock list.
9. Python unit tests cover DSA helpers.
