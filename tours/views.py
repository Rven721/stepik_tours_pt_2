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
    return render(request, 'tours/index.html', {'tour_list': tour_list, 'departures': departures})


def departure_view(request, dep):
    if dep not in departures:
        raise Http404
    dep_list = {}
    for key, value in tours.items():
        if value['departure'] == dep:
            dep_list[key] = value
    if len(dep_list) == 0:
        return render(request, 'tours/reject.html',
                      {'departures': departures, 'dep': dep, 'departure': departures[dep]})
    for value in dep_list.values():
        value['star_img'] = "★" * int(value['stars'])
    prises = [int(value['price']) for value in dep_list.values()]
    nights = [int(value['nights']) for value in dep_list.values()]
    begin = 'Найден' if len(dep_list) % 10 == 1 else 'Найдено'
    if len(dep_list) % 10 >= 5:
        ending = 'туров'
    elif len(dep_list) == 1:
        ending = 'тур'
    else:
        ending = 'тура'
    context = {
        'min_prise': min(prises),
        'max_prise': max(prises),
        'min_nights': min(nights),
        'max_nights': max(nights),
        'count': len(dep_list),
        'dep_list': dep_list,
        'departure': departures[dep],
        'dep': dep,
        'departures': departures,
        'ending': ending,
        'begin': begin,
    }
    return render(request, 'tours/departure.html', context)


def tour_view(request, tour_id):
    if int(tour_id) not in tours:
        raise Http404
    tour = tours[int(tour_id)]
    stars = "★" * int(tour['stars'])
    run = str(f"{tour['country']} {departures[tour['departure']]} {tour['nights']} ночей")
    return render(request, 'tours/tour.html',
                  {'tour': tour, 'stars': stars, 'run': run, 'departures': departures})
