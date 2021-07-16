
from django.urls import path,include
from .views import register,login,logout_user,profile,profile_pic_update,set
urlpatterns = [
    
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('logout/',logout_user,name="logout"),
    path('profile/<int:pk>/',profile,name="profile"),
    path('profile_pic_update/<int:pk>/',profile_pic_update,name="profile_pic_update"),
    path('set/',set,name="set"),
    
]