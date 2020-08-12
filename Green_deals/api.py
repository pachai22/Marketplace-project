from flask import Flask, request,jsonify,render_template,url_for,session as s
from sqlalchemy.orm import session
from werkzeug.utils import redirect
from methods import validate_credentials,get_category_list,get_items_list,formatted_cart_details,insert_into_cart,update_quantity,delete_item
app = Flask(__name__)
app.secret_key= 'super_secret_key'

@app.route('/login',methods = ['GET','POST'])
def login():
    msg = ' '
    if  'username' in request.form and 'password' in request.form:
        username = request.form['username']
        pswd = request.form['password']
        (result,userid) = validate_credentials(username,pswd)
        if result == True:
            s['logged in'] = True
            s['user_id']=userid
            s['user_name']= username
            s['password'] = pswd
            return "Logged in successfully"
            #return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return "Incorrect username/password"
    #return render_template('login.html', msg=msg)

@app.route('/categories',methods=['GET'])
def home():
    c_list=get_category_list()
    return jsonify(c_list)

@app.route('/categories/<id>',methods=['GET'])
def list_items(id):
    category_id = id
    item_list = get_items_list(category_id)
    return jsonify(item_list)

@app.route('/cart/<id>',methods=['GET'])
def get_cart_details(id):
    user_id = id
    result = formatted_cart_details(user_id)
    return jsonify(result)

@app.route('/cart/<id>',methods=['POST'])
def add_to_cart(id):
    user_id = id
    product_id = request.form['item_id']
    quantity = request.form['desired_quantity']
    result=insert_into_cart(product_id,quantity,user_id)
    if result== True:
        return "Added to cart successfully"
    else:
        return "Stock unavailable"


@app.route('/cart/<id>',methods= ['PUT'])
def update_cart_details(id):
    user_id = id
    product_id = request.form['item_id']
    quantity = request.form['desired_quantity']
    result = update_quantity(user_id,product_id,quantity)
    if result == True:
        return "Updated successfully"

@app.route('/cart/<id>',methods=['DELETE'])
def remove_item(id):
    flag = 1
    user_id = id
    product_id = request.form['item_id']
    result = delete_item(user_id,product_id)
    if result == True:
        return "Deleted successfully"

@app.route('/logout')
def logout():
    s.pop('logged in',None)
    s.pop('user_name',None)
    s.pop('password',None)
    s.pop('user_id',None)
    return "logged out successfully"

if __name__ == "__main__":
    app.run(debug=True)