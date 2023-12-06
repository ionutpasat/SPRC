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
        return {'id': self.id, 'valoare': self.valoare, 'timestamp': self.timestamp.strftime('%Y-%m-%d')}

db.create_all()

# ruta de test pentru sanity check
@app.route('/api/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route sanity check'}), 200)

# endpoint pentru crearea de tari
@app.route('/api/countries', methods=['POST'])
def create_country():
    try:
        required_keys = ['nume', 'lat', 'lon']
        data = request.get_json()        
        if len(data) >= 3 and all(key in data for key in required_keys):
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
        return make_response(jsonify({'message': 'Conflict'}), 409)

# endpoint pentru interogarea tuturor tarilor
@app.route('/api/countries', methods=['GET'])
def get_countries():
    countries = Country.query.all()
    # daca exista tari in baza de date, se intoarce un array de tari, daca nu se intoarce un array gol
    # care sa semnifice ca la momentul interogarii nu exista tari in baza de date
    if countries:
        return make_response(jsonify([country.json() for country in countries]), 200)

# endpoint pentru actualizarea unei tari dupa id
@app.route('/api/countries/<int:_id>', methods=['PUT'])
def update_country(_id):
    try:
        required_keys = ['id', 'nume', 'lat', 'lon']
        country = Country.query.filter_by(id=_id).first()
        # daca tara exista in baza de date, se actualizeaza datele acesteia
        if country is not None:
            data = request.get_json()
            if len(data) >= 4 and all(key in data for key in required_keys):
                # " It is commonly agreed that primary keys should be immutable 
                # (or as stable as possible since immutability can not be enforced in the DB). "
                # country.id = data['id'] // foreign key for cities
                # country.nume = data['nume'] 
                country.latitudine = data['lat']
                country.longitudine = data['lon']
                db.session.commit()
                return make_response(jsonify({'message': 'Country updated'}), 200)
            # daca request-ul nu foloseste un body valid, se intoarce un mesaj corespunzator
            return make_response(jsonify({'message': 'Bad Request'}), 400)
        # daca tara nu exista in baza de date, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Not found'}), 404)
    except:
        # daca se arunca exceptii in timpul executiei, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Conflict'}), 409)
    
# endpoint pentru stergerea unei tari
@app.route('/api/countries/<int:id>', methods=['DELETE'])
def delete_country(id):
    try:
        if id is None or not isinstance(id, int) or id < 0:
            # daca request-ul nu foloseste un parametru valid, se intoarce un mesaj corespunzator
            return make_response(jsonify({'message': 'Bad request'}), 400)
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
        return make_response(jsonify({'message': 'Conflict'}), 409)
    
# endpoint pentru crearea de orase
@app.route('/api/cities', methods=['POST'])
def create_city():
    try:
        required_keys = ['idTara', 'nume', 'lat', 'lon']
        data = request.get_json()
        if len(data) >= 4 and all(key in data for key in required_keys):
            if Country.query.filter_by(id=data['idTara']).first() is None:
                # daca tara nu exista in baza de date, se intoarce un mesaj corespunzator
                return make_response(jsonify({'message': 'Not found'}), 404)
            new_city = City(id_tara=data['idTara'], nume=data['nume'], latitudine=data['lat'], longitudine=data['lon'])
                # daca nu se arunca exceptii si datele sunt valide, se adauga in baza de date
            if new_city:
                db.session.add(new_city)
                db.session.commit()
                return make_response(jsonify({'id': new_city.id}), 201)
        # daca request-ul nu foloseste un body valid, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Bad request'}), 400)
    except:
        # daca se arunca exceptii in timpul executiei, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Conflict'}), 409)
    
# endpoint pentru interogarea tuturor oraselor
@app.route('/api/cities', methods=['GET'])
def get_cities():
    cities = City.query.all()
    # daca exista orase in baza de date, se intoarce un array de orase, daca nu se intoarce un array gol
    # care sa semnifice ca la momentul interogarii nu exista orase in baza de date
    if cities:
        return make_response(jsonify([city.json() for city in cities]), 200)

# endpoint pentru interogarea tuturor oraselor dintr-o tara
@app.route('/api/cities/country/<int:country_id>', methods=['GET'])
def get_cities_by_country(country_id):
    cities = City.query.filter_by(id_tara=country_id).all()
    if cities:
        return make_response(jsonify([city.json() for city in cities]), 200)

