from . import views
from clients import views as client_views
from django.urls import include, path
from scorm import views as scorm_views

urlpatterns = [
    path('login/', views.admin_login_view, name='admin-login'),
    path('logout/', views.admin_logout_view, name='admin-logout'),

    path('create-client/', client_views.create_client_view, name='create-client'),
    path('client-dashboard/', client_views.client_dashboard_view, name='client-dashboard'),
    path('get_client_details/<int:client_id>/', client_views.get_client_details, name='get_client_details'),
    path('update_client/<int:client_id>/', client_views.client_update_view, name='update_client'), 
    path('client-details/<int:client_id>/', client_views.client_details_view, name='client-details'),

    path('scorm-dashboard/', scorm_views.scorm_dashboard_view, name='scorm-dashboard'),
    path('upload-scorm/', scorm_views.upload_scorm_view, name='upload-scorm'), 
]
