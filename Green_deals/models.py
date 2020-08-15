from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer,primary_key=True)
    user_name = Column(String)
    password = Column(String)
    cart = relationship('Cart',backref='User')

class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer,primary_key=True)
    category_type = Column(String)
    items = relationship('Item',backref='Category')

class Item(Base):
    __tablename__ ='items'
    id = Column(Integer,primary_key=True)
    category_id = Column(Integer,ForeignKey('categories.category_id'))
    name = Column(String)
    price = Column(Integer)
    seller_id = Column(Integer,ForeignKey('seller.id'))
    quantity = Column(Integer)
    ids = relationship('Cart',backref='Item')

class Seller(Base):
    __tablename__ = 'seller'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    item = relationship('Item', backref='Seller')

class Cart(Base):
    __tablename__= 'cart'
    serial_no = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey('users.user_id'))
    item_id = Column(Integer,ForeignKey('items.id'))
    desired_quantity = Column(Integer)



