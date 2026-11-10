from math import ceil

from flask import Blueprint, render_template, request

from database import DBhandler

DB = DBhandler()

product_list_bp = Blueprint("product_list", __name__)

PER_PAGE = 6  # 한 페이지에 보여줄 상품 수


@product_list_bp.route("/list")
def product_list():
    # 주소의 ?page=2 값을 읽는다. 없거나 잘못된 값이면 1페이지.
    page = request.args.get("page", 1, type=int)

    items = list(DB.get_items().items())  # [(상품 이름, 상품 정보), ...]
    total = len(items)
    page_count = max(1, ceil(total / PER_PAGE))
    page = min(max(page, 1), page_count)

    start = (page - 1) * PER_PAGE
    page_items = items[start:start + PER_PAGE]

    return render_template(
        "product_list.html",
        items=page_items,
        page=page,
        page_count=page_count,
        total=total,
    )