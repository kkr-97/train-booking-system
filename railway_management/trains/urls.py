from django.urls import path
from .views import UpdateTrain, DeleteTrain, UpdateSeatAvailability, RegisterUser, LoginUser, AddTrain, GetTrainAvailability, GetSeatAvailability, BookSeat, GetBookingDetails, AdminLogin, AdminDashboard

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('add_train/', AddTrain.as_view(), name='add_train'),
    path('get_seat_availability/', GetSeatAvailability.as_view(), name='get_seat_availability'),
    path('book-seat/', BookSeat.as_view(), name='book-seat'),
    path('booking-details/', GetBookingDetails.as_view(), name='booking_details'),
    path('get_train_availability/', GetTrainAvailability.as_view(), name='get_train_availability'),
    # Admin URLs
    path('admin/login/', AdminLogin.as_view(), name='admin_login'),
    path('admin/dashboard/', AdminDashboard.as_view(), name='admin_dashboard'),
    path('admin/add_train/', AddTrain.as_view(), name='admin_add_train'),
    path('admin/update_train/<int:pk>/', UpdateTrain.as_view(), name='admin_update_train'),
    path('admin/delete_train/<int:pk>/', DeleteTrain.as_view(), name='admin_delete_train'),
    path('admin/update_seat_availability/<int:pk>/', UpdateSeatAvailability.as_view(), name='admin_update_seat_availability'),
]