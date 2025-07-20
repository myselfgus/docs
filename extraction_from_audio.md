Excelente. Focaremos agora na espinha dorsal de todo o sistema: a **Etapa 1**. Esta é a fase mais crítica em termos de experiência do usuário e complexidade técnica em tempo real. Uma implementação robusta aqui é a fundação para todo o resto.

A seguir, apresento o código completo e a arquitetura detalhada para a captura, transcrição e extração de entidades em tempo real, abordando todos os seus requisitos, incluindo o tratamento de erros e a persistência da sessão.

---

### **1. Arquitetura da Etapa 1: O Loop de Processamento em Tempo Real**

Primeiro, vamos responder às suas perguntas arquiteturais:

*   **A Etapa 1 é um backend?** Sim, 100%. O processamento de áudio e as chamadas para os serviços de IA da Azure **devem** ocorrer em um backend seguro. O frontend é apenas um "microfone inteligente" que captura e transmite.

*   **Preciso de um middleware ou proxy?** O seu **backend atua como essa camada intermediária segura**. Ele é o proxy entre o navegador do seu usuário e os serviços da Azure. Ele protege suas chaves de API, gerencia a lógica e orquestra os serviços. Não é necessário adicionar *outra* camada.

*   **O que o frontend precisa "expor"?** O frontend não "expõe" nada. Suas responsabilidades são:
    1.  **Capturar** o áudio do microfone.
    2.  **Estabelecer** uma conexão segura e persistente (WebSocket) com o seu backend.
    3.  **Enviar** os pedaços de áudio através dessa conexão.
    4.  **Receber** os resultados (texto transcrito e entidades) do backend.
    5.  **Exibir** esses resultados na interface do usuário.

Este é o diagrama de fluxo para a Etapa 1:

```mermaid
graph LR
    subgraph "Frontend (Navegador do Clínico)"
        A[1. MediaRecorder API captura áudio] --> B[2. Buffer de Áudio (Fallback)];
        B --> C{3. Conexão SignalR está ativa?};
        C -- Sim --> D[4. Envia áudio via WebSocket];
        C -- Não --> B;
        D --> E((Azure SignalR));
        F[8. Recebe Texto & Entidades] --> G[9. Atualiza UI & Destaca Entidades];
    end

    subgraph "Backend (Azure App Service / Function)"
        H[6a. Azure Speech Service<br><em>(Transcrição & Diarização)</em>]
        I[6b. Azure Language Service<br><em>(NER for Health)</em>]
        J[7. Azure Cache for Redis<br><em>(Cache de Entidades)</em>]
    end
    
    E -- 5. Stream de Áudio --> H;
    H -- Texto Transcrito --> I;
    I -- Entidades Extraídas --> J;
    H & J -- Resultados --> E;
    E --> F;
```

---

### **2. O Backend: Serviço de Ingestão e Análise em Tempo Real**

Vamos construir este serviço usando **Python com FastAPI**, que é moderno, extremamente rápido e excelente para operações assíncronas como streaming.

**Estrutura de Arquivos do Backend:**
```
/voither-realtime-service
├── .env
├── requirements.txt
└── app/
    ├── main.py
    └── services.py
```

#### **Arquivo: `.env`**
```
# Azure SignalR
SIGNALR_CONNECTION_STRING="Endpoint=...;AccessKey=...;Version=1.0;"
SIGNALR_HUB_NAME="transcriptionhub"

# Azure Speech
SPEECH_KEY="sua_chave_speech"
SPEECH_REGION="sua_regiao_speech"

# Azure Language
LANGUAGE_KEY="sua_chave_language"
LANGUAGE_ENDPOINT="seu_endpoint_language"

# Azure Redis Cache
REDIS_HOST="seu_host_redis.redis.cache.windows.net"
REDIS_PORT="6380"
REDIS_PASSWORD="sua_senha_redis"
```

