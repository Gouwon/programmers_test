from django.urls import path
from . import views


app_name = 'item'
extra_patterns = [
    path('<int:id>', views.ItemView.as_view(), name='details'),
]

urlpatterns = [
    path('', views.ItemListView.as_view(), name='lists'),
]
