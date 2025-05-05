from django.urls import path
from .api_view import (
    AutoPartListCreateAPIView, AutoPartDetailAPIView,
    AutoPartSearchAPIView, AutoPartReviewListAPIView,
    AutoPartReviewCreateAPIView, ReviewListBlocked,
    ReviewDetailBlocked, ReviewCreateAPIView
)
from reviews.api_view import (
    AutoPartListAPIView, AutoPartDetailAPIView,
    AutoPartListCreateAPIView as GenericAutoPartListCreateAPIView,
    AutoPartReviewListAPIView as GenericAutoPartReviewListAPIView,
    AutoPartReviewCreateAPIView as GenericAutoPartReviewCreateAPIView
)

urlpatterns = [
    # APIView endpoints (Video6 + Video5 profiling)
    path('parts/', AutoPartListCreateAPIView.as_view(), name='autopart-list-create'),
    path('parts/<int:pk>/', AutoPartDetailAPIView.as_view(), name='autopart-detail'),
    path('parts/search/', AutoPartSearchAPIView.as_view(), name='autopart-search'),
    path('parts/<int:pk>/reviews/', AutoPartReviewListAPIView.as_view(), name='autopart-reviews'),
    path('parts/<int:pk>/reviews/create/', AutoPartReviewCreateAPIView.as_view(), name='autopart-review-create'),

    path('reviews/', ReviewListBlocked.as_view(), name='review-list-blocked'),
    path('reviews/<int:pk>/', ReviewDetailBlocked.as_view(), name='review-detail-blocked'),
    path('reviews/create/', ReviewCreateAPIView.as_view(), name='review-create-blocked'),

    # GenericAPIView endpoints (Video6)
    path('generic/parts/', AutoPartListAPIView.as_view(), name='generic-part-list'),
    path('generic/parts/list/', AutoPartListAPIView.as_view(), name='generic-part-list-alt'),
    path('generic/parts/<int:pk>/', AutoPartDetailAPIView.as_view(), name='generic-part-detail'),
    path('generic/parts/<int:pk>/reviews/', AutoPartReviewListAPIView.as_view(), name='generic-part-reviews'),
    path('generic/parts/<int:pk>/reviews/create/', AutoPartReviewCreateAPIView.as_view(), name='generic-part-review-create'),

]