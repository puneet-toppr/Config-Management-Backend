from django.contrib import admin
from django.urls import path, include
from .views import FeatureView, FeatureGetPost
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('<int:f_id>/', csrf_exempt(FeatureView.as_view()), name = 'list_delete_one_feature'),
    #routes get/delete request for one feature with provided id

    path('', csrf_exempt(FeatureGetPost.as_view()), name = 'list_add_feature'),
    #routes get request to fetch all features at once
    #also routes post request to create a new feature
]

