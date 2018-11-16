import requests
from bs4 import BeautifulSoup
from utils import load_json, save_json, load_soup

url = "https://jobfairs.indeed.com"
cities_json_file_name = "jf_cities.json"



def crape_jobfair_detail(jobfair):
  soup = load_soup(jobfair["link"])
  # try the first case
  print("Processing", jobfair["name"])
  print("Link", jobfair["link"])
  # 1st case: https://jobfairs.indeed.com/Atlanta/fair/19048
  if soup.find("div", id="fair-header") is not None:
    fair_header = soup.find("div", id="fair-header")
    details = fair_header.find_all("div", "event-detail")
    p_description = soup.find("p", "description")
    date_time = details[0].find("div")
    date = date_time.b.string
    time = date_time.span.string
    location = details[1].find("div").get_text()
    cost = details[2].find("div").get_text().replace("Cost", "").strip()
    jobfair["time"] = time
    jobfair["location"] = location
    jobfair["cost"] = cost
    jobfair["description"] = p_description.string
  elif soup.find("div", "event-details") is not None:
    event_details = soup.find("div", "event-details")
    event_info_list = event_details.find_all("p", "event-info")
    address_label = event_details.find("p", "address-label")
    p_description = soup.find("p", "description")

    date = event_info_list[0].span.string
    time = event_info_list[1].span.string
    location = address_label.get_text().replace("Address:", "")
    description = p_description.string

    jobfair["date"] = date
    jobfair["time"] = time
    jobfair["location"] = location
    jobfair["cost"] = "Free"
    jobfair["description"] = p_description.string

  elif soup.find("div", id="event-detail-container") is not None:
    event_detail_container = soup.find("div", id="event-detail-container")
    event_time = event_detail_container.find("div", "event-detail-time")
    event_location = event_detail_container.find("div", "event-detail-location")
    description_div = soup.find("div", "col-xs-12 hide-max-md page-content")

    time = event_time.get_text()
    location = event_location.get_text()

    jobfair["time"] = time
    jobfair["location"] = location
    jobfair["description"] = description_div.get_text()
    jobfair["cost"] = "N/A"

cities = load_json(cities_json_file_name)

for city in cities:
  for jobfair in city["jobfair_list"]:
    crape_jobfair_detail(jobfair)

save_json(cities, cities_json_file_name)

# if __name__ == "__main__":
#   soup = load_soup("https://jobfairs.indeed.com/Atlanta/fair/19048")
#   # try the first case
#   with open("jobfair.html", "w") as f:
#     f.write(soup.prettify())
#   if soup.find("div", id="fair-header") is not None:
#     fair_header = soup.find("div", id="fair-header")
#     details = fair_header.find_all("div", "event-detail")
#     p_description = soup.find("p", "description")
#     date_time = details[0].find("div")
#     date = date_time.b.string
#     time = date_time.span.string
#     location = details[1].find("div").get_text()
#     cost = details[2].find("div").get_text().replace("Cost", "").strip()
#     print(date)
#     print(time)
#     print(location)
#   elif soup.find("div", "event-details") is not None:
#     event_details = soup.find("div", "event-details")
#     event_info_list = event_details.find_all("p", "event-info")
#     address_label = event_details.find("p", "address-label")
#     p_description = soup.find("p", "description")

#     date = event_info_list[0].span.string
#     time = event_info_list[1].span.string
#     location = address_label.get_text().replace("Address:", "")
#     description = p_description.string

#     print(date)
#     print(time)
#     print(location)
#     print(description)