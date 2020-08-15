from flask import Flask, request,jsonify,abort,render_template,url_for,session as s
from werkzeug.utils import redirect
from methods import validate_credentials,get_category_list,get_items_list,formatted_cart_details,insert_into_cart,update_quantity,delete_item,check_valid_user
app = Flask(__name__)
app.secret_key= 'super_secret_key'

@app.route('/login',methods = ['POST'])
def login():
    request_data = request.get_json()
    username = request_data['username']
    pswd = request_data['password']
    (result,userid) = validate_credentials(username,pswd)
    if result == True:
        s['logged in'] = True
        s['user_id']=userid
        s['user_name']= username
        s['password'] = pswd
        print(s)
        return "Logged in successfully"
    else:
        abort(401)


@app.route('/categories',methods=['GET'])
def categories():
    c_list=get_category_list()
    return jsonify(c_list)

@app.route('/categories/<id>',methods=['GET'])
def list_items(id):
    category_id = id
    item_list = get_items_list(category_id)
    print(item_list)
    return jsonify(item_list)

@app.route('/cart/<id>',methods=['GET'])
def get_cart_details(id):
    user_id = id
    valid = check_valid_user(user_id,s['user_id'])
    if valid == True:
        result = formatted_cart_details(user_id)
        return jsonify(result)
    else:
        abort(403)
        #return "Unauthorized user"

@app.route('/cart/<id>',methods=['POST'])
def add_to_cart(id):
    user_id = id
    request_data = request.get_json()
    valid = check_valid_user(user_id,s['user_id'])
    if valid == True:
        product_id = request_data['item_id']
        quantity = request_data['desired_quantity']
        result=insert_into_cart(product_id,quantity,user_id)
        if result== True:
            return "Added to cart successfully"
        else:
            return "Stock unavailable"
    else:
        abort(403)

@app.route('/cart/<id>',methods= ['PUT'])
def update_cart_details(id):
    user_id = id
    request_data = request.get_json()
    valid = check_valid_user(user_id,s['user_id'])
    if valid == True:
        product_id = request_data['item_id']
        quantity = request_data['desired_quantity']
        result = update_quantity(user_id,product_id,quantity)
        if result == True:
            return "Updated successfully"
    else:
        abort(403)

@app.route('/cart/<id>',methods=['DELETE'])
def remove_item(id):
    user_id = id
    request_data = request.get_json()
    valid = check_valid_user(user_id,s['user_id'])
    if valid == True:
        product_id = request_data['item_id']
        result = delete_item(user_id,product_id)
        if result == True:
            return "Deleted successfully"
    else:
        abort(403)

@app.route('/logout',methods=['GET'])
def logout():
    s.pop('logged in',None)
    s.pop('user_name',None)
    s.pop('password',None)
    s.pop('user_id',None)
    return "logged out successfully"

if __name__ == "__main__":
    app.run(debug=True)