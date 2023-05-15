from django.urls import path
from django.views.generic import TemplateView
from saas_02.core import views
from django.contrib.auth.decorators import login_required


app_name = "core"
urlpatterns = [
    path("", login_required(TemplateView.as_view(template_name='pages/demo.html')), name='demo'),
    path("upload/", views.ImageRecognitionView.as_view(), name='image-recognition'),
    # path("demo/", views.FileUploadView.as_view(), name='file-upload-demo'),

    # Reset Email
    path("change-email/", views.ChangeEmailView.as_view(), name='change-email'),
    path("get-email/", views.GetUserEmailView.as_view(), name='get-email'),

    # password
    path("password/", login_required(TemplateView.as_view(template_name='pages/reset_password.html')), name='password'), # html page
    path("password-reset/", views.ResetPasswordAPIView.as_view(), name='password-reset'), # html page

    # api-key
    path("api-key/", login_required(TemplateView.as_view(template_name='pages/api-key.html')), name='api-key'), # html page

    # billing 
    path("billing/", login_required(TemplateView.as_view(template_name='pages/billing.html')), name='billing'), # billing page
    path("billing-detail/", views.UserBillingDetailsView.as_view(), name='billing-detail'), # return user's billing status 

    #stipe subscribe
    path("create-checkout-session/", views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'), # return url checkout_session
    path("webhooks/stripe/", views.webhook, name='stripe-webhook'), # except stripe webhooks

    # cancel-subscription
    path("cancel-subscription/", views.CancelSubscriptionView.as_view(), name="cancel-subscription"),

#    loader
    path("loader/", login_required(TemplateView.as_view(template_name='pages/loader.html')), name='loader'), # billing page
]
