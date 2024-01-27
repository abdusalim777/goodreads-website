from django.urls import path

# from api.views import BookReviewDetailApiView, BookListAPIView
from rest_framework.routers import DefaultRouter
from api.views import BookReviewViewSet


app_name = 'api'
router = DefaultRouter()
router.register('reviews', BookReviewViewSet, basename='review')

urlpatterns = router.urls


# urlpatterns = [
#     path('reviews/', BookListAPIView.as_view(), name='review_list'),
#     path('reviews/<int:id>/', BookReviewDetailApiView.as_view(), name='review_detail')
# ]
