import requests
import json
import time
import os

pat = os.environ.get("PAT")
GITHUB_API_URL = "https://api.github.com"
ORG = ""
HEADERS = {
    "Authorization": f"token {pat}",
    "Accept": "application/vnd.github+json"
}

def add_collaborator(repo_name, username, permission):
    url = f"{GITHUB_API_URL}/repos/{ORG}/{repo_name}/collaborators/{username}"
    payload = {
        "permission": permission  # Puede ser 'pull', 'push' o 'admin'
    }
    response = requests.put(url, headers=HEADERS, json=payload)
    if response.status_code in [201, 204]:
        print(f"✔️ {username} agregado a {repo_name} con permiso {permission}")
    else:
        print(f"❌ Error al agregar {username} a {repo_name}: {response.status_code}")
        print(response.json())

def main():
    with open("colaboradores_por_repo.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for repo_name, collaborators in data.items():
        print(f"Procesando {repo_name}...")
        for collab in collaborators:
            username = collab["login"]
            perm = collab["permission"]
            # GitHub usa 'pull' para read, 'push' para write, 'admin' para admin
            gh_permission = {"read": "pull", "write": "push", "admin": "admin"}.get(perm, "pull")
            add_collaborator(repo_name, username, gh_permission)
            time.sleep(0.5)

if __name__ == "__main__":
    main()
