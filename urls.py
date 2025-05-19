from django.contrib import admin
from django.urls import path
from auapp.views import login_view,home,logout_view,signup,changepw,rnp


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/',login_view, name='login_view'),
    path('signup/',signup, name='signup'),
    path('logout_view/',logout_view, name='logout_view'),
    path("",home, name='home'),
    path('changepw/',changepw, name='changepw'),
    path('rnp/',rnp, name='rnp'),
    # Other paths as needed
]
