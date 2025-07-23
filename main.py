from playwright.sync_api import sync_playwright
import requests
import time

TOKEN = '8183523093:AAGQHpn1VEsUzeD_rZrbe8AdX0nOPvpHYbY'
CHAT_ID = '1837162112'
TITULO_ANTIGO = ''

def enviar_telegram(token, titulo, descricao, link):
    mensagem = f"{titulo}\n\n{descricao}\n{link}"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': mensagem}
    r = requests.post(url, data=payload)
    print("✅ Mensagem enviada!" if r.ok else "❌ Erro ao enviar.")

def extrair_trabalho():
    global TITULO_ANTIGO
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.workana.com/jobs?language=pt&publication=1d&skills=python")
        page.wait_for_timeout(5000)

        # Tenta aceitar cookies e fechar pop-up
        try: page.click('#onetrust-accept-btn-handler', timeout=3000)
        except: pass
        try: page.click('button.close', timeout=3000)
        except: pass

        projeto = page.locator('#projects .project-item').first
        titulo = projeto.locator('h2').inner_text()
        descricao = projeto.locator('p span').inner_text()
        link = projeto.locator('h2 span a').get_attribute('href')

        print("🔍 Título encontrado:", titulo)

        if titulo != TITULO_ANTIGO:
            TITULO_ANTIGO = titulo
            enviar_telegram(TOKEN, titulo, descricao, link)
        else:
            print("⏳ Nada novo...")

        browser.close()

# Loop infinito a cada 60 segundos
while True:
    extrair_trabalho()
    time.sleep(60)
