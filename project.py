from selenium import webdriver
from time import sleep
from func import *


# Abrindo driver
driver = webdriver.Chrome()
# Abrindo arquivo .yml
arquivo_yml = openYML('geral.yml')

# Acessado o site indicado 
url = arquivo_yml['url']
driver.get(url)

# Encontrando a caixa de seleção
xpath_caixa_select = arquivo_yml['xpaths']['caixa_select']
caixa_select = encontraCaixaSelect(driver, xpath_caixa_select)
sleep(2)

# Clicando na primeira opção da caixa de seleção (index 1 pois a primeira opção é o cabeçalho da caixa de seleção)
caixa_select.select_by_index(1)

# Resposta do captcha
xpath_image = arquivo_yml['xpaths']['captcha_img']
anticaptcha_key = arquivo_yml['key']
captcha_text = quebraCaptcha(driver, anticaptcha_key, xpath_image)

# Encontrando a caixa de resposta para o captcha 
xpath_caixa_captcha = arquivo_yml['xpaths']['caixa_captcha']
caixa_captcha = driver.find_element(By.XPATH, xpath_caixa_captcha)

# Preenchendo a caixa de resposta do captcha
caixa_captcha.send_keys(captcha_text)
sleep(1)

# Clicando em "Abrir Relatório"r
xpath_btn = arquivo_yml['xpaths']['btn']
driver.find_element(By.XPATH, xpath_btn).click()
time.sleep(5)

