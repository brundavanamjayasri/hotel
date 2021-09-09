from hotel.models import Room
from .availability import check_availability
from hotel.forms import AvailabilityForm

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