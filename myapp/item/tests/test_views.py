from django.test import TestCase
from django.urls import reverse

from item.views import (ItemView, ItemListView)
from .test_result_data.item_list_view_test_result import item_list_view_test_result
from .test_result_data.item_view_test_result import item_view_test_result


# Create your tests here.
class ItemViewTest(TestCase):
  def test_get(self):
      response = self.client.get(
          'http://127.0.0.1:5000/product/1/?skin_type=dry&category=suncare'
      )
      self.assertEqual(response.status_code, 404)
      self.assertJSONEqual(response.content, {
"result": "그러한 페이지가 없습니다.",
"status": 404
})
      response = self.client.get(
          reverse('programmers_test:details', args=[17]) + '?skin_type=dry'
      )
      self.assertEqual(response.status_code, 200)
      self.assertJSONEqual(response.content, item_view_test_result)
        
class ItemListViewTest(TestCase):
  def test_get(self):
      response = self.client.get(
          'http://127.0.0.1:5000/products/1/?skin_type=dry&category=suncare'
      )
      self.assertEqual(response.status_code, 404)
      self.assertJSONEqual(response.content,
      {
      "result": "그러한 페이지가 없습니다.",
      "status": 404
      })
      
      response = self.client.get(
          'http://127.0.0.1:5000/products?skin_type=dry&category=suncare'
      )
      self.assertEqual(response.status_code, 200)
      self.assertJSONEqual(response.content, item_list_view_test_result)
