# Inventory Stock Management System Using Data Structures and Algorithms
## 1. Introduction
Inventory tracking maintains accurate quantities and records of goods. This project offers a small browser-based system for product records and stock movement.
## 2. Problem statement
Manual tracking can create duplicate records, stock-count errors, and delayed replenishment.
## 3. Objectives
Maintain product catalog; record inward/outward transactions; prevent invalid stock changes; report low stock and valuation; demonstrate DSA.
## 4. Architecture
Browser UI → Flask routes → SQLAlchemy ORM → SQLite database. A separate C++17 file demonstrates DSA.
## 5. Functional requirements
Login; product search/add/delete/sort; stock inward/outward; low-stock list; reports; category and supplier pages.
## 6. Database schema
User(id, username, password_hash); Category(id, name); Supplier(id, name, company_name, contact_person, phone, email, address); Product(id, name, sku, quantity, purchase_price, selling_price, min_stock_level, unit, description, date_added, category_id, supplier_id); StockTransaction(id, product_id, transaction_type, quantity, note, created_at).
## 7. DSA concepts
Linear SKU search O(n); binary search on sorted names O(log n); sorting typically O(n log n); C++ unordered_map average O(1) lookup; queue FIFO; stack LIFO.
## 8. Testing
Unit tests cover SKU search, binary search, sorting, queue and stack. Manual tests: duplicate SKU rejected, outward stock cannot exceed quantity, invalid quantity rejected, low-stock alert appears at threshold.
## 9. Limitations
Basic demo login, reference-only categories/suppliers, no roles, and DSA undo stack does not reverse committed DB transactions.
## 10. Future scope
Role access, CSV/Excel export, purchase orders, barcode scanning, and transaction reversal with audit trail.
## 11. Conclusion
The application demonstrates inventory workflows, data modeling, validation, reports, and fundamental DSA concepts.
