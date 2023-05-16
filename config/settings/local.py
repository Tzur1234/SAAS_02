from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="AN40KrdsKR8aRLycvYR6wiJxZEkfd9gFXTu6kiCtDgrhjTeK83sD6at0szGjrjuk",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", '57fa-93-173-113-150.ngrok-free.app']

# 5-STRIPE-LAPTOP
# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")




# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa: F405


# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
# INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405
# # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
# MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa: F405
# # https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
# DEBUG_TOOLBAR_CONFIG = {
#     # "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
#     "SHOW_TEMPLATE_CONTEXT": True,
# }
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
if env("USE_DOCKER") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]  # noqa: F405

# Your stuff...




# STORAGES
# Your Spaces Bucket's origin URL: https://trydjangoloc.fra1.digitaloceanspaces.com
# ------------------------------------------------------------------------------
# https://django-storages.readthedocs.io/en/latest/#installation
INSTALLED_APPS += ["storages"]  # noqa: F405
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_ACCESS_KEY_ID = 'DO00PZ3VMZCV3BFRZNWL'
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_SECRET_ACCESS_KEY = 'aloOXzNreTok/8zl+3nbOwWFKihCnmxo8/6UfZYfJxs'
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_STORAGE_BUCKET_NAME = 'trydjangoloc'

AWS_S3_ENDPOINT_URL = 'https://fra1.digitaloceanspaces.com'

AWS_S3_REGION_NAME = 'fra1'

AWS_LOCATION = 'https://trydjangoloc.fra1.digitaloceanspaces.com'


AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": f"max-age=86400"
}

# STATIC
# ------------------------
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_STORAGE = "saas_02.cdn.backends.StaticRootS3Boto3Storage"

# MEDIA
# ------------------------------------------------------------------------------

DEFAULT_FILE_STORAGE = "saas_02.cdn.backends.MediaRootS3Boto3Storage"
# MEDIA_URL = f"https://{aws_s3_domain}/media/"


# STRIPE DOMAIN FOR SuccessUrl
DOMAIN = 'http://localhost:8000'

STRIPE_SIGNING_SECRET='whsec_pFMd5KfqtEUOuKKZnGA833fJl5EcE60I'




