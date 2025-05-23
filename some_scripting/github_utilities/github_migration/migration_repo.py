# MIGRATION SCRIPT #

import requests
import time
import os

# === CONFIGURACIÓN ===
pat = os.environ.get("PAT")
USERNAME = ''
DEST_ORG = ''

# === HEADERS PARA LA API ===
headers = {
    'Authorization': f'token {pat}',
    'Accept': 'application/vnd.github+json',
    "X-GitHub-Api-Version": "2022-11-28"
}

def get_private_repos(username):
    repos = []
    page = 1
    while True:
        #url = f'https://api.github.com/user/repos?visibility=private&per_page=100&page={page}'
        url = f'https://api.github.com/user/repos?per_page=100&page={page}'
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f'❌ Error al obtener repos: {resp.status_code} - {resp.text}')
            break
        data = resp.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def transfer_repo(repo_name):
    url = f'https://api.github.com/repos/{USERNAME}/{repo_name}/transfer'
    data = {
        "new_owner": DEST_ORG
    }
    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code == 202:
        print(f'✅ Transferencia iniciada para: {repo_name}')
    elif resp.status_code == 403:
        print(f'🚫 Permiso denegado para transferir {repo_name}')
    else:
        print(f'❌ Error al transferir {repo_name}: {resp.status_code} - {resp.text}')

# === EJECUCIÓN ===
repos = get_private_repos(USERNAME)
if len(repos) == 0:
    print(f'Se encontraron {len(repos)} repos privados. No se hace migración.')
    exit()
else:
    print(f'Se encontraron {len(repos)} repos privados.')

for repo in repos:
    repo_name = repo['name']
    print(f'🔄 Transfiriendo {repo_name}...')
    transfer_repo(repo_name)
    time.sleep(1.5)  # Para evitar rate-limiting
