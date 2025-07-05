from flask import Flask, url_for, render_template, redirect, request
import json

app = Flask(__name__)

#Thẻ đọc file json
def load_product():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)



@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        return redirect(url_for("home"))
    return render_template("warehouse.html")



@app.route("/home")
def home():
    products = load_product()

    # Tính tổng số lượng
    total_quantity = sum(p["Quantity"] for p in load_product())

    # Tính theo type (dựa vào toàn bộ data)
    type_counts = {}
    for p in load_product():
        p_type = p["type"]
        type_counts[p_type] = type_counts.get(p_type, 0) + p["Quantity"]

    #Lấy sort và type
    sort_option = request.args.get("sort", "az")
    type_filter = request.args.get("type", "all")
    search_query = request.args.get("query", "").strip().lower()

    #lọc theo name hoặc id nếu có query
    if search_query:
        products = [
            p for p in products
            if search_query in p["name"].lower() or search_query in str(p["id"]).lower()
        ]

    #Lọc theo loại
    if type_filter != "all":
        products = [p for p in products if p["type"].lower() == type_filter.lower()]

    # Sắp xếp
    if sort_option == "az":
        products.sort(key=lambda x: x["name"].lower())
    elif sort_option == "za":
        products.sort(key=lambda x: x["name"].lower(), reverse=True)

    return render_template("Home.html", 
                           products=products, 
                           total_quantity=total_quantity, 
                           type_counts=type_counts,
                           sort_option=sort_option,
                           type_filter=type_filter,
                           search_query = search_query
                           )

# @app.route("/add-product", methods = ["GET", "POST"])
# def add_product():


if __name__ == "__main__":
    app.run(debug=True)