# Inventory Stock Management System Using Data Structures and Algorithms

## Features
- Flask + SQLite inventory website with dashboard and charts
- Product catalog, unique SKU, search and sorting
- Stock inward/outward with validation against negative stock
- Low-stock alerts, transaction history, stock valuation reports
- Categories and supplier reference pages
- Python DSA helpers and C++17 demonstration

## Windows quick start
1. Install Python 3.10+ and extract this ZIP.
2. Open a terminal in the extracted folder.
3. Run:

```bat
py -m venv .venv
.venv\Scripts\activate
py -m pip install --upgrade pip
pip install -r requirements.txt
py app.py
```

4. Open http://127.0.0.1:5000
5. Demo login: **admin** / **admin123**

Database is created in `instance/inventory.db` on first run. To reset demo data, stop the app, delete that file, and run `py app.py` again.

## C++17 DSA demo
Compile with MinGW g++: `g++ -std=c++17 cpp\dsa_demo.cpp -o dsa_demo.exe` then run `dsa_demo.exe`.

## Academic deliverables
`docs/` contains synopsis, report, user manual, data dictionary, test plan, architecture diagram, editable DOCX report, PDF report, and 14-slide PPTX.

## Notes
This is a local academic demo. Change demo credentials/secret before deployment. The DSA stack is illustrative and does not undo committed database transactions. Categories and suppliers are seeded reference pages.
