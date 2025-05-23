import requests
import yaml
import base64
import re
import time
from requests.adapters import HTTPAdapter, Retry

# === CONFIGURACIÓN ===
# Change this to use secure manage of credentials.
GITHUB_USERNAME = ''
GITHUB_TOKEN = 'YOUR_PAT'
API_BASE = 'https://api.github.com'

session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retries)
session.mount('https://', adapter)
session.headers.update({
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json'
})

SUSPECT_NAMES = re.compile(r"(GH_TOKEN|PAT|PERSONAL|BOT|DEPLOY|ACCESS)", re.IGNORECASE)

def get_all_repos():
    repos = []
    page = 1
    while True:
        url = f"{API_BASE}/user/repos?per_page=100&page={page}&affiliation=owner"
        r = session.get(url)
        if r.status_code != 200:
            break
        data = r.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def get_collaborators(repo_full_name):
    url = f"{API_BASE}/repos/{repo_full_name}/collaborators"
    r = session.get(url)
    return r.json() if r.status_code == 200 else []

def list_workflow_files(repo_full_name):
    url = f"{API_BASE}/repos/{repo_full_name}/contents/.github/workflows"
    r = session.get(url)
    if r.status_code != 200:
        return []
    return [f['name'] for f in r.json() if f['name'].endswith('.yml') or f['name'].endswith('.yaml')]

def get_workflow_file(repo_full_name, filename):
    url = f"{API_BASE}/repos/{repo_full_name}/contents/.github/workflows/{filename}"
    r = session.get(url)
    if r.status_code != 200:
        return None
    content = base64.b64decode(r.json()['content'])
    return content.decode('utf-8')

def parse_secrets_from_yaml(yaml_content):
    try:
        doc = yaml.safe_load(yaml_content)
    except Exception:
        return []
    secrets = set()

    def extract_secrets(node):
        if isinstance(node, dict):
            for k, v in node.items():
                extract_secrets(v)
        elif isinstance(node, list):
            for item in node:
                extract_secrets(item)
        elif isinstance(node, str):
            found = re.findall(r"secrets\.([A-Z0-9_]+)", node)
            secrets.update(found)

    extract_secrets(doc)
    return list(secrets)

def analyze_repo(repo):
    full_name = repo['full_name']
    print(f"\n🔍 Analizando repo: {full_name}")
    collabs = get_collaborators(full_name)
    external_collabs = [c for c in collabs if c['type'] == 'User' and not c['site_admin']]

    workflow_files = list_workflow_files(full_name)
    if not workflow_files:
        print("  ⚠️ No hay workflows")
        return

    total_secrets = set()
    suspect_secrets = set()

    for wf in workflow_files:
        content = get_workflow_file(full_name, wf)
        if not content:
            continue
        secrets = parse_secrets_from_yaml(content)
        total_secrets.update(secrets)
        for s in secrets:
            if SUSPECT_NAMES.search(s):
                suspect_secrets.add(s)

    print(f"  📂 Workflows: {len(workflow_files)} | Secrets usados: {len(total_secrets)}")
    if suspect_secrets:
        print(f"  ⚠️ Secrets sospechosos: {', '.join(suspect_secrets)}")

    if external_collabs:
        print(f"  👥 Colaboradores externos: {[c['login'] for c in external_collabs]}")
        if suspect_secrets:
            print("  🔴 Riesgo: tokens personales pueden dejar de funcionar tras la transferencia")

def main():
    repos = get_all_repos()
    print(f"\n🔎 Procesando {len(repos)} repositorios...\n")
    for repo in repos:
        try:
            analyze_repo(repo)
        except Exception as e:
            print(f"  ⚠️ Error en {repo['full_name']}: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
