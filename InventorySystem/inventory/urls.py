from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.org_list, name='org_list'),
    url('auth', views.auth, name='auth'),
    url('add_org', views.add_org, name='add_org'),
    url('org_info', views.org_info, name='org_info'),
    url('wealth_info', views.wealth_info, name='wealth_info'),
    url('set_wealth', views.set_wealth, name='set_wealth'),
    url('add_wealth', views.add_wealth, name='add_wealth'),

]
