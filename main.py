from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import requests

TOKEN = '8183523093:AAGQHpn1VEsUzeD_rZrbe8AdX0nOPvpHYbY'
titulo_projeto_antigo = ''

def envia_trabalho_workana_telegram(token: str, titulo: str, descricao: str, link: str):
    TOKEN = token
    chat_id = '1837162112'
    mensagem = f'{titulo}\n{descricao}\n{link}'

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': mensagem
    }

    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print('Projeto enviado com sucesso!')
    
    else:
        print('Erro ao tentar enviar a mensagem para o telegram!')


def extrai_trabalhos(url: str):
    global TOKEN
    global titulo_projeto_antigo
    
    # Instala o driver do navegador Chrome
    service = Service(ChromeDriverManager().install())

    # Configura as opções do navegador
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    # Inicia o navegador Chrome
    navegador = webdriver.Chrome(service=service, options=options)

    # Entra no site
    navegador.get(url)

    # Espera implicita de 10 segundos
    navegador.implicitly_wait(10)

    # Aceita todos cookies
    cookies = navegador.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')
    cookies.click()

    # Espera 5 segundos
    time.sleep(5)

    # Fecha campo de login ou cadastro
    fecha_cadastro = navegador.find_element(By.XPATH, '//button[@class="close"]')
    fecha_cadastro.click()

    # Espera 5 segundos
    time.sleep(5)

    # Rolar pagina até o final
    navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Espera 2 segundos
    time.sleep(2)

    # Extrai projetos da workana
    container_projetos = navegador.find_element(By.XPATH, '//div[@id="projects"]')
    projetos = container_projetos.find_element(By.XPATH, './/div[@class="project-item js-project"]')
    
    titulo_projeto_atual = projetos.find_element(By.XPATH, './/div/h2').text
    descricao_projeto = projetos.find_element(By.XPATH, './/div/div/div/p/span').text
    link_projeto = projetos.find_element(By.XPATH, './/div/h2/span/a').get_attribute('href')

    print('Titulo Atual:', titulo_projeto_atual)

    if titulo_projeto_antigo != titulo_projeto_atual:
        titulo_projeto_antigo = titulo_projeto_atual
        print('Titulo Antigo:', titulo_projeto_antigo)

        envia_trabalho_workana_telegram(
            token=TOKEN,
            titulo=titulo_projeto_atual,
            descricao=descricao_projeto,
            link=link_projeto
        )

    else:
        print('Nenhum projeto recente! Procurando novamente.')

    navegador.close()

url = 'https://www.workana.com/jobs?language=pt&publication=1d&skills=python'

while True:
    extrai_trabalhos(url=url)
    time.sleep(5)
