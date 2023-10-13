import requests 

NUME = "Pasat Ionut"
GRUPA = "344C1"

def get_proof(response):
    return response.json()['proof']

def task1():
    URL = "https://sprc.dfilip.xyz/lab1/task1/check"

    params = f"nume={NUME}&grupa={GRUPA}"
    data = {"secret": "SPRCisNice",}
    header = {"secret2": "SPRCisBest",}

    r = requests.post(URL, data=data, params=params, headers=header) 
    
    print(r.json())
    print("proof TASK1")
    proof = get_proof(r)
    print(proof)

def task2():
    URL = "https://sprc.dfilip.xyz/lab1/task2"

    json = {"username": "sprc", 'password': 'admin', 'nume' : NUME}
    r = requests.post(URL, json=json)
    
    print("proof TASK2")
    proof = get_proof(r)
    print(proof)

def task3():
    URL_POST = "https://sprc.dfilip.xyz/lab1/task3/login"
    session = requests.Session()
    json = {"username": "sprc", 'password': 'admin', 'nume' : NUME}
    r = session.post(URL_POST, json=json)
    print(r.text)

    URL_GET = "https://sprc.dfilip.xyz/lab1/task3/check"
    r = session.get(URL_GET)
    print("proof TASK3")
    proof = get_proof(r)
    print(proof)

if __name__ == '__main__':
    task1()
    task2()
    task3()
