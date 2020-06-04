from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.contrib import admin, auth
from testo import views

app_name = 'testo'

urlpatterns = [
    path('add', views.articolo_insert, name='articolo-add'),
    path('details/<int:id>', views.articolo_details, name='articolo-details'),
    path('search', views.articolo_meta_search, name='articolo-meta-search'),
    path('compare', views.compare1, name='articolo-compare'),
    path('compare2/<int:id>', views.compare2, name='articolo-compare2'),
    path('compare_details/<int:id1>/<int:id2>', views.compare_details, name='compare-details'),
    path('translate/<int:id_term>', views.translate_termine, name='translate-termine'),
    path('register/', views.register, name='register'),
    path('load_text', views.loaded_text_view, name='load-text'),
    path('profile', views.profile_view, name='profile'),
    path('user/login', auth_views.LoginView.as_view(), name='login'),
    path('user/logout', auth_views.LogoutView.as_view(), name='logout'),
    path('delete/<int:id>', views.articolo_delete, name='delete'),
    path('blacklist_delete/<termine_bl>', views.blacklist_delete, name='blacklist-delete'),
    path('blacklist', views.blacklist, name='user-blacklist'),
    path('statistiche_articoli', views.statistiche_articoli, name='statistiche-articoli'),
    path('sinonimi/<int:id_term>', views.sinonimi_view, name='sinonimi'),
]

