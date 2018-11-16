import requests
from bs4 import BeautifulSoup
from utils import save_json

url = "https://jobfairs.indeed.com"

def city_card_to_dict(card):
  link = url + card.a["href"]
  name = card.a.p.string
  return {
    "link": link.replace("?page=1", ""),
    "name": name
  }

conn = requests.get(url)
if conn.status_code == 200:
  soup = BeautifulSoup(conn.text, "html.parser")
  city_container = soup.find("div", id="city-containers")
  city_cards = city_container.find_all("div", "city-card")
  city_data_list = [city_card_to_dict(city_card) for city_card in city_cards]
  save_json(city_data_list, "jf_cities.json")
else:
  print("Connection error", "Errorcode: ", conn.status_code)