# endpoint pentru actualizarea unui oras dupa id
@app.route('/api/cities/<int:id>', methods=['PUT'])
def update_city(id):
    try:
        required_keys = ['id', 'idTara', 'nume', 'lat', 'lon']
        city = City.query.filter_by(id=id).first()
        # daca orasul exista in baza de date, se actualizeaza datele acestuia
        if city:
            data = request.get_json()
            if len(data) >= 5 and all(key in data for key in required_keys):
                # " It is commonly agreed that primary keys should be immutable 
                # (or as stable as possible since immutability can not be enforced in the DB). "
                # city.id = data['id'] // foreign key for temperatures
                # city.id_tara = data['idTara']
                # city.nume = data['nume']
                city.latitudine = data['lat']
                city.longitudine = data['lon']
                db.session.commit()
                return make_response(jsonify({'message': 'City updated'}), 200)
            # daca request-ul nu foloseste un body valid, se intoarce un mesaj corespunzator
            return make_response(jsonify({'message': 'Bad Request'}), 400)
        # daca orasul nu exista in baza de date, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Not found'}), 404)
    except:
        # daca se arunca exceptii in timpul executiei, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Conflict'}), 409)

# endpoint pentru stergerea unui oras
@app.route('/api/cities/<int:id>', methods=['DELETE'])
def delete_city(id):
    try:
        if id is None or not isinstance(id, int) or id < 0:
            # daca request-ul nu foloseste un parametru valid, se intoarce un mesaj corespunzator
            return make_response(jsonify({'message': 'Bad request'}), 400)
        city = City.query.filter_by(id=id).first()
        # daca orasul exista in baza de date, se sterge
        if city:
            db.session.delete(city)
            db.session.commit()
            return make_response(jsonify({'message': 'City deleted'}), 200)
        # daca orasul nu exista in baza de date, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Not found'}), 404)
    except:
        # daca se arunca exceptii in timpul executiei, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Conflict'}), 409)
    
# endpoint pentru crearea de temperaturi
@app.route('/api/temperatures', methods=['POST'])
def add_temperature():
    try:
        requited_keys = ['valoare', 'idOras']
        data = request.get_json()
        if len(data) >= 2 and all(key in data for key in requited_keys):
            if City.query.filter_by(id=data['idOras']).first() is None:
                # daca orasul nu exista in baza de date, se intoarce un mesaj corespunzator
                return make_response(jsonify({'message': 'Not found'}), 404)
            new_temperature = Temperatures(valoare=data['valoare'], id_oras =data['idOras'])
            # daca nu se arunca exceptii si datele sunt valide, se adauga in baza de date
            if new_temperature:
                db.session.add(new_temperature)
                db.session.commit()
                return make_response(jsonify({'id': new_temperature.id}), 201)
        # daca request-ul nu foloseste un body valid, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Bad request'}), 400)
    except:
        # daca se arunca exceptii in timpul executiei, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Conflict'}), 409)
    
# endpoint pentru interogarea tuturor temperaturilor filtrate dupa query params
# cum ar fi latitudine, longitudine si timestamp intre 2 date
@app.route('/api/temperatures', methods=['GET'])
def get_temperatures():
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        # query-ul pentru orase se construieste dinamic in functie de existenta parametrilor
        query = City.query

        if lat is not None:
            query = query.filter_by(latitudine=lat)

        if lon is not None:
            query = query.filter_by(longitudine=lon)

        cities = query.all()
        if cities:
            # la fel si cel pentru temperaturi se construieste tot dinamic in functie de param
            temperature_query = Temperatures.query.filter(Temperatures.id_oras.in_([city.id for city in cities]))

            date_from = request.args.get('from')
            date_until = request.args.get('until')

            # daca se primesc ambele date, interogarea se face intre cele 2 date
            if date_from is not None and date_until is not None:
                temperature_query = temperature_query.filter(Temperatures.timestamp.between(date_from, date_until))
            # daca primesc doar data de inceput, interogarea se face de la data respectiva
            elif date_from is not None:
                temperature_query = temperature_query.filter(Temperatures.timestamp >= date_from)
            # daca primesc doar data de sfarsit, interogarea se face pana la data respectiva
            elif date_until is not None:
                temperature_query = temperature_query.filter(Temperatures.timestamp <= date_until)

            temperatures = temperature_query.all()
            if temperatures:
                return make_response(jsonify([temperature.json() for temperature in temperatures]), 200)
            return make_response(jsonify([]), 200)
    except:
        # daca se arunca exceptii in timpul executiei, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Conflict'}), 409)

