import pandas as pd

class Planilha():

    def __init__(self, arquivo):
        self.arquivo = pd.ExcelFile(rf"{arquivo}")

    def get_arquivo(self):
        return self.arquivo

    def get_arquivo_materia(self, materia):
        db = self.arquivo.parse(materia)
        db["Data de ingresso"] = db["Data de ingresso"].str.slice(0,4)
        return db
    


    
