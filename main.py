from flask import Flask,render_template,send_from_directory,jsonify,request ,session,redirect,url_for
import os
from app.database import get_db

collection=get_db()

app=Flask(__name__)
app.secret_key="your_secret_key_here"

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/<page>")
def render_page(page):
    file_path = os.path.join(app.template_folder, f"{page}.html")
    if os.path.exists(file_path):
        return render_template(f"{page}.html")
    else:
        return f"Page '{page}' not found."

@app.route("/registration",methods=["POST"])
def get_registration():
    data=request.form
    name=data.get("name","")
    password=data.get("password","")
    email_id=data.get("email_id","")

    response=collection.find_one({"email_id":email_id})
    if not response:
        collection.insert_one({"name":name,"email_id":email_id,"password":password})
        return jsonify({"Status":"Sucess","Message":"User registred Sucessfully"})
    else:
        return jsonify({"Status":"Error","Message":"Email_id alredy Exists"})




  
@app.route("/login",methods=["POST"])
def login():
    data=request.form
    name=data.get("name","")
    password=data.get("password","")

    response=collection.find_one({"name":name,"password":password})
    if response:
        session["logged_in"]=True
        return jsonify({"Status":"Success","redirect_url":url_for("add_product")}) 
    else:
        return jsonify({"Status":"Error","Message":"Invalid Credentials"})
    
   


@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if "logged_in" not in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        data = request.form
        product_name = data.get("product_name", "").strip()
        
 
        print(f"Product name submitted: {product_name}")
        
        if not product_name:
            return jsonify({"Status": "Error", "Message": "Product name cannot be empty"})
        
        
        existing = collection.find_one({"product_name": {"$regex": f"^{product_name}$", "$options": "i"}})
        
        if existing:
            print(f"Product already exists: {existing['product_name']}")
            return jsonify({"Status": "Error", "Message": "Product already exists"})
        else:


            collection.insert_one({
                "type": data.get("type", ""),
                "product_name": product_name,
                "price": float(data.get("price", 0)),
                "description": data.get("description", ""),
                "stock": int(data.get("stock", 0))
            })

            return redirect(url_for("product_success"))

    return render_template("add_product.html")
    


@app.route("/products", methods=["GET"])
def get_products():
    if "logged_in" not in session:
        return redirect(url_for("home"))

    data = request.args

    type = data.get("type", "")
    product_name = data.get("product_name", "")
    price = data.get("price", "")
    description = data.get("description", "")
    stock = data.get("stock", "")

    response = {}
    if product_name:
        response["product_name"] = {"$regex": product_name, "$options": "i"}
    if type:
        response["type"] = type
    if price:
        try:
            response["price"] = float(price)
        except:
            pass
    if description:
        response["description"] = description
    if stock:
        try:
            response["stock"] = int(stock)
        except:
            pass

    products_cursor = collection.find(response)
    products = []
    for product in products_cursor:
        product["_id"] = str(product["_id"])
        products.append(product)

    return render_template("products.html", products=products)

 
    


    
if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
    