# endpoint pentru interogarea tuturor temperaturilor pentru un oras dupa id
# si filtrate dupa query params: timestamp intre 2 date
@app.route('/api/temperatures/cities/<int:city_id>', methods=['GET'])
def get_temperatures_by_city(city_id):
    try:
        # query-ul pentru temperaturi se construieste dinamic in functie de param
        temperature_query = Temperatures.query.filter_by(id_oras=city_id)
        date_from = request.args.get('from')
        date_until = request.args.get('until')

        # daca se primesc ambele date, interogarea se face intre cele 2 date
        if date_from is not None and date_until is not None:
            temperature_query = temperature_query.filter(Temperatures.timestamp.between(date_from, date_until))
        # daca primesc doar data de inceput, interogarea se face de la data respectiva
        elif date_from is not None:
            temperature_query = temperature_query.filter(Temperatures.timestamp >= date_from)
        # daca primesc doar data de sfarsit, interogarea se face pana la data respectiva
        elif date_until is not None:
            temperature_query = temperature_query.filter(Temperatures.timestamp <= date_until)

        temperatures = temperature_query.all()
        # daca exista temperaturi pentru orasul respectiv, se intoarce un array de temperaturi, daca nu se intoarce un array gol
        return make_response(jsonify([temperature.json() for temperature in temperatures]), 200)
    except:
        # daca se arunca exceptii in timpul executiei, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Conflict'}), 409)
    
# endpoint pentru interogarea tuturor temperaturilor pentru o tara dupa id
@app.route('/api/temperatures/countries/<int:country_id>', methods=['GET'])
def get_temperatures_by_country(country_id):
    try:
    
        cities = City.query.filter_by(id_tara=country_id).all()
        if cities:
            # query-ul pentru temperaturi se construieste dinamic in functie de param
            temperature_query = Temperatures.query.filter(Temperatures.id_oras.in_([city.id for city in cities]))
            date_from = request.args.get('from')
            date_until = request.args.get('until')

            # daca se primesc ambele date, interogarea se face intre cele 2 date
            if date_from is not None and date_until is not None:
                temperature_query = temperature_query.filter(Temperatures.timestamp.between(date_from, date_until))
            # daca primesc doar data de inceput, interogarea se face de la data respectiva
            elif date_from is not None:
                temperature_query = temperature_query.filter(Temperatures.timestamp >= date_from)
            # daca primesc doar data de sfarsit, interogarea se face pana la data respectiva
            elif date_until is not None:
                temperature_query = temperature_query.filter(Temperatures.timestamp <= date_until)

            temperatures = temperature_query.all()
            # daca exista temperaturi pentru tara respectiva, se intoarce un array de temperaturi, daca nu se intoarce un array gol
            return make_response(jsonify([temperature.json() for temperature in temperatures]), 200)
        return make_response(jsonify([]), 200)
    except:
        # daca se arunca exceptii in timpul executiei, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Conflict'}), 409)
    
# 
@app.route('/api/temperatures/<int:id>', methods=['PUT'])
def update_temperature(id):
    try:
        # verific daca parametrii sunt valizi
        required_keys = ['id', 'valoare', 'idOras']
        temperature = Temperatures.query.filter_by(id=id).first()
        # daca temperatura exista in baza de date, se actualizeaza datele acesteia
        if temperature:
            data = request.get_json()
            if len(data) >= 3 and all(key in data for key in required_keys):
                temperature.valoare = data['valoare']
                temperature.id_oras = data['idOras']
                db.session.commit()
                return make_response(jsonify({'message': 'Temperature updated'}), 200)
            # daca request-ul nu foloseste un body valid, se intoarce un mesaj corespunzator
            return make_response(jsonify({'message': 'Bad request'}), 400)
        # daca temperatura nu exista in baza de date, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Not found'}), 404)
    except:
        # daca se arunca exceptii in timpul executiei, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Conflict'}), 409)
    
# delete a temperature success 200 bad request 400 not found 404
@app.route('/api/temperatures/<int:id>', methods=['DELETE'])
def delete_temperature(id):
    try:
        if id is None or not isinstance(id, int) or id < 0:
            # daca request-ul nu foloseste un parametru valid, se intoarce un mesaj corespunzator
            return make_response(jsonify({'message': 'Bad request'}), 400)
        temperature = Temperatures.query.filter_by(id=id).first()
        # daca temperatura exista in baza de date, se sterge
        if temperature:
            db.session.delete(temperature)
            db.session.commit()
            return make_response(jsonify({'message': 'Temperature deleted'}), 200)
        # daca temperatura nu exista in baza de date, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Not found'}), 404)
    except:
        # daca se arunca exceptii in timpul executiei, se intoarce un mesaj corespunzator
        return make_response(jsonify({'message': 'Conflict'}), 409)