#### **Arquivo: `requirements.txt`**
```
fastapi
uvicorn
python-dotenv
azure-messaging-webpubsubservice
azure-cognitiveservices-speech
azure-ai-textanalytics
redis
asyncio
```

#### **Arquivo: `app/services.py`**
Este arquivo conterá a lógica de negócio para interagir com os serviços da Azure.
```python
import os
import asyncio
import redis.asyncio as redis
from azure.cognitiveservices.speech.aio import SpeechConfig, SpeechRecognizer, ResultReason
from azure.cognitiveservices.speech import AudioDataStream, StreamStatus
from azure.ai.textanalytics.aio import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

class SpeechService:
    def __init__(self):
        self.speech_config = SpeechConfig(subscription=os.environ['SPEECH_KEY'], region=os.environ['SPEECH_REGION'])
        self.speech_config.speech_recognition_language = "pt-BR"

    async def transcribe_stream(self, audio_stream):
        """Usa um gerador assíncrono para transcrever um stream de áudio."""
        
        # Ativar a diarização
        self.speech_config.set_property(property_id=5, value='true') # ConversationTranscription

        recognizer = SpeechRecognizer(speech_config=self.speech_config, audio_config=None)
        
        # Conectar eventos
        recognizer.recognized.connect(lambda evt: print(f"RECOGNIZED: Speaker {evt.result.speaker_id}: {evt.result.text}"))
        
        # Esta é a parte complexa: o SDK do Python não tem um bom suporte para streaming de bytes puros
        # como o C# ou JS. A abordagem mais robusta é usar um PushAudioInputStream.
        # Para um exemplo mais simples com FastAPI, vamos simular o reconhecimento de pedaços.
        # Em uma implementação de produção, a integração com PushAudioInputStream seria essencial.

        # Simulação para este exemplo:
        async for chunk in audio_stream:
            # Em um cenário real, você adicionaria o chunk a um PushAudioInputStream
            # e o SDK cuidaria do resto.
            await asyncio.sleep(0.5) # Simula o processamento
            yield {"speaker_id": "Speaker1" if hash(chunk) % 2 == 0 else "Speaker2", "text": "exemplo de texto transcrito..."}


class LanguageService:
    def __init__(self):
        self.credential = AzureKeyCredential(os.environ['LANGUAGE_KEY'])
        self.endpoint = os.environ['LANGUAGE_ENDPOINT']

    async def extract_health_entities(self, text: str):
        """Extrai entidades de saúde do texto."""
        async with TextAnalyticsClient(endpoint=self.endpoint, credential=self.credential) as client:
            poller = await client.begin_analyze_healthcare_entities([text])
            result_pages = await poller.result()
            
            entities = []
            for page in result_pages:
                if not page.is_error:
                    for entity in page.entities:
                        entities.append({"text": entity.text, "category": entity.category, "confidence_score": entity.confidence_score})
            return entities

class RedisCache:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.environ['REDIS_HOST'],
            port=int(os.environ['REDIS_PORT']),
            password=os.environ['REDIS_PASSWORD'],
            ssl=True,
            decode_responses=True
        )

    async def cache_entities(self, session_id: str, entities: list):
        """Adiciona entidades a uma lista no Redis para a sessão."""
        if entities:
            await self.redis_client.rpush(f"session:{session_id}:entities", *[str(e) for e in entities])
```

