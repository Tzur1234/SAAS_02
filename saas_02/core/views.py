import math
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.status import (HTTP_200_OK,
                                    HTTP_500_INTERNAL_SERVER_ERROR,
                                      HTTP_400_BAD_REQUEST,
                                      HTTP_405_METHOD_NOT_ALLOWED,
                                      HTTP_406_NOT_ACCEPTABLE,
                                      HTTP_303_SEE_OTHER)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from saas_02.core.serializers import (ChangePasswordSerializer,
                                       SubscribeSerializer,
                                         FileSerializer,
                                         ChangeEmailSerializer)
from django.contrib.auth import authenticate
from saas_02.core.models import TrackedRequest, Membership
from django.conf import settings
from saas_02.core.image_detection import detect_faces
from saas_02.core.permissions import IsMember
from saas_02.core.models import Payment
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
User = get_user_model()

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
import datetime
from stripe.error import SignatureVerificationError

def get_user_from_token(request):
    '''
    The function take the token in the request 
    then use the token to retrieve the User object with the same token
    '''
    # Retieve the token
    token = request.META['HTTP_AUTHORIZATION'].split()[1]
    # Rerieve the user object
    try:
        user = Token.objects.get(key=token).user
        return user
    except Exception as e:
        print('Could not retrieve the user based on the given token: ', e)

def get_type_display(type):
    return settings.MEMBERSHIP_CHOICES(type)

