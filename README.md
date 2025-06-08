# 🔌 Plug Inteligente Controlado por Gestos

Projeto experimental que integra **visão computacional** com **IoT**, utilizando Python para controlar uma tomada inteligente com gestos da mão via webcam.

## ✨ Objetivo

Aprender na prática como conectar o mundo físico e digital, mesmo sem microcontroladores como Arduino ou ESP32. A ideia foi explorar uma automação doméstica usando apenas:

- Uma **tomada inteligente Tuya**
- Uma **webcam comum**
- **Visão computacional com MediaPipe**
- Integração via **Tuya API**

## 📷 Como funciona

- O sistema detecta sua mão pela webcam usando **MediaPipe**.
- Quando os **cinco dedos estão abertos**, a tomada é ligada.
- Quando a mão está **fechada (nenhum dedo aberto)**, a tomada é desligada.
- O controle é feito com base em reconhecimento de gestos estáveis nos últimos frames.

## 🧠 Tecnologias utilizadas

- 🐍 **Python**
- 🎥 **OpenCV** – captura de imagem em tempo real
- ✋ **MediaPipe (Hands)** – detecção de gestos com base em pontos das mãos
- ☁️ **Tuya OpenAPI** – automação da tomada inteligente
- 🔐 **dotenv** – para manter segredos da API seguros
- ⚙️ **Conda** – isolamento do ambiente, especialmente útil para evitar conflitos com o MediaPipe

## ⚠️ Observações

> ❗ O **MediaPipe** tem problemas de compatibilidade com versões do Python acima de 3.10 ou abaixo de 3.8. Por isso, é altamente recomendável usar o **Conda** para gerenciar o ambiente.


