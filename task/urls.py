from django.urls import path, include
from .views import *

urlpatterns = [
    path('', TasksList.as_view(), name='tasks'),
    path('<int:pk>/', TaskDetail.as_view(), name='task_detail'),
    path('create/', TaskCreate.as_view(), name='create_task'),
    path('<int:pk>/delete/', TaskDelete.as_view(), name='delete_task'),
    path('<int:pk>/update/', TaskUpdate.as_view(), name='edit_task'),
    path('categories/create/', CategoryCreate.as_view(), name='create_category'),
    path('categories/<int:pk>/delete/',
         CategoryDelete.as_view(), name='delete_category'),
]
