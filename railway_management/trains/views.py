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
from rest_framework_api_key.permissions import HasAPIKey

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
        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


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
        seats_requested = int(request.data.get('seats_requested'))
        train = get_object_or_404(Train, train_id=train_id)
        if train.total_seats >= seats_requested:
            train.total_seats -= seats_requested
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

class GetTrainAvailability(APIView):
    def get(self, request):
        from_city = request.GET.get('source')
        to_city = request.GET.get('destination')
        #date = request.GET.get('date')

        trains = Train.objects.all()
        if(from_city and to_city):
            trains = Train.objects.filter(source=from_city, destination=to_city)
        
        serializer = TrainSerializer(trains, many=True)

        return Response(serializer.data)
    

class AdminLogin(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_admin:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

class AdminDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_admin:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'message': 'Admin Dashboard'})


class AddTrain(APIView):
    permission_classes = [HasAPIKey | IsAuthenticated]

    def post(self, request):
        if not request.user.is_admin:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = TrainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateTrain(APIView):
    permission_classes = [HasAPIKey | IsAuthenticated]

    def put(self, request, pk):
        if not request.user.is_admin:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        train = get_object_or_404(Train, pk=pk)
        serializer = TrainSerializer(train, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteTrain(APIView):
    permission_classes = [HasAPIKey | IsAuthenticated]

    def delete(self, request, pk):
        if not request.user.is_admin:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        train = get_object_or_404(Train, pk=pk)
        train.delete()
        return Response({'message': 'Train deleted'}, status=status.HTTP_200_OK)

class UpdateSeatAvailability(APIView):
    permission_classes = [HasAPIKey | IsAuthenticated]

    def put(self, request, pk):
        if not request.user.is_admin:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        train = get_object_or_404(Train, pk=pk)
        serializer = TrainSerializer(train, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)