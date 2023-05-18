from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('progress/', views.progresses_index, name='index'),
    path('progresses/<int:progress_id>/', views.progresses_detail, name='detail'),
    path('progresses/create/', views.ProgressCreate.as_view(), name='progresses_create'),
    path('progresses/<int:pk>/update/', views.ProgressUpdate.as_view(), name='progresses_update'),
    path('progresses/<int:pk>/delete/', views.ProgressDelete.as_view(), name='progresses_delete'),
    path('progresses/<int:progress_id>/add_checklist/', views.add_checklist, name='add_checklist'),
    path('progresses/<int:progress_id>/assoc_recommendation/<int:recommendation_id>/', views.assoc_recommendation, name='assoc_recommendation'),
    path('progresses/<int:progress_id>/unassoc_recommendation/<int:recommendation_id>/', views.unassoc_recommendation, name='unassoc_recommendation'),
    path('recommendations/', views.RecommendationList.as_view(), name='recommendations_index'),
    path('recommendations/<int:pk>/', views.RecommendationDetail.as_view(), name='recommendations_detail'),
    path('recommendations/create/', views.RecommendationCreate.as_view(), name='recommendations_create'),
    path('recommendations/<int:pk>/update/', views.RecommendationUpdate.as_view(), name='recommendations_update'),
    path('recommendations/<int:pk>/delete/', views.RecommendationDelete.as_view(), name='recommendations_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('progresses/<int:progress_id>/add_photo/', views.add_photo, name='add_photo'),
]