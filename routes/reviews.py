from math import ceil

from flask import Blueprint, render_template, request

from database import DBhandler

DB = DBhandler()

reviews_bp = Blueprint("reviews", __name__)

PER_PAGE = 4  # 리뷰 목록: 한 페이지에 4개 (2 x 2)


@reviews_bp.route("/reg_reviews")
def reg_reviews():
    # 팀원 4: 리뷰 등록 화면을 구현한다.
    return render_template("register_review.html")


@reviews_bp.route("/reviews")
def reviews():
    # 주소의 ?page=2 값을 읽는다. 없거나 잘못된 값이면 1페이지.
    page = request.args.get("page", 1, type=int)

    # [(리뷰 ID, 리뷰 정보), ...] — 리뷰 ID는 push()로 자동 생성된 키
    # push 키는 등록 순서대로 정렬되므로, 뒤집어서 최신 리뷰가 먼저 나오게 한다.
    all_reviews = list(DB.get_reviews().items())[::-1]
    total = len(all_reviews)
    page_count = max(1, ceil(total / PER_PAGE))
    page = min(max(page, 1), page_count)

    start = (page - 1) * PER_PAGE
    page_reviews = all_reviews[start:start + PER_PAGE]

    # 2개씩 묶어서 한 줄로 만든다 → 2 x 2 배치
    rows = [page_reviews[i:i + 2] for i in range(0, len(page_reviews), 2)]

    return render_template(
        "review_list.html",
        rows=rows,
        page=page,
        page_count=page_count,
        total=total,
    )