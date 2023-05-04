from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.conf import settings

from django.utils import timezone
import datetime
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


MEMBERSHIP_CHOICES = (
    ('F', 'free_trial'),
    ('M', 'member'),
    ('N', 'not_member')
)

class Membership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES)
    start_date = models.DateTimeField(auto_now_add=True) # the date the user was created - also he start the memebership
    end_date = models.DateTimeField()
    
    stripe_subscription_id = models.CharField(max_length=40, blank=True, null=True)
    stripe_subscription_item_id = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return f"MemberShip Type: {self.type} |start_date: {self.start_date}, end_date: {self.end_date}"
    

# Model to tracked each API request of a user
class TrackedRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    endpoint = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    usage_record_id = models.CharField(max_length=50, blank=True, null=True) # ?


# When the user created ...
def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        customer = stripe.Customer.create(email=instance.email)
        instance.stripe_customer_id = customer.id
        instance.save()

        print('instance.stripe_customer_id: ', instance.stripe_customer_id)

        # start the 'free membership plane'
        membership = Membership.objects.create(
            user=instance,
            type='F',
            end_date=timezone.now() + datetime.timedelta(days=14)                         
        )

        print('new membership:  ', membership)



# When the user logged in ...
def user_logged_in_receiver(sender, request, user, *args, **kwargs):
    membership = user.membership
    
    # Update user free_trail status
    if user.on_free_trail:
        if timezone.now > membership.end_date:
            user.on_free_trail = False   
        
    # Update user membership
    elif user.is_member:
        sub = stripe.Subscription.retrieve(membership.stripe_subscription_id)
        if sub.status == "active":
            # Update the user's end period of time
            membership.end_date = datetime.datetime.fromtimestamp(
                sub.current_period_end)
            user.is_member = True
        else:
            user.is_member = False
    else:
        pass

    # save updates
    user.save()
    membership.save()



# Signals
post_save.connect(post_save_user_receiver,sender=User)
user_logged_in.connect(user_logged_in_receiver)

