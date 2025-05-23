import requests
import time
from requests.adapters import HTTPAdapter, Retry

# === CONFIGURACIÓN ===
# Change this to manage credentials safe (env or getenv).
GITHUB_USERNAME = 'YOUR_USERNAME'
GITHUB_TOKEN = 'YOUR_PAT'
API_BASE = 'https://api.github.com'

# Sesión con reintentos automáticos
session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    raise_on_status=False
)
adapter = HTTPAdapter(max_retries=retries)
session.mount('https://', adapter)
session.headers.update({
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json'
})

def get_all_repos():
    repos = []
    page = 1
    while True:
        url = f"{API_BASE}/user/repos?per_page=100&page={page}&affiliation=owner"
        r = session.get(url)
        if r.status_code != 200:
            raise Exception(f'Error obteniendo repos: {r.status_code} - {r.text}')
        data = r.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def get_deploy_keys(repo):
    url = f"{API_BASE}/repos/{repo}/keys"
    r = session.get(url)
    return r.json() if r.status_code == 200 else []

def get_collaborators(repo):
    url = f"{API_BASE}/repos/{repo}/collaborators"
    r = session.get(url)
    return r.json() if r.status_code == 200 else []

def get_secrets(repo):
    url = f"{API_BASE}/repos/{repo}/actions/secrets"
    r = session.get(url)
    return r.json().get('secrets', []) if r.status_code == 200 else []

def get_workflows(repo):
    url = f"{API_BASE}/repos/{repo}/actions/workflows"
    r = session.get(url)
    return r.json().get('workflows', []) if r.status_code == 200 else []

def get_hooks(repo):
    url = f"{API_BASE}/repos/{repo}/hooks"
    r = session.get(url)
    return r.json() if r.status_code == 200 else []

def get_actions_usage(repo):
    url = f"{API_BASE}/repos/{repo}/actions/runs"
    r = session.get(url)
    if r.status_code != 200:
        return 0
    runs = r.json().get('workflow_runs', [])
    count_recent = 0
    for run in runs:
        run_time = run.get("created_at")
        if run_time:
            t = time.strptime(run_time, "%Y-%m-%dT%H:%M:%SZ")
            timestamp = time.mktime(t)
            if time.time() - timestamp <= 7 * 86400:
                count_recent += 1
    return count_recent

def check_repo(repo):
    full_name = repo['full_name']
    print(f"\n🔍 Repositorio: {full_name}")
    problemas = []

    if repo['archived']:
        problemas.append("📦 Archivado")

    if repo['fork']:
        problemas.append("🌱 Es un fork")

    if repo['owner']['type'] == 'Organization':
        problemas.append("🏢 Ya pertenece a una organización")

    if not repo.get('permissions', {}).get('admin', False):
        problemas.append("🚫 No tenés permisos de admin")

    # Revisión técnica
    deploy_keys = get_deploy_keys(full_name)
    if deploy_keys:
        problemas.append(f"🔐 Tiene {len(deploy_keys)} deploy key(s) definidas")

    collabs = get_collaborators(full_name)
    externos = [c for c in collabs if c.get('type') == 'User']
    if externos:
        problemas.append(f"👤 Tiene {len(externos)} colaboradores externos")

    secrets = get_secrets(full_name)
    if secrets:
        problemas.append(f"🧪 Usa {len(secrets)} secret(s) de GitHub Actions")

    workflows = get_workflows(full_name)
    if workflows:
        print(f"  ✅ Tiene {len(workflows)} workflows definidos")
    else:
        print("  ⚠️ No tiene workflows definidos")

    hooks = get_hooks(full_name)
    if hooks:
        problemas.append(f"🔗 Tiene {len(hooks)} webhook(s) configurados")

    recent_runs = get_actions_usage(full_name)
    print(f"  📊 {recent_runs} ejecuciones de Actions en los últimos 7 días")
    if recent_runs > 0:
        problemas.append(f"⚙️ Tiene uso activo de GitHub Actions (últimos 7 días)")

    if problemas:
        print("  ❌ Problemas para transferencia:")
        for p in problemas:
            print(f"     - {p}")
    else:
        print("  ✅ Apto para transferencia sin problemas críticos")

def main():
    repos = get_all_repos()
    print(f"🔎 Analizando {len(repos)} repositorios...\n")
    for repo in repos:
        try:
            check_repo(repo)
        except Exception as e:
            print(f"  ⚠️ Error procesando {repo['full_name']}: {e}")

if __name__ == '__main__':
    main()
