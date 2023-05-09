from django.contrib import admin
from saas_02.core.models import Membership, Payment, TrackedRequest, File


admin.site.register(Membership)
admin.site.register(Payment)
admin.site.register(TrackedRequest)
admin.site.register(File)