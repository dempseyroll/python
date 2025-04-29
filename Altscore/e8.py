# Puerta mágica
import requests
import base64

apiKey = KEY
header_api = "API-KEY"
header_json = "application/json"
headers = {"accept": header_json, header_api: apiKey}

url = 'https://makers-challenge.altscore.ai/v1/s1/e8/actions/door'
cookie = "QWx0d2FydHM=" # Altwarts. Be careful
jar = requests.cookies.RequestsCookieJar()
jar.set('gryffindor', cookie, path='/')

r = requests.post(url=url, headers=headers, data='', cookies=jar)

while ("gryffindor" in r.cookies):
	jar.set('gryffindor', cookie, path='/')
	r = requests.post(url=url, headers=headers, data='', cookies=jar)
	cookies = r.cookies
	if ("Correcto" not in r.text):
		cookie = "cmV2ZWxpbwo="
		r = requests.post(url=url, headers=headers, data=cookie, cookies=jar)
		print(r.text)
	#print("HTTP Response Code: " + str(r.status_code))
	print("Response: " + r.text)
	#print("Headers: " + str(r.headers))
	cookie = cookies.get('gryffindor')
	decoded_cookie = base64.b64decode(cookie)
	d = decoded_cookie.decode("utf-8")
	print(d)
