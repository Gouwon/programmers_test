from django.db import models
from django.urls import reverse
from django.forms.models import model_to_dict


# Create your models here.
# Gender-Item N:1, Category-Item N:1, Ingredient-Item N:M

BASE_URL = u'https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/'


class Gender(models.Model):
    GENDER_NONE = 0
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_NONE, u'구분없음'),
        (GENDER_MALE, u'남자'),
        (GENDER_FEMALE, u'여자'),
    ]

    gender = models.IntegerField(choices=GENDER_CHOICES)

    def __str__(self):
        presentation_dictionary = {
            0: u'all',
            1: u'male',
            2: u'female',
        }
        return presentation_dictionary.get(self.gender, None)
    
class Category(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category
    
    def __repr__(self):
        return self.category

class Ingredient(models.Model):
    INGREDIENT_GOOD = 1
    INGREDIENT_NONE = 0
    INGREDIENT_HARM = -1
    INGREDIENT_CHOICES = [
        (INGREDIENT_GOOD, u'유익함'),
        (INGREDIENT_NONE, u'영향없음'),
        (INGREDIENT_HARM, u'유해함'),
    ]

    name = models.CharField(max_length=200)
    oily = models.IntegerField(choices=INGREDIENT_CHOICES)
    dry = models.IntegerField(choices=INGREDIENT_CHOICES)
    sensitive = models.IntegerField(choices=INGREDIENT_CHOICES)

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self.name)

class Item(models.Model):
    image_id = models.CharField(max_length=1023)
    name = models.CharField(max_length=1023)
    price = models.IntegerField(default=0)
    monthly_sales = models.IntegerField(default=0)

    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from . import views
        return reverse('item:details', args=[str(self.id)])

    def make_imgURL(self, full=False):
        """
        화장품의 이미지 주소를 인자값에 따라서 만듦. full이 True면 image, False면 thumbnail
        """
        self.imgURL = BASE_URL + 'thumbnail/' + self.image_id + '.jpg'
        if full:
            self.imgURL = BASE_URL + 'image/' + self.image_id + '.jpg'

    def get_json(self, info_level=0):
        """
        화장품 객체의 결과로서 보내줄 json 형식의 데이터를 info_level에 따라 만들어서 처리.
        info_level=0이면 결과값은 (id, imgUrl, name, price),
        1이면 결과값은 (id, imgUrl, name, price, ingredients, monthlySales)
        2이면 결과값은 (id, imgUrl, name, price, ingredients, monthlySales,
        gender, category)
        """
        def add_data(full=False):
            self.make_imgURL()
            data = model_to_dict(self)
            if full is None:
                del data['gender']
                del data['category']
                del data['monthly_sales']
                del data['ingredients']
                del data['image_id']
                data['imgUrl'] = self.imgURL
            elif full is False:
                del data['gender']
                del data['category']
                del data['image_id']
                data['imgUrl'] = self.imgURL
                data['monthlySales'] = data.pop('monthly_sales', 0)
                stringified_ingredients = \
                    [str(name) for name in data['ingredients']]
                data['ingredients'] = ','.join(stringified_ingredients)
            else:
                self.make_imgURL(True)
                del data['image_id']
                data['imgUrl'] = self.imgURL
                data['gender'] = str(self.gender)
                data['category'] = str(self.category)
                stringified_ingredients = \
                    [str(name) for name in data['ingredients']]
                data['ingredients'] = ','.join(stringified_ingredients)
            return data
        
        data_construct = {
            0: None,
            1: False,
            2: True,
        }

        return add_data(data_construct[info_level])
        