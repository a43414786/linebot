from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from foodlinebot import main
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^callback', main.callback),
]
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
#urlpatterns+=static('/static/', ['D:/static'])