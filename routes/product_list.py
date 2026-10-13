from flask import Blueprint, render_template

product_list_bp = Blueprint("product_list", __name__)


@product_list_bp.route("/list")
def product_list():
    # 팀원 3: 목록 화면을 구현한다. 이번 실습은 짧은 설명만 있어도 된다.
    return render_template("product_list.html")
