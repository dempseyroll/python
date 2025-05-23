import requests

# === CONFIGURACIÓN ===
# Change this to manage credentials safe (env or getenv)
GITHUB_USERNAME = 'YOUR_USER'
GITHUB_TOKEN = 'YOUR_PAT'
DEST_ORG = 'YOUR_ORG'  # opcional, para validar duplicados
API_BASE = 'https://api.github.com'

session = requests.Session()
session.headers.update({
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json'
})

def get_user_repos():
    repos = []
    page = 1
    while True:
        url = f'{API_BASE}/user/repos?per_page=100&page={page}&affiliation=owner'
        r = session.get(url)
        if r.status_code != 200:
            raise Exception(f'Error al obtener repos: {r.status_code} - {r.text}')
        data = r.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def check_name_conflict_in_org(repo_name):
    url = f'{API_BASE}/repos/{DEST_ORG}/{repo_name}'
    r = session.get(url)
    return r.status_code == 200  # True si ya existe

def check_transfer_eligibility(repo):
    issues = []

    if repo['archived']:
        issues.append('📦 Está archivado')
    
    if repo['fork']:
        issues.append('🌱 Es un fork (puede requerir atención especial)')
    
    if repo['owner']['type'] == 'Organization':
        issues.append('🏢 Ya pertenece a una organización')

    if not repo.get('permissions', {}).get('admin', False):
        issues.append('🚫 No tenés permisos de admin en este repo')

    if DEST_ORG and check_name_conflict_in_org(repo['name']):
        issues.append(f'❗ Ya existe un repositorio con el mismo nombre en la organización "{DEST_ORG}"')

    return issues

def main():
    repos = get_user_repos()
    for repo in repos:
        name = repo['full_name']
        print(f'\n🔍 Revisando: {name}')
        issues = check_transfer_eligibility(repo)
        if issues:
            print('  ❌ No puede transferirse directamente por:')
            for issue in issues:
                print(f'     - {issue}')
        else:
            print('  ✅ Este repositorio está en condiciones de ser transferido.')

if __name__ == '__main__':
    main()
