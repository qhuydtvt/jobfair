from utils import load_json, load_soup, save_json

cities_json_file_name = "jf_cities.json"
url = "https://jobfairs.indeed.com"

def jobfair_to_dict(jobfair):
  a = jobfair.a
  print(a)
  return {
    "link": url + a["href"] if "https://" not in a["href"] else a["href"],
    "name": a.h2.string,
    "date": a.find("p", "date").string,
    "location": a.find("p", "location").string,
    'description': a.find("p", "description").string,
  }

def scrape_joblist(city):
  print("City: ", city["name"])
  link = city["link"]
  print(link)
  page_no = 1
  if "page_max" not in city:
    city["page_max"] = -1
  city["jobfair_list"] = []
  print("Page max: ", city["page_max"])
  while page_no <= city["page_max"] or city["page_max"] == -1:
    print("Proccessing page", page_no)
    page_link = "{0}?page={1}".format(link, page_no)
    print(page_link)
    print("- " * 20)
    soup = load_soup(page_link)
    if city["page_max"] == -1:
      city["page_max"] = soup.find("div", "pagination").find("span", "step-links").find_all("a")[-2]["href"].replace("?page=", "")
      city["page_max"] = int(city["page_max"])
      print(city["page_max"])

    jobfair_container = soup.find("div", id="jfserp")
    jobfairs = [div for div in jobfair_container.find_all("div", "jobfair")]
    jobfairs.append(jobfair_container.find("div", "featured jobfair"))
    city["jobfair_list"].extend([jobfair_to_dict(job_fair) for job_fair in jobfairs if job_fair != None])
    page_no += 1



cities = load_json(cities_json_file_name)
for city in cities:
  scrape_joblist(city)

save_json(cities, cities_json_file_name)
