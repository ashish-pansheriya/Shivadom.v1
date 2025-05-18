
from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path 
from django.urls import path
from . import views
urlpatterns = [
    #path('post-home', PostListView.as_view(), name='post-home'),
#    path('', home, name='home'),
    path('', blogsearchview.as_view(), name='home'),
#    path('blog-home', blogsearchview.as_view(), name='blog-home'),
    path('blogs/', blogSearchListView.as_view(), name='blog-home'),
    path('blog/<int:pk>/', blogDetailView.as_view(), name='blog-detail'),
    path('blog/new/', blogCreateView.as_view(), name='blog-create'),
    path('blog/<int:pk>/update/', blogUpdateView.as_view(), name='blog-update'),
    path('blog/<int:pk>/delete/', blogDeleteView.as_view(), name='blog-delete'),
    path('ajax-search/', views.ajax_search, name='ajax-search'),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
