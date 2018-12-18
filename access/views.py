from rest_framework import generics
from .models import CustomUser, Agency
from .serializers import CustomUserSerializer, AgencySerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import get_user_model
from .fetchcitizendetails import get_citizen_details, map_citizen_details_to_model
import requests

class CitizenDetailsView(APIView):
    def post(self, request, *args, **kwargs):
        cid_number = request.data.get('cid_number')
        try:
            api_response = get_citizen_details(cid_number)
            citizen_data = map_citizen_details_to_model(api_response)
            return Response(citizen_data, status=status.HTTP_200_OK)
        except requests.HTTPError as http_err:
            # Handle HTTP errors (e.g., token endpoint not reachable, bad request, etc.)
            return Response({'detail': str(http_err)}, status=http_err.response.status_code)
        except requests.RequestException as err:
            # Handle non-HTTP errors (e.g., network issues)
            return Response({'detail': str(err)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)



class UserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        user_serializer = self.get_serializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Create Agency data
        agency_data = request.data.get('agency', {})
        agency_serializer = AgencySerializer(data=agency_data)
        if agency_serializer.is_valid():
            agency_serializer.save(user=user)
        else:
            user.delete()  # Rollback user creation if agency data is invalid
            return Response(agency_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(user_serializer.data)
        return Response(user_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserUpdate(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user_serializer = self.get_serializer(instance, data=request.data, partial=partial)
        user_serializer.is_valid(raise_exception=True)
        self.perform_update(user_serializer)

        # Update Agency data
        agency_data = request.data.get('agency', {})
        if instance.agency:
            agency_serializer = AgencySerializer(instance.agency, data=agency_data, partial=partial)
            if agency_serializer.is_valid():
                agency_serializer.save()
            else:
                return Response(agency_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(user_serializer.data)


class UserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()

class PasswordResetRequestView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            password_reset_url = request.build_absolute_uri(
                reverse('password-reset', args=[token])
            )
            send_mail(
                'Password Reset Request',
                f'Please click on the link to reset your password: {password_reset_url}',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            return Response({"message": "Password reset link sent."}, status=status.HTTP_200_OK)

        return Response({"error": "Email not found."}, status=status.HTTP_404_NOT_FOUND)


class PasswordResetView(APIView):
    def post(self, request, token, *args, **kwargs):
        password = request.data.get('password')
        user = User.objects.filter(username=request.data.get('username')).first()

        if user and default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({"message": "Password has been reset."}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid token or username."}, status=status.HTTP_400_BAD_REQUEST)