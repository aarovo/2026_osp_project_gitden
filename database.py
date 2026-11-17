import os

import firebase_admin
from firebase_admin import credentials, db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(BASE_DIR, "authentication", "serviceAccountKey.json")
DB_URL = "https://opensw-f8acb-default-rtdb.firebaseio.com/"


class DBhandler:
    def __init__(self):
        # Flask 디버그 모드에서 앱이 두 번 초기화되어도 오류가 나지 않게 한다.
        if not firebase_admin._apps:
            cred = credentials.Certificate(KEY_PATH)
            firebase_admin.initialize_app(cred, {"databaseURL": DB_URL})
        self.db = db.reference()

    # ---------- 상품 ----------
    def item_duplicate_check(self, name):
        """등록 가능한 상품 이름이면 True, 이미 있으면 False"""
        return self.db.child("item").child(name).get() is None

    def insert_item(self, name, data, img_path):
        """상품 저장 (Key: 상품 이름). 중복이면 False, 성공하면 True"""
        if not self.item_duplicate_check(name):
            return False
        item_info = {
            "seller": data.get("seller_id"),
            "price": data.get("price"),
            "addr": data.get("address"),
            "status": data.get("status"),
            "email": data.get("email"),
            "img_path": img_path,
        }
        self.db.child("item").child(name).set(item_info)
        return True

    def get_items(self):
        """등록된 상품 전체를 {상품 이름: 상품 정보} 형태로 반환 (없으면 빈 dict)"""
        return self.db.child("item").get() or {}

    def get_item_byname(self, name):
        """상품 이름으로 상품 하나를 반환 (없으면 None)"""
        return self.db.child("item").child(name).get()
    
    # ---------- 리뷰 ----------
    def get_reviews(self):
        """등록된 리뷰 전체를 {리뷰 ID(자동 생성 키): 리뷰 정보} 형태로 반환 (없으면 빈 dict)"""
        return self.db.child("review").get() or {}
    
    # ---------- 회원 ----------
    def user_duplicate_check(self, id_string):
        """사용 가능한 ID면 True, 이미 있으면 False"""
        return self.db.child("user").child(id_string).get() is None

    def insert_user(self, data, pw_hash):
        """회원 저장 (Key: ID). 비밀번호는 해시값을 받는다. 중복이면 False"""
        user_id = data.get("id")
        if not self.user_duplicate_check(user_id):
            return False
        user_info = {
            "id": user_id,
            "pw": pw_hash,
            "nickname": data.get("nickname"),
        }
        self.db.child("user").child(user_id).set(user_info)
        return True

    def get_user(self, id_string):
        """주어진 ID에 저장된 사용자 정보를 반환하며, 없으면 None을 반환한다."""
        return self.db.child("user").child(id_string).get()

    # ---------- 리뷰 ----------
    def get_review_by_id(self, review_id):
        """리뷰 ID로 리뷰 하나를 반환 (없으면 None)"""
        return self.db.child("review").child(review_id).get()
    # ---------- 좋아요 ----------
    def get_heart(self, user_id, item_name):
        """사용자가 해당 상품에 좋아요를 눌렀으면 True, 아니면 False를 반환한다."""
        return bool(self.db.child("heart").child(user_id).child(item_name).get())

    def set_heart(self, user_id, item_name, liked):
        """좋아요 상태를 저장하고, 저장한 값을 반환한다."""
        self.db.child("heart").child(user_id).child(item_name).set(bool(liked))
        return bool(liked)
