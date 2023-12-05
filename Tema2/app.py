from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

'''
Tabela de tari
Cheia primara este numele tarii
Id-ul este unic si este incrementat folosind o secventa
'''
class Country(db.Model):
    __tablename__ = 'country'

    id_sec = db.Sequence(__tablename__ + "_id_seq")
    id = db.Column(db.Integer, id_sec, server_default=id_sec.next_value(), unique=True, nullable=False)
    nume = db.Column(db.String(80), primary_key=True)
    latitudine = db.Column(db.Float, nullable=False)
    longitudine = db.Column(db.Float, nullable=False)

    def json(self):
        return {'id': self.id, 'nume': self.nume, 'lat': self.latitudine, 'lon': self.longitudine}

'''
Tabela de orase
Cheia primara este una compusa din id-ul tarii si numele orasului
Contine si o referinta catre tabela de tari prin foreign key catre id-ul tarii
Id-ul este unic si este incrementat folosind o secventa
'''
class City(db.Model):
    __tablename__ = 'city'

    id_sec = db.Sequence(__tablename__ + "_id_seq")
    id = db.Column(db.Integer, id_sec, server_default=id_sec.next_value(), unique=True, nullable=False)
    id_tara = db.Column(db.Integer, db.ForeignKey('country.id'), primary_key=True)
    nume = db.Column(db.String(80), primary_key=True)
    latitudine = db.Column(db.Float, nullable=False)
    longitudine = db.Column(db.Float, nullable=False)


    def json(self):
        return {'id': self.id, 'idTara': self.id_tara, 'nume': self.nume, 'lat': self.latitudine, 'lon': self.longitudine}

'''
Tabela de temperaturi
Cheia primara este una compusa din id-ul orasului si timestamp
Contine si o referinta catre tabela de orase prin foreign key catre id-ul orasului
Id-ul este unic si este incrementat folosind o secventa
'''
class Temperatures(db.Model):
    __tablename__ = 'temperatures'

    id_sec = db.Sequence(__tablename__ + "_id_seq")
    id = db.Column(db.Integer, id_sec, server_default=id_sec.next_value(), unique=True, nullable=False)
    valoare = db.Column(db.Integer, nullable=False)
    id_oras = db.Column(db.Integer, db.ForeignKey('city.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, server_default=db.func.now(), primary_key=True)

    def json(self):
        return {'id': self.id, 'valoare': self.valoare, 'timestamp': self.timestamp}

db.create_all()

# ruta de test pentru sanity check
@app.route('/api/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route sanity check'}), 200)

# endpoint pentru crearea de tari
@app.route('/api/countries', methods=['POST'])
def create_country():
    try:
        data = request.get_json()        
        if len(data) >= 3:
            new_country = Country(nume=data['nume'], latitudine=data['lat'], longitudine=data['lon'])
            # daca nu se arunca exceptii si datele sunt valide, se adauga in baza de date
            if new_country:
                db.session.add(new_country)
                db.session.commit()
                return make_response(jsonify({ 'id': new_country.id}), 201)
        # daca request-ul nu foloseste un body valid, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Bad request'}), 400)
    except:
        # daca se arunca exceptii in timpul executiei, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': len(data)}), 409)

# endpoint pentru interogarea tuturor tarilor
@app.route('/api/countries', methods=['GET'])
def get_countries():
    countries = Country.query.all()
    # daca exista tari in baza de date, se intoarce un array de tari, daca nu se intoarce un array gol
    # care sa semnifice ca la momentul interogarii nu exista tari in baza de date
    if countries:
        return make_response(jsonify([country.json() for country in countries]), 200)

# endpoint pentru actualizarea unei tari (necesita primirea tuturor parametrilor din structura unei)
@app.route('/api/countries/<int:_id>', methods=['PUT'])
def update_country(_id):
    try:
        country = Country.query.filter_by(id=_id).first()
        # daca tara exista in baza de date, se actualizeaza datele acesteia
        if country is not None:
            data = request.get_json()
            country.nume = data['nume']
            country.latitudine = data['lat']
            country.longitudine = data['lon']
            db.session.commit()
            return make_response(jsonify({'message': 'Country updated'}), 200)
        # daca tara nu exista in baza de date, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Not found'}), 404)
    except:
        # daca se arunca exceptii in timpul executiei, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Bad request'}), 400)
    
