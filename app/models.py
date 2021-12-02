from app import dbc

class location_data(dbc.Model):
    id = dbc.Column(dbc.Integer, primary_key=True)
    latitude = dbc.Column(dbc.String(128), index=True)
    longitude = dbc.Column(dbc.String(128), index=True)
    address = dbc.Column(dbc.String(512))
    timestamp = dbc.Column(dbc.DateTime)

    def __repr__(self):
        return '<latitude {}, longitude {}, address {}, timestamp {}>'.format(self.latitude, self.longitude,
                                                                              self.address, self.timestamp)