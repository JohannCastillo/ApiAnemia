from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status, exceptions
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.utils import json
from .serializers import *
from django.contrib.auth.models import User
from api.models import Apoderado

import requests
import json

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        user = User.objects.get(username=request.data['username'])
        if not user.check_password(request.data['password']):
            raise exceptions.AuthenticationFailed('Password is incorrect')
    except User.DoesNotExist:
        raise exceptions.AuthenticationFailed('User not found')
        
    user = UserSerializer(user).data
    return Response(user)

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
  
    serializer.save()
    user = User.objects.get(username=serializer.data['username'])
    data = UserSerializer(user).data

    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def validate_token(request):
    return Response({}, status=status.HTTP_200_OK)


# Login with google
@api_view(['POST'])
def google_login(request):
    serializer = GoogleLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    payload = {'access_token': serializer.data['access_token']}

    request = requests.get(
         'https://www.googleapis.com/oauth2/v2/userinfo', 
         params = payload
    )
    response =  json.loads(request.text)

    if 'error' in response: 
        raise exceptions.AuthenticationFailed('El token no es válido o se encuentra expirado') 
    
    try:
        user = User.objects.get(email=response['email'])
    except User.DoesNotExist: 
        user = User.objects.create_user(
            username=response['email'],
            email=response['email'], 
            password= make_password(BaseUserManager().make_random_password()),
        )
        user.save()
    
    find_apoderado_record = Apoderado.objects.filter(email=response['email']).first()
    if find_apoderado_record:
        # asignar usuario a apoderado
        find_apoderado_record.usuario = user
        find_apoderado_record.save()
    else: 
        # crear nuevo apoderado
        new_apoderado = Apoderado(
            nombre=serializer.data['nombre'],
            email=response['email'],
            usuario=user,
            dni = None,
        )
        new_apoderado.save()

    data = UserSerializer(user).data

    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
def google_search_user(request):
    serializer = GoogleValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    payload = {'access_token': serializer.data['access_token']}

    request = requests.get(
         'https://www.googleapis.com/oauth2/v2/userinfo', 
         params = payload
    )

    response =  json.loads(request.text)

    if 'error' in response: 
        raise exceptions.AuthenticationFailed('El token no es válido o se encuentra expirado') 
    
    try:
        user = User.objects.get(email=response['email'])

        if user.first_name == "":
            return Response({
                "CODE": "NOT_REGISTERED",
                "user": UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        

        return Response({
            "CODE": "ALREADY_REGISTERED",
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)

    except User.DoesNotExist: 
        user = User.objects.create_user(
            username=response['email'],
            email=response['email'], 
            password= make_password(BaseUserManager().make_random_password()),
        )
        user.save()
        return Response({
            "CODE": "NOT_REGISTERED",
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    
@api_view(['PUT'])
def complete_user_register(request):
    user = request.userdb
    print(user.email)

    serializer = GoogleRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user.first_name = serializer.data['name']
    user.save()

    find_apoderado_record = Apoderado.objects.filter(email=user.email).first()
    if find_apoderado_record:
        # asignar usuario a apoderado
        find_apoderado_record.usuario = user
        find_apoderado_record.save()
    else: 
        # crear nuevo apoderado
        new_apoderado = Apoderado(
            nombre=serializer.data['name'],
            email=user.email,
            usuario=user,
            dni = None,
        )
        new_apoderado.save()

    return Response(UserSerializer(user).data, status=status.HTTP_200_OK)