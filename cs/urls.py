from django.urls import path
from . import views

urlpatterns = [
    path('', views.case_list, name='case_list'),                    # 목록
    path('create/', views.case_create, name='case_create'),         # 생성
    path('<int:pk>/', views.case_detail, name='case_detail'),       # 상세
    path('<int:pk>/update/', views.case_update, name='case_update'),# 수정
    path('<int:pk>/delete/', views.case_delete, name='case_delete') # 삭제
]
