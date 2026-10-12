# Data Dictionary
- User: id primary key, username unique, password_hash.
- Category: id primary key, unique name.
- Supplier: id primary key, name, company/contact fields, phone, email, address.
- Product: id, name, unique SKU, quantity, purchase/selling price, minimum stock level, unit, description, date added, optional category/supplier foreign keys.
- StockTransaction: id, product foreign key, transaction type, quantity, note, timestamp.
