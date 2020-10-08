from django.urls import path, re_path
from api import views

urlpatterns = [ 
    path('api/schedule/', views.schedule_list),
    re_path(r'^api/schedule/(?P<year>[0-9]{4})/$', views.y_schedule_list),
    re_path(r'^api/schedule/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.y_m_schedule_list),
    re_path(r'^api/schedule/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.y_m_d_schedule_list)
]

