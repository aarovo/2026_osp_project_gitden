from pathlib import Path
from uuid import uuid4

from flask import Blueprint, current_app, render_template, request, url_for
from PIL import Image, UnidentifiedImageError

product_result_bp = Blueprint("product_result", __name__)


@product_result_bp.route("/result", methods=["POST"])
def result():
    product_name = request.form.get("product_name", "").strip()
    seller_id = request.form.get("seller_id", "").strip()
    price = request.form.get("price", "").strip()
    address = request.form.get("address", "").strip()
    status = request.form.get("status", "").strip()
    email = request.form.get("email", "").strip()
    image_file = request.files.get("picture")

    if not all((product_name, seller_id, price, address, status, email)) or not image_file or not image_file.filename:
        return render_template("error.html", message="모든 항목을 입력하고 사진을 선택해 주세요."), 400
    if not price.isdigit() or status not in ("새 상품", "거의 새 상품", "사용감 있음"):
        return render_template("error.html", message="가격과 상품 상태를 확인해 주세요."), 400

    # 확장자만 바꾼 파일을 받지 않도록 실제 사진 형식을 확인한다.
    try:
        with Image.open(image_file.stream) as image:
            image.verify()
            extension = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp"}.get(image.format)
        if extension is None:
            raise ValueError("Unsupported image")
    except (UnidentifiedImageError, OSError, ValueError):
        return render_template("error.html", message="PNG, JPG, WEBP 사진을 선택해 주세요."), 400

    image_file.stream.seek(0)
    upload_dir = Path(current_app.static_folder) / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    # 같은 파일명을 올려도 기존 사진을 덮어쓰지 않는다.
    saved_name = uuid4().hex + extension
    image_file.save(upload_dir / saved_name)

    return render_template(
        "result.html",
        product_name=product_name, seller_id=seller_id, price=price,
        address=address, status=status, email=email,
        image_url=url_for("static", filename="uploads/" + saved_name),
        filename=image_file.filename,
    )
