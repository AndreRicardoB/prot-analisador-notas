import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tabula
import os 



# Variáveis globais para armazenar os dados dos arquivos CSV
arquivo1 = None
arquivo2 = None
nova_variavel1 = None
nova_variavel2 = None

def selecionar_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        converter_pdf_para_csv(file_path)

def converter_pdf_para_csv(pdf_path):
    tables = tabula.read_pdf(pdf_path, pages='all')
    
    if not tables:
        mensagem.config(text="Nenhuma tabela encontrada no PDF.")
        return


    df = tables[0]

    colunas_float = df.columns[2:9]

    for coluna in colunas_float:
            if df[coluna].dtype == 'object':
                df[coluna] = df[coluna].str.replace(',', '.', regex=True)
                df[coluna] = df[coluna].astype(float)
    

    
    df.fillna(0, inplace=True)
    csv_file_path = pdf_path.replace('.pdf', '_tabela_extraida.csv')
    df.to_csv(csv_file_path, index=False)

    mensagem_escolhida = (f'Tabela extraída e salva como: {csv_file_path}')
    texto_dados.delete (1.0,tk.END)
    texto_dados.insert(tk.END, mensagem_escolhida)



# Função para abrir um arquivo CSV e armazenar os dados na variável correspondente
def abrir_arquivo1():
    global arquivo1
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        arquivo1 = pd.read_csv(file_path)
        arquivo1_label.config(text="Disciplina 1: " + os.path.basename(file_path))

def abrir_arquivo2():
    global arquivo2
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        arquivo2 = pd.read_csv(file_path)
        arquivo2_label.config(text="Disciplina 2: " + os.path.basename(file_path))

# Função para imprimir os dados

# Função para imprimir os dados
def imprimir_dados():
    global arquivo1, arquivo2, nova_variavel1, nova_variavel2, texto_dados
    if arquivo1 is not None and arquivo2 is not None:
        # Lista de colunas desejadas
        colunas_desejadas = ["AB1", "AB2", "RA", "PF", "MF", "FALTAS"]

        # Criando novas variáveis com as colunas desejadas
        nova_variavel1 = arquivo1[colunas_desejadas]
        nova_variavel2 = arquivo2[colunas_desejadas]

        # Limpando o widget de texto antes de adicionar novos dados
        texto_dados.delete(1.0, tk.END)


        # Adicione os dados ao widget de texto
        texto_dados.insert(tk.END, "Arquivo 1:\n")
        texto_dados.insert(tk.END, arquivo1.to_string(index=False))
        texto_dados.insert(tk.END, "\n\nArquivo 2:\n")
        texto_dados.insert(tk.END, arquivo2.to_string(index=False))
    else:
        texto_dados.delete(1.0, tk.END)  # Limpe o widget de texto
        texto_dados.insert(tk.END, "Por favor, selecione ambos os arquivos CSV antes de imprimir.")


# Função para criar e exibir o gráfico de barras comparando médias
def criar_grafico():
    global nova_variavel1, nova_variavel2
    if nova_variavel1 is not None and nova_variavel2 is not None:
        # Calcule as médias das colunas em ambas as variáveis
        media_variavel1 = nova_variavel1.mean()
        media_variavel2 = nova_variavel2.mean()

        # Definindo a largura das barras e a posição das barras
        largura_barra = 0.35
        x = range(len(media_variavel1))

        # Crie um gráfico de barras comparando as médias lado a lado
        plt.figure(figsize=(10, 6))
        plt.bar(x, media_variavel1, width=largura_barra, label="Disciplina 1", alpha=0.7)
        plt.bar([i + largura_barra for i in x], media_variavel2, width=largura_barra, label="Disciplina 2", alpha=0.7)
        plt.xlabel("Colunas")
        plt.ylabel("Média dos Valores")
        plt.title("Comparação de Médias entre Disciplina 1 e Disciplina 2")
        plt.xticks([i + largura_barra / 2 for i in x], media_variavel1.index)
        plt.legend()
        plt.show()
    else:
        texto_dados.delete(1.0, tk.END)
        texto_dados.insert(tk.END, "Por favor, selecione ambos os arquivos CSV antes de criar o gráfico.")


