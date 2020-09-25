from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.home_page, name='post_index'),
    path('about/', views.about_page, name='about_page'),
    path('contactus/', views.contact, name='contactus'),
    path('list/', views.post_list, name='post_list'),
    path('search/', views.post_search, name='post_search'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
]
