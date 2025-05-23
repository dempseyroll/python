import requests
import os

pat = os.environ.get("PAT")
headers = {
    "Authorization": f"token {pat}",
    "Accept": "application/vnd.github.v3+json"
}

def obtener_repositorios():
    url = "https://api.github.com/user/repos"
    repos = []
    page = 1
    while True:
        resp = requests.get(url, headers=headers, params={"per_page": 100, "page": page})
        if resp.status_code != 200:
            print("❌ Error:", resp.status_code)
            break
        data = resp.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def obtener_webhooks(repo_full_name):
    url = f"https://api.github.com/repos/{repo_full_name}/hooks"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"   ❌ Error al obtener webhooks: {resp.status_code}")
        return []
    return resp.json()

# Run
repos = obtener_repositorios()
print(f"🔍 Total repos encontrados: {len(repos)}")

for repo in repos:
    name = repo["full_name"]
    print(f"\n📁 {name}")
    hooks = obtener_webhooks(name)
    if not hooks:
        print("   ⚠️  Sin webhooks.")
        continue
    for hook in hooks:
        events = hook.get("events", [])
        url = hook.get("config", {}).get("url", "sin URL")
        print(f"   🔗 Webhook a: {url}")
        print(f"   📌 Eventos: {', '.join(events)}")
