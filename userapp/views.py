
from rest_framework import generics, status,permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import RegisterDB
from .serializers import userserializer,loginserializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail


class creation(generics.CreateAPIView):
    queryset = RegisterDB.objects.all()
    serializer_class = userserializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        self.send_verification_email(user.email, refresh_token)

        return Response({'access_token': access_token,
                         'message': 'User registered successfully. Check your email for verification.'},
                        status=status.HTTP_201_CREATED)

    def send_verification_email(self, email, refresh_token):
        subject = 'Account Verification'
        message = f'Click the following link to verify your account: http://127.0.0.1:8000//verify/{refresh_token}'
        from_email = 'your email'
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)


from django.shortcuts import get_object_or_404
from rest_framework.views import APIView


class EmailVerification(generics.GenericAPIView):
    def get(self, request, token):
        refresh_token = RefreshToken(token)
        user_id = refresh_token.payload['user_id']
        user = get_object_or_404(RegisterDB, id=user_id)

        if user.is_verified == 0:
            user.is_verified = 1
            user.save()

            return Response({'message': 'Email verification successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Email already verified.'}, status=status.HTTP_400_BAD_REQUEST)


from django.contrib.auth import authenticate

class UserLogin(generics.CreateAPIView):
    queryset = RegisterDB.objects.all()
    serializer_class = userserializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'message': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if user:
            if user.is_verified:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({'access_token': access_token, 'message': 'Login successful.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Email not verified. Please check your email for verification.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'Invalid credentials. Please check your email and password.'}, status=status.HTTP_401_UNAUTHORIZED)

from rest_framework.authtoken.models import Token


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            # Create or get a Token for the authenticated user
            token, created = Token.objects.get_or_create(user=user)

            return Response({'token': token.key, 'message': 'Login successful.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials.'},
                            status=status.HTTP_401_UNAUTHORIZED)
