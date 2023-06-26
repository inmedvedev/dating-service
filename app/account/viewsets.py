from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from .serializers import LoginEmailSerializer, LoginEmailCodeSerializer
from .models import User, LoginCodeEmail


class EmailAuthViewSet(GenericViewSet):
    def get_serializer_class(self):
        if self.action == 'send_confirmation_code':
            return LoginEmailSerializer
        elif self.action == 'login':
            return LoginEmailCodeSerializer

    @action(detail=False, methods=['post'])
    def send_confirmation_code(self, request):
        serializer = self.get_serializer_class()(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        email_code = serializer.save()
        send_mail(
            subject='Код авторизации',
            message=email_code.code,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )
        User.objects.get_or_create(email=email)
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = authenticate(
            request,
            email=serializer.validated_data['email'],
            email_code=serializer.validated_data['code'],
        )
        if user is not None:
            login(request, user)
        LoginCodeEmail.objects.filter(email=serializer.validated_data['email']).delete()
        return Response(data=serializer.validated_data, status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=['get'])
    def logout(self, request):
        logout(request)
        return Response(status=status.HTTP_202_ACCEPTED)
