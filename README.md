# Projeto IoT Sustentável: Substituindo Pilhas com Energia Renovável 🌞🔋

Este projeto apresenta uma solução sustentável para alimentar dispositivos IoT utilizando energia solar. A proposta é substituir o uso de pilhas e baterias convencionais, promovendo a utilização de energias renováveis e reduzindo o impacto ambiental.

## 🎯 Objetivos
1. **Sustentabilidade**: Substituir pilhas e baterias tradicionais por uma solução sustentável.
2. **Monitoramento inteligente**: Exibir dados em tempo real sobre o desempenho do painel solar.
3. **Análise climática**: Verificar as condições meteorológicas para o carregamento eficiente.

---

## ⚙️ Componentes Utilizados
- **Microcontrolador ESP32**: Para gerenciar a comunicação IoT e monitoramento dos sensores.
- **Painel Solar**: Para capturar a energia solar.
- **Bateria/Pilhas recarregáveis**: Armazenam a energia capturada.
- **MQTT**: Protocolo de comunicação para enviar os dados coletados do ESP32 para um servidor.
- **API de Clima**: Para verificar as condições climáticas locais.
- **Dashboard em Python**: Exibe informações sobre a tensão solar e condições climáticas.

---

## 🛠️ Configuração do Projeto

### 1. Montagem do Hardware
- Conecte o painel solar ao circuito de carregamento.
- Ligue o ESP32 ao sistema para monitorar a energia gerada e o estado da bateria.
- Certifique-se de que o circuito está devidamente protegido contra sobrecargas.

### 2. Configuração do MQTT
- Configure um servidor MQTT (local ou baseado na nuvem).
- Programe o ESP32 para enviar dados sobre tensão solar e status de carga para tópicos específicos do MQTT.

### 3. API de Clima
- Use uma API como OpenWeatherMap para obter informações meteorológicas.
- Configure no ESP32 para enviar os dados climáticos para o servidor MQTT.

### 4.🌦️ Integração com API de Clima
A API fornece dados como:

Condição climática atual: Ensolarado, nublado, etc.
Previsão de chuva: Para prevenir problemas de eficiência no painel.

### 5.🎥 Vídeo Demonstrativo
Confira o funcionamento completo do projeto no vídeo a seguir:

🔗 Link para o vídeo do projeto

https://www.youtube.com/watch?v=oEmdl7isbY0


# Dashboard e Monitoramento

Este projeto inclui um dashboard em Flask com integração de SocketIO, Chart.js e OpenWeatherMap para fornecer visualização em tempo real da tensão solar e informações climáticas. A interface exibe:

- **Gráfico de medição em formato de rosca (gauge)**: Mostra a porcentagem de tensão captada pelo painel solar.
- **Indicador de tensão**: Atualiza dinamicamente o valor da tensão recebida.
- **Consulta de condições climáticas**: O usuário pode inserir sua cidade para verificar se o clima está favorável para o uso eficiente do painel solar.

## 📋 Funcionalidades

### Monitoramento em Tempo Real
- Os dados recebidos via MQTT são enviados ao frontend utilizando SocketIO, garantindo atualizações dinâmicas sem necessidade de recarregar a página.

### Visualização de Dados
- Um gráfico de rosca dinâmico exibe a porcentagem da tensão captada pelo painel.

### Análise Climática
- Utiliza a API OpenWeatherMap para verificar as condições climáticas e determinar se estão favoráveis para carregamento.

## 📜 Requisitos
Certifique-se de instalar as dependências necessárias antes de executar o projeto:

```bash
from flask import Flask, render_template_string, request, jsonify
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import json
import requests
```

### 6. 👥Integrantes do Grupo

Ruan Melo, RM 557599

Rodrigo Jimenez, RM 558148

Pedro Josué, RM 554913



