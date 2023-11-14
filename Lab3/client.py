import requests

base_url = 'http://127.0.0.1:5000'

# Test GET request for movies
response = requests.get(f'{base_url}/movies')
print("GET /movies:")
print(response.json())

# Test POST request for adding movies
new_movies = [
    {'nume': 'Inception'},
    {'nume': 'Interstellar'},
    {'nume': 'The Dark Knight'}
]

for movie in new_movies:
    response = requests.post(f'{base_url}/movies', json=movie)
    print(f"\nPOST /movies with data {movie}:")
    print(response.json())

# Test GET request for movies after adding
response = requests.get(f'{base_url}/movies')
print("\nGET /movies:")
print(response.json())

# Test PUT request for updating a movie
updated_movie = {'nume': 'Inception 2.0'}
response = requests.put(f'{base_url}/movie/1', json=updated_movie)
print("\nPUT /movie/1:")
print(response.json())

# Test GET request for a specific movie by ID
response = requests.get(f'{base_url}/movie/1')
print("\nGET /movie/1:")
print(response.json())

# Test DELETE request for deleting a movie by ID
response = requests.delete(f'{base_url}/movie/2')
print("\nDELETE /movie/2:")
print(response.json())

# Test GET request for movies after deletion
response = requests.get(f'{base_url}/movies')
print("\nGET /movies:")
print(response.json())

# Test DELETE request for resetting the movie list
response = requests.delete(f'{base_url}/reset')
print("\nDELETE /reset:")
print(response.json())

# Test GET request for movies
response = requests.get(f'{base_url}/movies')
print("\nGET /movies:")
print(response.json())
