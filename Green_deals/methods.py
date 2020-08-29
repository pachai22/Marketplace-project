from flask import jsonify

from db import connect_db
from models import User,Category,Item,Cart,Seller

session = connect_db()

def validate_credentials(username,pswd):
    print(username,pswd)
    details = session.query(User).filter_by(user_name = username,password = pswd).first()
    if details != None:
        return True,details.user_id
    else:
        return False,username

def get_category_list():
    c_list = []
    categories = session.query(Category).all()
    for category in categories:
        dict = {}
        dict['category_id'] = category.category_id
        dict['category_type'] = category.category_type
        dict['image'] = category.image
        c_list.append(dict)
    return c_list

def get_items_list(category_id):
    item_list =[]
    category = session.query(Category).filter_by(category_id=category_id).first()
    item = category.items
    print(item)
    for detail in item:
        dict ={}
        dict['item_id'] = detail.id
        print(detail.id)
        dict['item_name'] = detail.name
        dict['item-price'] = int(detail.price)
        dict['available_quantity'] = detail.quantity
        dict['image'] = detail.image
        item_list.append(dict)
    return item_list

def check_valid_user(user_id,current_user):
    print(user_id,current_user)
    if int(current_user) == int(user_id) :
        print(current_user,user_id)
        return True
    else:
        return False

def get_products_list(user_id):
    product_list = []
    products = session.query(Cart).filter_by(user_id=user_id)
    for product in products:
        product_list.append(product.item_id)
    return product_list

def get_user_desired_quantity(user_id,item_id):
    quantity = session.query(Cart).filter_by(user_id=user_id, item_id=item_id).first()
    return quantity

def get_seller_detail(seller_id):
    seller = session.query(Seller).filter_by(id=seller_id).first()
    return seller


def formatted_cart_details(user_id):
    result = []
    product_list = get_products_list(user_id)
    items = session.query(Item).all()
    for item in items:
        print(item.id)
        if item.id in product_list:
            seller_id = item.seller_id
            quantity = get_user_desired_quantity(user_id,item.id)
            seller = get_seller_detail(seller_id)
            result.append(formatted_list(item, seller, quantity))
            print(result)
    return result

def formatted_list(row,seller,quantity):
    dict ={}
    dict['image'] = row.image
    dict['Product-id'] = row.id
    dict['Product-name'] = row.name
    dict['Product-price'] = int(row.price) * quantity.desired_quantity
    dict['Quantity'] = quantity.desired_quantity
    dict['seller-name'] = seller.name
    return dict

def insert_into_cart(product_id,quantity,user_id):
    available_stock = session.query(Item).filter_by(id=product_id).first()
    available_quantity = available_stock.quantity
    if available_quantity < int(quantity):
        return False
    else:
        product = Cart(user_id=user_id, item_id=product_id, desired_quantity=quantity)
        session.add(product)
        session.commit()
        return True

def update_quantity(user_id,product_id,quantity):
    product = session.query(Cart).filter_by(user_id=user_id, item_id=product_id).one()
    product.desired_quantity = quantity
    session.add(product)
    session.commit()
    return True

def delete_item(user_id,product_id):
    product = session.query(Cart).filter_by(user_id=user_id, item_id=product_id).one()
    session.delete(product)
    session.commit()
    return True