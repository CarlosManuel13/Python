import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import sys
import os

# Configuración cuenta de Gmail
smtp_server = "smtp.gmail.com"
smtp_port = 587
email_from = "[cuenta correo]"
email_password = "[clave app/ contraseña]"

# Determinar si se está ejecutando como script o como ejecutable
if getattr(sys, 'frozen', False):
    # Si está empaquetado con PyInstaller, usa el directorio del .exe
    base_path = Path(sys.executable).parent
else:
    # Si se ejecuta como script normal, usa el directorio del script
    base_path = Path(__file__).parent

# Definir la ruta del archivo CSV
csv_file = base_path / "microsoft_accounts.csv"  # Ajusta el nombre si es "office_usuarios_enviar.csv"

# Verificar que el archivo existe
if not csv_file.exists():
    print(f"Error: No se encontró el archivo '{csv_file.name}' en la misma carpeta que este programa.")
    input("Presiona Enter para cerrar...")
    exit()

# Leer el archivo CSV
df = pd.read_csv(csv_file)

# Función para enviar un correo
def enviar_correo(destinatario, dato1, dato2):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Credenciales de Office"
    msg["From"] = email_from
    msg["To"] = destinatario

    plantilla = f"""
                        <!DOCTYPE html>
                        <html lang="es">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Credenciales de Acceso</title>
                            <style>
                                body {{
                                    margin: 0;
                                    padding: 0;
                                    font-family: Arial, Helvetica, sans-serif;
                                    background-color: #f4f4f4;
                                    color: #333;
                                }}
                                .container {{
                                    width: 100%;
                                    max-width: 600px;
                                    margin: 0 auto;
                                    background-color: #ffffff;
                                    border-radius: 8px;
                                    overflow: hidden;
                                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                                }}
                                .header {{
                                    background-color: #007bff;
                                    color: #ffffff;
                                    padding: 20px;
                                    text-align: center;
                                }}
                                .content {{
                                    padding: 20px;
                                    text-align: center;
                                }}
                                .credentials {{
                                    background-color: #f9f9f9;
                                    padding: 15px;
                                    border: 1px solid #ddd;
                                    border-radius: 5px;
                                    text-align: left;
                                    margin: 20px auto;
                                    max-width: 400px;
                                }}
                                .credentials p {{
                                    margin: 10px 0;
                                }}
                                .steps {{
                                    text-align: left;
                                    max-width: 400px;
                                    margin: 20px auto;
                                }}
                                .steps ol {{
                                    padding-left: 20px;
                                }}
                                @media only screen and (max-width: 600px) {{
                                    .container {{
                                        width: 100%;
                                    }}
                                    .credentials, .steps {{
                                        max-width: 100%;
                                    }}
                                }}
                            </style>
                        </head>
                        <body>
                            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #f4f4f4;">
                                <tr>
                                    <td align="center">
                                        <div class="container">
                                            <div class="header">
                                                <h1 style="margin: 0; font-size: 24px;">Tus Credenciales de Acceso</h1>
                                            </div>
                                            <div class="content">
                                                <p>Hola [Nombre del Usuario],</p>
                                                <p>A continuación, te enviamos tus credenciales para acceder a la Suite de Office de Microsoft. Por favor, guárdalas en un lugar seguro.</p>
                                                <div class="credentials">
                                                    <p><strong>Usuario:</strong> {dato1}</p>
                                                    <p><strong>Contraseña:</strong> {dato2}</p>
                                                </div>
                                                <p>Sigue estos pasos para configurar tu acceso:</p>
                                                <div class="steps">
                                                    <ol>
                                                        <li>Accede a cualquier aplicación de Microsoft Office (Word, Excel, Outlook…).</li>
                                                        <li>Inicia sesión con tu usuario de Office.</li>
                                                        <li>Te solicitará introducir un número de teléfono y/o vincular a una aplicación móvil.</li>
                                                        <li>Tras la verificación en 2 pasos, se generará un código de aplicación. Guarda este código en un lugar seguro.</li>
                                                    </ol>
                                                </div>
                                                <p>Si necesitas ayuda, no dudes en contactarnos a <a href="mailto:it@nfq.es">it@nfq.es</a>.</p>
                                            </div>
                                        </div>
                                    </td>
                                </tr>
                            </table>
                        </body>
                        </html>
                        """

    parte_html = MIMEText(plantilla, "html")
    msg.attach(parte_html)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_from, email_password)
        server.sendmail(email_from, destinatario, msg.as_string())
        server.quit()
        print(f"Correo enviado a {destinatario}")
    except Exception as e:
        print(f"Error al enviar a {destinatario}: {str(e)}")

# Iterar sobre las filas del CSV
print("Iniciando envío de correos...")
for index, row in df.iterrows():
    email_destinatario = row[6]  # Columna G
    office_user = row[7]         # Columna H
    office_password = row[8]     # Columna I

    if pd.notna(email_destinatario):
        enviar_correo(email_destinatario, office_user, office_password)
    else:
        print(f"Fila {index + 1}: Correo vacío, omitiendo...")

print("Proceso terminado")
input("Presiona Enter para cerrar...")
