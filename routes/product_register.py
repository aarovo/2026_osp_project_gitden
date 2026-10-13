from flask import Blueprint, render_template

product_register_bp = Blueprint("product_register", __name__)


@product_register_bp.route("/reg_items")
def reg_items():
    # 팀원 1: register.html에 상품 등록 폼을 구현한다.
    return render_template("register.html")
