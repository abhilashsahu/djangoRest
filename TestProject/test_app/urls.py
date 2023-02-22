from django.urls import path, include
from .views import ProjectAPIView, ProjectDetailsView

urlpatterns = [
    path('projects/', ProjectAPIView.as_view(), name='projects'),
    path('project/<int:project_id>', ProjectDetailsView.as_view()),
]
