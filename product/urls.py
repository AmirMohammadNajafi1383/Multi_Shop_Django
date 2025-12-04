from django.urls import path

from . import views

app_name = 'product'
urlpatterns = [
    path('all', views.ProductsListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('navbar', views.NavBarPartialView.as_view(), name='navbar'),
    path('category', views.CategoryStyle.as_view(), name='category'),
]
