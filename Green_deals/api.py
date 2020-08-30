from flask import Flask, request,jsonify,abort,render_template,url_for,session as s
from werkzeug.utils import redirect
from flask_cors import CORS, cross_origin
from methods import validate_credentials,get_category_list,get_items_list,formatted_cart_details,insert_into_cart,update_quantity,delete_item,check_valid_user
app = Flask(__name__)
cors = CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.secret_key= 'super_secret_key'


@cross_origin()
@app.route('/login',methods = ['GET','POST'])
def login():
    request_data = request.get_json()
    username = request_data['username']
    pswd = request_data['password']
    print(username)
    print(pswd)
    (result,userid) = validate_credentials(username,pswd)
    if result == True:
        s['logged in'] = True
        s['user_id']=userid
        s['user_name']= username
        s['password'] = pswd
        print(s)
        return jsonify({'status':'200','user_id':userid})
    else:
        return jsonify({'status':'401'})
    
@cross_origin()
@app.route('/categories',methods=['GET'])
def categories():
    c_list=get_category_list()
    return jsonify(c_list)

@cross_origin()
@app.route('/categories/<id>',methods=['GET'])
def list_items(id):
    category_id = id
    item_list = get_items_list(category_id)
    print(item_list)
    return jsonify(item_list)

@cross_origin()
@app.route('/cart/<id>',methods=['GET'])
def get_cart_details(id):
    user_id = id
    result = formatted_cart_details(user_id)
    return jsonify(result)


@cross_origin()
@app.route('/cart/<id>',methods=['POST'])
def add_to_cart(id):
    user_id = id
    print(user_id)
    request_data = request.get_json()
    product_id = request_data['item_id']
    quantity = 1
    result=insert_into_cart(product_id,quantity,user_id)
    if result== True:
        return jsonify({'status':'Added to cart successfully'})
    elif result == "No":
        return jsonify({'status':'Item is already in cart'})
    else:
        return jsonify({'status':'stock unavailable'})


@cross_origin()
@app.route('/cart/<id>',methods= ['PUT'])
def update_cart_details(id):
    user_id = id
    request_data = request.get_json()
    product_id = request_data['item_id']
    quantity = request_data['desired_quantity']
    result = update_quantity(user_id,product_id,quantity)
    if result == True:
        return jsonify({'status':'Updated successfully'})

@cross_origin()
@app.route('/cart/<id>',methods=['DELETE'])
def remove_item(id):
    user_id = id
    print(user_id)
    request_data = request.get_json()
    product_id = request_data['item_id']
    print(product_id)
    result = delete_item(user_id,product_id)
    if result == True:
        return jsonify({'status':'Deleted successfully'})




if __name__ == "__main__":
    app.run(debug=True)