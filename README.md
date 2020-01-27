## 프로젝트 개요
 해당 프로젝트는 국내 모든 화장품 정보 플래폼, '화해'를 운용 중인 '버드뷰'의 프로그래머스 제출용 프로젝트입니다. 해당 프로젝트는 Python의 Back-End Framework인 Django를 활용한 간단한 RESTful API를 구성하는 프로젝트입니다.

## 프로젝트의 구성
 해당 프로젝트는 RESTful API를 구성하기 위하여 'Heroku'와 'gunicorn'을 통해서 배포 환경을 구성하고, Web Application으로서 Django를 이용하고 있습니다. 데이터 저장 및 관리의 부분은 MySQL 5.8을 사용하였습니다.

 
## 라이브러리
 해당 프로젝트에서 사용된 라이브러리는 과제의 최소 요구 라이브러리들로만 구성되어 있습니다.

* dj-database-url 0.5.0v
* Django 2.2.4v
* unicorn 19.9.0v
* mysqlclient 1.4.4v
* putz 2019.2v
* sqlparse 0.3.0v
* whitenoise 4.1.3v

## 설치 및 사용법
 이 프로젝트는 파이썬을 기본 개발 언어로 사용하고 있습니다. 따라서 Python 3.6이상에 원활하게 사용됩니다. 상기 라이브러리는 Python의 ```pip``` 를 이용하여 일괄적으로 설치할 수 있습니다.

```pip install -r requirements.txt```

 이후, 'Heroku'와 'gunicorn'을 통해서 Web Server가 배포되면, 웹 브라우저를 통해서 통해서 HTTP ```GET``` 메서드를 이용하여 사용자가 화장품에 대한 정보를 요청하면 Web Application인 Django가 요청을 처리하여 적절한 데이터를 MySQL에서 select하여 웹 브라우저에게 ```json``` 형식으로 응답을 하게 됩니다.

## DB의 구성
 DB는 RDBMS인 MySQL을 사용하고 있습니다. 제공받은 데이터를 통해서 크게 5개의 테이블로 다음과 같이 구성하였습니다. 
 
![ERR](https://github.com/Gouwon/programmers_test/blob/master/Programmers_eer.png?raw=true)

 * **item** : 화장품의 기본 정보를 저장하는 테이블
 *  **ingredient** : 화장품들에 사용되는 성분들의 기본 정보를 저장하는 테이블
 * **item-ingredients** : 각 화장품에 사용되는 성분들이 화장품과 mapping되는 테이블
 * **gender** : 화장품이 가지는 성별을 따로 정의한 테이블
 * **category** : 화장품이 가지는 카테고리를 따로 정의한 테이블

## Code
RESTful API를 구성하기 위해서 view를 함수형이 아닌 클래스형으로 처리하였습니다.
```
class  ItemView(generic.View):
	@response_in_json
	def get(self, request, id):
	...
```
또한 응답의 결과 값으로 ```json``` 형식으로 보내기 위해서 ```JsonResponse```으로 결과를 처리하였고, 이를 위하여 '**response_in_json**' 이라는 ```decorator```을 이용하여 각 클래스의 메서드들을 처리하였습니다.

이후, 적절한 요청에 대하여 django의 ORM을 이용하여 ```QuerySet```을 구하고, 요구사항에 맞게 결과값을 만들어서 웹 브라우저에게 응답합니다. item의 결과값으로 요구되는 ```json```의 데이터 구조가 다르기 때문에 ```models.py```에 정의된 ```item``` 클래스에는 요구되는 데이터 구조에 따라 값을 반환하는 ```get_json()``` 메서드를 구현하여 처리하였습니다.

```
def  get_json(self, info_level=0):
	def  add_data(full=False):
		... full에 따라 요청사항에 따라 dictionary를 만듦.
		return result		# ===> str(type(result)) == "<class 'dict'>"
		data_construct = {
				0: None,
				1: False,
				2: True,
		}
	return add_data(data_construct[info_level])
```

## Contacts
### 김건우 : jskd2938@gmail.com
