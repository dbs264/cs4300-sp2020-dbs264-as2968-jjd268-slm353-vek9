from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.services import initial_search as system

project_name = "Club Advisor"
net_id = "Daniel Sanderson: dbs264, Alexander Schmack: as2968, John DeMoully: jjd268, Sophia Markel: slm353, Victoria Katz: vek9"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	city = request.args.get('city')
	price = request.args.get('price')
	bar_name = request.args.get('bar_name')
	
	if not price:
		price = 5
	if not city:
		if query or bar_name:
			output_message = 'No results for this city'
			city = "new_york"
			data = ["If you did not enter a city, please do so in the form above"]
		else:
			output_message = ''
			data = []
	elif bar_name:
		output_message = "Your search: Bars like " + bar_name + " in " + city + " for " + "$" * int(price)
		data = map(lambda x: x["name"],system.search_data(bar_name,city))
	else:
		output_message = "Your search: " + query + " in " + city + " for " + "$" * int(price)
		data = map(lambda x: x["name"],system.search_data(query,city))

	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



