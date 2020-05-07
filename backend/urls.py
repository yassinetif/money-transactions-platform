
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from api import urls

admin.site.site_header = 'Money transfer admin'
admin.site.site_title = 'Money transfer admin'
admin.site.site_url = 'https://agents.monnamon.com/'
admin.site.index_title = 'Welcome into transactions platform administration'
admin.empty_value_display = '**Empty**'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urls)),
]