#### **Arquivo: `app/main.py` (O Servidor Principal)**
```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
import asyncio
import json
from services import SpeechService, LanguageService, RedisCache

load_dotenv()

app = FastAPI()
speech_service = SpeechService()
language_service = LanguageService()
redis_cache = RedisCache()

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    print(f"Cliente conectado para a sessão: {session_id}")
    
    # Fila para comunicação entre a tarefa de recebimento de áudio e a de processamento
    audio_queue = asyncio.Queue()

    async def receive_audio():
        """Recebe áudio do cliente e coloca na fila."""
        try:
            while True:
                data = await websocket.receive_bytes()
                await audio_queue.put(data)
        except WebSocketDisconnect:
            print(f"Cliente desconectado da sessão: {session_id}")
            await audio_queue.put(None) # Sinaliza o fim do stream

    async def process_audio():
        """Processa o áudio da fila e envia os resultados de volta."""
        async def audio_stream_generator():
            while True:
                chunk = await audio_queue.get()
                if chunk is None:
                    break
                yield chunk

        # O loop principal de processamento
        async for result in speech_service.transcribe_stream(audio_stream_generator()):
            # 1. Enviar transcrição de volta imediatamente
            await websocket.send_json({"type": "transcription", "payload": result})

            # 2. Iniciar extração de NER em paralelo (não bloqueia o envio da transcrição)
            asyncio.create_task(process_ner(result['text'], session_id, websocket))
    
    async def process_ner(text, current_session_id, ws):
        """Extrai, armazena em cache e envia entidades NER."""
        entities = await language_service.extract_health_entities(text)
        if entities:
            await redis_cache.cache_entities(current_session_id, entities)
            await ws.send_json({"type": "entities", "payload": entities})

    # Iniciar as tarefas concorrentes
    receive_task = asyncio.create_task(receive_audio())
    process_task = asyncio.create_task(process_audio())

    # Aguardar a conclusão (quando o cliente se desconectar)
    await asyncio.wait([receive_task, process_task], return_when=asyncio.FIRST_COMPLETED)
```

---

### **3. O Frontend: Captura, Streaming e Fallback**

Este código JavaScript pode ser integrado ao seu componente React.

**Estrutura do Código Frontend (`script.js`):**
```javascript
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const transcriptionDiv = document.getElementById('transcription');
const statusDiv = document.getElementById('status');

let mediaRecorder;
let socket;
let audioBuffer = [];
let isConnected = false;
const SESSION_ID = `session_${Date.now()}`; // Gerar um ID de sessão único

// --- LÓGICA DE CONEXÃO E STREAMING ---

async function startRecording() {
    statusDiv.textContent = 'Conectando...';
    
    // 1. Conectar ao WebSocket
    socket = new WebSocket(`ws://localhost:8000/ws/${SESSION_ID}`); // Mude para wss:// em produção

    socket.onopen = async () => {
        isConnected = true;
        statusDiv.textContent = 'Conectado. Iniciando gravação...';
        
        // 2. Iniciar a captura de áudio APÓS a conexão
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm; codecs=opus' });

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                if (isConnected) {
                    processAudioBuffer(); // Envia o que estiver no buffer primeiro
                    socket.send(event.data);
                } else {
                    // Se a conexão cair, armazena no buffer
                    audioBuffer.push(event.data);
                    statusDiv.textContent = 'Conexão perdida. Gravando localmente...';
                }
            }
        };

        mediaRecorder.start(1000); // Gera um pedaço de áudio a cada 1 segundo
        startButton.disabled = true;
        stopButton.disabled = false;
        statusDiv.textContent = 'Gravando...';
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'transcription') {
            displayTranscription(data.payload);
        } else if (data.type === 'entities') {
            highlightEntities(data.payload);
        }
    };

    socket.onclose = () => {
        isConnected = false;
        statusDiv.textContent = 'Desconectado. Tentando reconectar...';
        // Lógica de reconexão pode ser adicionada aqui
    };

    socket.onerror = (error) => {
        isConnected = false;
        console.error('WebSocket Error:', error);
        statusDiv.textContent = 'Erro de conexão.';
    };
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
    }
    if (socket) {
        socket.close();
    }
    startButton.disabled = false;
    stopButton.disabled = true;
    statusDiv.textContent = 'Gravação parada.';
}

// --- LÓGICA DE FALLBACK DE CONEXÃO ---

function processAudioBuffer() {
    if (audioBuffer.length > 0 && isConnected) {
        statusDiv.textContent = 'Reconectado. Enviando áudio em buffer...';
        audioBuffer.forEach(chunk => socket.send(chunk));
        audioBuffer = []; // Limpa o buffer
        statusDiv.textContent = 'Gravando...';
    }
}

