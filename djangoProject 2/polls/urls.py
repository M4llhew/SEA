from django.urls import path

from polls import views

app_name = "polls"
urlpatterns = [
    path("", views.login_view, name="default_login"),
    path("display", views.DisplayUsers, name="display"),
    path("update-progress", views.update_progress, name="update_progress"),
    path("delete-task", views.delete_task, name="delete_task"),
    path('update_task/<int:task_id>/', views.update_task, name='update_task'),
    path('new_task_form', views.create_new_task_form, name='new_task_form'),
    path('task_create', views.task_create, name='task_create'),
    path('logout', views.logout_view, name='logout'),
    path('login/', views.login_view, name='Login'),
    path('user_create', views.user_create, name='user_create'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/create_comment', views.create_comment_form, name='create_comment')

    # path("UpdateEmployeeNumber", views.update_employee_number, name="updateEmployee")
]
