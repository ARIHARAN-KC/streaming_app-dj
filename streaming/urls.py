from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_videos, name='search_videos'),
    path('profile/<str:username>/', views.user_profile, name='profile'),
    path('watch/<str:video_id>/', views.watch_video, name='watch'),
    path('upload/', views.upload_video, name='upload_video'),
    path('dub/<str:video_id>/', views.dub_video, name='dub_video'),
    path('profile/update/', views.update_profile, name='update_profile'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
