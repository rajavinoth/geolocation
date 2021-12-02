from flask import jsonify
import requests
import xmltodict
from app import dbc
from datetime import datetime, timedelta
from app.models import location_data
from app.main import blue_print

@blue_print.route('/myapp/get_address/<latitude>/<longitude>', methods=['GET'])
def my_app(latitude,longitude,current_time=datetime.utcnow()):
    result = validate_coordinates(latitude, longitude,current_time)
    return jsonify(name=result['location_address'], report_type=result['report_type'])

def validate_coordinates(latitude, longitude, current_time):
    check_time = current_time - timedelta(hours=24)
    coord_location = dbc.session.query(location_data.address). \
        filter(location_data.latitude == latitude,location_data.longitude == longitude,
                                                location_data.timestamp >= check_time). \
        first()
    if coord_location is None:
        get_coordinates_details = requests.get(
            f"http://nominatim.openstreetmap.org/reverse?format=xml&lat={latitude}&lon={longitude}&zoom=27&addressdetails=1")
        data_dict = xmltodict.parse(get_coordinates_details.text)
        # as_per_time = datetime.strptime(data_dict['reversegeocode']['@timestamp'], '%a, %d %b %y %H:%M:%S %z')
        location_address = data_dict['reversegeocode']['result']['#text']
        data = location_data(latitude=latitude, longitude=longitude, address=location_address, timestamp=current_time)
        dbc.session.add(data)
        dbc.session.commit()
        return {'location_address': location_address, 'report_type': 'new'}
    else:
        return {'location_address': coord_location[0], 'report_type': 'db'}
