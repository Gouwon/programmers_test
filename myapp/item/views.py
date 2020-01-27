from functools import wraps

from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from django.db.models import (Sum, Max)

from .models import (Gender, Category, Ingredient, Item)


# Create your views here.
def resonpse_in_json(f):
    """
    view 함수가 반환하는 결과값을 Json 형식으로 처리하여 브라우저에게 응답을 주는 데코레이터.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        result = f(*args, **kwargs)
        if str(type(result)) != "<class 'dict'>":
            result = {'result': result,
                'status': 200,
            }
        status = result.get('status', None)
        if status is None:
            status = 200
        return JsonResponse(
            result,
            json_dumps_params={
                'indent': 2, 
                'ensure_ascii': False
                }, 
            status=status,
        )
    return decorated_function

# Create your views here.
def index(request):
    return render(request, 'templates/index.html')

## 잘못된 요청이나 서버의 처리 오류 등이 있을 때, json의 형식으로 결과를 처리하기 위한 view 함수
@resonpse_in_json
def error403(request, exception):
    print('\n\n\n custom_forbidden request, exception', request, exception)
    return {'result': u'허용되지 않는 HTTP Request Method입니다.', 'status': 403}

@resonpse_in_json
def error404(request, exception):
    print('\n\n\n custom_page_not_found request&exception', request, exception)
    return {'result': u'그러한 페이지가 없습니다.', 'status': 404}

@resonpse_in_json
def error500(request):
    print('\n\n\n custom_server_error request, exception', request)
    return {'result': u'서버가 잘 모르나 봅니다.', 'status': 500}

class ItemView(generic.View):
    # PUT, POST, DELETE의 허용되지 않는 메소드 요청들을 json 형식으로 응답을 처리.
    @resonpse_in_json
    def custom_permission_denied(self, requset):
        return {'result': u'허용되지 않는 요청메소드입니다.'}

    def post(self, request, id):
        return self.custom_permission_denied(request)

    def put(self, request, id):
        return self.custom_permission_denied(request)

    def delete(self, request, id):
        return self.custom_permission_denied(request)

    @resonpse_in_json
    def get(self, request, id):
        """
        사용자가 요청한 쿼리 파라미터와 item id를 통해서 해당하는 item 객체를 찾고, 카테고리와 
        피부타입, 가격에 따라서 순서를 정해서 데이터를 dict 형식으로 결과를 처리
        """
        skin_type_dict = {
            'oily': 'ingredients__oily', 
            'dry': 'ingredients__dry',
            'sensitive': 'ingredients__sensitive'
            }

        # 적절한 쿼리 파라미터를 포함한 요청이 왔는지 확인
        skin_type = request.GET.dict().get('skin_type', None)
        if skin_type not in skin_type_dict.keys():
            return {'result': 'Bad Request'}

        try:
            # 요청한 item의 객체를 통해서, 카테고리를 확인하고, 요청한 정보대로 추천상품 처리
            item = Item.objects.get(id=id)
            query_set = Item.objects.filter(category_id=item.category_id)
            query_set = query_set.values('id').annotate(
                    sum=Sum(skin_type_dict.get(skin_type, None)),
                    price=Max('price'),
                    category=Max('category_id'),
                    ).exclude(id=item.id)
            query_set = query_set.order_by('-sum', 'price')
            query_set = query_set[:3]

            # filtering된 queryset을 이용하여 itme객체로 바꿔서 요청한 데이터를 처리
            recommanded_items = \
                    Item.objects.in_bulk(
                        [q_dict['id'] for q_dict in query_set]
                    )
            recommanded_items = \
                [item.get_json() for item in recommanded_items.values()]

            result = [item.get_json(info_level=2)]
            result.extend(recommanded_items)

        except Exception as sqlerr:
            print('\n\n\n ItemView.get().sqlerr >>>>>>> ', sqlerr)
            print(item.get_absolute_url())
            result = {'msg': u'해당하는 상품이 없습니다. ' + str(sqlerr)}
            
        finally:
            return result

class ItemListView(generic.View):
    # PUT, POST, DELETE의 허용되지 않는 메소드 요청들을 json 형식으로 응답을 처리.
    @resonpse_in_json
    def custom_permission_denied(self, requset):
        return JsonResponse({'result': u'허용되지 않는 요청메소드입니다.'}, status=403)

    def post(self, request, id):
        return self.custom_permission_denied(request)

    def put(self, request, id):
        return self.custom_permission_denied(request)

    def delete(self, request, id):
        return self.custom_permission_denied(request)

    def get_items_with_ingredients(self, ingredients_list):
        """
        ingredients_list에 들어있는 ingredient를 순회하면서 해당 성분들을 모두 포함하고 있는 
        item의 id를 set type으로 돌려준다.
        """
        result = set()
        query_set= Item.ingredients.through.objects.values('item_id')

        for index, ingredeint_name in enumerate(ingredients_list):
            query_result = query_set.filter(ingredient__name=ingredeint_name)

            if index == 0:
                result.update([query['item_id'] for query in query_result])

            else:
                sub_set = set([query['item_id'] for query in query_result])
                result &= sub_set

        return result

    @resonpse_in_json
    def get(self, request):
        """
        사용자가 요청한 쿼리 파라미터를 확인하고, 카테고리와 피부 타입에 따른 화장품 목록을 list로
        처리하거나, 요청에 맞는 결과가 없다면 dict형식으로 메세지를 결과값으로 처리
        """
        skin_type_dict = {
            'oily': 'ingredients__oily', 
            'dry': 'ingredients__dry',
            'sensitive': 'ingredients__sensitive',
        }
        required_query_parameter_list = ['skin_type', 'category']
        request_dictionary = request.GET.dict()

        try:
            # 적절한 쿼리 파라미터를 포함한 요청이 왔는지 확인
            for required_query_parameter in required_query_parameter_list:
                if required_query_parameter not in request_dictionary.keys():
                    raise Exception
            
            # 요구한 카테고리에 해당하는 화장품들을 포함하는 queryset으로 요구에 맞는 처리 시작
            query_set = Item.objects.values().filter(
            category__category=request_dictionary.get('category', None)
            )

            query_set = query_set.values('id').annotate(
                    sum=Sum(
                        skin_type_dict.get(
                            request_dictionary.get('skin_type', None),
                            None
                            )
                        ),
                    price=Max('price'),
                    category=Max('category_id'),
                    )

            try:
                # 포함/불포함해야 하는 성분이 있는지 확인하고, 있다면 이를 포함하고 있는
                # 화장품 id를 일단 따로 모아둠.
                include_ingredient = request_dictionary.get(
                    'include_ingredient', None
                )
                include_ingredient_id_set = set()
                if include_ingredient is not None:
                    include_ingredient = include_ingredient.split(',')
                    include_ingredient_id_set.update(
                        self.get_items_with_ingredients(include_ingredient)
                    )
                
                exclude_ingredient = request_dictionary.get(
                    'exclude_ingredient', None
                )
                exclude_ingredient_id_set = set()

                if exclude_ingredient is not None:
                    exclude_ingredient = exclude_ingredient.split(',')
                    exclude_ingredient_id_set.update(
                        self.get_items_with_ingredients(exclude_ingredient)
                    )
                    include_ingredient_id_set &= exclude_ingredient_id_set

                # 위에서의 결과, 포함/불포함 성분을 가지고 있는 화장품이 있다면, 그 화장품을 제외
                if len(include_ingredient_id_set) != 0:
                    query_set = query_set.filter(
                        id__in=include_ingredient_id_set
                    )
                
                # 요구사항에 맞춰서 화장품들의 순서를 처리
                query_set = query_set.order_by('-sum', 'price')
                page = int(request_dictionary.get('page', 0))
                query_set = query_set[50 * (page): 50 * (1 + page)]

                # 결과 queryset을 item 객체로 바꿔서 요청하는 데이터 형식으로 처리
                result = Item.objects.in_bulk(
                    [q_dict['id'] for q_dict in query_set]
                )
                result = [item.get_json(1) for item in result.values()]

                # 만약 결과값이 없다면 다음과 같이 처리
                if len(result) == 0:
                    result = {'msg': u'해당하는 상품이 없습니다.'}

            except Exception as sqlerr:
                print('\n\n\n ItemListView.get().sqlerr >>>>>>> ', sqlerr)
                result = {'msg': u'해당하는 상품이 없습니다. ' + str(sqlerr)}

        except Exception as sqlerr:
            print('\n\n\n ItemListView.get().sqlerr >>>>>>> ', sqlerr)
            result = {'msg': u'잘못된 요청입니다. 상품의 카테고리나 피부타입을 지정해주세요.'}

        finally:
            return result