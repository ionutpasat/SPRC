from flask import Flask, request, jsonify

app = Flask(__name__)

movies = []
index = 1

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/movies", methods=["GET"])
def handle_get():
    return jsonify(movies), 200


@app.route("/movies", methods=["POST"])
def handle_post():
    data = request.get_json()
    global index
    movies.append({'id':index, 'nume':data['nume']})
    index = index + 1
    return data, 201

@app.route("/movie/<int:numar>", methods=["PUT"])
def handle_put(numar):
    data = request.get_json(silent=True)
    found = 0
    for elem in movies:
        if elem['id'] == numar:
            found = 1
    if found == 0:
        return "not found", 404
    for elem in movies:
        if elem['id'] == numar:
            elem['nume'] = data['nume']
    return data, 200

@app.route("/movie/<int:numar>", methods=["GET"])
def handle_get_by_id(numar):
    for elem in movies:
        if elem['id'] == numar:
            return elem, 200
    return {'error':'not found'}, 404

@app.route("/movie/<int:numar>", methods=["DELETE"])
def handle_delete_by_id(numar):
    for elem in movies:
        if elem['id'] == numar:
            e = elem
            movies.remove(elem)
            return e, 200
    return 'not found', 404

@app.route("/reset", methods=["DELETE"])
def handle_delete():
    movies.clear()
    return {'success':'movies cleared'}, 200


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)