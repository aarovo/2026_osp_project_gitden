# 깃든 마켓 Flask 팀 프로젝트

팀원별 Blueprint로 페이지를 나누어 작성한 Flask 실습 프로젝트다.
상품 등록 폼에서 입력값과 사진을 POST로 전송하면 결과 화면에 모두 표시한다.
사진은 static/uploads/에 저장하며 상품 데이터베이스는 사용하지 않는다.

## 실행

Python 3.10 이상을 사용한다.

```bash
python -m venv venv
source venv/bin/activate
# Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

http://127.0.0.1:5000 에 접속한다.
`venv`, `.venv`, 캐시, 환경변수 파일은 Git에 올리지 않는다.

## 역할과 수정 범위

| 담당 | 주소 | 직접 수정할 파일 |
| --- | --- | --- |
| 팀원 1: 상품 등록 | GET `/reg_items` | `routes/product_register.py`, `templates/register.html` |
| 팀원 2: 상품 결과 | POST `/result` | `routes/product_result.py`, `templates/result.html` |
| 팀원 3: 상품 목록 | GET `/list` | `routes/product_list.py`, `templates/product_list.html` |
| 팀원 4: 리뷰 | GET `/reg_reviews`, GET `/reviews` | `routes/reviews.py`, `templates/register_review.html`, `templates/review_list.html` |
| 통합 담당 | GET `/` | `app.py`, `templates/index.html`, `templates/error.html`, `static/style.css`, `requirements.txt` |

자기 담당 파일에서 작업한다. 공통 파일 변경이 필요하면 통합 담당과 먼저 조율한다.
README와 PR 템플릿도 공통 담당이 관리한다.

개별 화면 스타일이 필요하면 자기 전용 파일을 새로 만든다.
예: `static/product_register.css`, `static/product_result.css`, `static/product_list.css`, `static/reviews.css`.
`extra_css` 블록에서 연결하면 공통 CSS를 수정하지 않아도 된다.
입력용 이미지 이름도 담당별로 다르게 정한다.

## 구조

```text
app.py                     # 앱 생성, 홈, Blueprint 연결
routes/                    # 팀원별 Python 파일
  product_register.py
  product_result.py
  product_list.py
  reviews.py
templates/
  index.html               # 공통 틀과 홈
  register.html
  result.html
  product_list.html
  register_review.html
  review_list.html
  error.html
static/
  style.css                # 공통 스타일
  images/                  # 입력용 상품 이미지
```

각 Python 파일은 Flask Blueprint를 사용한다. `app.py`에서 이미 연결해 두었으므로
팀원은 자기 함수와 HTML을 수정하면 된다.
모든 페이지는 `index.html`을 상속하고 `content` 블록에 본문을 작성한다.

## 상품 담당 1·2가 함께 사용할 규칙

등록 폼은 `method="post"`, `enctype="multipart/form-data"`를 사용한다.
전송 주소는 `url_for('product_result.result')`이다.

| 입력 항목 | HTML name / 서버 키 |
| --- | --- |
| 상품명 | `product_name` |
| 판매자 ID | `seller_id` |
| 가격 | `price` |
| 주소 | `address` |
| 상태 | `status` |
| 이메일 | `email` |
| 사진 | `picture` |

- 가격: 0 이상의 정수, 원 단위
- 상태: `새 상품`, `거의 새 상품`, `사용감 있음`
- 사진: PNG, JPEG, WEBP; 전체 요청 크기 최대 5MB
- 모든 항목 필수

결과 처리 함수는 글자 입력값을 `request.form`, 사진을 `request.files`에서 받는다.
결과 HTML에는 아래 이름으로 값을 전달한다.

- `product_name`, `seller_id`, `price`, `address`, `status`, `email`: 글자 입력값을 각각 전달
- `image_url`: 브라우저에서 표시할 수 있는 이미지 주소 또는 data URI
- `filename`: 입력한 사진의 파일명

`result.html`에 모든 입력값과 사진을 표시한다. 사용자 입력에 `|safe`를 사용하지 않는다.
정상 제출은 200, 잘못된 입력은 400으로 처리한다.
`/result`에서 사진을 검증하고 고유한 파일명으로 저장한 뒤 결과 화면을 반환한다.
이번 과제는 데이터베이스 저장을 요구하지 않는다.

Blueprint를 사용하므로 `url_for`에는 아래 전체 이름을 쓴다.

```text
index
product_register.reg_items
product_result.result
product_list.product_list
reviews.reg_reviews
reviews.reviews
```

## 각자 브랜치에서 작업하고 PR 올리기

처음 시작할 때:

```bash
git clone https://github.com/aarovo/2026_osp_project_gitden.git
cd 2026_osp_project_gitden
git switch main
git pull --ff-only origin main
git switch -c feature/product-register
```

브랜치 이름은 담당에 따라 하나를 선택한다.

- 팀원 1: `feature/product-register`
- 팀원 2: `feature/product-result`
- 팀원 3: `feature/product-list`
- 팀원 4: `feature/reviews`

상품 등록 담당의 커밋 예시:

```bash
git add routes/product_register.py templates/register.html
git commit -m "Implement product registration form"
git push -u origin feature/product-register
```

다른 담당자는 자기 파일과 브랜치 이름으로 바꾼다.
GitHub에서 **base: main**, **compare: 자기 브랜치**로 PR을 생성한다.
담당 기능, 변경 내용, 실행 확인을 PR 템플릿에 적는다.
추가 작업은 main에 직접 push하지 않고, 통합 담당이 검토한 뒤 PR을 병합한다.

작업 중 다른 PR이 main에 합쳐졌으면 자기 브랜치에서:

```bash
git fetch origin
git merge origin/main
```

충돌이 생기면 파일 소유 담당과 확인해 해결한다. 강제 push는 하지 않는다.

## 통합 확인 및 제출

- 홈과 메뉴로 연결된 네 페이지가 모두 열리는지 확인한다.
- 모든 페이지에 공통 메뉴가 보이는지 확인한다.
- 상품 입력값 6개와 사진이 POST로 전송되고 결과 화면에 모두 출력되는지 확인한다.
- 등록 화면의 입력값과 결과 화면의 값이 같은지 확인한다.
- `python app.py`로 실행되는지 확인한다.
- 상품 목록, 리뷰 등록, 리뷰 목록은 짧은 설명만 있어도 된다.

최종 제출: 이 저장소 URL과 스크린샷 2장(입력한 상품 등록 화면, 같은 입력의 결과 화면).
팀에서 한 번만 제출한다. screenshots/에 실제 입력 화면과 POST 결과 화면을 포함했다.
입력용 엽서 이미지는 static/images/sample-product.jpg에 있다.
스크린샷의 판매자 ID, 이메일, 장소는 시연용 정보다. 실행 중 업로드한 사진은 Git에서 제외한다.
