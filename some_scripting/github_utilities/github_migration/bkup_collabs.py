import requests
import time
import os

# You must create the PAT env variable with your access token.
pat = os.environ.get("PAT")

GITHUB_API_URL = "https://api.github.com"

HEADERS = {
    "Authorization": f"token {pat}",
    "Accept": "application/vnd.github+json"
}

def get_all_repos():
    repos = []
    page = 1
    while True:
        url = f"{GITHUB_API_URL}/user/repos?visibility=private&affiliation=owner&per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Error al obtener repos en página {page}: {response.status_code}")
            break
        page_repos = response.json()
        if not page_repos:
            break
        repos.extend(page_repos)
        page += 1
        time.sleep(0.5)  # Evita rate limit
    return repos

def get_collaborators(owner, repo_name):
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo_name}/collaborators"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error al obtener colaboradores de {repo_name}: {response.status_code}")
        print(f"Detalle: {response.json().get('message', '')}")
        return []
    return response.json()

def main():
    result = {}  # {repo_name: [{login, permission}]}
    repos = get_all_repos()
    print(f"Se encontraron {len(repos)} repositorios privados.")
    for repo in repos:
        repo_name = repo["name"]
        owner = repo["owner"]["login"]
        print(f"Procesando: {repo_name}")
        collaborators = get_collaborators(owner, repo_name)
        result[repo_name] = []
        for collab in collaborators:
            perm = collab.get("permissions", {})
            permission = "admin" if perm.get("admin") else "write" if perm.get("push") else "read"
            result[repo_name].append({
                "login": collab["login"],
                "permission": permission
            })
        time.sleep(0.5)
    
    # Guardar resultado en archivo JSON
    import json
    with open("colaboradores_por_repo.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("Resultado guardado en 'colaboradores_por_repo.json'.")

if __name__ == "__main__":
    main()
