from django.test import TestCase
from item.models import (Gender, Category, Ingredient, Item)


# Create your tests here.
class GenderTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: # Set up non-modified objects used by all test methods")
        cls.gender = Gender.objects.create(gender=0)

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        return super().setUp()
    
    def test_gender_str(self):
      expected = u'all'
      self.assertEquals(expected, str(self.gender))

class CategoryTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category(category='suncare')
    
    def test_category_str(self):
        expected = u'suncare'
        self.assertEquals(expected, str(self.category))

class IngredientTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ingredient = Ingredient(
            name='ready',
            dry=1,
            oily=-1,
            sensitive=-1)
    
    def test_ingredient_str(self):
        expected = u'ready'
        self.assertEquals(expected, str(self.ingredient))

class ItemTestCase(TestCase):
    BASE_URL = u'https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/'

    @classmethod
    def setUpTestData(cls):

        gender = Gender(gender=1)
        gender.save()
        category = Category(category='basemakeup')
        category.save()

        ingredient1 = Ingredient(
            name='foo',
            dry=0,
            oily=1,
            sensitive=-1
        )
        ingredient1.save()
        ingredient2 = Ingredient(
            name='bar',
            dry=-1,
            oily=0,
            sensitive=1
        )
        cls.item = Item(
            image_id='asdlfk1234ss',
            name='recursion',
            price=23000,
            monthly_sales=4444,
            gender=gender,
            category=category
        )
        ingredient2.save()
        cls.item.save()
        print('=====================')
        print('\n\n\n>>>>>> ', cls.item, cls.item.id)
        cls.item.make_imgURL()
        cls.item.ingredients.add(ingredient1)
        cls.item.ingredients.add(ingredient2)

    def test_item_str(self):
        expected = u'recursion'
        self.assertEquals(expected, str(self.item))
    
    def test_get_absolute_url(self):
        expected = '/product/1001'
        self.assertEquals(expected, self.item.get_absolute_url())
    
    def test_make_imgURL(self):
        expected = self.BASE_URL + 'thumbnail/' + self.item.image_id + '.jpg'
        self.assertEquals(expected, self.item.imgURL)
    
    def test_get_json(self):
        expected = {
            'id':1001,
            'imgUrl': u'https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/asdlfk1234ss.jpg',
            'name': 'recursion',
            'price': 23000
        }
        self.assertDictEqual(expected, self.item.get_json(0))