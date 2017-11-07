"""syproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static


from eforms.views import (
    test_menu, homepage, list_eform,
    CreateEFormActivity, 
    ViewEFormActivity, 
    ApproveEFormActivity, 
    ViewBasicEFormActivity, 
    ViewReviewEFormActivity,
    DeleteEFormActivity,
    EditEFormActivity    
    )


from .views import login, logout
#from django.contrib.auth import views as  auth

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^menu/$', test_menu),

    #url(r'^eforms/([0-9]{1})/Create/$', CreateEFormActivity.as_view(), name="create"),    
    url(r'^eforms/(?P<pk>[0-9]+)/Create/$', CreateEFormActivity.as_view(), name="create"),

    #url(r'^eforms/UpdateRequest$', update_list_eform, name="update_request"),    

    url(r'^eforms/UpdateRequest$', list_eform, name="update_request"),    
    url(r'^eforms/$', list_eform),

    url(r'^eforms/(?P<pk>[0-9]+)/View/(?P<tk>\d+)$', ViewEFormActivity.as_view(), name="view"),
    url(r'^eforms/(?P<pk>[0-9]+)/ViewBasic/(?P<tk>\d+)$', ViewBasicEFormActivity.as_view()),
    url(r'^eforms/(?P<pk>[0-9]+)/ViewReview/(?P<tk>\d+)$', ViewReviewEFormActivity.as_view()),

    url(r'^eforms/(?P<pk>[0-9]+)/Edit/(?P<tk>\d+)$', EditEFormActivity.as_view(), name="edit"),    


    url(r'^eforms/(?P<pk>[0-9]+)/Delete/(?P<tk>\d+)$', DeleteEFormActivity.as_view()),


    url(r'^eforms/(?P<pk>[0-9]+)/Approve/(?P<tk>\d+)$', ApproveEFormActivity.as_view(), name="approve"),


    #url(r'auth/', include('django.contrib.auth.urls')),
    url(r'^accounts/login/$',  login), url(r'^accounts/logout/$', logout),        
    #url(r'^accounts/login/$',  auth.login), url(r'^accounts/logout/$', auth.logout),    
    #url(r'^index/$',list_eform),       
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [url(r'^',homepage)]     

