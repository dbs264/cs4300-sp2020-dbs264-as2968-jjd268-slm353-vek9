from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.services import initial_search as system
from app.irsystem.services import bars_list

project_name = "Club Advisor"
net_id = "Daniel Sanderson: dbs264, Alexander Schmack: as2968, John DeMoully: jjd268, Sophia Markel: slm353, Victoria Katz: vek9"

@irsystem.route('/suggestions')
def suggestions():
	query = request.args.get('search')
	city = request.args.get('city')
	price = request.args.get('price')
	bar_name = request.args.get('bar_name')
	attribute_list = [request.args.get('attribute1'), request.args.get('attribute2'), request.args.get('attribute3'), request.args.get('attribute4')]
	
	if not query:
		query = ''
	#if no price entered assuming max price
	if not price:
		price = 5
	#if no location entered in a search, dont display results
	if not city:
		if query or bar_name:
			output_message = 'Please enter a location above'
			city = "new_york"
			data = [0]
		else:
			output_message = ''
			data = []
	#if given bar name, retrieve with similar bars
	elif bar_name:
		output_message = "Your search: Bars like " + bar_name + " in " + city + " for " + "$" * int(price)
		data = system.search_data(bar_name,city)
	#retrieve based on additional preferences, need to factor in presets
	else:
		start = "Your search: " + query
		for i in attribute_list:
			if i:
				start += ", " + str(i) 
		output_message = start + " in " + city + " for " + "$" * int(price)
		data = system.search_data(query,city)

	return render_template('suggestions.html', name=project_name, netid=net_id, output_message=output_message, data=data)

@irsystem.route('/')
def search():
	return render_template('search.html')

#this one should return all of the bars in one city
@irsystem.route('/cities')
def cities():
	city = request.args.get('city')
	bars = bars_list.bars_list_for_city(city)
	return render_template('search.html')

