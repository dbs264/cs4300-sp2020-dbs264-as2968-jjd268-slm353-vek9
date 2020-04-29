from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.services import cosine_sim_search as cosine_system
from app.irsystem.services import bar_search as bar_system
from app.irsystem.services import bars_list

project_name = "Club Advisor"
net_id = "Daniel Sanderson: dbs264, Alexander Schmack: as2968, John DeMoully: jjd268, Sophia Markel: slm353, Victoria Katz: vek9"


@irsystem.route('/suggestions')
def suggestions():
    query = request.args.get('search')
    city = request.args.get('city')
    location = request.args.get('location')
    price = request.args.get('price')
    bar_name = request.args.get('bar_name')

    if not price:
        price = 5
    # if no location entered in a search, dont display results
    if not city:
        if query or bar_name:
            output_message = 'Please enter a City'
            city = "new_york"
            data = [0]
        else:
            output_message = ''
            data = []
    # if given bar name, retrieve with similar bars
    elif bar_name:
        output_message = "Your search: Bars like " + bar_name + \
            " in " + location + "(" + city + ") for " + "$" * int(price)
        data = bar_system.search(bar_name, city, int(price), location)
    # retrieve based on additional preferences, need to factor in presets
    else:
        if not query:
            query = ''
        start = "Your search: " + query
        output_message = start + " in " + location + \
            "(" + city + ") for " + "$" * int(price)
        data = cosine_system.search(query, city, int(price), location)

    return render_template('suggestions.html', name=project_name, netid=net_id, output_message=output_message, data=data)

# initial page with city search
@irsystem.route('/')
def search():
    return render_template('search.html')


@irsystem.route('/preference_search')
def preference_search():
    city = request.args.get('city')
    return render_template('preference_search.html', city=city)


@irsystem.route('/bar_search')
def bar_search():
    cities_list = ["new_york", "New York",
                   "Miami", "miami", "montreal", "Montreal"]
    city = request.args.get('city')
    bars = []
    if city in cities_list:
        bars = bars_list.bars_list_for_city(city)
    return render_template('bar_search.html', bars=bars, city=city)


@irsystem.route('/get_cities_list')
def get_cities():
    return ["New York", "Montreal", "Miami"]
