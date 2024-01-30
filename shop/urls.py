from django .urls import path
from .import views
from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('category/<slug:category_slug>/', views.products_by_category, name='products_by_category'),
    path('products/<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('search',views.searching,name='search'),
    path('register/',views.Register,name='register'),
    path('login/',views.custom_login,name='login'),
    path('logout/', logout_page, name='logout'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('viewcart/',view_cart,name='viewcart'),
    path('update_to_cart/', update_to_cart, name='update_to_cart'),
    path('delete_from_cart/', delete_from_cart, name='delete_from_cart'),
]