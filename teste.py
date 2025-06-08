from tuya_connector import TuyaOpenAPI
from dotenv import load_dotenv
import os
import time

# Carrega as variáveis do arquivo .env
load_dotenv()

# Pega as variáveis de ambiente
ACCESS_ID = os.getenv("ACCESS_ID")
ACCESS_KEY = os.getenv("ACCESS_KEY")
API_ENDPOINT = os.getenv("API_ENDPOINT")
DEVICE_ID = os.getenv("DEVICE_ID")

# Inicializa e conecta à API
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()  # Obtém o access_token automaticamente

# Mostra informações do token (útil para debug)
print("\n Token de Acesso:")
print(openapi.token_info)

# Ligar a tomada
command_on = {
    "commands": [
        {"code": "switch_1", "value": True}
    ]
}
response_on = openapi.post(f"/v1.0/devices/{DEVICE_ID}/commands", command_on)
print("\n Resposta ao LIGAR a tomada:")
print(response_on)

# Espera antes de desligar
time.sleep(5)

# Desligar a tomada
command_off = {
    "commands": [
        {"code": "switch_1", "value": False}
    ]
}
response_off = openapi.post(f"/v1.0/devices/{DEVICE_ID}/commands", command_off)
print("\n🔌 Resposta ao DESLIGAR a tomada:")
print(response_off)
