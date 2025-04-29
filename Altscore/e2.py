import requests
import json

apiKey = KEY
header_api = "API-KEY"
header_json = "application/json"
headers = {"Content-Type": header_json, header_api: apiKey}

solution_url = "https://makers-challenge.altscore.ai/v1/s1/e2/solution"
stars_report = open("stars_report.txt", 'a', encoding='utf-8')

# Challenge #
#### This was the way to obtain all the readings from all pages and write into a file ###
# with stars_report as f:
# 	for page in range(1,35):
# 		stars = f"https://makers-challenge.altscore.ai/v1/s1/e2/resources/stars?page={page}&sort-by=resonance&sort-direction=desc"
# 		r = requests.get(url=stars, headers=headers)
# 		stars_data = r.text
# 		f.write(stars_data + "\n")


######################################################################
# To obtain only de resonances #
resonances = []

with open("stars_report.txt", 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():  # Evita líneas vacías
            item = json.loads(line)
            resonances.append(item[0]['resonance'])

#print(resonances)

sum = 0
for i in range(len(resonances)):
	sum += resonances[i]

average_resonance = sum / len(resonances)
print("La resonancia promedio es de " + str(average_resonance)) 
