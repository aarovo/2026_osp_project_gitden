from pathlib import Path
from uuid import uuid4

from flask import Blueprint, render_template, current_app, redirect, request, url_for
from PIL import Image, UnidentifiedImageError

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


@reviews_bp.route("/reviews")
def reviews():
    # 팀원 4: 리뷰 목록 화면을 구현한다.
    return render_template("review_list.html")
