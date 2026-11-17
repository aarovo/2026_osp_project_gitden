from flask import Blueprint, jsonify, request, session
from database import DBhandler

DB = DBhandler()

likes_bp = Blueprint("likes", __name__)

@likes_bp.route("/item_like/<item_name>", methods=["GET", "POST"])
def like_item(item_name):
    user_id = session.get("id")
    if user_id is None:
        return jsonify({"error": "로그인이 필요합니다."}), 401
    if DB.get_item_byname(item_name) is None:
        return jsonify({"error": "존재하지 않는 상품입니다."}), 404
    if request.method == "GET":
        return jsonify({"liked": DB.get_heart(user_id, item_name)}), 200
    data = request.get_json(silent=True) or {}
    saved = DB.set_heart(user_id, item_name, data.get("liked", False))
    return jsonify({"liked": saved}), 200 