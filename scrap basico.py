import tkinter as tk
from tkinter import messagebox

import requests
from bs4 import BeautifulSoup

import pandas as pd
import os


# HEADERS DE NAVEGADOR
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
"Referer": "https://www.google.com/",
"Connection": "keep-alive"
}


def scraper_mercadolivre(url):

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Erro:", response.status_code)
        return [], [], []

    soup = BeautifulSoup(response.text, "html.parser")

    produtos = soup.select("div.poly-card")

    nomes = []
    precos = []
    links = []

    for produto in produtos:

        try:

            titulo = produto.select_one("a.poly-component__title")
            nome = titulo.text.strip()
            link = titulo["href"]

            preco = produto.select_one(".andes-money-amount__fraction").text.strip()

            nomes.append(nome)
            precos.append(preco)
            links.append(link)

        except:
            pass

    return nomes, precos, links


def buscar():

    url = entrada_url.get()

    if url == "":
        messagebox.showerror("Erro", "Digite uma URL")
        return

    if "mercadolivre" not in url:

        messagebox.showerror("Erro", "Esse app suporta apenas Mercado Livre")
        return

    nomes, precos, links = scraper_mercadolivre(url)

    if len(nomes) == 0:

        messagebox.showerror("Erro", "Nenhum produto encontrado")
        return

    dados = pd.DataFrame({
        "Produto": nomes,
        "Preço": precos,
        "Link": links
    })

    pasta = os.path.dirname(__file__)
    caminho = os.path.join(pasta, "produtos.xlsx")

    dados.to_excel(caminho, index=False)

    messagebox.showinfo(
        "Sucesso",
        f"{len(nomes)} produtos salvos em produtos.xlsx"
    )


# INTERFACE

janela = tk.Tk()
janela.title("Extrator Mercado Livre")
janela.geometry("420x220")


titulo = tk.Label(
    janela,
    text="Scraper de Produtos Mercado Livre",
    font=("Arial", 14)
)

titulo.pack(pady=10)


entrada_url = tk.Entry(
    janela,
    width=45
)

entrada_url.pack(pady=10)


botao = tk.Button(
    janela,
    text="Buscar produtos",
    command=buscar
)

botao.pack(pady=10)


janela.mainloop()