import pandas as pd
from datetime import date

dados = pd.read_csv('Atendimento.csv')

local = "DOURADOS"
solicitante = "AGR"
atendimento = "A1 NÃO CONSTA"
certificado = "A1"
meta = "SIM"
resolvido = "SIM"
data = date.today().strftime("%d/%m/%Y")

condition = " Local == '{}' & Solicitante == '{}' & Atendimento == '{}' & Certificado == '{}' & Meta == '{}' & Resolvido == '{}' & Data == '{}'".format(local,solicitante,atendimento,certificado,meta,resolvido,data)
        
x = dados.query(condition)
dados["Local"][0] = "ze"
print(dados)