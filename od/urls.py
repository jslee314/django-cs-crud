from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_list, name='od_upload_list'),          # 업로드 목록 + 업로드 폼
    path('<int:pk>/', views.run_detail, name='od_run_detail'),   # 분석 결과 상세
    path('<int:upload_id>/analyze/', views.analyze_now, name='od_analyze_now'),  # 수동 분석 실행
]