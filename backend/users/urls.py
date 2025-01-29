from django.urls import path
from users.views import CreateUser, UpdateUser, DeleteUser, Success

urlpatterns = [
    path("success", Success.as_view(), name="success"),
    path("create", CreateUser.as_view(), name="create"),
    path("update/<int:pk>", UpdateUser.as_view(), name="update"),
    path("delete/<int:pk>", DeleteUser.as_view(), name="delete"),
]


app_name = "users"
