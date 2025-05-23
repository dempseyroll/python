import requests

# Configure data - CHANGE: use env or getenv to manage credentials safe.
GITHUB_TOKEN = "YOUR_PAT"
DISCORD_WEBHOOK_URL = "https://YOUR_WEBHOOK" # Don't forget the /github at the end!
GITHUB_USER_OR_ORG = "YOUR_USER"
ES_ORGANIZACIÓN = False  # True si se usa una organización

# Headers for auth
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Get repo list
def obtener_repositorios():
    if ES_ORGANIZACIÓN:
        url = f"https://api.github.com/orgs/{GITHUB_USER_OR_ORG}/repos"
    else:
        url = "https://api.github.com/user/repos"
    print(f"Consultando: {url}")
    repos = []
    page = 1
    while True:
        resp = requests.get(url, headers=headers, params={"per_page": 100, "page": page})
        if resp.status_code != 200:
            print("❌ Error al obtener repositorios:", resp.status_code, resp.text)
            break
        data = resp.json()
        if not data:
            print("✅ No hay más repositorios.")
            break
        repos.extend(data)
        page += 1
    print(f"🔍 Total repos encontrados: {len(repos)}")
    return repos

# Create webhook in a repo
def crear_webhook(full_repo_name):
    url = f"https://api.github.com/repos/{full_repo_name}/hooks"
    data = {
        "name": "web",
        "active": True,
        "events": ["pull_request"],
        "config": {
            "url": DISCORD_WEBHOOK_URL,
            "content_type": "json"
        }
    }
    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code == 201:
        print(f"✅ Webhook creado en {full_repo_name}")
    elif resp.status_code == 422 and "already_exists" in resp.text:
        print(f"⚠️ Webhook ya existe en {full_repo_name}")
    else:
        print(f"❌ Error en {full_repo_name}: {resp.status_code} - {resp.text}")

# Run
if __name__ == "__main__":
    #print("Obteniendo repositorios...")
    repos = obtener_repositorios()
    for repo in repos:
        crear_webhook(repo["full_name"])
