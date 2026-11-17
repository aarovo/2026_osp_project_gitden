from flask import Blueprint, render_template

from database import DBhandler

DB = DBhandler()

reviews_bp = Blueprint("reviews", __name__)


@reviews_bp.route("/reg_reviews")
def reg_reviews():
    return render_template("register_review.html")


@reviews_bp.route("/reviews")
def reviews():
    # 팀원 4: 리뷰 목록 화면을 구현한다.
    return render_template("review_list.html")

@reviews_bp.route("/view_review_detail/<review_id>")
def review_detail(review_id):
    # Firebase에서 해당 리뷰 ID의 데이터 가져오기
    data = DB.get_review_by_id(review_id)

    # 존재하지 않는 리뷰라면 404 처리
    if data is None:
        return render_template(
            "error.html",
            message="리뷰를 찾을 수 없습니다."
        ), 404

    return render_template(
        "review_detail.html",
        review_id=review_id,
        data=data
    )