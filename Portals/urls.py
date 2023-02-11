from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    #path('categorys/', include('NewsPortal.urls')),
    path('', include('NewsPortal.urls')),
    path('accounts/', include('allauth.urls'))

]
