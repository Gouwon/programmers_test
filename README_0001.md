피부 타입마다 성분 기반으로 화장품을 추천해 주는 서비스의 API서버를 Django를 이용해 만들어 주세요.
요구 사항
피부 타입은 다음의 3가지 종류가 있습니다.
지성 (oily)
건성 (dry)
민감성 (sensitive)
화장품을 구성하는 성분들은 피부 타입 별로 가질 수 있는 성질이 3 종류가 있습니다.
유익함 (+1)
영향없음 (0)
유해함 (-1)
예를 들어 성분 A, B, C로 구성된 화장품의 경우 성분 A, B, C가 각 피부타입에 대해 가지는 성질을 다음과 같이 나타낼 수 있습니다.
유익한 성질은 O, 유해한 성질은 X, 영향이 없을 경우 빈 문자열 ("") 로 나타냅니다.
성분명	지성	건성	민감성
A	O	O	X
B	O		X
C	O	O	
화장품을 구성하는 성분이 피부 타입에 유익할 경우 +1, 유해할 경우 -1, 영향이 없을 경우 0점으로 계산하면
아래와 같이 이 화장품이 피부 타입 별로 미치는 영향을 수치로 표현할 수 있습니다.
지성	건성	민감성
+3	+2	-2
이와 같은 데이터를 구성하기 위해 다음과 같이 JSON 데이터가 주어집니다.
상품목록
상품 Id
상품 이미지 Id
상품명
가격
성별(남/여/구분없음)
카테고리(스킨케어, 마스크팩, 선케어, 베이스메이크업)
구성 성분 이름(콤마로 구분)
이번 달 판매 수량
성분목록
이름
지성영향
건성영향
민감성영향
JSON
서버를 실행하면 상품목록과 성분목록 데이터가 DB에 입력되어 있어야 합니다.(초기 DB설정 방법은 STEP 2. 개발 환경 설정 다운로드에서 다운로드 받은 파일의 readme.md를 참고하세요)
테이블 구조는 자유롭게 설계하시면 됩니다.
JSON데이터에 포함된 imageId를 통해 image의 url을 만들어낼 수 있습니다.
base url은 https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/이며 뒤에 폴더 명을 통해 fullsize와 thumbnail을 구분합니다.
imageId가 1e0396a3-71b9-4cb1-b545-c1e38083c838라면,
full image URL은 다음과 같습니다.(폴더 명이 image): https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/image/1e0396a3-71b9-4cb1-b545-c1e38083c838.jpg
thumbnail image URL은 다음과 같습니다.(폴더 명이 thumbnail): https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/1e0396a3-71b9-4cb1-b545-c1e38083c838.jpg
상품 목록
json다운로드
예시
[
    {
      "id": 17,
      "imageId": "4e47e2fa54e84fedbe56b610475adf0c_520",
      "name": "화해 에센스 토너",
      "price": 23000,
      "gender": "all",
      "category": "skincare",
      "ingredients": "Glycerin,Methyl Gluceth-20,Pulsatilla Koreana Extract,Purified Water",
      "monthlySales": 1682
    },
    {
      "id": 19,
      "imageId": "4e47e2fa54e84fedbe56b610475adf0c_521",
      "name": "화해 스킨 솔루션 마스크",
      "price": 4800,
      "gender": "male",
      "category": "maskpack",
      "ingredients": "Glycerin,Sodium Hyaluronate,Xanthan Gum,Niacinamide,Orchid Extract",
      "monthlySales": 463
    },


    ...


    {
      "id": 68,
      "imageId": "4e47e2ei82lshfedbe56b610475adf0c_633",
      "name": "화해 화이트 브라이트닝 컨트롤 베이스",
      "price": 44000,
      "gender": "female",
      "category": "basemakeup",
      "ingredients": "Alcohol,Purified Water,Vinyl Dimethicone,PEG-10 Dimethicone",
      "monthlySales": 4437
    }
]
성분 목록
json다운로드
예시
[
{
  "name": "Alcohol",
  "oily": "O",
  "dry": "X",
  "sensitive": "X"
},
{
  "name": "Glycerin",
  "oily": "",
  "dry": "O",
  "sensitive": ""
},
{
  "name": "Stearic Acid",
  "oily": "X",
  "dry": "",
  "sensitive": ""
},

...

{
  "name": "Titanium Dioxide",
  "oily": "O",
  "dry": "",
  "sensitive": "O"
}
]
성분목록과 상품목록은 가상 데이터로 실제 상품과 관련이 없습니다.
API 구성하기
주어진 데이터를 활용해 API를 구성해야 합니다.
상품 목록 조회하기
피부 타입 별로 상품 목록을 필터링해 조회할 수 있습니다.
기능 상세
주어진 피부 타입에 대한 성분 점수를 계산해서 높은 상품 순으로 보여집니다. 점수가 같다면 낮은 가격의 상품을 먼저 표시합니다.
상품 목록을 50개 단위로 페이징 합니다. 인자로 페이지 번호가 주어지면, 해당되는 상품 목록이 보여집니다.
상품 카테고리를 선택할 수 있습니다.
제외해야 하는 성분들을 지정할 수 있습니다.
exclude_ingredient 인자로 전달한 성분들을 모두 가지지 않는 상품들만 목록에 포함합니다.
포함해야 하는 성분들을 지정할 수 있습니다.
include_ingredient 인자로 전달한 성분들을 모두 가지고 있는 상품들만 목록에 포함합니다.
URL
/products
Method
GET
Request Header 구조 예시
GET /products?skin_type=dry
Content-Type: application/json
Query Parameter
Parameter	Type	Description
skin_type	String	(필수) 지성(oily)/건성(dry)/민감성(sensitive) 중 택 1
category	String	(선택) 상품 카테고리
page	Integer	(선택) 페이지 번호
exclude_ingredient	String	(선택) 제외해야 하는 성분 목록(콤마로 구분)
include_ingredient	String	(선택) 포함해야 하는 성분 목록(콤마로 구분)
Sample Call
/products?skin_type=oily&category=skincare&page=3&include_ingredient=Glycerin
Success Response
[
    {
      "id": 17,
      "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
      "name": "화해 에센스 토너",
      "price": 23000,
      "ingredients": "Glycerin,Methyl Gluceth-20,Pulsatilla Koreana Extract,Purified Water",
      "monthlySales": 1682
    },
    {
      "id": 23,
      "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
      "name": "화해 엔젤 토너",
      "price": 4800,
      "ingredients": "Glycerin,Sodium Hyaluronate,Xanthan Gum,Niacinamide,Orchid Extract",
      "monthlySales": 463
    },


    ...


    {
      "id": 88,
      "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
      "name": "화해 화이트 브라이트닝 소프너 인리치드",
      "price": 24000,
      "ingredients": "Glycerin,Alcohol,Purified Water,Vinyl Dimethicone,PEG-10 Dimethicone",
      "monthlySales": 4437
    }
]
Response Body 구성
Column	Type	Description
id	Integer	상품 아이디
imgUrl	String	제품의 이미지 URL
name	String	상품명
price	Integer	가격
ingredients	String	성분 명(콤마로 구분)
monthlySales	Integer	이번 달 판매 수량
상품 상세 정보 조회하기
상품 상세 정보를 조회할 수 있습니다. 같은 카테고리의 상위 3개 추천 상품들도 함께 조회할 수 있습니다.
기능 상세
상품 id로 특정 상품의 상세 정보를 조회할 수 있습니다.
이미지 id를 base URL과 조합해 상품 이미지를 불러올 수 있는 URL을 보여줍니다.
같은 카테고리의 상품 중 상위 3개의 추천 상품 정보를 조회할 수 있습니다.
인자로 받은 피부 타입에 대한 성분 점수가 높은 순서로 추천합니다. 점수가 같다면, 가격이 낮은 상품을 먼저 추천합니다.
추천 상품 정보는 상품 아이디, 상품 썸네일 이미지 URL, 상품명, 가격 을 포함합니다.
URL
/product/:id
Method
GET
Request Header 구조 예시
GET /product/17?skin_type=oily
Content-Type: application/json
Query Parameter
Parameter	Type	Description
skin_type	String	(필수) 지성(oily)/건성(dry)/민감성(sensitive) 중 택 1
Sample Call
/product/17?skin_type=oily
Success Response
[
    {
      "id": 17,
      "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/image/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
      "name": "화해 에센스 토너",
      "price": 23000,
      "gender": "all",
      "category": "skincare",
      "ingredients": "Glycerin,Methyl Gluceth-20,Pulsatilla Koreana Extract,Purified Water",
      "monthlySales": 1682
    },
    {
      "id": 23,
      "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
      "name": "화해 엔젤 토너",
      "price": 33000
    },
    {
      "id": 37,
      "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
      "name": "화해 화이트 브라이트닝 소프너 인리치드",
      "price": 24800
    },
    {
      "id": 141,
      "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
      "name": "화해 퍼펙트 스킨케어",
      "price": 14800
    }
]
Response Body 구성
상품 상세 정보 response body는 해당 id 상품 정보와 3개의 추천 상품 정보를 배열로 구성합니다.
상품 정보
Column	Type	Description
id	Integer	상품 아이디
imgUrl	String	상품 fullsize 이미지 URL
name	String	상품명
price	Integer	가격
gender	String	성별(남/여/구분 없음)
category	String	카테고리
ingredients	String	성분 명(콤마로 구분)
monthlySales	Integer	이번 달 판매 수량
추천 상품 정보
Column	Type	Description
id	Integer	상품 아이디
imgUrl	String	상품 thumbnail 이미지 URL
name	String	상품명
price	Integer	가격
전반적인 구현과 관련한 요청 사항
테스트 코드를 작성하는 경우 가산점이 있습니다.
프로젝트 구조 및 성능: 사용하는 프레임워크의 Best practice를 활용해서 프로젝트를 구성해 주세요.
기능성: 버그 없이 기능이 정상적으로 동작해야 합니다.
코딩 스타일: 다른 사람이 읽기 쉽고, 디버그하기 쉽도록 Clean한 코딩 스타일을 유지해 주세요.