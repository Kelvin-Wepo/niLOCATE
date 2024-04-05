from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
from backendCode.geocoding import reverse_geocoding, geocoding_from_address
from backendCode.nearbyplaces import search_nearby_places
from home_page.models import BusInformation
from backendCode.findBusByDirection import find_distance
from django.conf import settings
# Create your views here.


# def searchnearby_address(request):
#     location = request.POST['userlocationaddress']
#     # print(location)
#     text = settings.GOOGLE_API_KEY
#     url = f"https://maps.googleapis.com/maps/api/js?key={text}&callback=initMap&libraries=&v=weekly"
#     data = geocoding_from_address(location)
#     nearby_list = search_nearby_places(data['lat'], data['lng'])
#     data.update({'nearlist': nearby_list})
#     data.update({'text': url})
#     return render(request, 'smartTracking/searchnearby.html', data)

# Assuming `api_key` is set outside the function
api_key = settings.GOOGLE_API_KEY

def searchnearby_address(request):
    if request.method == 'POST':
        location = request.POST.get('userlocationaddress', '')
        url = f"https://maps.googleapis.com/maps/api/js?key={api_key}&callback=initMap&libraries=&v=weekly"

        data = geocoding_from_address(location)
        if data is None:
            # Handle the case where no geocoding data is found
            return render(request, 'smartTracking/error.html', {'message': 'No geocoding data found'})

        nearby_list = search_nearby_places(data.get('lat', ''), data.get('lng', ''))
        if nearby_list is None:
            # Handle the case where no nearby places are found
            return render(request, 'smartTracking/error.html', {'message': 'No nearby places found'})

        data.update({'nearlist': nearby_list, 'text': url})
        return render(request, 'smartTracking/searchnearby.html', data)
    else:
        return HttpResponseNotAllowed(['POST'])






def searchnearby_latlng(request):
    location = str(request.POST['userLocation'])
    lat, lng = location.split(sep=',', maxsplit=1)
    formatted_address = reverse_geocoding(location)
    nearby_list = search_nearby_places(lat=lat, lng=lng)
    text = settings.GOOGLE_API_KEY
    url = f"https://maps.googleapis.com/maps/api/js?key={text}&callback=initMap&libraries=&v=weekly"
    data = {
        'formatted_address': formatted_address,
        'nearlist': nearby_list,
        'text': url

    }
    # print(location)
    return render(request, 'smartTracking/searchnearby.html', data)


def finddirection(request):
    bus_list = []
    start = str(request.POST['from'])
    end = str(request.POST['to'])
    try:
        buses = BusInformation.objects.filter(bus_viaroad__iregex=start).filter(bus_viaroad__iregex=end)
        for bus in buses:
            bus_id = bus.bus_id
            bus_id = "bus" + str(bus_id)
            bus_name = bus.bus_name
            bus_raw_route = bus.route_id.routes
            bus_raw_route = bus_raw_route.split(sep=',')
            for i in range(0, len(bus_raw_route)):
                if start.lower() == bus_raw_route[i].lower():
                    start_index = i
                if end.lower() == bus_raw_route[i].lower():
                    end_index = i
            # print('Start_index' + str(start_index))
            # print('End_index' + str(end_index))
            bus_route = []
            if start_index < end_index:
                for i in range(start_index, end_index+1):
                    bus_route.append(bus_raw_route[i])
            elif start_index > end_index:
                for i in range(end_index, start_index+1):
                    bus_route.append(bus_raw_route[i])
            else:
                bus_route.append(bus_raw_route[start_index])
            distance = find_distance(bus_route)
            # print(bus_route)
            list_route = []
            for i in range(0, len(bus_route), 2):
                if i + 1 == len(bus_route):
                    temp = (bus_route[i], None)
                else:
                    temp = (bus_route[i], bus_route[i + 1])
                list_route.append(temp)
            data = {
                'bus_id': bus_id,
                'bus_name': bus_name,
                'bus_route': list_route,
                'distance': distance
            }
            bus_list.append(data)
            length = len(bus_list)
            # print(bus_list)
        contex = {
            'From': start,
            'To': end,
            'Number_of_bus': length,
            'bus_list': bus_list,
        }
        return render(request, 'smartTracking/finddirection.html', contex)
    except:
        contex = {
            'check': 1,
            'From': start,
            'To': end,
            'Number_of_bus': 0
        }
        return render(request, 'smartTracking/finddirection.html', contex)


def findspecificbus(request):
    bus_name_from_user = str(request.POST['bus_name'])
    try:
        buses = BusInformation.objects.filter(bus_name__iexact=bus_name_from_user)
        bus = buses[0]
        ssource_destination = str(bus.bus_sourcetodestination)
        start, end = ssource_destination.split(sep='-', maxsplit=1)
        routes = bus.route_id.routes
        routes = routes.split(sep=',')
        list_route = []
        for i in range(0, len(routes), 2):
            if i + 1 == len(routes):
                temp = (routes[i], None)
            else:
                temp = (routes[i], routes[i + 1])
            list_route.append(temp)
        data = {
            'check': 0,
            'bus_id': bus.bus_id,
            'bus_name': bus.bus_name,
            'start': start,
            'end': end,
            'routes': list_route
        }
        return render(request, 'smartTracking/findspecificbus.html', data)

    except:
        data = {
            'check': 1,
            "error": bus_name_from_user
        }
        return render(request, 'smartTracking/findspecificbus.html', data)

        # ssource_destination = str(bus.bus_sourcetodestination)
        # start, end = ssource_destination.split(sep='-', maxsplit=1)
        # routes = bus.route_id.routes
        # routes = routes.split(sep=',')
        # list_route = []
        # for i in range(0, len(routes), 2):
        #     if i + 1 == len(routes):
        #         temp = (routes[i], None)
        #     else:
        #         temp = (routes[i], routes[i + 1])
        #     list_route.append(temp)
        # data = {
        #     'check': 0,
        #     'bus_id': bus.bus_id,
        #     'bus_name': bus.bus_name,
        #     'start': start,
        #     'end': end,
        #     'routes': list_route
        # }
        # return render(request, 'smartTracking/findspecificbus.html', data)


def allbuses(request):
    buses = BusInformation.objects.all()
    buses_list = []
    for bus in buses:
        source_destination = str(bus.bus_sourcetodestination)
        start, end = source_destination.split(sep='-', maxsplit=1)
        routes = bus.route_id.routes
        routes = routes.split(sep=',')
        design = str(routes[0])
        for r in range(1, len(routes) - 1):
            design = design + '<->' + str(routes[r])
        data = {
            'bus_id': bus.bus_id,
            'bus_name': bus.bus_name,
            'start': start,
            'end': end,
            'routes': design
        }
        buses_list.append(data)
    contex = {
        'contex': buses_list
    }
    # print(routes)
    return render(request, 'smartTracking/allbuses.html', contex)

# urls of smarttracking apps
# {% url 'searchnearby'%}
# {% url 'finddirection'%}
# {% url 'findspecificbus'%}
# {% url 'allbuses'%}
