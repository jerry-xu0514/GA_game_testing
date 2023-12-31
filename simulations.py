import requests
import json
import sys
import numpy as np

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def get_results(population, url = 'http://10.41.0.159:8080/simulator'):

    headers = {
        'Content-Type': 'application/json'
    }

    population_j = json.dumps(population, cls=NpEncoder)
    loaded_population = json.loads(population_j)

    response = requests.post(url, json=loaded_population, headers=headers)

    return response.json()

def store(filename, population):
    json_object = json.dumps(population, indent = 4, cls=NpEncoder)
    with open(filename, 'w') as f:
        f.write(json_object)