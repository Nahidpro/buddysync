from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import AccountSerializer
from users.models import Account
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
class TestView(APIView):
    def get(self, request):
       
        
        return Response("Hello, this is a test message!", content_type="text/plain", status=status.HTTP_200_OK)

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        password = data.get("password")

        # Password validation
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"password": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize the serializer with the request data
        serializer = AccountSerializer(data=data)

        # Check if the serializer is valid
        if serializer.is_valid():
            serializer.save()  
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)

        
        print("Serializer Errors:", serializer.errors)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = AccountSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = AccountSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected endpoint!"})