class ImageRecognitionView(APIView):
    permission_classes = (IsMember,)
    # throttle_scope = 'demo'
    def post(self, request, *args, **kwargs):
        user = get_user_from_token(request)
        
        
        if user.membership.type == 'M': 

            try :
                # Create new usage record  
                usage_record = stripe.SubscriptionItem.create_usage_record(
                    user.membership.stripe_subscription_item_id,
                    quantity=1,
                    timestamp=math.floor(datetime.datetime.now().timestamp()),
                    )
            except Exception as e:
                print("Error when creating usage record: ", str(e))
            

                                 
            tracked_request = TrackedRequest()
            tracked_request.user = user
            tracked_request.endpoint = '/api/upload/image-recognition/'
            tracked_request.usage_record_id = usage_record.id        
            tracked_request.save()
       

        
        # Check image size
        length = request.META.get('CONTENT_LENGTH')
        if int(length) > 5000000:
            return Response(data={'message': 'Image Size is greater than 5MB !'}, status=HTTP_400_BAD_REQUEST)

        try:
            file_serializer = FileSerializer(data=request.data)
            if file_serializer.is_valid():
                file_serializer.save()
                image_path = file_serializer.data['file']
                recognition = detect_faces(image_path=image_path)
                data = {
                    "message": 'The image was uploaded !',
                    'result': recognition 
                }
                return Response(data=data, status=HTTP_200_OK)
            else:
                return Response(data={"message": file_serializer.errors['file'][0]}, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('Erorr: ', e)
            return Response(data={"message": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

class ChangeEmailView(APIView):  
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        # Retrieve the user 
        user = get_user_from_token(request)
       
        # Retriveing the new email (serialized)
        try:
            serializer = ChangeEmailSerializer(data=request.data)
            if serializer.is_valid():
                if serializer.data['email1Value'] != '' and serializer.data['email2Value'] != '':
                    if serializer.data['email1Value'] == serializer.data['email2Value']:
                        # Delete all old email Adresses
                        user.emailaddress_set.all().delete()
                        print(' Check remaining EmailAdresses' ,user.emailaddress_set.all())

                        # Set new email
                        user.email=serializer.data['email2Value']
                        user.save()
                        return Response(data={'message': 'Email was succesfuly updated !', 'type': 'success'}, status=HTTP_200_OK)
                    else:
                        return Response(data={'message': 'both emails must be the same !', 'type': 'danger'}, status=HTTP_400_BAD_REQUEST)
                else:
                    return Response(data={'message': 'both emails must be filled !', 'type': 'danger'}, status=HTTP_400_BAD_REQUEST)
            else:
                 return Response(data={'message': 'receive invalid data !', 'type': 'danger'}, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            print('Error: ', e)
            return Response(data={'message': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
                  
class GetUserEmailView(APIView):
    '''
    the function recieve GET request
    Based on the Token in the headers, returns the user's email
    '''
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        user = get_user_from_token(request)
        obj = {'email': user.email}
        print('the new email form backend: ', obj)
        return Response(obj, status=HTTP_200_OK)

class ResetPasswordAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request_user = get_user_from_token(request)

        parsed_password = ChangePasswordSerializer(data=request.data)
        if parsed_password.is_valid():
            current_password = parsed_password.data['current_password']
            password1 = parsed_password.data['password1']
            password2 = parsed_password.data['password2']


            if password1 == password2:
                auth_user = authenticate(username=request_user.username, password=current_password)
                if auth_user != None:
                    # change user's password
                    request_user.set_password(password2)
                    request_user.save()
                    return Response(data={'Response message': 'Success !'}, status=HTTP_200_OK)
                else:
                    return Response(data={'Response message': 'Current Password is wrong !'}, status=HTTP_400_BAD_REQUEST)
                    
            else:
                return Response(data={'Response message': 'passwords are not the same !'}, status=HTTP_400_BAD_REQUEST)

        else:
            
            return Response(data={'Response message': 'Data is not valid'}, status=HTTP_400_BAD_REQUEST)
    
class UserBillingDetailsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = get_user_from_token(request)
        membership = user.membership



        # count All API requests since the begging of the month
        today = datetime.datetime.now() #today
        month_start = datetime.date(today.year, today.month, 1) # the beggining of the month
        tracked_request_count = TrackedRequest.objects.filter(user=user, timestamp__gte=month_start).count()

        # Callculate due
        amount_due = 0
        if user.is_member:
            # USE API to check the monthly due
            amount_due = stripe.Invoice.upcoming(
                customer=user.stripe_customer_id)['amount_due'] / 100


        # object to return
        obj = {
            'membershipType': membership.get_type_display(),    
            'free_trial_end_date': membership.end_date,
            'next_billing_date': membership.end_date,
            'api_request_count': tracked_request_count, 
            'amount_due': amount_due 
        }

        print('User billing ojbect' ,obj)

        return Response(data=obj, status=HTTP_200_OK)

class CancelSubscriptionView(APIView):
    permission_classes = (IsMember,)

    def post(self, request, *args, **kwargs):
        user = get_user_from_token(request)
        membership = user.membership

        # check if the user is under membership
        if membership.type == 'M' and not user.on_free_trial:

            try:
                # update stripe subscription
                sub = stripe.Subscription.retrieve(membership.stripe_subscription_id)
                sub.delete()
            except Exception as e:
                return Response({"message": f"We could't cancel the subcription: {str(e)}"}, status=HTTP_500_INTERNAL_SERVER_ERROR)


            # update user instance
            user.is_member = False
            user.on_free_trial = False 
            user.save()

            # update the membership
            membership.type = 'N'
            membership.save()

            # delete all TrackRequests and Payment requests
            # print('All Tracked Request user', TrackedRequest.objects.filter(user=user))
            # TrackedRequest.objects.filter(user=user).delete()
            # print('All Payments the user has payed', Payment.objects.filter(user=user))


            return Response({"message": "The subscription was canceled succssesfuly"}, status=HTTP_200_OK)
        else:
            return Response({"message": "You haven't subscribe !"}, status=HTTP_400_BAD_REQUEST)


# not in use
class SubscribeView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = get_user_from_token(request)
        membership = user.membership

        try:
            # get stripe Customer
            customer = stripe.Customer.retrieve(user.stripe_customer_id)

            # serialize post data (stripeToken)    
            # get the stripe_token from the serialize data

            # create the stripe subscribtion obj for this customer obj
            sub = stripe.Subscription.create(customer= customer.id,
                                              items=[{'plane': settings.STRIPE_PLAN_ID }])
            

            # update the membership plane
            membership.type = 'M'
            membership.start_date = datetime.datetime.now() 
            membership.end_date = datetime.datetime.fromtimestamp(
                sub.current_period_end
                )
            membership.stripe_subscription_id = sub.id 
            membership.save()

            # update the user object
            user.is_member = True
            user.on_free_trial = False
            user.save()

            # create a payment
            payment = Payment()
            payment.user = user
            payment.amount = sub.plan.amount / 100
            payment.save()

            
            return Response({'message': 'Success!'}, status=HTTP_200_OK)

        except stripe.error.CardError as e:
            return Response({'message': 'Your card has been declined!'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        except stripe.error.StripeErorr as e:
            return Response({'message': f'There is a stripe error: \n {str(e)}'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(data={'message':'An error has occured'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

class CreateCheckoutSessionView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(slef, request, *args, **kwargs):
        user = get_user_from_token(request)
        try: 

            checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1N6ASaESXHNK1nmVHT8o8Vno'                    
                },
            ],
            mode='subscription',
            success_url= settings.DOMAIN + '/api/billing/',
            cancel_url= settings.DOMAIN + '/api/billing/',
            customer = user.stripe_customer_id)
        
            return Response(data={
                'message': 'Success !',
                'checkout_session_url' : checkout_session.url,
            }, status=HTTP_303_SEE_OTHER)
        
        except Exception as e:
            return Response(data={'message': f"Error ! : {str(e)}"})

@csrf_exempt        
def webhook(request, *args, **kwargs):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_SIGNING_SECRET
        )

        # subscriving event
        if event['type'] == 'checkout.session.completed':

            stripe_customer_id = event.data.object.customer
            user = User.objects.get(stripe_customer_id=stripe_customer_id)
            membership = user.membership
            
            sub = stripe.Subscription.retrieve(event.data.object.subscription)

            print("sub['items']['data'][0]['id']: !!: ", sub['items']['data'][0]['id'])

            # update the membership plane
            membership.type = 'M'
            membership.stripe_subscription_item_id = sub['items']['data'][0]['id']
            membership.start_date = datetime.datetime.now() 
            membership.end_date = datetime.datetime.fromtimestamp(
                sub.current_period_end
                )
            membership.stripe_subscription_id = sub.id 
            membership.save()

            print('the membership type: ', membership.type)
            print('the membership user: ', membership.user)

            # update the user object
            user.is_member = True
            user.on_free_trial = False
            user.save()

            # create a payment
            payment = Payment()
            payment.user = user
            # print('sub.plan.amount: ', sub.plan.amount)
            payment.amount = event.data.object.amount_total / 100
            payment.save()

            return HttpResponse(status=200)
        else:
            #un-subscribe event
            pass
            
    except ValueError as e:
        print('Error !',e)
        return HttpResponse(status=400)
    except SignatureVerificationError as e:
        print('Error !!',e)
        return HttpResponse(status=400)
      

    
    # ... handle other event types




            
             
             
              
            



    
