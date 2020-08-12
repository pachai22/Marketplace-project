from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer,primary_key=True)
    user_name = Column(String)
    password = Column(String)
    item = relationship('Item',backref='User')
    cart = relationship('Cart',backref='User')

def validate_credentials(username,pswd,details):
    flag =0
    userid = " "
    for row in details:
        print(row.user_name)
        if row.user_name == username and row.password == pswd:
            userid=row.user_id
            flag = 1
    if flag == 1:
        return True,userid
    else:
        return False,userid


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
    seller_id = Column(Integer,ForeignKey('users.user_id'))
    quantity = Column(Integer)
    ids = relationship('Cart',backref='Item')

class Cart(Base):
    __tablename__= 'cart'
    serial_no = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey('users.user_id'))
    item_id = Column(Integer,ForeignKey('items.id'))
    desired_quantity = Column(Integer)

def formatted_list(row,user,quantity):
    return "Product-name : "+str(row.name)+" Product-price : "+str(row.price)+" Quantity : "+str(quantity.desired_quantity)+" Seller-name : "+str(user.user_name)


