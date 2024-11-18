from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep
from typing import Dict
from .src.domain.models.aacc import Aacc
from .src.domain.models.aacc_para_avaliacao import AaccParaAvaliacao
from .src.data.use_cases.aacc.register_aacc import AaccRegister
from datetime import date, datetime
from .src.infra.db.repositories.aacc_repository import AaccRepository
from datetime import datetime

def scrapper_retorno(aac: Aacc, aac_avaliação: AaccParaAvaliacao):

        print("Webscrapping sendo executado...")
        options = Options()
        # options.add_argument("--headless")


        download_directory = "/home/lucas/Desktop/projetos/IC/hub_ferramentas_si/hub_ferramentas_SI/ferramentas/aacc_app/comprovantes_aac"

        options.set_preference('browser.download.folderList', 2)
        options.set_preference('browser.download.dir', download_directory)
        options.set_preference('browser.download.manager.showWhenStarting', False)
        options.set_preference('browser.helperApps.neverAsk.saveToDisk','text/plain,application/pdf')
        options.set_preference("pdfjs.disabled", True)

        navegador = webdriver.Firefox(options=options)

        link = "https://uspdigital.usp.br/jupiterweb/webLogin.jsp"

        navegador.get(url=link)
        sleep(1)


        #login do jupiter
        inputUsuario = navegador.find_element(by=By.NAME, value="codpes")
        inputUsuario.send_keys("1364328")
        sleep(1)

        inputSenha = navegador.find_element(by=By.NAME, value="senusu")
        inputSenha.send_keys("Shazam_12!")
        sleep(1)

        botaoEntrar = navegador.find_element(by=By.NAME, value="Submit")
        botaoEntrar.click()
        sleep(1)

        botao_trocar_perfil = navegador.find_element(by=By.XPATH, value='//*[@id="listMenuRoot2"]/li[8]/a')
        botao_trocar_perfil.click()
        sleep(1)

        botao_coordenador = navegador.find_element(by=By.XPATH, value='//*[@id="layout_conteudo"]/a')
        botao_coordenador.click()
        sleep(2)

        botao_aluno = navegador.find_element(by=By.XPATH, value='//*[@id="listMenuRoot2"]/li[2]/a')
        botao_aluno.click()
        sleep(2)

        botao_creditos = navegador.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/ul/li[2]/table/tbody/tr/td/font/a[1]')
        botao_creditos.click()
        sleep(2)

        botao_requerimentos = navegador.find_element(by=By.XPATH, value='//*[@id="layout_conteudo"]/table[1]/tbody/tr/td/ul/li[2]/a')
        botao_requerimentos.click()
        sleep(2)

        botao_aac = navegador.find_element(by=By.XPATH, value='//*[@id="layout_conteudo"]/ul/li/a')
        botao_aac.click()
        sleep(2)

        botao_aac_coordenador = navegador.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/div[3]/table/tbody/tr/td/div/div[1]/div/form/div[4]/select/option[2]")
        botao_aac_coordenador.click()
        sleep(2)

        botao_buscar = navegador.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/div[3]/table/tbody/tr/td/div/div[1]/div/form/input[1]")
        botao_buscar.click()
        sleep(3)

        # Locate the table by its ID
        table = navegador.find_element(By.ID, 'retorno')

        # Extract headers (if any)
        headers = []
        header_row = table.find_element(By.TAG_NAME, 'tr')
        for th in header_row.find_elements(By.TAG_NAME, 'th'):
            headers.append(th.text.strip())

        for tr in table.find_elements(By.TAG_NAME, 'tr')[1:]:  # Skip the header row if headers exist
            cells = tr.find_elements(By.TAG_NAME, 'td')
            nro_usp = cells[0].get_attribute('innerText')
            if nro_usp == aac.aluno:
                cells[0].click()
                sleep(2)
                botao_parecer = navegador.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div[3]/table/tbody/tr/td/div/div[2]/table[2]/tbody/tr/td/div/div[5]/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/div')
                botao_parecer.click()

                titulo = navegador.find_element(by=By.XPATH, value='/html/body/div[10]/div[2]/form/table[1]/tbody/tr[3]/td[2]/span').get_attribute("innerText")
                inicio = navegador.find_element(by=By.XPATH, value='/html/body/div[10]/div[2]/form/table[1]/tbody/tr[4]/td[2]/span').get_attribute("innerText")
                fim = navegador.find_element(by=By.XPATH, value='/html/body/div[10]/div[2]/form/table[1]/tbody/tr[4]/td[4]/span').get_attribute("innerText")

                aux_inicio = aac.inicio
                aux_fim = aac.fim

                if aux_inicio is not None:
                    if isinstance(aux_inicio, str):
                        try:
                            aux_inicio = datetime.strptime(aux_inicio, "%Y-%m-%d")
                        except ValueError:
                            pass  # ou trate o erro de conversão de acordo com suas necessidades
                    aux_inicio = aux_inicio.strftime("%d/%m/%Y")

                if aux_fim is not None:
                    if isinstance(aux_fim, str):
                        try:
                            aux_fim = datetime.strptime(aux_fim, "%Y-%m-%d")
                        except ValueError:
                            pass  # ou trate o erro de conversão de acordo com suas necessidades
                    aux_fim = aux_fim.strftime("%d/%m/%Y")


                if inicio == "": inicio = None
                if fim == "": fim = None

                if titulo == aac.titulo and inicio == aux_inicio and fim == aux_fim:
                    #completa com o parecer
                    if aac_avaliação.status == 1:
                         #foi deferida
                         deferido = navegador.find_element(by=By.XPATH, value='//*[@id="starstpce"]/option[4]')
                         deferido.click()
                    elif aac_avaliação.status == 2:
                         indeferido = navegador.find_element(by=By.XPATH, value='/html/body/div[10]/div[2]/form/table[2]/tbody/tr[1]/td[2]/select/option[5]')
                         indeferido.click()

                    sleep(1)
                    carga_aprovada = navegador.find_element(by=By.XPATH, value='/html/body/div[10]/div[2]/form/table[2]/tbody/tr[2]/td[2]/input')
                    carga_aprovada.send_keys(aac_avaliação.carga_aprovada)

                    sleep(1)
                    parecer = navegador.find_element(by=By.XPATH, value='/html/body/div[10]/div[2]/form/table[2]/tbody/tr[3]/td[2]/textarea')
                    parecer.send_keys(aac_avaliação.comentarios)

                    sleep(1)
                    parecerista = navegador.find_element(by=By.XPATH, value='/html/body/div[10]/div[2]/form/table[2]/tbody/tr[4]/td[2]/input')
                    parecerista.send_keys("1364328")

                    sleep(1)
                    data = navegador.find_element(by=By.XPATH, value='/html/body/div[10]/div[2]/form/table[2]/tbody/tr[5]/td[2]/input')
                    data.send_keys(f"{date.today().strftime('%d/%m/%Y')}")

                    sleep(10)

                    break

                else: 
                     
                    fechar = navegador.find_element(by=By.XPATH, value='/html/body/div[10]/div[1]/a/span')
                    fechar.click()
                    sleep(1)

        
        navegador.quit()

        print("Webscrapping finalizado!")
