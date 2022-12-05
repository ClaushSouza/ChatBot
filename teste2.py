from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import *
from webbrowser import get
from tkinter import filedialog
from tkinter import messagebox
import time
import tkinter.font as tkFont

contatos = []
mensagem = []
imagem = []

# Validação para não adicionar um contato vazio

def validarContato():
    if len(inputContato.get()) != 0:
        adicionarContato()
    else:
        messagebox.showerror("INVÁLIDO", "DIGITE UM CONTATO/GRUPO")

# Validação para não mandar uma mensagem vazia


def validarMesangem():
    if len(message.get('1.0', 'end-1c')) != 0:
        adicionarMensagem()
    else:
        messagebox.showerror("INVÁLIDO", "DIGITE UMA MENSAGEM")

# Validação para não entrar no site do WhatsApp Web, sem ter adicionado o contato e mensagem ou imagem


def validarEnviarMensagem():
    if len(contatos) != 0:
        if len(message.get('1.0', 'end-1c')) != 0:
            chat()
        elif len(imagem) != 0:
            chat()
        else:
            messagebox.showerror("INVÁLIDO", "Nenhuma mensagem adicionada")
    else:
        messagebox.showerror("INVÁLIDO", "Nenhum contato adicionado")


# Funcão que adiciona o contato no array "contatos"
def adicionarContato():
    contatos.append(inputContato.get())
    listContatos['text'] = ', '.join(contatos)
    inputContato.delete(0, END)
    print(contatos)


# Funcão que remove o contato no array "contatos"
def removerContato():
    contatos.clear()
    inputContato.delete(0, END)
    listContatos['text'] = ""
    print(contatos)

# Funcão que adiciona mensagem no array "mensagem"


def adicionarMensagem():
    mensagem.append(message.get('1.0', 'end-1c'))
    print(mensagem)

# Funcão que remove a mensagem no array "mensagem"


def removerMensagem():
    mensagem.clear()
    message.delete("1.0", "end")
    print(mensagem)

# Funcão que adiciona imagem no array "imagem"


def adicionarImagem():
    image = filedialog.askopenfilename(initialdir='/', title="Select a File", filetypes=(
        ("Image files", ["*jpg*", "*png*", "*jpeg*"]), ("all files", "*-*")))
    imagem.append(image)
    dirImagem['text'] = imagem
    print(imagem)

# Funcão que remove a imagem no array "imagem"


def removerImagem():
    imagem.clear()
    dirImagem['text'] = ""
    print(imagem)

# Função para deixar a janela no centro do monitor


def center(janela):
    janela.update_idletasks()
    width = janela.winfo_width()
    frm_width = janela.winfo_rootx() - janela.winfo_x()
    win_width = width + 2 * frm_width
    height = janela.winfo_height()
    titlebar_height = janela.winfo_rooty() - janela.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = janela.winfo_screenwidth() // 2 - win_width // 2
    y = janela.winfo_screenheight() // 2 - win_height // 2
    janela.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    janela.deiconify()


def chat():
    # Abre o Chrome
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://web.whatsapp.com/')  # Abre o site Whatsapp Web
    time.sleep(25)  # da um sleep de 25 segundos, tempo para scannear o QRCODE

    # Função que pesquisa o Contato/Grupo

    def buscar_contato(contato):
        campo_pesquisa = driver.find_element(
            By.XPATH, '//div[contains(@class,"copyable-text selectable-text")]')
        time.sleep(2)
        campo_pesquisa.click()
        campo_pesquisa.send_keys(contato)
        campo_pesquisa.send_keys(Keys.ENTER)

    # Função que envia a mensagem
    def enviar_mensagem(mensagem):
        for message in mensagem:
            mensagemFormat = message.split("\n")
            campo_mensagem = driver.find_element(
                By.XPATH, '//p[contains(@class,"selectable-text copyable-text")]')
            campo_mensagem.click()
            time.sleep(2)

            for msg in mensagemFormat:
                campo_mensagem.send_keys(msg)
                campo_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)

            campo_mensagem.send_keys(Keys.ENTER)
            time.sleep(2)

    # Função que envia midia como mensagem

    def enviar_midia(imagem):
        if len(imagem) != 0:
            for imagens in imagem:
                driver.find_element(
                    By.CSS_SELECTOR, "span[data-icon='clip']").click()
                attach = driver.find_element(
                    By.CSS_SELECTOR, "input[type='file']")
                attach.send_keys(imagens)
                time.sleep(2)
                send = driver.find_element(
                    By.XPATH, '//div[contains(@class, "_165_h _2HL9j")]')
                send.click()
                time.sleep(2)

    # Percorre todos os contatos/Grupos e envia as mensagens
    for contato in contatos:
        buscar_contato(contato)
        enviar_mensagem(mensagem)
        enviar_midia(imagem)
        time.sleep(2)


