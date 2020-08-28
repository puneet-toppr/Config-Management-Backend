from django.contrib import admin
from django.urls import path, include
from .views import DomainView, DomainGetPost
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('<int:d_id>/', csrf_exempt(DomainView.as_view()), name = 'list_delete_one_domain'),
    #routes get/delete request for one domain with provided id

    path('', csrf_exempt(DomainGetPost.as_view()), name = 'list_add_domain'),
    #routes get request to fetch all domains at once
    #also routes post request to create a new domain
]


