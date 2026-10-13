from flask import Flask, render_template

from routes.product_register import product_register_bp
from routes.product_result import product_result_bp
from routes.product_list import product_list_bp
from routes.reviews import reviews_bp

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

# 공통 담당: 팀원은 routes/의 자기 담당 파일에서 작업한다.
app.register_blueprint(product_register_bp)
app.register_blueprint(product_result_bp)
app.register_blueprint(product_list_bp)
app.register_blueprint(reviews_bp)


@app.route("/")
def index():
    return render_template("index.html")


@app.errorhandler(413)
def too_large(error):
    return render_template("error.html", message="사진을 포함한 전송 크기는 5MB 이하여야 합니다."), 413


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
