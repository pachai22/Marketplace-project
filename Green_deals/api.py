from flask import Flask, request,jsonify,render_template,url_for,session as s
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import redirect
from entities import User,Category,validate_credentials,Item,Cart,formatted_list
from db_connection import connect_db
app = Flask(__name__)
app.secret_key= 'super_secret_key'

@app.route('/login',methods = ['GET','POST'])
def login():
    msg = ' '
    if  'username' in request.form and 'password' in request.form:
        username = request.form['username']
        pswd = request.form['password']
        details = session.query(User).all()
        (result,userid) = validate_credentials(username,pswd,details)
        if result == True:
            s['logged in'] = True
            s['user_id']=userid
            s['user_name']= username
            s['password'] = pswd
            return "Logged in successfully"
        else:
            msg = 'Incorrect username/password!'
    return "Incorrect username/password"
    #return render_template('login.html', msg=msg)

@app.route('/home',methods=['GET'])
def home():
    c_list=[]
    categories = session.query(Category).all()
    for category in categories:
        c_list.append(category.category_type)
    return jsonify(c_list)


@app.route('/home/<id>',methods=['GET'])
def list_items(id):
    item_list=[]
    category_id = id
    category = session.query(Category).filter_by(category_id = category_id).first()
    item = category.items
    for detail in item:
        item_list.append(detail.name)
    return jsonify(item_list)

@app.route('/cart/<id>',methods=['GET'])
def get_cart_details(id):
    result =[]
    product_list=[]
    user_id = id
    user = session.query(User).filter_by(user_id = user_id).first()
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
            quantity = session.query(Cart).filter_by(user_id=user_id,item_id = item.id).first()
            seller = session.query(User).filter_by(user_id=seller_id).first()
            result.append(formatted_list(item,seller,quantity))
            print(result)
    return jsonify(result)

@app.route('/cart/<id>',methods=['POST'])
def add_to_cart(id):
    user_id = id
    product_id = request.form['item_id']
    quantity = request.form['desired_quantity']
    available_stock = session.query(Item).filter_by(id = product_id).first()
    available_quantity=available_stock.quantity
    if available_quantity < int(quantity):
        return "stock unavailable"
    else:
        product= Cart(user_id=user_id,item_id = product_id,desired_quantity=quantity)
        session.add(product)
        session.commit()
        return "Added to cart successfully"

@app.route('/cart/<id>',methods= ['PUT'])
def update_cart_details(id):
    user_id = id
    product_id = request.form['item_id']
    quantity = request.form['desired_quantity']
    product = session.query(Cart).filter_by(user_id = user_id,item_id = product_id).one()
    product.item_id = product_id
    product.desired_quantity = quantity
    session.add(product)
    session.commit()
    return "Updated successfully"

@app.route('/cart/<id>',methods=['DELETE'])
def remove_item(id):
    flag = 1
    user_id = id
    product_id = request.form['item_id']
    product = session.query(Cart).filter_by(user_id=user_id,item_id = product_id).one()
    session.delete(product)
    session.commit()
    #if flag == 1:
        #return "false"
    #else:
    return "Deleted successfully"

@app.route('/logout')
def logout():
    s.pop('logged in',None)
    s.pop('user_name',None)
    s.pop('password',None)
    s.pop('user_id',None)
    return "logged out successfully"

db = connect_db()
Session = sessionmaker(bind=db)
session = Session()
print("Database connected successfully")
if __name__ == "__main__":
    app.run(debug=True)
