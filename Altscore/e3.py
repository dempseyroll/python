import requests
import json

apiKey = KEY
header_api = "API-KEY"
header_json = "application/json"
headers = {"Content-Type": header_json, header_api: apiKey}
planets = open('planets.txt', 'a')


solution_url = "https://makers-challenge.altscore.ai/v1/s1/e3/solution"

# Challenge #
### PLANETS ###
with planets as f:
	for page in range(1,7):
		planets = f"https://swapi.dev/api/planets/?page={page}"
		r = requests.get(url=planets, verify=False)
		planet_data = r.text
		f.write(planet_data + "\n")

planets = []

with open("planets.txt", 'r', encoding='utf-8') as f:
	for line in f:
		if line.strip():  # Evita líneas vacías
			item = json.loads(line)
			for i in range(len(item['results'])):
				planets.append(item['results'][i]['name'])

with open("planets.txt", 'w', encoding='utf-8') as f:
	for i in range(len(planets)):
		f.write(planets[i] + "\n")
#########################################################################################################
### PERS ###
characters = open('chars.txt','a')
with characters as f:
	for page in range(1,10):
		people = f"https://swapi.dev/api/people/?page={page}"
		r = requests.get(url=people, verify=False)
		people_data = r.text
		f.write(people_data + "\n")

people = []

with open("chars.txt", 'r', encoding='utf-8') as f:
	for line in f:
		clean_line = line.strip().replace(" ", "%20")  # Evita líneas vacías
		item = json.loads(clean_line)
		for i in range(len(item['results'])):
			people.append(item['results'][i]['name'])

with open("chars.txt", 'w', encoding='utf-8') as f:
	for i in range(len(people)):
		f.write(people[i] + "\n")
#########################################################################################################
# People information in the Oracle
api = {"API-KEY" : KEY, "accept":"application/json"}
info_base64 = []
with open("chars.txt", 'r', encoding='utf-8') as f:
	for line in f:
		#if line.strip():  # Evita líneas vacías
		pers = f"https://makers-challenge.altscore.ai/v1/s1/e3/resources/oracle-rolodex?name={line}"
		r = requests.get(url=pers, headers=api)
		resp = r.text
		print(pers)
		info_base64.append(resp)

print(len(info_base64))
# SUBMIT SOLUTION ? #
# for i in range(len(planets)):
# 	r = requests.post(url=solution_url, headers=headers, json={'planet':planets[i]})
# 	resp = r.text
# 	print(resp)
