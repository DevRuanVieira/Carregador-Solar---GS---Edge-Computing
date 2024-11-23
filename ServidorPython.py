from flask import Flask, render_template_string, request, jsonify
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import json
import requests

# Constantes para MQTT
MQTT_BROKER = "23.22.163.175"  # Substitua pelo endereço do seu broker
MQTT_TOPICS = ["/TEF/device075/attrs/p", "/TEF/device076/attrs/p"]  # Adicione tópicos se necessário

# API Key para o OpenWeatherMap (Substitua pela sua própria chave)
API_KEY = "3582bab7ae92c5aa865d5abefe95f99f"

# Inicializa o aplicativo Flask e o SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Variável global para armazenar o último valor do potenciômetro
ultimo_valor = {}

# Funções de callback do MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado com código de resultado " + str(rc))
    # Inscreve-se em vários tópicos
    for topic in MQTT_TOPICS:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    global ultimo_valor
    try:
        payload = json.loads(msg.payload)
        # Usa o tópico como chave para armazenar valores
        ultimo_valor[msg.topic] = payload
        # Emite dados para o cliente
        socketio.emit('novo_dado', {'topico': msg.topic, 'valor': payload})
        print(f"Mensagem recebida no tópico {msg.topic}: {payload}")  # Saída de depuração
    except json.JSONDecodeError:
        print("Falha ao decodificar JSON")

# Configura o cliente MQTT e conecta
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, 1883, 60)
client.loop_start()  # Inicia o loop MQTT em uma thread separada

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Visualizador de Dados do Potenciômetro</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
            <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                canvas {
                    max-width: 400px;
                    margin: auto;
                }
                #valor-potenciometro {
                    font-size: 48px; /* Tamanho da fonte aumentado */
                    font-weight: bold; /* Texto em negrito */
                }
                #clima-info {
                    font-size: 24px;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="mt-5">Tensão Painel Solar</h1>
                <canvas id="gauge" width="400" height="400"></canvas>
                <div id="valor-potenciometro" class="mt-3">
                    Aguardando dados...
                </div>

                <div class="mt-5">
                    <label for="cidade">Digite o nome da sua cidade:</label>
                    <input type="text" id="cidade" class="form-control" placeholder="Ex: São Paulo">
                    <button id="check-clima" class="btn btn-primary mt-2">Verificar Clima</button>
                    <div id="clima-info" class="mt-3"></div>
                </div>
            </div>

            <script>
                var ctx = document.getElementById('gauge').getContext('2d');
                var gaugeChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Valor', 'Restante'],
                        datasets: [/* Adicionando estruturas dinâmicas com loops */
                            {
                                label: 'Valor do Potenciômetro',
                                data: [0, 100], // Valores iniciais (a serem atualizados)
                                backgroundColor: ['#36A2EB', '#E0E0E0'],
                                borderWidth: 1,
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        cutoutPercentage: 70,
                        animation: {
                            animateRotate: true,
                        }
                    }
                });

                $(document).ready(function() {
                    var socket = io.connect('http://' + document.domain + ':' + location.port);
                    socket.on('novo_dado', function(data) {
                        $('#valor-potenciometro').text('Tensão em porcentagem: ' + data.valor);
                        // Atualiza o gráfico gauge com o novo valor
                        gaugeChart.data.datasets[0].data[0] = data.valor; // Atualiza a parte do valor do gráfico de rosca
                        gaugeChart.data.datasets[0].data[1] = 100 - data.valor; // Parte restante (supondo que o valor máximo seja 100)
                        gaugeChart.update(); // Atualiza o gráfico
                    });

                    $('#check-clima').click(function() {
                        var cidade = $('#cidade').val();
                        if (cidade) {
                            $.get('/verificar_clima/' + cidade, function(data) {
                                $('#clima-info').text(data.clima);
                            }).fail(function() {
                                $('#clima-info').text('Erro ao buscar clima. Verifique a cidade ou tente novamente mais tarde.');
                            });
                        } else {
                            $('#clima-info').text('Por favor, insira uma cidade.');
                        }
                    });
                });
            </script>
        </body>
        </html>
    ''')

@app.route('/verificar_clima/<cidade>')
def verificar_clima(cidade):
    # URL da API OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
    try:
        response = requests.get(url)
        clima_data = response.json()

        if clima_data.get('cod') != 200:
            return jsonify({'clima': 'Cidade não encontrada ou erro na API.'})

        temperatura = clima_data['main']['temp']
        descricao = clima_data['weather'][0]['description']
        nascer_do_sol = clima_data['sys']['sunrise']
        por_do_sol = clima_data['sys']['sunset']
        agora = int(clima_data['dt'])  # Horário atual (timestamp Unix)

        # Determina se é dia ou noite
        if agora < nascer_do_sol or agora > por_do_sol:
            clima_info = "Está de noite. Não haverá produção de energia solar."
        else:
            # Avalia o clima apenas se for dia
            if temperatura > 25 and 'clear' in descricao.lower():
                clima_info = "O clima está ótimo para o painel solar!"
            elif temperatura < 0 or 'rain' in descricao.lower():
                clima_info = "O clima não está ideal para o painel solar."
            else:
                clima_info = "O clima está moderado para o painel solar."

        return jsonify({'clima': clima_info})

    except Exception as e:
        print(e)
        return jsonify({'clima': 'Erro ao consultar o clima.'})


if __name__ == '__main__':
    socketio.run(app, debug=True)
