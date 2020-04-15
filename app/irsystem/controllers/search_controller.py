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
	if not city:
		city = "new_york"
	if not price:
		price = 5
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query + " in " + city + " for " + "$" * int(price)
		data = map(lambda x: x["name"],system.search_data(query,city))

	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



