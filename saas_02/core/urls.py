from django.urls import path
from django.views.generic import TemplateView
from saas_02.core import views


app_name = "core"
urlpatterns = [
    path("", TemplateView.as_view(template_name='pages/demo.html'), name='demo'),
    path("demo/", views.FileUploadView.as_view(), name='file-upload-demo'),

    path("change-email/", views.ChangeEmailView.as_view(), name='change-email'),
    path("get-email/", views.GetUserEmailView.as_view(), name='get-email'),

    # password
    path("password/", TemplateView.as_view(template_name='pages/reset_password.html'), name='password'), # html page
    path("password-reset/", views.ResetPasswordAPIView.as_view(), name='password-reset'), # html page
    
    # billing 
    path("billing/", TemplateView.as_view(template_name='pages/billing.html'), name='billing'), # billing page

    
]
