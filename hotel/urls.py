from django.urls import path
from .views import BookingListView, RoomDetailView, CancelBookingView,RoomListView
from django.contrib.auth.decorators import login_required


app_name = 'hotel'

urlpatterns = [
    #path('', BookingFormView.as_view(), name='BookingFormView'),
    path('booking_list/', BookingListView.as_view(), name='BookingListView'),
    path('room_list/',RoomListView,name='RoomListView'),
    path('room/<category>',login_required(RoomDetailView.as_view()),name='RoomDetailView'),
    #path('room/<category>', RoomDetailView.as_view(), name='RoomDetailView'),
    path('booking/cancel/<pk>', CancelBookingView.as_view(),
         name='CancelBookingView'),
    #path('checkout/', CheckoutView.as_view(), name='CheckoutView'),
    #path('success/', success_view, name='success_view'),
    #path('cancel/', cancel_view, name='cancel_view'),
    #path('contact-us/', contact_us, name="contact_us")

]