from django.urls import path
from .views import CourseList, CourseDetail, ChapterDetail, VideosDetail

urlpatterns = [
    path('', CourseList.as_view(), name='course-list'),
    path('course/<int:pk>/', CourseDetail.as_view(), name='course-detail'),
    path('chapter/<int:pk>/', ChapterDetail.as_view(), name='chapter-detail'),
    path('videos/<int:pk>/', VideosDetail.as_view(), name='videos-detail'),
]
