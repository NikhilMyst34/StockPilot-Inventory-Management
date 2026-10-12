from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
db=SQLAlchemy()
class User(db.Model):
 id=db.Column(db.Integer,primary_key=True); username=db.Column(db.String(80),unique=True,nullable=False); password_hash=db.Column(db.String(255),nullable=False)
 def set_password(self,p='admin123'): self.password_hash=generate_password_hash(p)
 def check_password(self,p): return check_password_hash(self.password_hash,p)
class Category(db.Model):
 id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(100),unique=True,nullable=False); products=db.relationship('Product',backref='category',lazy=True)
class Supplier(db.Model):
 id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(120),nullable=False); company_name=db.Column(db.String(160),default=''); contact_person=db.Column(db.String(120),default=''); phone=db.Column(db.String(40),default=''); email=db.Column(db.String(120),default=''); address=db.Column(db.Text,default=''); products=db.relationship('Product',backref='supplier',lazy=True)
class Product(db.Model):
 id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(120),nullable=False); sku=db.Column(db.String(50),unique=True,nullable=False); quantity=db.Column(db.Integer,default=0,nullable=False); purchase_price=db.Column(db.Float,default=0.0,nullable=False); selling_price=db.Column(db.Float,default=0.0,nullable=False); min_stock_level=db.Column(db.Integer,default=5,nullable=False); unit=db.Column(db.String(20),default='pcs'); description=db.Column(db.Text,default=''); date_added=db.Column(db.DateTime,default=datetime.utcnow); category_id=db.Column(db.Integer,db.ForeignKey('category.id')); supplier_id=db.Column(db.Integer,db.ForeignKey('supplier.id')); transactions=db.relationship('StockTransaction',backref='product',lazy=True,cascade='all, delete-orphan')
class StockTransaction(db.Model):
 id=db.Column(db.Integer,primary_key=True); product_id=db.Column(db.Integer,db.ForeignKey('product.id'),nullable=False); transaction_type=db.Column(db.String(20),nullable=False); quantity=db.Column(db.Integer,nullable=False); note=db.Column(db.String(255),default=''); created_at=db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
