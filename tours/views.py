from random import randint

from django.http import Http404
from django.shortcuts import render

from .data import departures, tours


def main_view(request):
    rand_list = set()
    while len(rand_list) < 6:
        rand_list.add(randint(1, 16))
    tour_list = {}
    for i in rand_list:
        tour_list[i] = tours[i]
        try:
            tour_list[i]['ru_departure'] = departures[tour_list[i]['departure']]
        except KeyError:
            pass
    return render(request, 'tours/index.html', {'tour_list': tour_list})


def departure_view(request, dep):
    if dep not in departures:
        raise Http404
    dep_list = {}
    for tour_id, tour_details in tours.items():
        if tour_details['departure'] == dep:
            dep_list[tour_id] = tour_details
    if len(dep_list) == 0:
        return render(request, 'tours/reject.html', {'dep': dep, 'departure': departures[dep]})
    prises = [int(tour_details['price']) for tour_details in dep_list.values()]
    nights = [int(tour_details['nights']) for tour_details in dep_list.values()]
    begin = 'Найден' if len(dep_list) % 10 == 1 else 'Найдено'
    context = {
        'min_prise': min(prises),
        'max_prise': max(prises),
        'min_nights': min(nights),
        'max_nights': max(nights),
        'count': len(dep_list),
        'departure': departures[dep],
        'dep_list': dep_list,
        'dep': dep,
        'begin': begin,
    }
    return render(request, 'tours/departure.html', context)


def tour_view(request, tour_id):
    if tour_id not in tours:
        raise Http404
    tour = tours[tour_id]
    run = str(f"{tour['country']} {departures[tour['departure']]}")
    return render(request, 'tours/tour.html', {'tour': tour, 'run': run, })
