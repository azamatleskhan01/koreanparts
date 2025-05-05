from django.contrib import admin
from django.urls import  include
from reviews import views
from django.urls import path
from reviews.api_view import (
    AutoPartListCreateAPIView, AutoPartDetailAPIView,
    AutoPartSearchAPIView, AutoPartReviewListAPIView,
    AutoPartReviewCreateAPIView, ReviewCreateAPIView,
    ReviewListBlocked, ReviewDetailBlocked
)

#########################################################
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("catalog/", views.catalog_view, name="catalog"),
    path("cart/", views.cart_view, name="cart"),
    path("search/", views.search_view, name="search_view"),
    path("part/<int:part_id>/review/", views.add_review, name="add_review"),
    path("part/<int:part_id>/", views.part_detail, name="part_detail"),

    #####################################################################################

    path('parts/', AutoPartListCreateAPIView.as_view(), name='autopart-list-create'),
    path('parts/<int:pk>/', AutoPartDetailAPIView.as_view(), name='autopart-detail'),
    path('parts/search/', AutoPartSearchAPIView.as_view(), name='autopart-search'),
    path('parts/<int:pk>/reviews/', AutoPartReviewListAPIView.as_view(), name='autopart-reviews'),
    path('parts/<int:pk>/reviews/create/', AutoPartReviewCreateAPIView.as_view(), name='autopart-review-create'),
    path('reviews/', ReviewListBlocked.as_view(), name='review-list-blocked'),
    path('reviews/<int:pk>/', ReviewDetailBlocked.as_view(), name='review-detail-blocked'),
    path('reviews/create/', ReviewCreateAPIView.as_view(), name='review-create-blocked'),


    #####################################################################################
    path("reviews/", include("reviews.urls")),  # обязательно
    ###########################################################

    path('api/v1/', include('reviews.urls')),
    #######################################################################################

    path('silk',include('silk.urls',namespace='silk')),
]



