import json
from bs4 import BeautifulSoup
import requests

def save_json(data, file_name):
  with open(file_name, "w") as f:
    f.write(json.dumps(data))


def load_json(file_name):
  with open(file_name, "r") as f:
    text = f.read()
    return json.loads(text)


def load_soup(url):
  conn = requests.get(url)
  if conn.status_code == 200:
    return BeautifulSoup(conn.text, "html.parser")
  else:
    return None