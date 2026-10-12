from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from models import db, User, Product, Category, Supplier, StockTransaction
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


def login_required(f):
    @wraps(f)
    def w(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return w


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username', '')).first()
        if user and user.check_password(request.form.get('password', '')):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.context_processor
def globals():
    return {'current_user': session.get('username')}


@app.route('/')
@login_required
def dashboard():
    products = Product.query.order_by(Product.name).all()
    transactions = StockTransaction.query.order_by(StockTransaction.created_at.desc()).limit(8).all()
    low_stock = [p for p in products if p.quantity <= p.min_stock_level]
    categories = Category.query.order_by(Category.name).all()
    labels = [c.name for c in categories]
    values = [sum(p.quantity for p in c.products) for c in categories]
    total_value = sum(p.quantity * p.purchase_price for p in products)
    return render_template('dashboard.html', products=products, recent=transactions,
                           low_stock=low_stock, cat_labels=labels, cat_values=values,
                           total_value=total_value)


@app.route('/products')
@login_required
def products():
    q = request.args.get('q', '').lower()
    ps = Product.query.all()
    ps = [p for p in ps if q in p.name.lower() or q in p.sku.lower()]
    sort = request.args.get('sort', 'name')
    ps.sort(key=lambda p: getattr(p, {'quantity': 'quantity', 'price': 'selling_price'}.get(sort, 'name')),
            reverse=sort in ('quantity', 'price'))
    return render_template('products.html', products=ps, q=q, sort=sort,
                           categories=Category.query.all(), suppliers=Supplier.query.all())


@app.route('/products/add', methods=['POST'])
@login_required
def add_product():
    name = request.form.get('name', '').strip()
    sku = request.form.get('sku', '').strip().upper()
    if not name or not sku:
        flash('Name and SKU are required.', 'danger')
        return redirect(url_for('products'))
    if Product.query.filter_by(sku=sku).first():
        flash('SKU already exists.', 'danger')
        return redirect(url_for('products'))
    try:
        product = Product(
            name=name, sku=sku,
            quantity=max(0, int(request.form.get('quantity', 0))),
            purchase_price=max(0, float(request.form.get('purchase_price', 0))),
            selling_price=max(0, float(request.form.get('selling_price', 0))),
            min_stock_level=max(0, int(request.form.get('min_stock_level', 5))),
            unit=request.form.get('unit', 'pcs') or 'pcs',
            description=request.form.get('description', ''),
            category_id=int(request.form['category_id']) if request.form.get('category_id') else None,
            supplier_id=int(request.form['supplier_id']) if request.form.get('supplier_id') else None
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added.', 'success')
    except (ValueError, TypeError):
        db.session.rollback()
        flash('Check numeric values.', 'danger')
    return redirect(url_for('products'))


@app.route('/products/<int:pid>/delete', methods=['POST'])
@login_required
def delete_product(pid):
    product = db.session.get(Product, pid)
    if product:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted.', 'success')
    return redirect(url_for('products'))


def stock_move(kind):
    try:
        product = db.session.get(Product, int(request.form.get('product_id', 0)))
        quantity = int(request.form.get('quantity', 0))
        if not product or quantity <= 0 or (kind == 'OUTWARD' and quantity > product.quantity):
            raise ValueError
        product.quantity += quantity if kind == 'INWARD' else -quantity
        db.session.add(StockTransaction(product_id=product.id, transaction_type=kind,
                                        quantity=quantity, note=request.form.get('note', '')))
        db.session.commit()
        flash('Stock movement saved.', 'success')
    except (ValueError, TypeError):
        db.session.rollback()
        flash('Choose a product and valid quantity; outward cannot exceed available stock.', 'danger')
    return redirect(url_for('stock_inward' if kind == 'INWARD' else 'stock_outward'))


@app.route('/stock/inward', methods=['GET', 'POST'])
@login_required
def stock_inward():
    if request.method == 'POST':
        return stock_move('INWARD')
    return render_template('stock.html', products=Product.query.order_by(Product.name).all(), kind='INWARD')


@app.route('/stock/outward', methods=['GET', 'POST'])
@login_required
def stock_outward():
    if request.method == 'POST':
        return stock_move('OUTWARD')
    return render_template('stock.html', products=Product.query.order_by(Product.name).all(), kind='OUTWARD')


@app.route('/low-stock')
@login_required
def low_stock():
    products = [p for p in Product.query.order_by(Product.name).all() if p.quantity <= p.min_stock_level]
    return render_template('low_stock.html', products=products)


@app.route('/reports')
@login_required
def reports():
    products = Product.query.order_by(Product.name).all()
    transactions = StockTransaction.query.order_by(StockTransaction.created_at.desc()).all()
    total_value = sum(p.quantity * p.purchase_price for p in products)
    return render_template('reports.html', products=products, transactions=transactions, total_value=total_value)


@app.route('/categories')
@login_required
def categories():
    return render_template('categories.html', categories=Category.query.order_by(Category.name).all())


@app.route('/suppliers')
@login_required
def suppliers():
    supplier_list = Supplier.query.order_by(Supplier.name).all()
    return render_template('suppliers.html', suppliers=supplier_list)


@app.route('/suppliers/add', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            flash('Supplier name is required.', 'danger')
            return render_template('add_supplier.html')
        supplier = Supplier(
            name=name,
            company_name=request.form.get('company_name', '').strip(),
            contact_person=request.form.get('contact_person', '').strip(),
            phone=request.form.get('phone', '').strip(),
            email=request.form.get('email', '').strip(),
            address=request.form.get('address', '').strip()
        )
        db.session.add(supplier)
        db.session.commit()
        flash('Supplier added successfully!', 'success')
        return redirect(url_for('suppliers'))
    return render_template('add_supplier.html')


@app.route('/suppliers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            flash('Supplier name is required.', 'danger')
            return render_template('edit_supplier.html', supplier=supplier)
        supplier.name = name
        supplier.company_name = request.form.get('company_name', '').strip()
        supplier.contact_person = request.form.get('contact_person', '').strip()
        supplier.phone = request.form.get('phone', '').strip()
        supplier.email = request.form.get('email', '').strip()
        supplier.address = request.form.get('address', '').strip()
        db.session.commit()
        flash('Supplier updated successfully!', 'success')
        return redirect(url_for('suppliers'))
    return render_template('edit_supplier.html', supplier=supplier)


def init_db():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            user = User(username='admin')
            user.set_password('admin123')
            db.session.add(user)
        if Category.query.count() == 0:
            db.session.add_all([Category(name='Electronics'), Category(name='Stationery'), Category(name='General')])
        if Supplier.query.count() == 0:
            db.session.add_all([
                Supplier(name='Demo Supplies', company_name='Demo Supplies Pvt Ltd', phone='9999999999'),
                Supplier(name='Office Depot', phone='8888888888')
            ])
        db.session.commit()
        if Product.query.count() == 0:
            category_ids = {c.name: c.id for c in Category.query.all()}
            supplier = Supplier.query.first()
            db.session.add_all([
                Product(name='Wireless Mouse', sku='ELEC-001', quantity=18, purchase_price=350,
                        selling_price=499, min_stock_level=5, category_id=category_ids['Electronics'],
                        supplier_id=supplier.id if supplier else None),
                Product(name='A4 Notebook', sku='STAT-001', quantity=4, purchase_price=35,
                        selling_price=60, min_stock_level=10, category_id=category_ids['Stationery'],
                        supplier_id=supplier.id if supplier else None),
                Product(name='USB-C Cable', sku='ELEC-002', quantity=12, purchase_price=120,
                        selling_price=199, min_stock_level=5, category_id=category_ids['Electronics'],
                        supplier_id=supplier.id if supplier else None)
            ])
            db.session.commit()


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