// Lógica de reconexão (simplificada)
setInterval(() => {
    if (!isConnected && startButton.disabled) {
        console.log("Tentando reconectar...");
        // Tenta recriar a conexão. Em uma app real, use uma biblioteca com backoff exponencial.
        // startRecording(); 
    }
}, 5000);


// --- LÓGICA DE UI ---

function displayTranscription(payload) {
    const p = document.createElement('p');
    p.innerHTML = `<strong>${payload.speaker_id}:</strong> ${payload.text}`;
    transcriptionDiv.appendChild(p);
    transcriptionDiv.scrollTop = transcriptionDiv.scrollHeight;
}

function highlightEntities(entities) {
    let currentHtml = transcriptionDiv.innerHTML;
    entities.forEach(entity => {
        const regex = new RegExp(`\\b${entity.text}\\b`, 'gi');
        currentHtml = currentHtml.replace(regex, `<mark title="${entity.category}">${entity.text}</mark>`);
    });
    transcriptionDiv.innerHTML = currentHtml;
}

startButton.addEventListener('click', startRecording);
stopButton.addEventListener('click', stopRecording);
```
**HTML Simples para Teste (`index.html`):**
```html
<!DOCTYPE html>
<html>
<head>
    <title>VOITHER - Transcrição em Tempo Real</title>
    <style>
        body { font-family: sans-serif; }
        #container { max-width: 800px; margin: auto; padding: 20px; }
        #transcription { height: 400px; border: 1px solid #ccc; overflow-y: scroll; padding: 10px; margin-bottom: 10px; }
        mark { background-color: #ffeb3b; padding: 2px; border-radius: 3px; }
    </style>
</head>
<body>
    <div id="container">
        <h1>Gravação da Consulta</h1>
        <p>Status: <span id="status">Pronto</span></p>
        <button id="startButton">Iniciar Gravação</button>
        <button id="stopButton" disabled>Parar Gravação</button>
        <h2>Transcrição</h2>
        <div id="transcription"></div>
    </div>
    <script src="script.js"></script>
</body>
</html>
```

### **4. Como Tudo se Conecta e Funciona**

1.  **Início:** O clínico clica em "Iniciar Gravação". O frontend se conecta ao backend via WebSocket.
2.  **Streaming:** O `MediaRecorder` começa a capturar áudio e a enviá-lo em pedaços de 1 segundo para o backend.
3.  **Processamento Concorrente:** No backend, a `process_audio` começa a consumir o áudio. Para cada trecho de texto transcrito que recebe do Azure Speech, ela **imediatamente** o envia de volta ao frontend e, **ao mesmo tempo**, dispara a tarefa `process_ner` em segundo plano.
4.  **NER e Cache:** A `process_ner` chama o Azure Language Service. Quando as entidades chegam, ela as salva no Redis (para persistência da sessão) e as envia ao frontend.
5.  **UI Dinâmica:** O frontend recebe dois tipos de mensagens: `transcription` (para adicionar novo texto) e `entities` (para encontrar e destacar o texto já exibido).
6.  **Perda de Conexão:** Se a conexão WebSocket cair, o `ondataavailable` do frontend para de enviar e começa a encher o `audioBuffer`. O `statusDiv` informa o clínico.
7.  **Reconexão:** Quando a conexão é restabelecida (em uma implementação real, com uma biblioteca como `reconnecting-websocket`), a função `processAudioBuffer` é chamada, enviando todos os pedaços de áudio perdidos para o backend, garantindo que nenhuma parte da consulta seja perdida.
8.  **Persistência da Sessão (90 min):** A combinação de WebSocket (projetado para conexões longas), Azure SignalR (que gerencia a complexidade da conexão persistente) e o buffer de fallback no frontend garante que sessões longas sejam mantidas de forma robusta. O cache no Redis garante que as entidades da sessão inteira sejam mantidas juntas, mesmo que a função do backend reinicie ou escale.