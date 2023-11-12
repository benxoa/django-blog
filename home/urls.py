from django.urls import path,include
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("about", about, name="about"),
    path("contact", contact, name="contact"),
    
    path("article/<int:pk>", article, name="article"),
    
    path("login", login_page, name="login"),
    path("signup", signup, name='signup'),
    path("logout", logout_page, name="logout"),
    


]