# Interface gráfica com TKINTER
janela = Tk()
janela.title("Chat Bot")  # TÍTULO
janela.geometry("800x900")  # TAMANHO E ALUTRA DA JANELA
janela.configure(background="#fff")  # CONFIGURAÇÃO DE COR DO FUNDO

# Para a janela ficar no centro do tela
center(janela)
janela.attributes('-alpha', 0.0)
center(janela)
janela.attributes('-alpha', 1.0)

# Não poder maximizar e nem minimizar a janela da interface gráfica
janela.resizable(width=False, height=False)


# Icones
lixeiraIcon = PhotoImage(file="image/lixeira.png")
pictureIcon = PhotoImage(file="image/picture.png")
contatoIcon = PhotoImage(file="image/contato.png")
messageIcon = PhotoImage(file="image/message.png")
sendIcon = PhotoImage(file="image/send.png")
exitIcon = PhotoImage(file="image/exit.png")


# Foto robô
foto = PhotoImage(file="image/bot.png")
foto.subsample(3, 3)
figura = Label(image=foto, background="#fff")
figura.place(x=320, y=0, width=150, height=150)

# Title
fontStyle = tkFont.Font(family="Lucida Grande", size=15)
title = Label(janela, text="Mensagens automática WhatsApp", font=fontStyle)
title.place(x=250, y=150)


labelContato = Label(janela, text="Digite um contato/grupo: ",
                     background="#fff").place(x=50, y=230, width=150, height=30)
inputContato = Entry(janela)
inputContato.place(x=200, y=230, width=160, height=25)

# Lista com os contato(a) a ser(em) enviado(s)
listContatos = Label(janela, text="", foreground="green")
listContatos.place(x=50, y=270)

# Botões de adicionar e remover contato
buttonAdd = Button(janela, text="  Adicionar contato",
                   command=validarContato, image=contatoIcon, compound=LEFT)
buttonAdd.place(x=380, y=230, height=30)
buttonClear = Button(janela, text="  Remover contato",
                     command=removerContato, image=lixeiraIcon, compound=LEFT)
buttonClear.place(x=520, y=230, height=30)


# Digitar mensagem a ser enviada
labelMessage = Label(janela, text="  Digite uma mensagem: ",
                     background="#fff").place(x=40, y=310, width=150, height=30)
message = Text(janela)
message.place(x=50, y=350, width=700, height=300)

# Botões de adicionar e remover mensagem
buttonAddMsg = Button(janela, text='  Adicionar mensagem', command=validarMesangem, image=messageIcon,
                      compound=LEFT)
buttonAddMsg.place(x=50, y=670, height=30)
buttonClearMsg = Button(janela, text='  Remover mensagem', command=removerMensagem, image=lixeiraIcon,
                        compound=LEFT)
buttonClearMsg.place(x=210, y=670, height=30)

# Botões de adicionar e remover imagem
buttonAddImg = Button(janela, text='  Adicionar imagem',
                      command=adicionarImagem, image=pictureIcon, compound=LEFT)
buttonAddImg.place(x=50, y=730, height=30)
buttonClearImg = Button(janela, text="  Remover imagem",
                        command=removerImagem, image=lixeiraIcon, compound=LEFT)
buttonClearImg.place(x=210, y=730, height=30)

# Texto com os arquivos permitidos
textArquivos = Label(
    janela, text="Arquivos suportados: JPG, PNG, JPEG", foreground="#0000FF")
textArquivos.place(x=360, y=730, height=30)

# Text com o diretório da imagem
dirImagem = Label(janela, text="")
dirImagem.place(x=50, y=780, height=30)


buttonExit = Button(janela, text='Exit   ',
                    command=janela.destroy, image=exitIcon, compound=RIGHT)
buttonExit.place(x=50, y=820, height=30, width=80)

# Botão de enviar mensagem
buttonSend = Button(janela, text='Enviar mensagem   ',
                    command=validarEnviarMensagem, image=sendIcon, compound=RIGHT)
buttonSend.place(x=630, y=820, height=30, width=150)

janela.mainloop()