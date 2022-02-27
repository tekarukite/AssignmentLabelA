from django.contrib import admin
from django.urls import path, include
from users import views

urlpatterns = [
    path('web/', include('productWebsite.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # new
    path("register", views.register_request, name="register")
]
