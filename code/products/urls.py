from django.urls import path

app_name = 'products'
from .views import (
    ProductListView,
    # product_list_view,
    # ProductDetailView,
    ProductDetailSlugView,
    # product_detail_view,
    # ProductFeaturedListView,
    # ProductFeaturedDetailView
)

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('<slug>', ProductDetailSlugView.as_view(), name='detail'),
]