# Função para criar e exibir o gráfico de dispersão com o cálculo do desvio padrão
def criar_grafico_dispersao():
    '''    global nova_variavel1, nova_variavel2'''
    if nova_variavel1 is not None and nova_variavel2 is not None:
        plt.figure(figsize=(12, 5))  # Ajuste o tamanho da figura conforme necessário


        escolha_do_usuario = variavel_escolhida.get()
        variavel1 = nova_variavel1[escolha_do_usuario]
        variavel2 = nova_variavel2[escolha_do_usuario]
        variavel_string = str(escolha_do_usuario)
        variavel_scatter1 = list(range(len(variavel1)))
        variavel_scatter2 = list(range(len(variavel2))) 

        # Primeiro gráfico
        plt.subplot(1, 2, 1)
        plt.scatter(variavel_scatter1, variavel1)
        plt.title('Dispersão de Disciplina 1')
        plt.xlabel('Alunos')
        plt.ylabel(f'Dispersão em {variavel_string}')

        # Segundo gráfico
        plt.subplot(1, 2, 2)
        plt.scatter(variavel_scatter2, variavel2)
        plt.title('Dispersão de Disciplina 2')
        plt.xlabel('Alunos')
        plt.ylabel(f'Dispersão em {variavel_string}')

    
        plt.show()
    else:
        texto_dados.delete(1.0, tk.END)
        texto_dados.insert(tk.END, "Por favor, selecione ambos os arquivos CSV antes de criar o gráfico.")


# Criando a janela
root = tk.Tk()
root.title("Protótipo comparador de notas")

# Botões para selecionar os arquivos CSV
selecionar_arquivo1_button = tk.Button(root, text="Selecionar Arquivo CSV 1", command=abrir_arquivo1)
selecionar_arquivo1_button.grid(column=1, row=0)

selecionar_arquivo2_button = tk.Button(root, text="Selecionar Arquivo CSV 2", command=abrir_arquivo2)
selecionar_arquivo2_button.grid(column=4, row=0)

# Botão para imprimir os dados
imprimir_dados_button = tk.Button(root, text="Imprimir Dados", command=imprimir_dados)
imprimir_dados_button.grid(column=3, row=2)

# Botão para criar e exibir o gráfico de barras
criar_grafico_button = tk.Button(root, text="Criar Gráfico de Barras", command=criar_grafico)
criar_grafico_button.grid(column=3, row=3)


# Botão para criar e exibir o gráfico de dispersão
criar_dispersao_button = tk.Button(root, text="Criar Gráfico de Dispersão", command=criar_grafico_dispersao)
criar_dispersao_button.grid(column=3,row=4, pady=5)

# Criar rótulos para exibir o nome dos arquivos
arquivo1_label = tk.Label(root, text="")
arquivo1_label.grid(column=1, row=1)

arquivo2_label = tk.Label(root, text="")
arquivo2_label.grid(column=4, row=1)

variaveis_disponiveis = ['AB1', 'AB2', 'RA', 'PF', 'MF', 'FALTAS']
variavel_escolhida = tk.StringVar() 
variavel_escolhida.set(variaveis_disponiveis[0])
variavel_combo = tk.OptionMenu(root, variavel_escolhida, *variaveis_disponiveis)
variavel_combo.grid(column=3, row=5 )


# Crie um widget de texto para exibir os dados
texto_dados = tk.Text(root, height=25, width=100)
texto_dados.grid(column=1, row=6, columnspan=5)

# Definindo o programa pra abrir maximizado
largura_tela = 800
altura_tela = 1040
#largura_tela = root.winfo_screenwidth()
#altura_tela = root.winfo_screenheight()
root.geometry(f"{largura_tela}x{altura_tela}")

# Criando botão pra selecionar o pdf
btn_selecionar = tk.Button(root, text="Selecionar PDF", command=selecionar_pdf)
btn_selecionar.grid(column=4, row=4)

# Rótulo para exibir a mensagem de status
#mensagem = tk.Label(root, text="", fg="green")
#mensagem.grid(column=1, row=10)




# Iniciar a interface gráfica
root.mainloop()
