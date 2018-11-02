"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from lists import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^lists/new$', views.new_list, name='new_list'),
    url(r'^lists/(\d+)/$', views.view_list, name='view_list'),  # lists/the-only-list-in-the-world/$
    url(r'^lists/(\d+)/add_item$', views.add_item, name='add_item'),
]

## the (.+) captures all of the text between the two /  
## the captured text will get passed to the view as an argument
## BUT (.+) is a "greedy" regular expression
## it captures 1/add_item from lists/1/add_item/, but django is guessing that we want a trailing slash and cutting off the end
## fix this by specifying a number be found in the regex with \d+