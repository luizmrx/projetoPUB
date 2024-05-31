from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep
from typing import Dict
from .src.domain.models.aacc import Aacc
from .src.data.use_cases.aacc.register_aacc import AaccRegister
from datetime import date, datetime
from .src.infra.db.repositories.aacc_repository import AaccRepository

def scrapper():

        print("Webscrapping sendo executado...")
        options = Options()
        options.add_argument("--headless")


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
        sleep(2)

        # Locate the table by its ID
        table = navegador.find_element(By.ID, 'retorno')

        # Extract headers (if any)
        headers = []
        header_row = table.find_element(By.TAG_NAME, 'tr')
        for th in header_row.find_elements(By.TAG_NAME, 'th'):
            headers.append(th.text.strip())

        for tr in table.find_elements(By.TAG_NAME, 'tr')[1:]:  # Skip the header row if headers exist
            cells = tr.find_elements(By.TAG_NAME, 'td')
            nro_usp = "98989898"
            cells[0].click()
            sleep(1)
            botao_consultar = navegador.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div[3]/table/tbody/tr/td/div/div[2]/table[2]/tbody/tr/td/div/div[5]/div/table/tbody/tr/td[1]/table/tbody/tr/td[1]/div')
            botao_consultar.click()
            sleep(1)
            info = coletar_info(navegador)
            carregar_aacc(info, nro_usp)
        
        navegador.quit()

        print("Webscrapping finalizado!")

def coletar_info(navegador):
     
    texto_atividade = navegador.find_element(by=By.XPATH, value='//*[@id="atividadeModAlterar"]').get_attribute('innerText')

    texto_area = navegador.find_element(by=By.XPATH, value='/html/body/div[6]/div[2]/form/table/tbody/tr[2]/td[2]/select')
    area = texto_area.get_attribute('value')


    texto_ano_semestre = navegador.find_element(by=By.XPATH, value='//*[@id="periodoModAlterar"]')
    ano_semestre = texto_ano_semestre.get_attribute('innerText')

    texto_titulo = navegador.find_element(by=By.XPATH, value='/html/body/div[6]/div[2]/form/table/tbody/tr[4]/td[2]/input')
    titulo = texto_titulo.get_attribute('value')


    texto_inicio = navegador.find_element(by=By.XPATH, value='/html/body/div[6]/div[2]/form/table/tbody/tr[5]/td[2]/input')
    inicio = texto_inicio.get_attribute('value')


    texto_fim = navegador.find_element(by=By.XPATH, value='/html/body/div[6]/div[2]/form/table/tbody/tr[6]/td[2]/input')
    fim = texto_fim.get_attribute('value')


    texto_carga = navegador.find_element(by=By.XPATH, value='/html/body/div[6]/div[2]/form/table/tbody/tr[7]/td[2]/input')
    carga_horaria = texto_carga.get_attribute('value')


    texto_documento = navegador.find_element(by=By.XPATH, value='/html/body/div[6]/div[2]/form/table/tbody/tr[11]/td[2]/span/a')
    texto_documento.click()
    
    sleep(3)
    fechar_documento = navegador.find_element(by=By.XPATH, value='/html/body/div[14]/div[1]/a/span')
    fechar_documento.click()

    sleep(2)

    resposta = {
         "texto_atividade": texto_atividade,
         "area": area,
         "texto_ano_semestre": ano_semestre,
         "titulo": titulo,
         "inicio": inicio,
         "fim": fim,
         "carga_horaria": carga_horaria,
         "texto_documento": texto_documento
    }

    botao_fechar = navegador.find_element(by= By.XPATH, value='/html/body/div[6]/div[1]/a')
    botao_fechar.click()
    sleep(1)

    return resposta


def carregar_aacc(info: Dict, nro_usp: str) -> None:
     

    response = Aacc(
        id_aacc="teste",
        aluno= nro_usp,
        doc=info["texto_documento"],
        data_envio= date.today(),
        status=0,
        atividade=info["texto_atividade"],
        area = info["area"],
        ano_semestre=info["texto_ano_semestre"],
        titulo= info["titulo"],
        inicio= datetime.strptime(info["inicio"], "%d/%m/%Y").strftime("%Y-%m-%d"),
        fim=datetime.strptime(info["fim"], "%d/%m/%Y").strftime("%Y-%m-%d"),
        carga_horaria=info["carga_horaria"]
    )


    aacc_repository = AaccRepository()
    use_case = AaccRegister(aacc_repository=aacc_repository)

    use_case.register_aacc(response)
