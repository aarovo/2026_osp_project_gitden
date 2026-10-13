from flask import Blueprint, render_template

product_result_bp = Blueprint("product_result", __name__)


@product_result_bp.route("/result", methods=["POST"])
def result():
    # TODO(팀원 2): request.form으로 6개 입력값을 받는다.
    product_name = request.form.get("product_name")
    seller_id = request.form.get("seller_id")
    price = request.form.get("price")
    address = request.form.get("address")
    status = request.form.get("status")
    email = request.form.get("email")

    # TODO(팀원 2): request.files["picture"]로 사진을 받고 검증한다.
    image_file=request.files["picture"]
    image_file.save("static/image/{}", format(image_file.filename))
    # TODO(팀원 2): data, image_url, filename을 result.html에 전달한다.
    # 구현 전에는 501을 반환해 처리 완료로 오해하지 않도록 한다.
    return render_template("result.html", 
                           product_name=product_name, seller_id=seller_id, price= price, 
                           address=address, status=status, email=email,
                           image_url="static/image/{}", filename=format(image_file.filename))
