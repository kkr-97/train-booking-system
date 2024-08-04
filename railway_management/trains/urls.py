from django.urls import path
from .views import RegisterUser, LoginUser, AddTrain, GetSeatAvailability, BookSeat, GetBookingDetails

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('add_train/', AddTrain.as_view(), name='add_train'),
    path('get_seat_availability/', GetSeatAvailability.as_view(), name='get_seat_availability'),
    path('book-seat/', BookSeat.as_view(), name='book-seat'),
    path('booking-details/', GetBookingDetails.as_view(), name='booking_details'),
]
