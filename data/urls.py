__author__ = "Sabyasachi Nandy <sabyasachi.nandy@vphrase.com"

from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "data"

urlpatterns = [
    path(
        '<int:pk>/delete/',
        views.DataRUDView.as_view(),
        name=views.DataRUDView.name
    ),
    path(
        'list',
        views.DataListView.as_view(),
        name=views.DataListView.name
    ),
    path(
        'create',
        views.DataCreateView.as_view(),
        name=views.DataCreateView.name
    ),

]
