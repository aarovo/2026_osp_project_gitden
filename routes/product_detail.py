from flask import Blueprint, render_template
from database import DBhandler

DB = DBhandler()

product_detail_bp = Blueprint('product_detail', __name__)

@product_detail_bp.route("/view_detail/<name>")
def view_item_detail(name):
    data = DB.db.child("item").child(str(name)).get()
    return render_template("product_detail.html", name=name, data=data)