
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from apps.api import urls
from django.contrib.staticfiles import views
from django.urls import re_path

admin.site.site_header = 'Money transfer admin'
admin.site.site_title = 'Money transfer admin'
admin.site.site_url = 'https://agents.monnamon.com/'
admin.site.index_title = 'Welcome into transactions platform administration'
admin.empty_value_display = '**Empty**'

urlpatterns = [
    path('admin_tools/', include('admin_tools.urls')),
    path('admin/', admin.site.urls),
    path('', include(urls)),
    re_path(r'^static/(?P<path>.*)$', views.serve), ]
