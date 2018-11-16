from utils import load_json
import pyexcel
from collections import OrderedDict

def extract_exhibitor(desription):
  lines = desription.split("\n")
  exhibitors = []
  l = len(lines)
  for i in range(len(lines)):
    if "Exhibitor" == lines[i] or "Featured Exhibitors" == lines[i]:
      pass
      # print(lines[i])
    if ("Exhibitor" == lines[i] or "Featured Exhibitors" == lines[i]) and i < l - 1 and lines[i + 1] != "":
      for j in range(i + 1, len(lines)):
        if lines[j] == "":
          break
        exhibitors.append(lines[j])
      break
  
  return "\n".join(exhibitors)



cities_json_file_name = "jf_cities.json"

cities = load_json(cities_json_file_name)

records = []

for city in cities:
  for jobfair in city["jobfair_list"]:
    # print("---------------")
    # print(jobfair)
    exhibitor_string = extract_exhibitor(jobfair["description"])
    # print(exhibitor_string)
    records.append(
      OrderedDict(
        {
          "Name": jobfair["name"],
          "City": city["name"],
          "Date": jobfair["date"],
          "Time": jobfair["time"],
          "Location": jobfair["location"],
          "Cost": jobfair["cost"],
          "Link": jobfair["link"],
          "Exhibitors": exhibitor_string,
          "Description": jobfair["description"],
        }
      )
    )

pyexcel.save_as(records=records, dest_file_name="jobfair.xlsx")