import requests
import os

# === CONFIGURACIÓN ===
pat = os.environ.get("PAT")
ORG_NAME = ''
EMAILS_FILE = 'emails.txt'  # archivo con un email por línea
ROLE = 'direct_member'  # 'direct_member' para miembros, 'admin' si querés admins

# === HEADERS PARA LA API ===
headers = {
    'Authorization': f'token {pat}',
    'Accept': 'application/vnd.github+json'
}

# === FUNCIÓN PARA INVITAR ===
def invite_user_by_email(email):
    url = f'https://api.github.com/orgs/{ORG_NAME}/invitations'
    data = {
        'email': email.strip(),
        'role': ROLE
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f'✅ Invitación enviada a: {email}')
    elif response.status_code == 422 and 'errors' in response.json():
        print(f'⚠️  Ya fue invitado o es miembro: {email}')
    else:
        print(f'❌ Error con {email}: {response.status_code} - {response.text}')

# === CARGAR EMAILS Y PROCESAR ===
with open(EMAILS_FILE, 'r') as f:
    emails = [line.strip() for line in f if line.strip()]

print(f'Invitando a {len(emails)} usuarios...')
for email in emails:
    invite_user_by_email(email)
