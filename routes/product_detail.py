from flask import Blueprint, render_template

from database import DBhandler

DB = DBhandler()

product_detail_bp = Blueprint("product_detail", __name__)


@product_detail_bp.route("/view_detail/<name>")
def view_item_detail(name):
    data = DB.get_item_byname(name)
    if data is None:
        return render_template("error.html", message="상품을 찾을 수 없습니다."), 404
    return render_template("product_detail.html", name=name, data=data)
