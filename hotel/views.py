from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView, View,DeleteView

#from django.views.generic import Deleteview
from .models import Room, Booking
from .forms import AvailabilityForm
from hotel.booking_functions.availability import check_availability
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from hotel.booking_functions.get_room_cat_url_list import get_room_cat_url_list
from hotel.booking_functions.get_room_category_human_format import get_room_category_human_format
#rom hotel.booking_functions.get_available_rooms import get_available_rooms

from hotel.booking_functions.book_room import book_room
# Create your views here.

def RoomListView(request):
    room_category_url_list = get_room_cat_url_list()
    context={
      "room_list":room_category_url_list,
    }
    
    return render (request,'room_list_view.html',context)


class BookingListView(ListView):
    template_name = 'booking_list.html'
    model=Booking
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
                booking_list=Booking.objects.all()
                return booking_list
        else:
            booking_list=Booking.objects.filter(user=self.request.user)
            return booking_list

@method_decorator(login_required,name='get')
class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        human_format_room_category=get_room_category_human_format(category)
        form = AvailabilityForm()
        if human_format_room_category is not None:
            context = {
                'room_category': human_format_room_category,
                'form': form,
            }
            return render(request, 'room_detail_view.html', context)
        else:
            return HttpResponse('Category does not exist')

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        
        form = AvailabilityForm(request.POST)
        def get_available_rooms(category,check_in,check_out):
            room_list = Room.objects.filter(category=category)
            available_rooms = []
    

    #form = AvailabilityForm()
    #if form.is_valid():
     #data = form.cleaned_data


            for room in room_list:
                if check_availability(room,data['check_in'],data['check_out']):
                    available_rooms.append(room)
                if len(available_rooms) > 0:
                    return available_rooms
                else:
                    return None 
        
        if form.is_valid():
            data = form.cleaned_data
        available_rooms=get_available_rooms(
            category,data['check_in'],data['check_out'])

        if available_rooms is not None:
        
            booking=book_room(request,available_rooms[0],
            data['check_in'],data['check_out'])
            return HttpResponse(booking)
        else:
            return HttpResponse('All of this category of rooms are booked!! Try another one')


'''class BookingView(FormView):
    form_class = AvailabilityForm
    template_name = 'availability_form.html'
    def form_valid(self, form):
        data = form.cleaned_data
        room_list = Room.objects.filter(category=data['room_category'])
        available_rooms = []
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)
        if len(available_rooms) > 0:
            room = available_rooms[0]
            booking = Booking.objects.create(
                user=self.request.user,
                room=room,
                check_in=data['check_in'],
                check_out=data['check_out']
            )
            booking.save()
            return HttpResponse('booking')
        else:
            return HttpResponse('All of this category of rooms are booked!! Try another one')'''
class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('hotel:BookingListView')