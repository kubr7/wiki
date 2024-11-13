from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new-page/", views.new_page, name="new-page"),
    path("edit/", views.edit, name="edit"),
    path("save-edit/", views.save_edit, name="save-edit"),
    path('delete/<str:title>/', views.delete_page, name='delete_page'),
    path("random-page/", views.random_page, name="random-page")
]