from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import Train, Booking, User
from .serializers import UserSerializer, TrainSerializer, BookingSerializer
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny

class RegisterUser(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(f"Authenticating user: {username}")  # Debug line
        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            print(f"User authenticated: {username}")  # Debug line
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        print("Authentication failed")  # Debug line
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class AddTrain(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_admin:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = TrainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetSeatAvailability(APIView):
    def get(self, request):
        source = request.query_params.get('source')
        destination = request.query_params.get('destination')
        trains = Train.objects.filter(source=source, destination=destination)
        serializer = TrainSerializer(trains, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BookSeat(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        train_id = request.data.get('train_id')
        seats_requested = request.data.get('seats_requested')
        train = get_object_or_404(Train, train_id=train_id)

        if train.available_seats >= seats_requested:
            train.available_seats -= seats_requested
            train.save()

            Booking.objects.create(
                user=request.user,
                train=train,
                seats_booked=seats_requested
            )
            return Response({'message': 'Booking successful'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Not enough seats available'}, status=status.HTTP_400_BAD_REQUEST)

class GetBookingDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
