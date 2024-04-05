import os, yaml, base64, urllib.request
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from anticaptchaofficial.imagecaptcha import *


def openYML(arq, origin_path = os.getcwd()):
    '''
    função que abre o arquivo yml

    --------------------------------
    input: 
        arq: str, nome do arquivo
        origin_path: str, caminho do arquivo

    output:
        yml: dict, dicionário com o conteúdo do arquivo
    --------------------------------    
    '''
    yml = False
    # Abre o arquivo yml
    with open(f'{origin_path}\\{arq}', encoding = 'utf8') as yamlfile:
        # Tenta fazer o load do arquivo, se não conseguir, imprime o erro
        try:
            yml = yaml.safe_load(yamlfile)
        except yaml.YAMLError as exc:
            print(exc)

    return yml


def encontraCaixaSelect(driver, xpath):
    '''
    encontra caixa select, onde estao as opcoes de entidade para download
    
    --------------------------------
    input: 
        driver: webdriver, driver do navegador
        xpath: str, xpath do elemento select
    output:
        caixa_select: Select, elemento select    
    --------------------------------  
    '''
    # Espera o elemento carregar
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    # Encontra a caixa de select
    select_element = driver.find_element(By.XPATH, xpath)
    # Guarda o elemento select
    caixa_select = Select(select_element)

    return caixa_select


def quebraCaptcha(driver, key, xpath_image):
    '''
    função que quebra o captcha

    --------------------------------
    input: 
        driver: webdriver, driver do navegador
        key: str, chave do anticaptcha
        xpath_image: str, xpath da imagem do captcha
    output:
        captcha_text: str, texto do captcha
    --------------------------------
    '''
    # Encontrando a imagem do captcha
    img = driver.find_element(By.XPATH, xpath_image)
    # Pegando a url da imagem
    img_url = img.get_attribute('src')
    # Convertendo a url em base64
    img_base64 = base64.b64encode(urllib.request.urlopen(img_url).read())
    
    # Criando um arquivo temporario com a imagem
    with open("tmp.image", "wb") as fh:
        fh.write(base64.urlsafe_b64decode(img_base64))
    
    # Anticaptcha
    solver = imagecaptcha()
    # Printando processo
    solver.set_verbose(1)
    # Chave que contém crédito para resolver o captcha 
    solver.set_key(key)
    # Respondendo captcha
    captcha_text = solver.solve_and_return_solution('tmp.image')
    # Printa caso consiga resolver o captcha, se não, mostra o erro 
    if captcha_text != 0:
        print ("captcha text: "+captcha_text)
    else:
        print ("task finished with error "+solver.error_code)

    return captcha_text
