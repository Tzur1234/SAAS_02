from django.contrib import admin
from saas_02.core.models import Membership, Payment, TrackedRequest, File


# admin.site.register(Membership)
admin.site.register(Payment)
admin.site.register(TrackedRequest)
admin.site.register(File)


@admin.register(Membership)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'type',
        'start_date',
        'end_date',
        'stripe_subscription_id',
        'stripe_subscription_item_id',
    )
    