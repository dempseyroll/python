import requests

measure = "https://makers-challenge.altscore.ai/v1/s1/e1/resources/measurement"
apiKey = KEY
header_api = "API-KEY"
header_json = "application/json"
headers = {"Content-Type": header_json, header_api: apiKey}

solution_url = "https://makers-challenge.altscore.ai/v1/s1/e1/solution"

### Test measurement ###
while True:
	r = requests.get(url=measure, headers=headers)
	print(r.text)
########################

# Solution #
#for i in range(0,50):
#	r_sol = requests.post(url=solution_url, headers=headers, json={'speed': i})
#	print("For " + str(i) + " value is " + r_sol.text)


# Data obtained:
