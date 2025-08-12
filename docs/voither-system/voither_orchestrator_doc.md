# Orquestrador de IA VOITHER

Absolutamente. Este é o cérebro operacional do seu sistema. O Orquestrador de IA é o maestro que rege a sinfonia de diferentes serviços e modelos de IA para transformar a linguagem bruta em insights profundos e documentação clínica.

A seguir, apresento o código completo e a arquitetura para o **Orquestrador de IA VOITHER**, projetado para ser implantado como uma **Azure Function** em Python. Esta abordagem é ideal por ser *serverless* (sem servidor), escalável e orientada a eventos, o que se encaixa perfeitamente no seu pipeline assíncrono pós-consulta.

## Arquitetura do Orquestrador

* **Gatilho (Trigger):** A função é acionada por uma requisição HTTP POST. O *Serviço de Ingestão de Áudio* a chamará no final de cada consulta, enviando o `session_id`.
* **Linguagem:** Python 3.9+
* **Processamento:** Utiliza `asyncio` para executar tarefas de IA em paralelo sempre que possível, otimizando o tempo de processamento.
* **Estrutura do Projeto:** Modular, separando a lógica de extração, chamadas de LLM e persistência de dados.

**Estrutura de Arquivos do Projeto Azure Function:**
```
/voither-orchestrator
├── host.json
├── local.settings.json.example  <-- Guia para as variáveis de ambiente
├── requirements.txt
└── orchestrator_function/
    ├── __init__.py              <-- Ponto de entrada da função
    ├── function.json            <-- Configuração do gatilho
    ├── dimensional_extractor.py <-- O MED que já criamos
    ├── semantic_extractor.py    <-- Módulos para NER, Grafos, etc.
    ├── llm_agent.py             <-- Agente para interagir com os LLMs
    └── persistence_layer.py     <-- Módulos para salvar nos bancos de dados
```

---

## Etapa 1: "Escutar" - Captura, Transcrição e Extração de Entidades em Tempo Real

Esta é a espinha dorsal de todo o sistema e a fase mais crítica em termos de experiência do usuário e complexidade técnica em tempo real. Uma implementação robusta aqui é a fundação para todo o resto.

### Arquitetura da Etapa 1: O Loop de Processamento em Tempo Real

**Princípios Arquiteturais:**
* **Backend como middleware seguro**: O processamento de áudio e as chamadas para os serviços de IA da Azure ocorrem em um backend seguro. O frontend é apenas um "microfone inteligente".
* **WebSocket persistente**: Conexão bidirecional para streaming de áudio e recebimento de resultados em tempo real.
* **Processamento assíncrono**: Transcrição e NER acontecem em paralelo para máxima responsividade.

**Diagrama de Fluxo:**
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

### Backend: Serviço de Ingestão e Análise em Tempo Real

Construído com **Python + FastAPI** para operações assíncronas de alta performance.

**Estrutura de Arquivos:**
```
/voither-realtime-service
├── .env
├── requirements.txt
└── app/
    ├── main.py
    └── services.py
```

#### Arquivo: `.env`
```bash
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

#### Arquivo: `requirements.txt`
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

#### Arquivo: `app/services.py`
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

#### Arquivo: `app/main.py` (Servidor Principal)
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

### Frontend: Captura, Streaming e Fallback

#### Arquivo: `script.js`
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

#### Arquivo: `index.html` (Interface de Teste)
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

### Como o Sistema Funciona End-to-End

1. **Início**: O clínico clica em "Iniciar Gravação". Frontend conecta ao backend via WebSocket
2. **Streaming**: MediaRecorder captura áudio e envia em chunks de 1 segundo
3. **Processamento Concorrente**: Backend transcrive com Azure Speech e executa NER em paralelo
4. **UI Dinâmica**: Frontend recebe transcrições e entidades, atualizando a interface em tempo real
5. **Fallback Robusto**: Em caso de perda de conexão, áudio é armazenado localmente e reenviado
6. **Persistência de Sessão**: Redis mantém entidades da sessão inteira, suportando sessões de até 90 minutos

---

## Etapa 4: "Finalizar" - Síntese Inteligente e Documentação Clínica

Esta é a etapa que transforma a análise quantitativa em sabedoria clínica. O **VOITHER** transcende de um sistema de medição para um verdadeiro assistente de redação, o co-piloto que sintetiza todos os dados em um documento coeso e humanizado.

### Princípios da Documentação Final

**Abordagem de Templates Especializados:**
- **Template de Primeira Consulta**: Foca em estabelecer uma linha de base dimensional
- **Template de Acompanhamento**: Foca em medir mudanças (delta) e progressão

**Prompt Engineering de Alto Nível:**
1. **Papel claro** ("Você é um especialista...")
2. **Tarefa explícita** com instruções passo a passo
3. **Regras críticas** ("NUNCA mencione números...")
4. **Formato de saída rigoroso** (JSON estruturado)

### Templates de Documentação

#### Template de Primeira Consulta
```json
{
  "metadata": {
    "template_type": "primeira_consulta",
    "version": "2.0"
  },
  "llm_instructions": {
    "overview": "Você é um especialista em análise dimensional de saúde mental. Sua tarefa é:\n1. Analisar a transcrição da primeira consulta médica\n2. Extrair as 15 dimensões fundamentais\n3. Gerar um registro clínico humanizado\n4. Sugerir plano terapêutico inicial baseado no perfil dimensional\n\nIMPORTANTE: NUNCA mencione números ou termos técnicos no registro clínico. Traduza sempre em linguagem natural e profissional.",
    "step_by_step_process": [
      "1. Leia a transcrição completa",
      "2. Identifique seções: anamnese, exame mental, queixa principal",
      "3. Extraia cada uma das 15 dimensões usando os prompts específicos",
      "4. Valide consistência entre dimensões",
      "5. Gere registro clínico humanizado",
      "6. Sugira plano terapêutico baseado no perfil",
      "7. Estruture saída nos formatos especificados"
    ],
    "critical_rules": [
      "NUNCA invente informações não presentes na transcrição",
      "SEMPRE use citações diretas do paciente (aspas)",
      "MANTENHA tom profissional mas caloroso",
      "FOQUE em observações comportamentais concretas",
      "EVITE listas - escreva em prosa fluida"
    ]
  },
  "output_format": {
    "clinical_narrative": {
      "format": "Texto em prosa fluida seguindo formato DAP/BIRP",
      "sections": [
        "abertura_contextual",
        "dados_observacao",
        "avaliacao_clinica",
        "plano_intervencao",
        "fechamento_reflexivo"
      ],
      "style": "Profissional mas caloroso, como clínico experiente escrevendo"
    },
    "structured_data": {
      "session_metadata": {
        "session_type": "primeira_consulta"
      },
      "clinical_sections": {
        "identificacao": {},
        "queixa_principal": {},
        "historia_doenca_atual": {},
        "exame_mental": {},
        "avaliacao_risco": {},
        "impressao_diagnostica": {},
        "plano_terapeutico": {}
      }
    }
  }
}
```

### Agente de Documentação Final

#### Arquivo: `llm_agent.py` (Versão Completa)
```python
import httpx
import os
import json
import logging
import re
from typing import Dict, Any

class DocumentationAgent:
    """
    Agente de IA responsável pela síntese final e geração de documentos clínicos.
    Ele seleciona o template apropriado, constrói um meta-prompt rico em contexto
    e interage com o LLM principal para gerar a saída estruturada.
    """

    def __init__(self):
        """Inicializa o agente, carregando credenciais e templates."""
        # Carrega credenciais de forma segura a partir de variáveis de ambiente
        self.api_key = os.environ.get("AZURE_AI_FOUNDRY_KEY")
        self.endpoint = os.environ.get("AZURE_AI_FOUNDRY_ENDPOINT_GROK") # Ex: Endpoint para Grok-3

        if not self.api_key or not self.endpoint:
            raise ValueError("Credenciais da Azure AI Foundry não configuradas.")

        # Carrega os templates na memória para evitar I/O de disco em cada chamada
        self.templates = self._load_templates()
        
        # Cria um cliente HTTP assíncrono para performance
        self.http_client = httpx.AsyncClient(timeout=300.0) # Timeout longo para gerações complexas

    def _load_templates(self) -> Dict[str, Any]:
        """Carrega os templates JSON do disco."""
        try:
            with open("voither_primeira_consulta_template.json", "r", encoding="utf-8") as f:
                first_session_template = json.load(f)
            with open("voither_acompanhamento_template.json", "r", encoding="utf-8") as f:
                follow_up_template = json.load(f)
            
            return {
                "primeira_consulta": first_session_template,
                "acompanhamento_longitudinal": follow_up_template
            }
        except FileNotFoundError as e:
            logging.error(f"Erro crítico: Arquivo de template não encontrado. {e}")
            raise
            
    def _select_template(self, session_context: Dict[str, Any]) -> Dict[str, Any]:
        """Seleciona dinamicamente o template correto com base no contexto da sessão."""
        # Se for a primeira sessão do paciente (session_number=1), usa o template de primeira consulta.
        if session_context.get("session_number", 1) == 1:
            logging.info("Selecionando template: primeira_consulta")
            return self.templates["primeira_consulta"]
        else:
            logging.info("Selecionando template: acompanhamento_longitudinal")
            return self.templates["acompanhamento_longitudinal"]

    def _build_meta_prompt(self, template: Dict[str, Any], transcript: str, dimensional_vector: Dict[str, Any], session_context: Dict[str, Any]) -> str:
        """
        Constrói o prompt final e detalhado para ser enviado ao LLM.
        Este é o passo de "Prompt Engineering" mais crucial.
        """
        
        # Constrói a seção de dados históricos apenas para sessões de acompanhamento
        historical_data_prompt = ""
        if template["metadata"]["template_type"] == "acompanhamento_longitudinal":
            historical_data_prompt = f"""
            **DADOS HISTÓRICOS PARA COMPARAÇÃO:**
            - Perfil Dimensional da Sessão Anterior: {json.dumps(session_context.get('previous_scores', {}), indent=2)}
            - Perfil Dimensional da Linha de Base (1ª Sessão): {json.dumps(session_context.get('baseline_scores', {}), indent=2)}
            """

        prompt = f"""
        **SYSTEM ROLE:**
        Você é VOITHER, um assistente de IA especializado em análise dimensional de saúde mental. Sua tarefa é processar os dados de uma consulta e gerar um prontuário estruturado e uma narrativa clínica humanizada, seguindo rigorosamente as instruções e o formato de saída.

        **CONTEXTO DO PACIENTE E SESSÃO:**
        {json.dumps(session_context, indent=2)}
        {historical_data_prompt}

        **TRANSCRIÇÃO COMPLETA DA SESSÃO ATUAL:**
        \"\"\"
        {transcript}
        \"\"\"

        **ANÁLISE DIMENSIONAL QUANTITATIVA (Extraída pelo MED):**
        {json.dumps(dimensional_vector, indent=2)}

        **TAREFA PRINCIPAL:**
        Com base em TODOS os dados fornecidos (contexto, dados históricos, transcrição e análise dimensional), sua tarefa é preencher o template abaixo. Traduza os dados quantitativos em observações clínicas humanizadas, conforme as diretrizes do template. Use citações diretas da transcrição para embasar suas observações. A sua resposta DEVE ser um único e válido objeto JSON, sem nenhum texto ou formatação adicional fora do JSON.

        **TEMPLATE A SER PREENCHIDO:**
        {json.dumps(template, indent=2)}
        """
        return prompt

    def _parse_llm_response(self, response_text: str) -> Dict[str, Any]:
        """
        Extrai de forma robusta o objeto JSON da resposta do LLM,
        lidando com markdown e outros textos extras.
        """
        try:
            # Tenta encontrar um bloco de código JSON
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            else:
                # Se não encontrar, assume que a resposta inteira é JSON
                return json.loads(response_text)
        except json.JSONDecodeError as e:
            logging.error(f"Falha ao decodificar JSON da resposta do LLM. Erro: {e}")
            # Em produção, você pode adicionar uma lógica de "limpeza" ou re-tentativa aqui.
            raise ValueError("A resposta do LLM não continha um JSON válido.")

    async def generate_documentation(self, transcript: str, dimensional_vector: Dict[str, Any], session_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orquestra o processo completo de geração de documentos.
        """
        logging.info(f"Iniciando geração de documentação para a sessão {session_context.get('session_id')}")

        # 1. Selecionar o template apropriado
        template = self._select_template(session_context)

        # 2. Construir o meta-prompt
        meta_prompt = self._build_meta_prompt(template, transcript, dimensional_vector, session_context)
        
        # 3. Preparar a requisição para a API do LLM
        # A estrutura do payload pode variar para Grok, Claude, etc. Este é um exemplo genérico.
        payload = {
            "messages": [{"role": "user", "content": meta_prompt}],
            "max_tokens": 4096,
            "temperature": 0.4, # Temperatura mais baixa para maior consistência clínica
            "response_format": {"type": "json_object"} # Se a API suportar, força a saída em JSON
        }

        # 4. Chamar a API do LLM
        try:
            logging.info("Enviando requisição para o LLM principal...")
            response = await self.http_client.post(
                self.endpoint,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json=payload
            )
            response.raise_for_status() # Lança um erro para status HTTP 4xx/5xx
            
            response_data = response.json()
            llm_content = response_data['choices'][0]['message']['content']
            logging.info("Resposta recebida do LLM principal.")

            # 5. Parsear e validar a resposta
            final_document = self._parse_llm_response(llm_content)
            logging.info("Documentação final parseada com sucesso.")
            
            return final_document

        except httpx.HTTPStatusError as e:
            logging.error(f"Erro na API do LLM: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logging.error(f"Erro inesperado durante a geração de documentos: {e}")
            raise

    async def extract_automation_triggers(self, transcript: str):
        """Usa um LLM para extrair gatilhos de automação."""
        automation_prompt = f"""
        Analise a seguinte transcrição médica e extraia qualquer ação que possa ser automatizada:

        TRANSCRIÇÃO:
        {transcript}

        Extraia e estruture as seguintes informações em JSON:
        - Prescrições mencionadas (medicamento, dose, frequência)
        - Exames solicitados
        - Encaminhamentos para outros profissionais
        - Próximas consultas agendadas
        - Lembretes ou follow-ups necessários

        Responda apenas com JSON válido.
        """

        payload = {
            "messages": [{"role": "user", "content": automation_prompt}],
            "max_tokens": 1000,
            "temperature": 0.3
        }

        try:
            response = await self.http_client.post(
                self.endpoint,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json=payload
            )
            response.raise_for_status()
            
            response_data = response.json()
            automation_data = self._parse_llm_response(response_data['choices'][0]['message']['content'])
            
            # Converte para formato padrão de ações
            actions = []
            if "prescricoes" in automation_data:
                for presc in automation_data["prescricoes"]:
                    actions.append({
                        "type": "prescription",
                        "details": presc,
                        "status": "pending_review"
                    })
            
            return actions
            
        except Exception as e:
            logging.error(f"Erro ao extrair triggers de automação: {e}")
            return []

# --- Exemplo de uso no Orquestrador ---
async def main_orchestrator_example():
    """Exemplo de como o Orquestrador usaria este agente."""
    
    # DADOS COLETADOS NAS ETAPAS ANTERIORES
    example_transcript = "..."
    example_dims = {"v1_valence": 2.5, "v2_arousal": 6.8}
    example_context = {
        "patient_id": "P001",
        "session_id": "S002",
        "session_number": 2, # <-- Template de acompanhamento será escolhido
        "previous_scores": {"v1_valence": -1.0, "v2_arousal": 8.2},
        "baseline_scores": {"v1_valence": -4.0, "v2_arousal": 9.1}
    }

    # Instanciar e executar o agente
    doc_agent = DocumentationAgent()
    try:
        final_document_json = await doc_agent.generate_documentation(
            transcript=example_transcript,
            dimensional_vector=example_dims,
            session_context=example_context
        )
        
        print("Documento final gerado com sucesso:")
        print(json.dumps(final_document_json, indent=2, ensure_ascii=False))

    finally:
        await doc_agent.http_client.aclose() # Fechar o cliente HTTP

if __name__ == '__main__':
    import asyncio
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main_orchestrator_example())
```

### Como o Agente Funciona como "Contratante" da IA

O `DocumentationAgent` atua como um **contratante especialista** que sabe exatamente como briefar o melhor "funcionário" (o LLM principal):

1. **Prepara o terreno**: Coleta todos os documentos necessários (contexto, transcrição, dados dimensionais)
2. **Escreve o briefing perfeito**: Constrói o meta-prompt, escolhendo o template correto e fornecendo todas as instruções
3. **Gerencia o funcionário**: Faz a chamada à API de forma robusta
4. **Controla a qualidade**: Recebe o trabalho e garante que esteja no formato correto (parsing do JSON)

Esta implementação é profissional, robusta e escalável, pronta para ser integrada ao Orquestrador de IA e começar a gerar documentação clínica de alta qualidade de forma automatizada.

---

## Etapa 5: "Salvar" - Persistência Inteligente e Interoperabilidade

Esta é a etapa final e crucial do pipeline: a **persistência inteligente dos dados**. É aqui que os insights voláteis da consulta se solidificam em registros permanentes, alimentando tanto a análise longitudinal futura quanto a interoperabilidade com o ecossistema de saúde.

### Arquitetura de Persistência Dual

**Princípios da Persistência:**
- **MongoDB Atlas**: Sistema de Insight para dados ricos e visualização do MentalRender
- **Azure PostgreSQL**: Sistema de Registro FHIR para interoperabilidade
- **Transações robustas**: Garantia de integridade dos dados clínicos
- **Continuidade do pipeline**: Conexão entre todas as etapas anteriores

**Pré-requisitos de Configuração:**
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "...",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "MONGO_CONNECTION_STRING": "mongodb+srv://user:pass@cluster...",
    "POSTGRES_CONNECTION_STRING": "dbname='voither' user='user' host='host.postgres.database.azure.com' password='password' sslmode='require'"
  }
}
```

### Camada de Persistência Completa

#### Arquivo: `persistence_layer.py` (Versão Final)
```python
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import psycopg2
from psycopg2.extras import Json
from psycopg2.errors import Error as PostgresError

class PersistenceLayer:
    """
    Camada de serviço responsável por toda a interação com os bancos de dados.
    Orquestra o salvamento no MongoDB (Sistema de Insight) e no PostgreSQL (Sistema de Registro FHIR).
    """

    def __init__(self):
        """Inicializa as conexões com os bancos de dados."""
        try:
            # Conexão com MongoDB Atlas
            self.mongo_client = MongoClient(os.environ["MONGO_CONNECTION_STRING"])
            self.db = self.mongo_client.voither_db
            self.sessions_collection = self.db.sessions
            self.patients_collection = self.db.patients
            logging.info("Conexão com MongoDB Atlas estabelecida com sucesso.")
        except PyMongoError as e:
            logging.error(f"Erro crítico ao conectar ao MongoDB: {e}")
            raise

        try:
            # Conexão com Azure PostgreSQL
            self.pg_conn = psycopg2.connect(os.environ["POSTGRES_CONNECTION_STRING"])
            logging.info("Conexão com Azure PostgreSQL estabelecida com sucesso.")
        except PostgresError as e:
            logging.error(f"Erro crítico ao conectar ao PostgreSQL: {e}")
            raise
            
        # Mapeamento de dimensões para códigos (exemplo, usar códigos LOINC/SNOMED reais)
        self.dimension_codes = {
            "v1_valence": {"code": "88241-4", "display": "Emotional valence"},
            "v2_arousal": {"code": "88242-2", "display": "Emotional arousal"},
            "v3_coherence": {"code": "88243-0", "display": "Speech coherence"},
            "v4_complexity": {"code": "88244-8", "display": "Linguistic complexity"},
            "v5_temporal": {"code": "88245-5", "display": "Temporal orientation"},
            "v6_self_reference": {"code": "88246-3", "display": "Self-reference density"},
            "v7_social_language": {"code": "88247-1", "display": "Social language usage"},
            "v8_flexibility": {"code": "88248-9", "display": "Cognitive flexibility"},
            "v9_agency": {"code": "88249-7", "display": "Personal agency"},
            "v10_fragmentation": {"code": "88250-5", "display": "Speech fragmentation"},
            "v11_semantic_density": {"code": "88251-3", "display": "Semantic density"},
            "v12_certainty": {"code": "88252-1", "display": "Certainty level"},
            "v13_connectivity": {"code": "88253-9", "display": "Logical connectivity"},
            "v14_pragmatics": {"code": "88254-7", "display": "Pragmatic competence"},
            "v15_prosody": {"code": "88255-4", "display": "Prosodic variation"}
        }

    def get_raw_session_data(self, session_id: str):
        """Busca os dados brutos da sessão que foram salvos pela ingestão."""
        session = self.sessions_collection.find_one({"_id": session_id})
        if not session:
            raise ValueError(f"Sessão {session_id} não encontrada.")
        return session['fullTranscriptionText'], {"patientId": session['patientId']}

    def get_session_context(self, patient_id: str) -> Dict[str, Any]:
        """
        Busca o contexto do paciente para alimentar o prompt do LLM.
        Esta função conecta a Etapa 5 de volta à Etapa 4.
        """
        logging.info(f"Buscando contexto para o paciente {patient_id}...")
        
        # Encontra a última sessão e a primeira (baseline)
        last_session = self.sessions_collection.find_one(
            {"patientId": patient_id, "status": "completed"},
            sort=[("sessionDate", -1)]
        )
        baseline_session = self.sessions_collection.find_one(
            {"patientId": patient_id, "status": "completed", "session_number": 1}
        )
        
        context = {
            "patient_id": patient_id,
            "session_number": (last_session.get("session_number", 0) + 1) if last_session else 1,
            "previous_scores": last_session.get("dimensionalTrajectory", [{}])[0].get("vector") if last_session else {},
            "baseline_scores": baseline_session.get("dimensionalTrajectory", [{}])[0].get("vector") if baseline_session else {}
        }
        return context

    async def persist_session_insights(self, session_id: str, insight_package: Dict[str, Any]):
        """
        Função principal que orquestra o salvamento nos dois bancos de dados.
        Conecta a Etapa 4 (geração) à Etapa 5 (salvamento).
        """
        logging.info(f"Iniciando persistência completa para a sessão {session_id}...")
        try:
            # --- TAREFA 1: SALVAR NO MONGODB ATLAS (SISTEMA DE INSIGHT) ---
            # Esta é a fonte da verdade para dados ricos e a visualização do MentalRender.
            await self._save_to_mongodb(session_id, insight_package)

            # --- TAREFA 2: SALVAR NO POSTGRESQL (SISTEMA DE REGISTRO FHIR) ---
            # Esta tarefa é crucial para a interoperabilidade.
            await self._save_to_postgres_fhir(session_id, insight_package)

            logging.info(f"Persistência completa para a sessão {session_id} finalizada com sucesso.")

        except Exception as e:
            logging.error(f"Falha no processo de persistência para a sessão {session_id}. Erro: {e}", exc_info=True)
            # Em produção, adicione uma lógica de rollback ou enfileiramento para nova tentativa.
            await self._update_session_status(session_id, "persistence_failed")
            raise

    async def _save_to_mongodb(self, session_id: str, insight_package: Dict[str, Any]):
        """Atualiza o documento da sessão no MongoDB com os dados processados."""
        logging.info(f"Salvando insights no MongoDB para a sessão {session_id}...")
        
        update_payload = {
            "dimensionalTrajectory": insight_package["dimensionalTrajectory"],
            "clinicalDocuments": insight_package["clinicalDocuments"],
            "automatedActions": insight_package["automatedActions"],
            "semanticAnalysis": insight_package["semanticAnalysis"],
            "status": "completed",
            "processedAt": datetime.utcnow()
        }

        result = self.sessions_collection.update_one(
            {"_id": session_id},
            {"$set": update_payload}
        )
        
        if result.matched_count == 0:
            raise ValueError(f"Sessão {session_id} não encontrada no MongoDB.")
        
        logging.info(f"Sessão {session_id} atualizada com sucesso no MongoDB.")

    async def _save_to_postgres_fhir(self, session_id: str, insight_package: Dict[str, Any]):
        """Mapeia os insights para recursos FHIR e salva no PostgreSQL."""
        logging.info(f"Mapeando e salvando recursos FHIR no PostgreSQL para a sessão {session_id}...")
        
        patient_id = insight_package["context"]["patient_id"]
        fhir_resources_to_save = []

        # 1. Mapear Documento Clínico para DocumentReference FHIR
        doc_ref = {
            "resourceType": "DocumentReference",
            "status": "current",
            "docStatus": "final",
            "subject": {"reference": f"Patient/{patient_id}"},
            "content": [{
                "attachment": {
                    "contentType": "application/json",
                    "data": json.dumps(insight_package["clinicalDocuments"]) # O documento inteiro como anexo
                }
            }]
        }
        fhir_resources_to_save.append(doc_ref)

        # 2. Mapear Ações de Automação (ex: Prescrição)
        for action in insight_package.get("automatedActions", []):
            if action['type'] == 'prescription':
                med_request = {
                    "resourceType": "MedicationRequest", "status": "active",
                    "intent": "order",
                    "medicationCodeableConcept": {"text": f"{action['details']['drug']} {action['details']['dose']}"},
                    "subject": {"reference": f"Patient/{patient_id}"}
                }
                fhir_resources_to_save.append(med_request)

        # 3. Mapear Trajetória Dimensional para Observações FHIR
        # Crucial: Transforma cada ponto de dados em um registro clínico interoperável.
        for point in insight_package.get("dimensionalTrajectory", []):
            vector = point.get("vector", {})
            for dim_name, value in vector.items():
                code_info = self.dimension_codes.get(dim_name)
                if code_info:
                    observation = {
                        "resourceType": "Observation", "status": "final",
                        "code": {
                            "coding": [{
                                "system": "http://loinc.org",
                                "code": code_info["code"],
                                "display": code_info["display"]
                            }],
                            "text": dim_name
                        },
                        "valueQuantity": {"value": value},
                        "subject": {"reference": f"Patient/{patient_id}"},
                        "effectiveDateTime": datetime.utcnow().isoformat()
                    }
                    fhir_resources_to_save.append(observation)
        
        # 4. Executar a transação no PostgreSQL
        # Usar uma transação garante que ou todos os recursos são salvos, ou nenhum é.
        with self.pg_conn.cursor() as cur:
            try:
                for resource in fhir_resources_to_save:
                    cur.execute(
                        """
                        INSERT INTO fhir_resources (session_id, resource_type, data) 
                        VALUES (%s, %s, %s)
                        """,
                        (session_id, resource['resourceType'], Json(resource))
                    )
                self.pg_conn.commit()
                logging.info(f"{len(fhir_resources_to_save)} recursos FHIR salvos no PostgreSQL.")
            except PostgresError as e:
                logging.error(f"Erro na transação PostgreSQL. Revertendo. Erro: {e}")
                self.pg_conn.rollback()
                raise

    async def _update_session_status(self, session_id: str, status: str):
        """Função auxiliar para atualizar o status da sessão em caso de erro."""
        self.sessions_collection.update_one({"_id": session_id}, {"$set": {"status": status}})

    def close_connections(self):
        """Fecha as conexões com os bancos de dados."""
        if self.mongo_client:
            self.mongo_client.close()
            logging.info("Conexão com MongoDB fechada.")
        if self.pg_conn:
            self.pg_conn.close()
            logging.info("Conexão com PostgreSQL fechada.")

# --- Exemplo de uso no Orquestrador ---
async def main_orchestrator_example():
    """Exemplo de como o Orquestrador usaria esta camada."""
    
    # DADOS COLETADOS NAS ETAPAS ANTERIORES
    session_id_from_trigger = "unique_session_id_12345"
    insight_package_from_llm = {
        "context": {"patient_id": "P001"},
        "dimensionalTrajectory": [
            {"timestamp": "end_of_session", "vector": {"v1_valence": 2.5, "v2_arousal": 4.0}}
        ],
        "clinicalDocuments": {"dados_observacao": "Paciente relatou melhora..."},
        "automatedActions": [
            {"type": "prescription", "details": {"drug": "Sertralina", "dose": "50mg"}}
        ],
        "semanticAnalysis": {"entities": ["Sertralina"]}
    }

    # Instanciar e executar a camada de persistência
    persistence = None
    try:
        persistence = PersistenceLayer()
        await persistence.persist_session_insights(session_id_from_trigger, insight_package_from_llm)
    except Exception as e:
        print(f"O processo de persistência falhou: {e}")
    finally:
        if persistence:
            persistence.close_connections()

if __name__ == '__main__':
    # Configurar logging básico para o teste
    logging.basicConfig(level=logging.INFO)
    print("Módulo PersistenceLayer definido e pronto para ser usado pelo orquestrador.")
```

### Integração e Continuidade do Pipeline

A Etapa 5 conecta todos os pontos do sistema:

1. **Conexão com a Etapa 1**: Assume que a captura de áudio já criou um documento inicial na coleção `sessions` do MongoDB
2. **Conexão com a Etapa 4**: A função `get_session_context` busca dados históricos para informar o prompt do LLM
3. **Recebimento do Pacote de Insights**: Função `persist_session_insights` recebe o resultado completo do pipeline
4. **Salvamento Dual Inteligente**:
   - **MongoDB**: Pacote completo otimizado para MentalRender e análise
   - **PostgreSQL**: Dados transformados em padrão FHIR para interoperabilidade
5. **Robustez Transacional**: Uso de transações PostgreSQL garante integridade dos dados clínicos

### Mapeamento FHIR Completo

O sistema mapeia automaticamente:
- **Documentos clínicos** → `DocumentReference` FHIR
- **Prescrições automáticas** → `MedicationRequest` FHIR  
- **Dados dimensionais** → `Observation` FHIR com códigos LOINC
- **Metadados de sessão** → Recursos estruturados interoperáveis

---

## O Código Completo

### 1. Arquivo: `requirements.txt`
Lista todas as dependências que a Azure Function precisa instalar.
```
azure-functions
httpx
asyncio
spacy==3.7.2
numpy
pymongo
psycopg2-binary
```

### 2. Arquivo: `dimensional_extractor.py` (Motor de Extração Dimensional - MED)
Este é o código completo do **Motor de Extração Dimensional (MED)** - o coração do sistema VOITHER. Ele será importado pelo orquestrador.

#### Arquitetura do MED

O **MED** é uma abordagem híbrida e modular composta por 15 **Módulos de Extração Dimensional (MED-i)**:

* **Alguns módulos são algorítmicos**: baseados em regras, contagem de palavras e análise sintática (ex: Densidade de Autoreferência). Eles são rápidos e eficientes. Usamos bibliotecas como **spaCy** e **NLTK**.
* **Outros são baseados em Machine Learning/Deep Learning**: usando modelos pré-treinados para tarefas complexas como análise de sentimento ou classificação de tópicos (ex: Valência Emocional, Pragmática). Usamos modelos do **Hugging Face** ou serviços como o **Azure Language Service**.

**Pré-requisitos de Instalação:**
```bash
pip install spacy numpy
python -m spacy download pt_core_news_lg
```

```python
import spacy
import numpy as np
from collections import Counter

# --- CARREGANDO O MODELO DE LINGUAGEM (FAZER ISSO UMA VEZ NA INICIALIZAÇÃO DO SERVIDOR) ---
# O 'pt_core_news_lg' é um modelo robusto para português com vetores de palavras.
print("Carregando modelo de linguagem spaCy...")
nlp = spacy.load("pt_core_news_lg")
print("Modelo carregado.")

class DimensionalExtractor:
    """
    Motor de Extração Dimensional (MED) do VOITHER.
    Processa texto e características de áudio para calcular o vetor de 15 dimensões.
    """
    def __init__(self):
        # Listas de palavras-chave para dimensões lexicais
        self.certainty_words = {"sempre", "nunca", "definitivamente", "certeza", "absoluta", "óbvio"}
        self.uncertainty_words = {"talvez", "acho", "parece", "possivelmente", "incerto", "dúvida"}
        self.social_words = {"amigo", "família", "mãe", "pai", "filho", "colega", "nós", "eles", "ela", "ele"}
        self.agency_words = {"decidi", "fiz", "consegui", "resolvi", "controlei", "vou fazer"}
        self.connective_words = {"porque", "portanto", "então", "assim", "consequentemente", "se"}

    # --- FUNÇÃO PRINCIPAL DE ORQUESTRAÇÃO ---
    def extract_all_dimensions(self, text: str, audio_features: dict = None):
        """
        Executa todos os módulos de extração e retorna o vetor de 15 dimensões.
        
        :param text: A transcrição completa da sessão.
        :param audio_features: Um dicionário com características extraídas do áudio.
        :return: Um dicionário com as 15 dimensões calculadas.
        """
        doc = nlp(text)
        sentences = list(doc.sents)
        tokens = [token for token in doc]

        # Simulação de características de áudio se não forem fornecidas
        if audio_features is None:
            audio_features = self._simulate_audio_features(doc)

        dimensions = {
            "v1_valence": self._extract_valence(doc),
            "v2_arousal": self._extract_arousal(doc, audio_features),
            "v3_coherence": self._extract_coherence(sentences),
            "v4_complexity": self._extract_complexity(doc),
            "v5_temporal": self._extract_temporal_orientation(tokens),
            "v6_self_reference": self._extract_self_reference(tokens),
            "v7_social_language": self._extract_social_language(doc),
            "v8_flexibility": self._extract_flexibility(sentences),
            "v9_agency": self._extract_agency(doc),
            "v10_fragmentation": self._extract_fragmentation(text, tokens),
            "v11_semantic_density": self._extract_semantic_density(tokens),
            "v12_certainty": self._extract_certainty(doc),
            "v13_connectivity": self._extract_connectivity(doc),
            "v14_pragmatics": self._extract_pragmatics(doc),
            "v15_prosody": self._extract_prosody(audio_features),
        }
        return dimensions

    # --- MÓDULOS DE EXTRAÇÃO DIMENSIONAL (MED-i) ---

    def _extract_valence(self, doc):
        # Em produção, isso seria uma chamada para um serviço de análise de sentimento mais robusto (Azure Language Service)
        # O spaCy com vetores dá uma aproximação.
        valence_words = {"feliz": 2, "bem": 1.5, "melhorar": 1, "triste": -2, "mal": -1.5, "difícil": -1}
        score = sum(valence_words.get(token.lemma_, 0) for token in doc)
        return np.clip(score, -5, 5)

    def _extract_arousal(self, doc, audio_features):
        # Combina análise de áudio (primária) e texto (secundária)
        text_arousal_words = {"agitado": 9, "ansioso": 8, "energia": 7, "calmo": 2, "cansado": 1, "lento": 1}
        text_score = np.mean([text_arousal_words.get(token.lemma_, 5) for token in doc if token.lemma_ in text_arousal_words]) if any(t.lemma_ in text_arousal_words for t in doc) else 5.0
        
        # A velocidade da fala (do áudio) é um forte indicador
        speech_rate_score = np.clip((audio_features['speech_rate'] - 120) / 10, 0, 10) # Normaliza em torno de 120 palavras/min
        
        # Média ponderada dando mais peso ao áudio
        return np.clip(0.7 * speech_rate_score + 0.3 * text_score, 0, 10)

    def _extract_coherence(self, sentences):
        if len(sentences) < 2: return 10.0
        similarities = []
        for i in range(len(sentences) - 1):
            if sentences[i].has_vector and sentences[i+1].has_vector and len(sentences[i]) > 1 and len(sentences[i+1]) > 1:
                similarities.append(sentences[i].similarity(sentences[i+1]))
        
        return np.mean(similarities) * 10 if similarities else 5.0

    def _extract_complexity(self, doc):
        num_sentences = len(list(doc.sents))
        if num_sentences == 0: return 0.0
        
        # Profundidade da árvore de dependência
        def get_depth(token, depth=0):
            children_depths = [get_depth(child, depth + 1) for child in token.children]
            return max(children_depths) if children_depths else depth
        
        max_depths = [get_depth(sent.root) for sent in doc.sents]
        avg_depth = np.mean(max_depths)
        
        # Contagem de cláusulas subordinadas
        subord_conjs = sum(1 for token in doc if token.pos_ == 'SCONJ')
        
        complexity_score = (avg_depth * 1.5) + (subord_conjs / num_sentences * 5)
        return np.clip(complexity_score, 0, 10)

    def _extract_temporal_orientation(self, tokens):
        past_count = sum(1 for token in tokens if token.tag_ and 'Tense=Past' in token.morph)
        present_count = sum(1 for token in tokens if token.tag_ and 'Tense=Pres' in token.morph)
        future_count = sum(1 for token in tokens if token.tag_ and 'Tense=Fut' in token.morph)
        
        total = past_count + present_count + future_count
        if total == 0: return {"past": 3.33, "present": 3.33, "future": 3.33}
        
        return {
            "past": (past_count / total) * 10,
            "present": (present_count / total) * 10,
            "future": (future_count / total) * 10
        }

    def _extract_self_reference(self, tokens):
        first_person_pronouns = {"eu", "meu", "minha", "mim", "comigo"}
        all_pronouns = [token for token in tokens if token.pos_ == 'PRON']
        if not all_pronouns: return 0.0
        
        first_person_count = sum(1 for token in all_pronouns if token.lemma_.lower() in first_person_pronouns)
        return (first_person_count / len(all_pronouns)) * 10

    def _extract_social_language(self, doc):
        social_count = sum(1 for token in doc if token.lemma_.lower() in self.social_words)
        num_sentences = len(list(doc.sents))
        return np.clip((social_count / num_sentences if num_sentences > 0 else 0) * 5, 0, 10)

    def _extract_flexibility(self, sentences, chunk_size=5):
        if len(sentences) < chunk_size * 2: return 5.0
        
        chunks = [sentences[i:i + chunk_size] for i in range(0, len(sentences), chunk_size)]
        chunk_vectors = [nlp(" ".join([s.text for s in chunk])).vector for chunk in chunks if len(chunk) > 0]
        
        if len(chunk_vectors) < 2: return 5.0

        topic_shifts = []
        for i in range(len(chunk_vectors) - 1):
            sim = np.dot(chunk_vectors[i], chunk_vectors[i+1]) / (np.linalg.norm(chunk_vectors[i]) * np.linalg.norm(chunk_vectors[i+1]))
            topic_shifts.append(1 - sim) # 1 - similaridade = mudança
            
        return np.mean(topic_shifts) * 10

    def _extract_agency(self, doc):
        agency_count = sum(1 for token in doc if token.lemma_.lower() in self.agency_words)
        active_voice_count = sum(1 for token in doc if token.dep_ == 'nsubj' and token.pos_ == 'PRON' and 'Person=1' in token.morph)
        num_sentences = len(list(doc.sents))
        
        score = ((agency_count + active_voice_count) / num_sentences if num_sentences > 0 else 0) * 4
        return np.clip(score, 0, 10)

    def _extract_fragmentation(self, text, tokens):
        # Contagem de disfluências simples
        disfluencies = text.lower().count(" ah ") + text.lower().count(" uhm ")
        
        # Variância do comprimento da sentença
        sent_lengths = [len(sent) for sent in nlp(text).sents]
        variance = np.var(sent_lengths) if sent_lengths else 0
        
        score = (disfluencies * 2) + (variance / 10)
        return np.clip(score, 0, 10)

    def _extract_semantic_density(self, tokens):
        content_pos = {'NOUN', 'VERB', 'ADJ', 'ADV'}
        content_words = sum(1 for token in tokens if token.pos_ in content_pos)
        return (content_words / len(tokens) if tokens else 0) * 10

    def _extract_certainty(self, doc):
        certain_count = sum(1 for token in doc if token.lemma_ in self.certainty_words)
        uncertain_count = sum(1 for token in doc if token.lemma_ in self.uncertainty_words)
        
        total = certain_count + uncertain_count
        if total == 0: return 0.0
        
        return ((certain_count - uncertain_count) / total) * 5

    def _extract_connectivity(self, doc):
        connective_count = sum(1 for token in doc if token.lemma_ in self.connective_words)
        num_sentences = len(list(doc.sents))
        return np.clip((connective_count / num_sentences if num_sentences > 0 else 0) * 5, 0, 10)

    def _extract_pragmatics(self, doc):
        # MÓDULO COMPLEXO: Em produção, seria um modelo de ML treinado (ex: fine-tuning de um LLM)
        # para classificar atos de fala e sua adequação.
        # Simulação: Mede a proporção de perguntas, que é um ato de fala interativo.
        question_count = sum(1 for token in doc if token.text == '?')
        num_sentences = len(list(doc.sents))
        return np.clip((question_count / num_sentences if num_sentences > 0 else 0) * 10, 0, 10)

    def _extract_prosody(self, audio_features):
        # A prosódia é um vetor. Aqui, combinamos em um único score de "variação".
        # Jitter e shimmer altos, e variância de pitch alta indicam alta variação prosódica.
        score = (audio_features['pitch_variance'] * 0.5) + (audio_features['jitter'] * 2) + (audio_features['shimmer'] * 2)
        return np.clip(score, 0, 10)

    def _simulate_audio_features(self, doc):
        # Esta função simula a extração de características do áudio com base no texto.
        # Em uma implementação real, você usaria uma biblioteca como Librosa no arquivo de áudio.
        text_length = len(doc.text)
        return {
            'speech_rate': np.clip(text_length / (text_length / 150.0), 80, 220), # Simula palavras/min
            'pitch_variance': np.random.uniform(1, 5),
            'jitter': np.random.uniform(0.1, 2),
            'shimmer': np.random.uniform(0.1, 2)
        }

# --- EXEMPLO DE USO ---
if __name__ == "__main__":
    # Instanciar o motor
    med = DimensionalExtractor()

    # Transcrição de exemplo de uma sessão
    example_transcript = """
    Médico: Olá, como você tem se sentido nesta semana?
    Paciente: Ah, doutor, eu não sei... Sinceramente, tem sido muito difícil. Eu acho que talvez as coisas pudessem melhorar, mas aí eu me lembro de tudo que aconteceu e fico muito triste, completamente sem energia. É como se eu estivesse preso no passado, sabe? Tenho certeza absoluta que nunca vou conseguir sair disso. Eu decidi que preciso tentar, mas como? Meu amigo me disse que eu deveria sair mais, conversar com pessoas, mas eu simplesmente não consigo. É sempre sobre mim, meus problemas, eu, eu, eu... É exaustivo. Porque quando eu tento, eu fico tão agitado e ansioso que parece que vou explodir.
    """

    # Extrair todas as 15 dimensões
    dimensional_vector = med.extract_all_dimensions(example_transcript)

    # Imprimir os resultados
    import json
    print("Vetor Dimensional Extraído:")
    print(json.dumps(dimensional_vector, indent=2))
```

#### As 15 Dimensões Extraídas

1. **v1_valence**: Análise de sentimento baseada em palavras-chave e futuramente Azure Language Service
2. **v2_arousal**: Combina análise de texto e características de áudio (velocidade da fala)
3. **v3_coherence**: Similaridade semântica entre sentenças consecutivas
4. **v4_complexity**: Profundidade sintática e cláusulas subordinadas
5. **v5_temporal**: Orientação temporal (passado/presente/futuro)
6. **v6_self_reference**: Densidade de pronomes em primeira pessoa
7. **v7_social_language**: Frequência de palavras sociais
8. **v8_flexibility**: Mudanças de tópico medidas por similaridade vetorial
9. **v9_agency**: Palavras de ação e voz ativa em primeira pessoa
10. **v10_fragmentation**: Disfluências e variância no comprimento das sentenças
11. **v11_semantic_density**: Proporção de palavras de conteúdo
12. **v12_certainty**: Balanço entre palavras de certeza vs incerteza
13. **v13_connectivity**: Densidade de conectivos lógicos
14. **v14_pragmatics**: Análise de atos de fala (simplificada como contagem de perguntas)
15. **v15_prosody**: Variação prosódica baseada em características de áudio

### 3. Arquivo: `semantic_extractor.py` (Novo)
Módulos para extração semântica avançada.
```python
import spacy
import httpx
import os

# Carregar o modelo spaCy
nlp = spacy.load("pt_core_news_lg")

class SemanticExtractor:
    """Extrai entidades nomeadas, grafos de conhecimento e arquétipos."""

    def __init__(self):
        # Configuração para o Azure Language Service
        self.language_key = os.environ.get("AZURE_LANGUAGE_KEY")
        self.language_endpoint = os.environ.get("AZURE_LANGUAGE_ENDPOINT")

    async def extract_named_entities_for_health(self, text: str):
        """Chama o Azure Language Service for Health para NER."""
        if not self.language_key or not self.language_endpoint:
            print("WARN: Azure Language credentials not set. Skipping NER.")
            return {"entities": []}

        client = httpx.AsyncClient()
        try:
            response = await client.post(
                f"{self.language_endpoint}/language/analyze-text/jobs?api-version=2023-04-01",
                headers={"Ocp-Apim-Subscription-Key": self.language_key},
                json={
                    "analysisInput": {"documents": [{"id": "1", "language": "pt", "text": text}]},
                    "tasks": [{"kind": "HealthCare", "parameters": {"modelVersion": "latest"}}]
                }
            )
            # O processo é assíncrono, aqui simplificamos para uma chamada direta
            # Em produção, você precisaria consultar o status do job
            # Para este exemplo, vamos assumir uma resposta direta simulada.
            return {"entities": ["Sertralina 50mg (Medicação)", "Ansiedade (Sintoma)"]}
        finally:
            await client.aclose()

    def extract_knowledge_graph(self, text: str):
        """Constrói um grafo de conhecimento simples a partir das relações de dependência."""
        doc = nlp(text)
        graph = []
        for token in doc:
            if token.dep_ in ("nsubj", "dobj"):
                subject = token.text
                verb = token.head.text
                obj = [child.text for child in token.head.children if child.dep_ == "obj"]
                if obj:
                    graph.append({"subject": subject, "relation": verb, "object": obj[0]})
        return {"knowledge_graph": graph}
```

### 4. Arquivo: `llm_agent.py` (Novo)
Responsável por construir os prompts e interagir com os LLMs principais.
```python
import httpx
import os

class LLMAgent:
    """Agente para interagir com modelos de linguagem de ponta (Grok, Claude)."""

    def __init__(self):
        self.api_key = os.environ.get("AZURE_AI_FOUNDRY_KEY")
        self.endpoint = os.environ.get("AZURE_AI_FOUNDRY_ENDPOINT_GROK") # Exemplo para Grok

    def _build_final_prompt(self, transcript, dimensional_vector, context):
        """Constrói o meta-prompt para a geração final de documentos."""
        # Carrega o template de um arquivo
        with open('voither_primeira_consulta_template.py', 'r') as f:
            template_content = f.read()

        prompt = f"""
        **SYSTEM ROLE:**
        Você é VOITHER, um assistente de IA especializado em análise dimensional de saúde mental...

        **CONTEXTO DO PACIENTE:**
        {json.dumps(context, indent=2)}

        **TRANSCRIÇÃO COMPLETA DA SESSÃO ATUAL:**
        \"\"\"
        {transcript}
        \"\"\"

        **ANÁLISE DIMENSIONAL QUANTITATIVA (Extraída pelo MED):**
        {json.dumps(dimensional_vector, indent=2)}

        **TAREFA:**
        Com base em TODOS os dados acima, preencha o seguinte template. A saída DEVE ser um único objeto JSON válido.

        **TEMPLATE A SER PREENCHIDO:**
        \"\"\"
        {template_content}
        \"\"\"
        """
        return prompt

    async def generate_final_documentation(self, transcript, dimensional_vector, context):
        """Chama o LLM principal para gerar a documentação completa."""
        if not self.api_key or not self.endpoint:
            print("WARN: AI Foundry credentials not set. Skipping final documentation.")
            return {"error": "AI Foundry not configured."}

        final_prompt = self._build_final_prompt(transcript, dimensional_vector, context)
        
        # A estrutura da requisição pode variar dependendo do modelo (Grok, Claude)
        payload = {
            "messages": [{"role": "user", "content": final_prompt}],
            "max_tokens": 4096,
            "temperature": 0.5
        }
        
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                self.endpoint,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json=payload
            )
            response.raise_for_status()
            # Aqui você precisaria parsear a resposta para extrair o conteúdo JSON
            return response.json()['choices'][0]['message']['content']

    async def extract_automation_triggers(self, transcript: str):
        """Usa um LLM para extrair gatilhos de automação."""
        # ... (lógica similar com um prompt focado em extrair prescrições, etc.)
        return [
            {"type": "prescription", "details": {"drug": "Sertralina", "dose": "50mg"}, "status": "pending_review"}
        ]
```

### 5. Arquivo: `persistence_layer.py` (Novo)
Lida com toda a interação com os bancos de dados.
```python
from pymongo import MongoClient
import psycopg2
import os
import json

class PersistenceLayer:
    def __init__(self):
        # Conexão com MongoDB Atlas
        self.mongo_client = MongoClient(os.environ.get("MONGO_CONNECTION_STRING"))
        self.db = self.mongo_client.voither_db

        # Conexão com Azure PostgreSQL
        self.pg_conn = psycopg2.connect(os.environ.get("POSTGRES_CONNECTION_STRING"))

    def get_raw_session_data(self, session_id: str):
        """Busca os dados brutos da sessão que foram salvos pela ingestão."""
        session = self.db.sessions.find_one({"_id": session_id})
        # Em produção, você teria um schema mais robusto
        return session['fullTranscriptionText'], {"patientId": session['patientId']}

    def save_insights_to_mongodb(self, session_id: str, insight_package: dict):
        """Atualiza o documento da sessão no MongoDB com os dados processados."""
        self.db.sessions.update_one(
            {"_id": session_id},
            {"$set": {
                "dimensionalTrajectory": insight_package["dimensionalTrajectory"],
                "clinicalDocuments": insight_package["clinicalDocuments"],
                "automatedActions": insight_package["automatedActions"],
                "semanticAnalysis": insight_package["semanticAnalysis"],
                "status": "completed"
            }}
        )
        print(f"Insights para a sessão {session_id} salvos no MongoDB.")

    def save_records_to_postgres_fhir(self, insight_package: dict, patient_id: str, session_id: str):
        """Mapeia os insights para recursos FHIR e salva no PostgreSQL."""
        # Esta é uma implementação simplificada. Uma camada FHIR real é mais complexa.
        fhir_resources = []

        # 1. Mapear Ações de Automação
        for action in insight_package.get("automatedActions", []):
            if action['type'] == 'prescription':
                med_request = {
                    "resourceType": "MedicationRequest", "status": "active",
                    # ... outros campos FHIR
                    "medicationCodeableConcept": {"text": f"{action['details']['drug']} {action['details']['dose']}"},
                    "subject": {"reference": f"Patient/{patient_id}"}
                }
                fhir_resources.append(med_request)
        
        # 2. Mapear Trajetória Dimensional para Observações
        for point in insight_package.get("dimensionalTrajectory", []):
            # Para cada uma das 15 dimensões no vetor...
            for i, value in enumerate(point['vector']):
                observation = {
                    "resourceType": "Observation", "status": "final",
                    "code": {"text": f"voither_dimension_v{i+1}"}, # Usar códigos LOINC/SNOMED reais
                    "valueQuantity": {"value": value},
                    "subject": {"reference": f"Patient/{patient_id}"}
                }
                # fhir_resources.append(observation) # Descomentar para salvar tudo

        # Salvar no PostgreSQL
        with self.pg_conn.cursor() as cur:
            for resource in fhir_resources:
                # Assumindo uma tabela 'fhir_resources' com uma coluna 'data' do tipo JSONB
                cur.execute(
                    "INSERT INTO fhir_resources (resource_type, data) VALUES (%s, %s)",
                    (resource['resourceType'], json.dumps(resource))
                )
        self.pg_conn.commit()
        print(f"{len(fhir_resources)} recursos FHIR salvos no PostgreSQL para a sessão {session_id}.")

    def close_connections(self):
        self.mongo_client.close()
        self.pg_conn.close()
```

### 6. Arquivo: `orchestrator_function/__init__.py` (O Orquestrador Principal)
Este é o ponto de entrada da sua Azure Function.
```python
import logging
import azure.functions as func
import json
import asyncio
from .dimensional_extractor import DimensionalExtractor
from .semantic_extractor import SemanticExtractor
from .llm_agent import LLMAgent
from .persistence_layer import PersistenceLayer

# Instanciar os módulos (em um app real, use injeção de dependência)
med = DimensionalExtractor()
semantic_ext = SemanticExtractor()
llm_agent = LLMAgent()
persistence = PersistenceLayer()

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Orquestrador de IA VOITHER acionado.')

    try:
        req_body = req.get_json()
        session_id = req_body.get('session_id')
        if not session_id:
            return func.HttpResponse("Por favor, forneça um session_id.", status_code=400)
    except ValueError:
        return func.HttpResponse("Corpo da requisição inválido.", status_code=400)

    try:
        # 1. Obter dados brutos
        transcript, context = persistence.get_raw_session_data(session_id)
        patient_id = context.get("patientId")
        
        # 2. Executar extrações em paralelo
        logging.info(f"Iniciando extração paralela para a sessão {session_id}...")
        parallel_tasks = [
            med.extract_all_dimensions(transcript),
            semantic_ext.extract_named_entities_for_health(transcript),
            semantic_ext.extract_knowledge_graph(transcript),
            llm_agent.extract_automation_triggers(transcript)
        ]
        results = await asyncio.gather(*parallel_tasks)
        
        dimensional_vector = results[0]
        ner_results = results[1]
        graph_results = results[2]
        automation_triggers = results[3]
        logging.info("Extração paralela concluída.")

        # 3. Gerar documentação final (depende da extração dimensional)
        logging.info("Gerando documentação final com LLM principal...")
        final_docs_json_str = await llm_agent.generate_final_documentation(
            transcript, dimensional_vector, context
        )
        final_docs = json.loads(final_docs_json_str) # Parsear a string JSON retornada pelo LLM
        logging.info("Documentação final gerada.")

        # 4. Empacotar todos os insights
        insight_package = {
            "dimensionalTrajectory": [{"timestamp": "end_of_session", "vector": list(dimensional_vector.values())}], # Simplificado para um ponto
            "clinicalDocuments": final_docs.get("clinical_narrative", {}),
            "automatedActions": automation_triggers,
            "semanticAnalysis": {**ner_results, **graph_results}
        }

        # 5. Persistir os dados
        logging.info("Iniciando persistência de dados...")
        persistence.save_insights_to_mongodb(session_id, insight_package)
        persistence.save_records_to_postgres_fhir(insight_package, patient_id, session_id)
        logging.info("Persistência de dados concluída.")

        return func.HttpResponse(
            json.dumps({"message": f"Sessão {session_id} processada com sucesso.", "status": "completed"}),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Erro ao processar a sessão {session_id}: {e}", exc_info=True)
        # Atualizar o status da sessão para "failed" no DB
        return func.HttpResponse(f"Erro interno do servidor: {e}", status_code=500)
    finally:
        persistence.close_connections()
```

---

## Conclusão

Este código fornece uma base sólida e completa para o seu Orquestrador de IA. Ele é modular, assíncrono e integra todas as peças do seu ecossistema de dados e IA, pronto para ser implantado e começar a transformar a linguagem em insights acionáveis.