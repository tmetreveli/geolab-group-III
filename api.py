import requests

def api_route():
    api = "https://fakestoreapi.com/products"
    data = requests.get(api)
    print(data.json())
    for product in data.json():
        print(product["title"])

"""
Request - > response
"""

api_route()