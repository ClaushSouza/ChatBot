from cProfile import label
from cgitb import text
from tkinter import *
import tkinter as tk
from tokenize import Number
from webbrowser import get
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from tkinter import *
from tkinter import ttk


contatos = []
mensagens = []
imagens = []

msgError = "Digite uma mensagem valida"

def validacao():
    if len(InputNumber.get()) != 0:
        adicionarNumber()
    else:
        msgError


def adicionarNumber():
    contatos.append(InputNumber.get())
    InputNumber.delete(0,END)
    ListaContatos['text'] = ', '.join(contatos)
    print(contatos)
    print(len(InputNumber.get()))

def ApagarNumber():
    contatos.clear()
    ListaContatos['text'] = ''
    print(contatos)

def adicionarMensagem():
    mensagens.append(InputMensagem.get('1.0', 'end-1c'))
    print(mensagens)

def ApagarMensagem():
    mensagens.clear()
    print(mensagens)

def adicionarFoto():
    imagem = filedialog.askopenfilename(initialdir='/', title="Select a File", filetypes=(
        ("Image files", ["*jpg*", "*png*", "*jpeg*"]), ("all files", "*.*")))
    imagens.append(imagem)
    print(imagens)

def ApagarFoto():
    imagens.clear()
    print(imagens)


def enviar():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://web.whatsapp.com/')  # abre o site Whatsapp Web
    time.sleep(30)  # da um sleep de 15 segundos, tempo para scannear o QRCODE

    # Funcao que pesquisa o Contato/Grupo

    def buscar_contato(contato):
        campo_pesquisa = driver.find_element(
            By.XPATH, '//div[contains(@class,"copyable-text selectable-text")]')
        time.sleep(0.1)
        campo_pesquisa.click()
        campo_pesquisa.send_keys(contato)
        campo_pesquisa.send_keys(Keys.ENTER)

    # Funcao que envia a mensagem
    def enviar_mensagem(mensagens):
        for mensagem in mensagens:
            mensageFormat = mensagem.split("\n")
            campo_mensagem = driver.find_element(
                By.XPATH, '//p[contains(@class,"selectable-text copyable-text")]')
            campo_mensagem.click()
            time.sleep(1)

            for msg in mensageFormat:
                campo_mensagem.send_keys(msg)
                campo_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)
        
            campo_mensagem.send_keys(Keys.ENTER)
            time.sleep(1)



    # Funcao que envia midia como mensagem

    def enviar_midia(imagens):
        driver.find_element(By.CSS_SELECTOR, "span[data-icon='clip']").click()
        attach = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        attach.send_keys(imagens)
        time.sleep(2)
        send = driver.find_element(
            By.XPATH, '//div[contains(@class, "_165_h _2HL9j")]')
        send.click()

    # Percorre todos os contatos/Grupos e envia as mensagens
    for contato in contatos:
        buscar_contato(contato)
        enviar_mensagem(mensagens)
        enviar_midia(imagens)
        time.sleep(2)


app = Tk()
app.title("ChatBot")
app.geometry("700x700")
app.configure(background="#fff") #CONFIGURAÇÃO DE COR DO FUNDO

LabelNumber = Label(app, text="Digite um contato/grupo: ").place(x=50,y=50,width=150,height=30)
InputNumber = tk.Entry(app)
InputNumber.place(x= 200, y=50, width=160, height=25)

ListaContatos = Label(app, text='')
ListaContatos.place(x= 200, y=100)
botaoNumber = Button(app, text='Adicionar Numero', command=validacao)
botaoNumber.place(x=380, y=50, height=30)
botaoApagar = Button(app, text="Remover contato", command=ApagarNumber)
botaoApagar.place(x=500, y=50, height=30)

LabelMensagem = Label(app, text='Digite uma Mensagem:').place(x=50,y=100,width=150,height=30)
InputMensagem = tk.Text(app)
InputMensagem.place(x=50, y=150, width=600, height=300)
botaoMensagem = Button(app, text='Adicionar Mensagem',
                       command=adicionarMensagem)
botaoMensagem.place(x=50, y=470, height=30)
botaoApagarMsg = Button(app, text="Remover Mensagem", command=ApagarMensagem)
botaoApagarMsg.place(x=180, y=470, height=30)


botaoImagem = Button(app, text='Adicionar Foto', command=adicionarFoto)
botaoImagem.place(x=50, y=510, height=30)
botaoApagarFoto = Button(app, text="Remover Foto", command=ApagarMensagem)
botaoApagarFoto.place(x=145, y=510, height=30)

botaoEnviar = Button(app, text='Enviar', command=enviar)
botaoEnviar.place(x=50, y=550, height=30, )

app.mainloop()