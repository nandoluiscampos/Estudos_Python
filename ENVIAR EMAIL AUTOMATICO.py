import smtplib
import email.message

def enviar_email():
    corpo_email = f"""
    <p>Bom Dia NandoLuis aqui é o Python!!</p>
    <p>Segue os dados da B3 e Mercados Mundiais</p>
    <p>{dados_ibov}</p>
    <p>Abs Python </p>
    """
    msg = email.message.Message()
    msg['Subject'] = "Email Automatico - Dados de Mercado"
    msg['From'] = 'nandoluisartdesejo@gmail.com'
    msg['To'] = 'cafecomtrocotrader@gmail.com'
    password = 'LuisC256'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')

    enviar_email()
    
