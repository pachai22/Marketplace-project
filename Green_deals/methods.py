from db_connection import connect_db
from entities import User,Category,Item,Cart

session = connect_db()

def validate_credentials(username,pswd):
    flag =0
    userid = " "
    details = session.query(User).all()
    for row in details:
        print(row.user_name)
        if row.user_name == username and row.password == pswd:
            userid=row.user_id
            flag = 1
    if flag == 1:
        return True,userid
    else:
        return False,userid

def get_category_list():
    c_list = []
    categories = session.query(Category).all()
    for category in categories:
        c_list.append(category.category_type)
    return c_list

def get_items_list(category_id):
    item_list =[]
    category = session.query(Category).filter_by(category_id=category_id).first()
    item = category.items
    for detail in item:
        item_list.append(detail.name)
    return item_list

def formatted_cart_details(user_id):
    result = []
    product_list = []
    user = session.query(User).filter_by(user_id=user_id).first()
    print(user.user_name)
    products = session.query(Cart).filter_by(user_id=user_id)
    for product in products:
        product_list.append(product.item_id)
    print(product_list)
    items = session.query(Item).all()
    for item in items:
        print(item.id)
        if item.id in product_list:
            seller_id = item.seller_id
            quantity = session.query(Cart).filter_by(user_id=user_id, item_id=item.id).first()
            seller = session.query(User).filter_by(user_id=seller_id).first()
            result.append(formatted_list(item, seller, quantity))
            print(result)
    return result

def formatted_list(row,user,quantity):
    return "Product-name : "+str(row.name)+" Product-price : "+str(row.price)+" Quantity : "+str(quantity.desired_quantity)+" Seller-name : "+str(user.user_name)

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
    product.item_id = product_id
    product.desired_quantity = quantity
    session.add(product)
    session.commit()
    return True

def delete_item(user_id,product_id):
    product = session.query(Cart).filter_by(user_id=user_id, item_id=product_id).one()
    session.delete(product)
    session.commit()
    return True