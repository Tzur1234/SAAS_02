from rest_framework import serializers
from django.contrib.auth import get_user_model
from saas_02.core.models import File
User = get_user_model()

class ChangePasswordSerializer(serializers.Serializer):
    '''
    A serializer convert 3 parameters: pass1, pass2 and currentPassword
    to something that can be rendered into JSON content type
    python objects --> serilize data
    python objects <-- serilize data

    '''
    current_password = serializers.CharField(style={'input_type': 'password'})
    password1 = serializers.CharField(style={'input_type': 'password'})
    password2 = serializers.CharField(style={'input_type': 'password'})
    

class SubscribeSerializer(serializers.Serializer):
    stripeToken = serializers.CharField(max_length=60)

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        
class ChangeEmailSerializer(serializers.Serializer):
    email1Value = serializers.EmailField()
    email2Value = serializers.EmailField()