from tours.data import departures


def menu(request):
    return {'departures': departures}
