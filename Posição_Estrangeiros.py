import pandas as pd
from bs4 import BeautifulSoup as bs
import requests as rq
import pyautogui
import time
import pyperclip

# buscar a posição dos entrangeiros
url = 'https://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-tipo-de-participante-ptBR.asp'
tai = pd.read_html(url)[0]

dados_compra =  float(tai.iloc[265,1])
dados_venda  =  float(tai.iloc[265,3])
soma = dados_compra - dados_venda
print("Resultado da posição dos estrangeiros",soma)
time.sleep(1)

# buscar variação dos indices
#vai começar
# opção 1 - abrir navegador novo e entrar no chrome
pyautogui.press("winleft")
time.sleep(3)
pyautogui.write("google chrome")
time.sleep(1)
pyautogui.press("enter")
time.sleep(5)
pyautogui.hotkey("ctrl" , "t")
link = "https://br.investing.com/indices/major-indices"
pyperclip.copy(link)
pyautogui.hotkey("ctrl","v")
time.sleep(1)
pyautogui.hotkey("Enter")
time.sleep(15)
pyautogui.hotkey("ctrl" , "f")
pyautogui.write("baixar dados")
time.sleep(1)
pyautogui.hotkey("ctrl" , "enter")
pyautogui.click(1354, 717, clicks=8)
time.sleep(2)
pyautogui.click(774, 491, clicks=1)
time.sleep(3)
pyautogui.click(1345, 697, clicks=1)
time.sleep(1)
# fechar o chrome
pyautogui.hotkey("alt", 'f4')
#soma da planilha
dados = pd.read_csv(r"C:/Users/nando/Downloads/Principais Índices Mundiais.csv")
resultado = dados['Variação'].sum() / 100   # soma do valor
print("Resultado Indices Mundiais",resultado)

#pegar os dados do us dollar
HEADERS = ({'user-agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
html_completo = rq.get("https://br.investing.com/currencies/us-dollar-index", headers=HEADERS)
html_formatado = bs(html_completo.content)
#print(html_formatado.prettify())
nome_dolar = html_formatado.find("h1", class_="float_lang_base_1 relativeAttr").text
porcentagem = html_formatado.find("div", class_="top bold inlineblock").text
dados_dolar = nome_dolar + porcentagem
print("Resultado Dollar Futuro",dados_dolar)

#################################################################################################################
# mostra o id do último grupo adicionado
def last_chat_id(token):
    try:
        url = "https://api.telegram.org/bot{}/getUpdates".format(token)
        response = rq.get(url)
        if response.status_code == 200:
            json_msg = response.json()
            for json_result in reversed(json_msg['result']):
                message_keys = json_result['message'].keys()
                if ('new_chat_member' in message_keys) or ('group_chat_created' in message_keys):
                    return json_result['message']['chat']['id']
            print('Nenhum grupo encontrado')
        else:
            print('A resposta falhou, código de status: {}'.format(response.status_code))
    except Exception as e:
        print("Erro no getUpdates:", e)

# enviar mensagens utilizando o bot para um chat específico
def send_message(token, chat_id, message):
    try:
        data = {"chat_id": chat_id, "text": msg}
        url = "https://api.telegram.org/bot{}/sendMessage".format(token)
        rq.post(url, data)
    except Exception as e:
        print("Erro no sendMessage:", e)

# token único utilizado para manipular o bot (não deve ser compartilhado)
# exemplo: '1413778757:AAFxmr611LssAHbZn1uqV_NKFsbwK3TT-wc'
token = '1942912563:AAHabBKdjmX07FHkHScn_H508hByMCJtH4w'

# id do chat que será enviado as mensagens
chat_id = last_chat_id(token)

print("Id do chat:", chat_id)

# exemplo de mensagem
msg = f"""
BOM DIA SEGUE A ANALISE DE HOJE!!

Resultado da posição dos estrangeiros, {soma}

Resultado Indices Mundiais, {resultado}

Resultado Dollar Futuro, {dados_dolar}

Calendário econômico
https://br.investing.com/economic-calendar/
Noticias Investing
https://br.investing.com/news/
Noticias Infomoney
https://www.infomoney.com.br/ultimas-noticias/

Bons Trades!!!
NLXCAPITAL_BOT
"""
# enviar a mensagem
send_message(token, chat_id, msg)


