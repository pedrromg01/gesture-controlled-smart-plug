import cv2
import mediapipe as mp
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

# Inicializa a API Tuya
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

def ligar_tomada():
    openapi.post(f"/v1.0/iot-03/devices/{DEVICE_ID}/commands", {
        "commands": [{"code": "switch_1", "value": True}]
    })
    print("[INFO] Tomada LIGADA")

def desligar_tomada():
    openapi.post(f"/v1.0/iot-03/devices/{DEVICE_ID}/commands", {
        "commands": [{"code": "switch_1", "value": False}]
    })
    print("[INFO] Tomada DESLIGADA")

# =================== DETECÇÃO DE GESTO ===================
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Estado atual da tomada
estado_tomada = None  # None = desconhecido, True = ligada, False = desligada

# Histórico dos últimos gestos para estabilidade
historico_gestos = []

# Função para contar dedos abertos
def contar_dedos_abertos(hand_landmarks):
    dedos_abertos = 0
    tips = [4, 8, 12, 16, 20]  # Pontas do polegar, indicador, médio, anelar, mínimo
    
    # Polegar (eixo X pois é diferente dos outros dedos)
    if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0] - 1].x:
        dedos_abertos += 1
    
    # Demais dedos (eixo Y)
    for tip_id in tips[1:]:
        if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
            dedos_abertos += 1

    return dedos_abertos

# Inicia a câmera
cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("[ERRO] Não foi possível acessar a webcam.")
            break

        # Converte imagem para RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        gesto_atual = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                dedos_abertos = contar_dedos_abertos(hand_landmarks)

                if dedos_abertos == 5:
                    gesto_atual = "aberta"
                elif dedos_abertos == 0:
                    gesto_atual = "fechada"
                else:
                    gesto_atual = "neutro"  # não muda o estado

                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        else:
            gesto_atual = "neutro"

        # Atualiza histórico dos gestos (mantém máximo 5)
        historico_gestos.append(gesto_atual)
        if len(historico_gestos) > 5:
            historico_gestos.pop(0)

        # Contagem dos gestos confiáveis
        if historico_gestos.count("aberta") >= 4 and estado_tomada != True:
            ligar_tomada()
            estado_tomada = True
        elif historico_gestos.count("fechada") >= 4 and estado_tomada != False:
            desligar_tomada()
            estado_tomada = False
        # Se neutro ou inconstante, não faz nada (mantém estado atual)

        cv2.imshow('Controle de Tomada Tuya - Pressione Q para sair', image)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
