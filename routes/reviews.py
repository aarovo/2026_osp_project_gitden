from flask import Blueprint, render_template

reviews_bp = Blueprint("reviews", __name__)


@reviews_bp.route("/reg_reviews")
def reg_reviews():
    # 팀원 4: 리뷰 등록 화면을 구현한다.
    return render_template("register_review.html")


@reviews_bp.route("/reviews")
def reviews():
    # 팀원 4: 리뷰 목록 화면을 구현한다.
    return render_template("review_list.html")
