from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.org_list, name='org_list'),
    url('auth', views.auth, name='auth'),
    url('add_org', views.add_org, name='add_org'),
    url('delete_org', views.delete_org, name='delete_org'),    
    url('org_info', views.org_info, name='org_info'),
    url('wealth_info', views.wealth_info, name='wealth_info'),
    url('add_wealth', views.add_wealth, name='add_wealth'),
    url('delete_wealth', views.delete_wealth, name='delete_wealth'),
    url('ap', views.ap, name='ap'),

]
