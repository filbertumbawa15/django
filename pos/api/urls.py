from django.urls import path, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'
urlpatterns = [
    # path('api/v1/login', LoginView.as_view()),
    # path('api/v1/logout', LogoutView.as_view()),
    # path('api/v1/register', RegisterView.as_view()),
    path('api/table-resto', views.TableRestoListApiView.as_view()),
    path('api/table-resto/<int:id>', views.TableRestoDetailApiView.as_view()),
    path('api/category', views.CategoryListApiView.as_view()),
    path('api/category/<int:id>', views.CategoryDetailApiView.as_view()),
]