from pathlib import Path
from uuid import uuid4

from flask import Blueprint, render_template, current_app, redirect, request, url_for
from PIL import Image, UnidentifiedImageError
from math import ceil

from database import DBhandler

DB = DBhandler()

reviews_bp = Blueprint("reviews", __name__)

@reviews_bp.route("/reg_reviews", defaults={"name": ""})
@reviews_bp.route("/reg_reviews/<name>")
def reg_reviews(name):
    # 팀원 4: 리뷰 등록 화면을 구현한다.
    return render_template("register_review.html", name=name)

@reviews_bp.route("/submit_review_post", methods=["POST"])
def reg_review_submit_post():
    product_name = request.form.get("product_name", "").strip()
    title = request.form.get("title", "").strip()
    body = request.form.get("body", "").strip()
    rating = request.form.get("rating", "").strip()
    image_file = request.files.get("photo")

    if not all((product_name, title, body, rating)) or not image_file or not image_file.filename:
        return render_template("error.html", message="모든 항목을 입력하고 사진을 선택해 주세요."), 400

    try:
        with Image.open(image_file.stream) as image:
            image.verify()
            extension = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp"}.get(image.format)
        if extension is None:
            raise ValueError("Unsupported image")
    except (UnidentifiedImageError, OSError, ValueError):
        return render_template("error.html", message="PNG, JPG, WEBP 사진을 선택해주세요."), 400

    image_file.stream.seek(0)
    upload_dir = Path(current_app.static_folder) / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    saved_name = uuid4().hex + extension
    img_path = "static/uploads/" + saved_name
    image_file.save(upload_dir / saved_name)

    review_info = {
        "product_name": product_name,
        "title": title,
        "body": body, 
        "rating": int(rating),       
    }

    try:
        DB.insert_review(review_info, img_path)
    except Exception:
        current_app.logger.exception("Firebase 리뷰 저장 실패")
        (upload_dir / saved_name).unlink(missing_ok=True)
        return render_template(
            "error.html",
            massage="리뷰 저장 중 오류가 발생했습니다. 다시 시도해 주세요."
        ), 500

    return redirect(url_for("reviews.reviews"))

PER_PAGE = 4  # 리뷰 목록: 한 페이지에 4개 (2 x 2)

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