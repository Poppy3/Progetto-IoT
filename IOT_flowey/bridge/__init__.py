cons = [
{"p": "COM3", "b": 9600, "t": "geranio", "id": "442217262fbc447bbab8f677f4a50fd1"},
{"p": "COM3bis", "b": 9600, "t": "geranio", "id": "442217262fbc447bbab8f677f4a50fd1"},
{"p": "asd", "b": 9600, "t": "geranio", "id": "442217262fbc447bbab8f677f4a50fd1"},
{"p": "COM3qwebis", "b": 9600, "t": "geranio", "id": "442217262fbc447bbab8f677f4a50fd1"},
]

ports = [d["p"] for d in cons]

print(ports)
