import sys
import subprocess

subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

import os 
import PyPDF2
import re
import pandas as pd
import numpy as np

def main(): 

    dicionario_meses = {'Janeiro': 1, 'Fevereiro': 2, 'Marco': 3, 'Abril': 4, 'Maio': 5, 'Junho': 6, 'Julho': 7, 'Agosto': 8, 'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12}

    df_extracao = pd.DataFrame(columns=['Ano', 'Mes', 'Valor', 'Guia'])

    print('Iniciando a extração de dados dos PDFs...')

    for count, filename in enumerate(os.listdir("./Guias/")):

        pdf_file = open(f'./Guias/{filename}', 'rb')

        read_pdf = PyPDF2.PdfReader(pdf_file)
        texto = read_pdf.pages[0].extract_text()[:]
        texto = texto.replace('ç', 'c')

        mes = re.findall(r'[a-zA-Z]+\/', texto)[0][:-1]

        ano = re.findall(r'\/[0-9]+', texto)[0][1:]

        valor = re.findall(r'[0-9]+,[0-9]+CPF', texto)[0][:-3]
        valor = valor.replace(',', '.',)
        valor = float(valor)

        df_extracao.loc[count] = [ano, mes, valor, filename]

    print('')
    print('Finalizando a extração de dados dos PDFs...')
    df_extracao['Mes'] = df_extracao['Mes'].map(dicionario_meses)
    df_extracao.sort_values(by=['Ano', 'Mes'], inplace=True)
    df_extracao.reset_index(drop=True, inplace=True)
    print('Pronto! Veja como ficou:')
    print('')
    print(df_extracao.info())
    print('')
    print(df_extracao.head())
    print('')

    df_extracao.to_excel('planilha_fgts.xlsx', index=False)

    print(f"Valor total a ser pago: R$ {str(df_extracao['Valor'].sum())}")

if __name__ == '__main__': 
      
    main() 