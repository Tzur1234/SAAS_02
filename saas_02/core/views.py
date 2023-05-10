import sys
import threading
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.status import (HTTP_200_OK,
                                    HTTP_500_INTERNAL_SERVER_ERROR,
                                      HTTP_400_BAD_REQUEST,
                                      HTTP_405_METHOD_NOT_ALLOWED,
                                      HTTP_406_NOT_ACCEPTABLE)
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

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
import datetime

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


class FileUploadView(APIView):
    permission_classes = (AllowAny,)

   
    def post(self, request, *args, **kwargs):
        # Check image size < 5MB
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

class ImageRecognitionView(APIView):
    permission_classes = (IsMember,)
    def post(self, request, *args, **kwargs):
        user = get_user_from_token(request)
        
        # track the requests of the user
        tracked_request = TrackedRequest()
        tracked_request.user = user
        tracked_request.endpoint = '/api/upload/image-recognition/'
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
                        return Response(data={'message': 'Email was succesfuly updated !'}, status=HTTP_200_OK)
                    else:
                        return Response(data={'message': 'both emails must be the same !'}, status=HTTP_400_BAD_REQUEST)
                else:
                    return Response(data={'message': 'both emails must be filled !'}, status=HTTP_400_BAD_REQUEST)
            else:
                 return Response(data={'message': 'receive invalid data !'}, status=HTTP_400_BAD_REQUEST)

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
            print('amount_due: ',amount_due)

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

class CeatePaymentIntentView(APIView):

    '''
    Create PaymentIntent object 
    Return the client_secret, used to complete a payment from your frontend.
    '''
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):            
        user = get_user_from_token(request)
        membership = user.membership

        try:
            customer = stripe.Customer.retrieve(user.stripe_customer_id)
            serializer = SubscribeSerializer(data=request.data)

            print('customer:', customer)
            print('membership:', membership)

            if serializer.is_valid():
                # get the token
                stipe_token = serializer.data['stripeToken']
                print('stipe_token:', stipe_token)

                # create the stripe subscription
                subscription = stripe.Subscription.create(
                    customer=customer.id,
                    items=[{"plan": settings.STRIPE_PLAN_ID}]
                )
                
                
                 # update the membership
                membership.stripe_subscription_id = subscription.id
                membership.stripe_subscription_item_id = subscription['items']['data'][0]['id']
                membership.type = 'M'
                membership.start_date = datetime.datetime.now()
                membership.end_date = datetime.datetime.fromtimestamp(subscription.current_period_end)
                membership.save()

                # update the user
                user.is_member = True
                user.on_free_trial = False
                user.save()

                # create the payment
                payment = Payment()
                payment.amount = subscription.plan.amount / 100
                payment.user = user
                payment.save()

                return Response({'message': "success"}, status=HTTP_200_OK)
            
            else:
                return Response(data={'message':'this givven data is invalid'}, status=HTTP_400_BAD_REQUEST)

            
        except stripe.error.CardError as e:
            return Response({'message': "Your card has been declined"}, status=HTTP_400_BAD_REQUEST)

        except stripe.error.StripeError as e:
            return Response({'message': "There was an error. You have not been billed. If this persists please contact support"}, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": "We apologize for the error. We have been informed and are working on the problem."}, status=HTTP_400_BAD_REQUEST)

class CancelSubscriptionView(APIView):
    permission_classes = (IsMember,)

    def post(self, request, *args, **kwargs):
        user = get_user_from_token(request)
        membership = user.membership

        try:
            # update stripe subscription
            sub = stripe.Subscription.retrieve(membership.stripe_subscription_id)
            sub.delete()
        except Exception as e:
            return Response({"message": "We apologize for the error. there is a stripe problem"}, status=HTTP_500_INTERNAL_SERVER_ERROR)


        # update user instance
        user.is_member = False 
        user.save()

        # update the membership
        membership.type = 'N'
        membership.save()


        return Response({"message": "The subscription was canceled succssesfuly"}, status=HTTP_200_OK)


        



            
             
             
              
            



    