# endpoint pentru stergerea unei tari
@app.route('/api/countries/<int:id>', methods=['DELETE'])
def delete_country(id):
    try:
        country = Country.query.filter_by(id=id).first()
        # daca tara exista in baza de date, se sterge
        if country:
            db.session.delete(country)
            db.session.commit()
            return make_response(jsonify({'message': 'Country deleted'}), 200)
        # daca tara nu exista in baza de date, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Not found'}), 404)
    except:
        # daca se arunca exceptii in timpul executiei, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Bad request'}), 400)
    
# endpoint pentru crearea de orase
@app.route('/api/cities', methods=['POST'])
def create_city():
    try:
        data = request.get_json()
        new_city = City(id_tara=data['idTara'], nume=data['nume'], latitudine=data['lat'], longitudine=data['lon'])
        # daca nu se arunca exceptii si datele sunt valide, se adauga in baza de date
        if new_city and len(data) >= 4:
            db.session.add(new_city)
            db.session.commit()
            return make_response(jsonify({'id': new_city.id}), 201)
        # daca request-ul nu foloseste un body valid, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Bad request'}), 400)
    except:
        # daca se arunca exceptii in timpul executiei, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Conflict'}), 409)
    

@app.route('/api/cities', methods=['GET'])
def get_cities():
    cities = City.query.all()
    if cities:
        return make_response(jsonify([city.json() for city in cities]), 200)
    return make_response(jsonify({'message': 'Not found'}), 404)

# get all cities by country_id success 200 not found 404
@app.route('/api/cities/country/<int:country_id>', methods=['GET'])
def get_cities_by_country(country_id):
    cities = City.query.filter_by(id_tara=country_id).all()
    if cities:
        return make_response(jsonify([city.json() for city in cities]), 200)
    return make_response(jsonify({'message': 'Not found'}), 404)

# update a city success 200 bad request 400 not found 404 conflict 409
# body {id, country_id, name, latitudine, longitudine}
@app.route('/api/cities/<int:id>', methods=['PUT'])
def update_city(id):
    try:
        city = City.query.filter_by(id=id).first()
        if city:
            data = request.get_json()
            city.id_tara = data['idTara']
            city.nume = data['nume']
            city.latitudine = data['lat']
            city.longitudine = data['lon']
            db.session.commit()
            return make_response(jsonify({'message': 'City updated'}), 200)
        return make_response(jsonify({'message': 'Not found'}), 404)
    except:
        return make_response(jsonify({'message': 'Bad request'}), 400)

# delete a city success 200 bad request 400 not found 404
@app.route('/api/cities/<int:id>', methods=['DELETE'])
def delete_city(id):
    try:
        city = City.query.filter_by(id=id).first()
        if city:
            db.session.delete(city)
            db.session.commit()
            return make_response(jsonify({'message': 'City deleted'}), 200)
        return make_response(jsonify({'message': 'Not found'}), 404)
    except:
        return make_response(jsonify({'message': 'Bad request'}), 400)
    
# create a temperature success 201 and temperature_id bad request 400 not found 404 conflict 409
# body {value, city_id}
@app.route('/api/temperatures', methods=['POST'])
def add_temperature():
    try:
        data = request.get_json()
        new_temperature = Temperatures(valoare=data['valoare'], id_oras =data['idOras'])
        if new_temperature:
            db.session.add(new_temperature)
            db.session.commit()
            return make_response(jsonify({'id': new_temperature.id}), 201)
        return make_response(jsonify({'message': 'Bad request'}), 400)
    except:
        return make_response(jsonify({'message': 'Conflict'}), 409)
    
