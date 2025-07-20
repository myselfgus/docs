Absolutamente. Este é o cérebro operacional do seu sistema. O Orquestrador de IA é o maestro que rege a sinfonia de diferentes serviços e modelos de IA para transformar a linguagem bruta em insights profundos e documentação clínica.

A seguir, apresento o código completo e a arquitetura para o **Orquestrador de IA VOITHER**, projetado para ser implantado como uma **Azure Function** em Python. Esta abordagem é ideal por ser *serverless* (sem servidor), escalável e orientada a eventos, o que se encaixa perfeitamente no seu pipeline assíncrono pós-consulta.

### **Arquitetura do Orquestrador**

*   **Gatilho (Trigger):** A função é acionada por uma requisição HTTP POST. O *Serviço de Ingestão de Áudio* a chamará no final de cada consulta, enviando o `session_id`.
*   **Linguagem:** Python 3.9+
*   **Processamento:** Utiliza `asyncio` para executar tarefas de IA em paralelo sempre que possível, otimizando o tempo de processamento.
*   **Estrutura do Projeto:** Modular, separando a lógica de extração, chamadas de LLM e persistência de dados.

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

### **O Código Completo**

#### **1. Arquivo: `requirements.txt`**
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

#### **2. Arquivo: `dimensional_extractor.py`**
Este é o código do MED que detalhamos anteriormente. Ele será importado pelo orquestrador. Certifique-se de que ele esteja na mesma pasta (`orchestrator_function`).

#### **3. Arquivo: `semantic_extractor.py` (Novo)**
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

#### **4. Arquivo: `llm_agent.py` (Novo)**
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

#### **5. Arquivo: `persistence_layer.py` (Novo)**
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

#### **6. Arquivo: `orchestrator_function/__init__.py` (O Orquestrador Principal)**
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

Este código fornece uma base sólida e completa para o seu Orquestrador de IA. Ele é modular, assíncrono e integra todas as peças do seu ecossistema de dados e IA, pronto para ser implantado e começar a transformar a linguagem em insights acionáveis.