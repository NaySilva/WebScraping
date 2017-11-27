from django.conf.urls import url

from core import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^question/1/$', views.question1, name='question1'),
    url(r'^question/2/$', views.question2, name='question2'),
    url(r'^question/3/$', views.question3, name='question3'),
    url(r'^question/4/$', views.question4, name='question4'),
    url(r'^question/5/$', views.question5, name='question5'),
    url(r'save/4/$', views.saveDataQ4, name='save-data-q4'),
    url(r'^save/(?P<q_id>[\d]+)/$', views.saveData, name='save-data'),
]