# get all temperatures
#body {latitudine, longitudine, from: Date, until: Date}
@app.route('/api/temperatures', methods=['GET'])
def get_temperatures():
    try:
        data = request.get_json()
        lat = request.args.get('lat')
        lon = request.args.get('lon')

        query = City.query

        if lat is not None:
            query = query.filter_by(latitudine=lat)

        if lon is not None:
            query = query.filter_by(longitudine=lon)

        cities = query.all()
        if cities:
            temperature_query = Temperatures.query.filter(Temperatures.id_oras.in_([city.id for city in cities]))

            date_from = request.args.get('from')
            date_until = request.args.get('until')

            if date_from is not None and date_until is not None:
                temperature_query = temperature_query.filter(Temperatures.timestamp.between(date_from, date_until))
            elif date_from is not None:
                temperature_query = temperature_query.filter(Temperatures.timestamp >= date_from)
            elif date_until is not None:
                temperature_query = temperature_query.filter(Temperatures.timestamp <= date_until)

            temperatures = temperature_query.all()
            if temperatures:
                return make_response(jsonify([temperature.json() for temperature in temperatures]), 200)
            return make_response(jsonify([]), 200)
        return make_response(jsonify({'message': 'Not found'}), 404)
    except:
        return make_response(jsonify({'message': 'Bad request'}), 400)

# get all temperatures by city_id and from: Date, until: Date
@app.route('/api/temperatures/cities/<int:city_id>', methods=['GET'])
def get_temperatures_by_city(city_id):
    try:
        temperature_query = Temperatures.query.filter_by(id_oras=city_id)
        date_from = request.args.get('from')
        date_until = request.args.get('until')

        if date_from is not None and date_until is not None:
            temperature_query = temperature_query.filter(Temperatures.timestamp.between(date_from, date_until))
        elif date_from is not None:
            temperature_query = temperature_query.filter(Temperatures.timestamp >= date_from)
        elif date_until is not None:
            temperature_query = temperature_query.filter(Temperatures.timestamp <= date_until)

        temperatures = temperature_query.all()
        if temperatures:
            return make_response(jsonify([temperature.json() for temperature in temperatures]), 200)
        return make_response(jsonify({'message': 'Not found'}), 404)
    except:
        return make_response(jsonify({'message': 'Bad request'}), 400)
    
# get all temperatures by country_id and from: Date, until: Date
@app.route('/api/temperatures/countries/<int:country_id>', methods=['GET'])
def get_temperatures_by_country(country_id):
    try:
        cities = City.query.filter_by(id_tara=country_id).all()
        if cities:
            temperature_query = Temperatures.query.filter(Temperatures.id_oras.in_([city.id for city in cities]))
            date_from = request.args.get('from')
            date_until = request.args.get('until')

            if date_from is not None and date_until is not None:
                temperature_query = temperature_query.filter(Temperatures.timestamp.between(date_from, date_until))
            elif date_from is not None:
                temperature_query = temperature_query.filter(Temperatures.timestamp >= date_from)
            elif date_until is not None:
                temperature_query = temperature_query.filter(Temperatures.timestamp <= date_until)

            temperatures = temperature_query.all()
            if temperatures:
                return make_response(jsonify([temperature.json() for temperature in temperatures]), 200)
            return make_response(jsonify({'message': 'Not found'}), 404)
        return make_response(jsonify({'message': 'Not found'}), 404)
    except:
        return make_response(jsonify({'message': 'Bad request'}), 400)
    
# update a temperature success 200 bad request 400 not found 404 conflict 409
# body {id, value, city_id}
@app.route('/api/temperatures/<int:id>', methods=['PUT'])
def update_temperature(id):
    try:
        temperature = Temperatures.query.filter_by(id=id).first()
        if temperature:
            data = request.get_json()
            temperature.valoare = data['valoare']
            temperature.id_oras = data['idOras']
            db.session.commit()
            return make_response(jsonify({'message': 'Temperature updated'}), 200)
        return make_response(jsonify({'message': 'Not found'}), 404)
    except:
        return make_response(jsonify({'message': 'Bad request'}), 400)
    
# delete a temperature success 200 bad request 400 not found 404
@app.route('/api/temperatures/<int:id>', methods=['DELETE'])
def delete_temperature(id):
    try:
        temperature = Temperatures.query.filter_by(id=id).first()
        if temperature:
            db.session.delete(temperature)
            db.session.commit()
            return make_response(jsonify({'message': 'Temperature deleted'}), 200)
        return make_response(jsonify({'message': 'Not found'}), 404)
    except:
        return make_response(jsonify({'message': 'Bad request'}), 400)
