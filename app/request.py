import requests
from .models import Quote

url = "http://quotes.stormconsultancy.co.uk/random.json"

def get_quotes():
    '''
    Function that consumes the http request to get the random quotes
    '''
   
    response = requests.get(url).json()

    random_quote = Quote(response.get("quote"),response.get("author"))
    return random_quote