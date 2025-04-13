import os
import smtplib
import ssl
from flask import Flask, request, render_template, redirect, flash
from email.message import EmailMessage
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

app = Flask(__name__)
app.secret_key = 'segredo_super_secreto'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
SENHA_APP = os.getenv("SENHA_APP")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        assunto = request.form['assunto']
        corpo = request.form['mensagem']
        destinatarios = request.form['destinatarios'].split(',')

        msg = EmailMessage()
        msg['Subject'] = assunto
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = ', '.join(destinatarios)
        msg.set_content(corpo)
        msg.add_alternative(f"""\
        <html>
          <body>
            <h3>{assunto}</h3>
            <p>{corpo}</p>
          </body>
        </html>
        """, subtype='html')

        arquivo = request.files.get('anexo')
        if arquivo and arquivo.filename != '':
            filename = secure_filename(arquivo.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            arquivo.save(filepath)
            with open(filepath, 'rb') as f:
                msg.add_attachment(f.read(), maintype='application',
                                   subtype='octet-stream', filename=filename)

        try:
            contexto = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp:
                smtp.login(EMAIL_REMETENTE, SENHA_APP)
                smtp.send_message(msg)
            flash('Email enviado com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao enviar email: {e}', 'danger')

        return redirect('/')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
