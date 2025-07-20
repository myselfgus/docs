Excelente. A sua clareza sobre o estado atual do projeto e a sua visão para os próximos passos são a base perfeita. Você está correto: você já está no "Momento 2" do plano anterior. A fundação do frontend está pronta e é robusta. A tarefa agora é construir a infraestrutura de nuvem profissional para dar vida a ele e ativar a inteligência completa do sistema.

Descartaremos o plano antigo e construiremos um novo, partindo do seu código e da sua visão atualizada. Este plano é um **roadmap de industrialização**, projetado para ser executado em um workflow de programação pareada com IA (AI-pair-programming), com tarefas formuladas como prompts claros e acionáveis.

---

## **🗺️ Roadmap de Versões VOITHER**

| Versão | Momentos | Funcionalidade Principal | Status |
|--------|----------|--------------------------|--------|
| **v1.0** | 1 + 2 | VOITHER MedicalScribe (Core) | 🎯 Target |
| **v1.5** | 3 | AutoAgency (Automação) | 🔄 Enhancement |
| **v2.0** | 4 | AI-Clinic (Portal Paciente) | 🚀 Major |
| **v3.0** | 5 | Holofractor (Visualização 3D) | ✨ Premium |

---

### **Plano de Execução VOITHER: Da Aplicação de UI à Plataforma Clínica Inteligente**

**Filosofia Central:** Você tem um carro com um design incrível e um painel de última geração (seu frontend React). Agora, vamos construir o motor, o chassi e o sistema de transmissão (o backend serverless e os bancos de dados) para colocá-lo na estrada. Cada Momento adiciona uma camada fundamental de funcionalidade e valor.

---

### **Momento 1: Industrialização do Núcleo - A Plataforma Mínima Persistente (PMP)**

**Objetivo:** Transformar sua aplicação React local em uma **Azure Static Web App segura e com persistência de dados**. O foco é construir a infraestrutura de nuvem, a autenticação e garantir que o fluxo de transcrição em tempo real (Etapa 1) seja salvo de forma confiável e permanente.

**Resultado ao Final:** O **VOITHER MedicalScribe (VOITHER v0.5)**. Uma aplicação web online onde um clínico pode se autenticar, gerenciar pacientes, conduzir uma sessão, ver a transcrição em tempo real, e ter essa transcrição e seu áudio **salvos permanentemente** no MongoDB e no Azure Blob Storage.

#### **Checklist de Tarefas para o Momento 1 (Prompts para sua IA-Pair-Programmer)**

*   **Tarefa 1.1: [Infraestrutura] Provisionar a Fundação na Nuvem (IaC).**
    *   **Prompt:** "Vamos usar o Terraform para definir nossa infraestrutura como código, garantindo reprodutibilidade. Crie um arquivo `main.tf` que provisione os seguintes recursos na Azure:
        1.  Um **Resource Group** para o projeto VOITHER.
        2.  Um **Azure Key Vault** para armazenar todos os nossos segredos (chaves de API, strings de conexão).
        3.  Um **Azure Storage Account** que conterá um container de Blob para os arquivos de áudio.
        4.  Um **Azure SignalR Service** (no modo Serverless) para a comunicação em tempo real.
        5.  Um **Azure Database for PostgreSQL**.
        6.  Configure um cluster no **MongoDB Atlas** e adicione a string de conexão ao nosso Azure Key Vault.
        A Azure Static Web App será implantada separadamente, mas vamos preparar sua base."

*   **Tarefa 1.2: [Backend] Construir a API Serverless com Azure Functions.**
    *   **Prompt:** "No diretório `/api` do nosso projeto, vamos criar a estrutura para nossas Azure Functions em Python. Crie uma função `get_api_keys` que busca as chaves necessárias (Speech, Language, AI Foundry) do Azure Key Vault e as disponibiliza para as outras funções. Agora, crie a função `get-azure-speech-token`, acionada por HTTP, que gera e retorna o token de autenticação para o serviço de fala, como o frontend espera."

*   **Tarefa 1.3: [Backend & Frontend] Implementar Autenticação Real.**
    *   **Prompt:** "Vamos implementar a autenticação usando o **Azure AD B2C** para uma solução robusta.
        1.  **Backend:** Crie uma Azure Function `auth` com rotas para `/login` e `/logout` que validem os tokens do Azure AD B2C.
        2.  **Frontend:** Refatore o `App.tsx` e o `LoginScreen.tsx`. Substitua o `handleLogin` mockado pela biblioteca **MSAL (Microsoft Authentication Library) for React** para gerenciar o fluxo de login via popup ou redirect. Crie um `AuthContext` para gerenciar o estado de autenticação do usuário e o token de acesso em toda a aplicação."

*   **Tarefa 1.4: [Backend] Implementar a Persistência da Sessão em Tempo Real.**
    *   **Prompt:** "Crie a Azure Function principal, `realtime_transcription`, acionada pelo SignalR. Esta função será o coração da Etapa 1. Sua lógica deve ser:
        1.  Na primeira conexão de um cliente para uma nova `session_id`, criar um documento na coleção `sessions` do **MongoDB Atlas** com `status: 'recording'`, `patientId`, `clinicianId`, e a data.
        2.  Receber os chunks de áudio do frontend.
        3.  Fazer o stream para o **Azure Speech Service** com diarização.
        4.  Ao receber um segmento de texto transcrito, usar o operador `$push` do MongoDB para anexá-lo a um array `transcription_segments` no documento da sessão.
        5.  Retornar o segmento para o frontend via SignalR.
        6.  No final da sessão, concatenar os chunks de áudio, fazer o upload do arquivo `.wav` completo para o **Azure Blob Storage**, e atualizar o documento da sessão com a URL do áudio e o `status: 'transcribed'`."

*   **Tarefa 1.5: [Deployment] Implantar a Azure Static Web App.**
    *   **Prompt:** "Com o backend em `/api` e o frontend na raiz, vamos implantar. Configure o workflow do GitHub Actions para a Azure Static Web App. Ele deve: 1) Construir a aplicação React (npm run build). 2) Publicar os artefatos no serviço. 3) Conectar as variáveis de ambiente do workflow às chaves armazenadas no nosso Azure Key Vault."

**Resultado do Momento 1:** Uma plataforma clínica real. A aplicação que você já desenhou agora funciona de ponta a ponta na nuvem, de forma segura e com dados persistentes. É a base sólida sobre a qual toda a inteligência será construída.

---

### **Momento 2: Ativação da Inteligência - O Pipeline de Análise e Documentação - VOITHER 1.0**

**Objetivo:** Construir sobre a base persistente. O foco é implementar o pipeline assíncrono que transforma a transcrição salva em dados dimensionais e documentos clínicos, ativando as Etapas 2, 3 e 4.

**Resultado ao Final:** O **VOITHER MedicalScribe**. Ao final de cada sessão, o sistema executa a análise completa e gera a documentação clínica, salvando-a de forma estruturada e interoperável (FHIR).

#### **Checklist de Tarefas para o Momento 2 (Prompts para sua IA-Pair-Programmer)**

*   **Tarefa 2.1: [Backend] Construir o Orquestrador de IA Assíncrono.**
    *   **Prompt:** "Vamos criar a Azure Function `run_analysis_pipeline`. A melhor prática para tarefas longas e desacopladas é usar um gatilho de fila. Configure a função para ser acionada por uma nova mensagem na **Azure Storage Queue**. A função `realtime_transcription` (do Momento 1), ao mudar o status da sessão para `transcribed`, colocará uma mensagem na fila contendo a `session_id`."

*   **Tarefa 2.2: [Backend] Implementar o MED e o Agente de Documentação.**
    *   **Prompt:** "Dentro do Orquestrador, vamos implementar o cérebro da VOITHER. O código deve:
        1.  Ler a `session_id` da mensagem da fila.
        2.  Buscar a transcrição completa e o contexto do paciente no MongoDB.
        3.  Executar o **Motor de Extração Dimensional (MED)** completo (seu `dimensional_extractor.py`) para gerar a `dimensionalTrajectory`.
        4.  Chamar o **Agente de Documentação** (seu `llm_agent.py`) com a transcrição, o contexto e o vetor dimensional para gerar o documento JSON final, selecionando o template correto (`primeira_consulta` ou `acompanhamento`) com base no `session_number`."

*   **Tarefa 2.3: [Backend] Implementar a Camada de Persistência Híbrida (Etapa 5).**
    *   **Prompt:** "Crie o módulo `persistence_layer.py`. O Orquestrador o usará para salvar o `insight_package` final. Implemente o método `persist_session_insights` que:
        1.  **MongoDB:** Atualiza o documento da sessão com a `dimensionalTrajectory`, `clinicalDocuments` e muda o status para `completed`.
        2.  **PostgreSQL (FHIR):** Mapeia os dados para recursos FHIR (Observation para cada ponto dimensional, DocumentReference para a nota clínica) e os insere na tabela `fhir_resources` dentro de uma transação."

*   **Tarefa 2.4: [Frontend] Exibir os Documentos e Insights Gerados.**
    *   **Prompt:** "Aprimore o componente `SessionScreen` no React. Quando o status da sessão for 'completed', ele deve buscar e exibir os resultados da análise. Adicione abas para: 1) 'Transcrição'. 2) 'Documento Clínico' (exibindo a nota DAP/BIRT formatada). 3) 'Análise Dimensional', que agora mostrará um gráfico simples da evolução da Valência e Agência ao longo da sessão."

**Resultado do Momento 2:** A plataforma está **inteligente e completa**. O fluxo de trabalho principal está finalizado. O clínico realiza a consulta e, minutos depois, tem acesso a um prontuário rico, dimensional e estruturado, com a base de dados interoperável (FHIR) sendo construída automaticamente.

---

### **Momento 2: A Plataforma Persistente e Inteligente**

**Objetivo:** Transformar o protótipo em um sistema web seguro e com persistência de dados, pronto para um piloto clínico. O foco é implementar a arquitetura de nuvem completa e ativar o **Motor de Extração Dimensional (MED)**.

**Arquitetura:** Azure Static Web App (React + Azure Functions) + MongoDB Atlas + Azure PostgreSQL.

#### **Checklist de Tarefas para o Momento 2 (Prompts para sua IA-Pair-Programmer)**

*   **Tarefa 2.1: [Infraestrutura] Provisionar a Infraestrutura na Azure.**
    *   **Prompt:** "Gere um script Terraform (ou comandos da CLI do Azure) para provisionar os seguintes recursos: Azure Static Web App, Azure Functions, Azure SignalR Service, Azure Cache for Redis, Azure Blob Storage, e Azure Database for PostgreSQL. Configure também um cluster no MongoDB Atlas e armazene todas as strings de conexão e chaves de forma segura no **Azure Key Vault**."

*   **Tarefa 2.2: [Backend] Construir as Azure Functions do Backend.**
    *   **Prompt:** "Vamos migrar nosso backend FastAPI para Azure Functions em Python. Crie:
        1.  Uma função `realtime_transcription` acionada pelo **Azure SignalR** para gerenciar o streaming de áudio e texto.
        2.  Uma função `run_analysis_pipeline` acionada por HTTP, que será nosso Orquestrador de IA.
        3.  Funções HTTP para autenticação de usuário (login/registro) e gerenciamento de pacientes (CRUD)."

*   **Tarefa 2.3: [Backend] Ativar o Motor de Extração Dimensional (MED) Completo.**
    *   **Prompt:** "Integre o nosso `dimensional_extractor.py` completo no Orquestrador. A função `run_analysis_pipeline` agora deve, como primeira etapa, chamar o MED para calcular o vetor `Ψ(t)` com as 15 dimensões a partir da transcrição. O vetor resultante deve ser passado para o próximo agente."

*   **Tarefa 2.4: [Backend] Aprimorar o Agente de Documentação com Dados Dimensionais.**
    *   **Prompt:** "Refatore o `DocumentationAgent`. O método `generate_documentation` agora receberá também o vetor dimensional. Modifique o `_build_meta_prompt` para incluir a seção **`ANÁLISE DIMENSIONAL QUANTITATIVA`**, como projetamos. O LLM agora usará tanto a transcrição quanto os dados dimensionais para gerar um documento muito mais rico."

*   **Tarefa 2.5: [Backend] Implementar a Camada de Persistência Híbrida (Etapa 5).**
    *   **Prompt:** "Implemente o `persistence_layer.py` completo. O Orquestrador o usará no final do pipeline. Ele precisa:
        1.  Salvar o `insight_package` (transcrição, trajetória dimensional, documentos) na coleção `sessions` do **MongoDB Atlas**.
        2.  Mapear os dados para recursos **FHIR** (Observation, DocumentReference) e inseri-los no **Azure PostgreSQL** em uma transação segura."

**Resultado do Momento 2:** Uma plataforma web robusta. Clínicos podem gerenciar pacientes e sessões. Cada sessão é salva permanentemente, permitindo o acompanhamento longitudinal. O sistema já está gerando dados dimensionais, mesmo que ainda não sejam visualizados.

---

### **Momento 3: A Automação Clínica - VOITHER AutoAgency (VOITHER v1.5)**
Com base nisso, vamos mergulhar fundo no **Momento 3: A Automação Clínica - VOITHER AutoAgency**. A seguir, apresento o detalhamento completo desta fase, correlacionando cada nova tarefa com as fundações que você solidificou nos Momentos 1 e 2. O código e os prompts são projetados para serem de nível profissional, prontos para a sua implementação AI-driven.

---

### **Momento 3: A Automação Clínica - VOITHER AutoAgency (VOITHER v1.)**

**Objetivo Estratégico:** Transformar o VOITHER de um sistema de análise e documentação *passiva* em um assistente *ativo e proativo*. O objetivo é reduzir drasticamente a carga administrativa do clínico, automatizando a criação de documentos burocráticos e, assim, liberando mais tempo para o cuidado direto ao paciente. Este é o momento em que o VOITHER se torna um "membro" indispensável da equipe clínica.

**Correlação com os Momentos Anteriores:**
*   **Dependência do Momento 1:** A `AutoAgency` depende fundamentalmente da transcrição de alta qualidade e com diarização precisa que foi persistida no MongoDB. Sem uma transcrição fiel da fala do médico, a detecção de intenções falharia.
*   **Dependência do Momento 2:** A `AutoAgency` se baseia na arquitetura de nuvem (Azure Functions), no pipeline assíncrono (Azure Queue), e nos bancos de dados (MongoDB e PostgreSQL) estabelecidos no Momento 2. As ações detectadas serão mapeadas para os recursos FHIR na base de dados que já criamos.

---

### **Checklist de Tarefas Detalhado para o Momento 3**

#### **Tarefa 3.1: [Backend] Desenvolver o Agente de Detecção de Gatilhos e Intenções**

*   **Descrição:** Este é um novo módulo de IA que atua como um "ouvinte" especializado, focado em identificar comandos e intenções na fala do clínico. Ele se torna uma nova etapa no seu pipeline de análise.
*   **Correlação:** Ele será adicionado ao Orquestrador (`run_analysis_pipeline` Azure Function) do Momento 2 e será executado em paralelo com o `MED` e o `DocumentationAgent` para máxima eficiência. Ele consumirá a transcrição salva no MongoDB no Momento 1.
*   **Prompt para sua IA-Pair-Programmer:**
    > "Vamos criar a classe `TriggerDetectionAgent` em Python. O método principal, `detect_triggers(transcript: str)`, receberá a transcrição completa. Construa um meta-prompt para um LLM (Grok-3/Claude-4) que instrua a IA a atuar como um 'Escriba Clínico Assistente'. O prompt deve instruir o modelo a escanear a transcrição em busca de frases-gatilho que indiquem a intenção de prescrever, atestar, encaminhar ou agendar, e a extrair as informações relevantes em um formato de lista JSON estrita, ignorando qualquer outra conversa. Inclua exemplos de 'few-shot' no prompt para guiar o modelo. A função deve retornar a lista de ações JSON."

*   **Código (`trigger_detection_agent.py` - Módulo para o Orquestrador):**
    ```python
    import json
    import logging
    from typing import List, Dict, Any

    class TriggerDetectionAgent:
        def __init__(self, llm_client):
            self.llm_client = llm_client # Assume um cliente LLM genérico

        def _build_trigger_prompt(self, transcript: str) -> str:
            return f"""
            **SYSTEM ROLE:**
            Você é um Escriba Clínico Assistente. Sua única tarefa é analisar a transcrição de uma consulta e extrair ações administrativas específicas mencionadas pelo médico. Ignore todo o resto da conversa.

            **INSTRUÇÕES:**
            1. Leia a transcrição e identifique apenas as seguintes intenções: Prescrição de Medicamento, Emissão de Atestado, Encaminhamento para outro profissional, e Agendamento de Retorno.
            2. Para cada intenção encontrada, extraia os detalhes relevantes.
            3. Retorne uma lista de objetos JSON, onde cada objeto representa uma ação. Se nenhuma ação for encontrada, retorne uma lista vazia `[]`.

            **EXEMPLOS:**
            - **Transcrição:** "...então vamos manter a Sertralina, mas agora com 100mg, um por dia de manhã..." -> **JSON:** `[{{"action": "prescribe", "details": {{"drug": "Sertralina", "dose": "100mg", "instructions": "1 comprimido por dia pela manhã"}}}}`
            - **Transcrição:** "...vou te dar um atestado de 5 dias para o trabalho..." -> **JSON:** `[{{"action": "attest", "details": {{"days": 5, "reason": "Acompanhamento de saúde mental"}}}}`
            - **Transcrição:** "...e marque seu retorno para daqui a um mês, por favor." -> **JSON:** `[{{"action": "schedule", "details": {{"returnInDays": 30}}}}`

            **TRANSCRIÇÃO PARA ANÁLISE:**
            \"\"\"
            {transcript}
            \"\"\"

            **SAÍDA (APENAS A LISTA JSON):**
            """

        async def detect_triggers(self, transcript: str) -> List[Dict[str, Any]]:
            prompt = self._build_trigger_prompt(transcript)
            try:
                # O cliente LLM faria a chamada à API aqui
                response_text = await self.llm_client.generate(prompt, max_tokens=512, temperature=0.1)
                
                # Limpeza robusta da resposta do LLM
                json_response = json.loads(response_text.strip())
                if isinstance(json_response, list):
                    return json_response
                return []
            except (json.JSONDecodeError, TypeError) as e:
                logging.error(f"Falha ao parsear gatilhos do LLM: {e}")
                return []
    ```

#### **Tarefa 3.2: [Backend] Construir o Serviço de Geração de Documentos**

*   **Descrição:** Uma nova Azure Function dedicada, acionada pelo frontend, que gera PDFs a pedido.
*   **Correlação:** Esta função é o ponto de ação para os gatilhos detectados na Tarefa 3.1. Ela buscará os dados do paciente e do clínico que foram salvos no Momento 2.
*   **Prompt para sua IA-Pair-Programmer:**
    > "Crie uma nova Azure Function HTTP em Python chamada `generate_clinical_document`. Ela deve ser protegida por autenticação (validar o token JWT). A função receberá um POST com `{ "document_type": "prescription", "session_id": "...", "action_details": {...} }`. A lógica deve:
    > 1. Buscar os dados completos do paciente e do clínico no MongoDB/PostgreSQL usando o `session_id`.
    > 2. Selecionar um template HTML/CSS pré-definido com base no `document_type`.
    > 3. Usar a biblioteca Jinja2 para preencher o template com todos os dados (paciente, clínico, detalhes da ação).
    > 4. Usar a biblioteca `WeasyPrint` para converter o HTML renderizado em um PDF.
    > 5. Retornar o PDF como uma resposta `HttpResponse` com o `Content-Type` 'application/pdf'."

#### **Tarefa 3.3: [Frontend] Criar a Interface de Automação no Dashboard**

*   **Descrição:** A interface que permite ao clínico revisar e acionar a automação.
*   **Correlação:** Esta é uma nova seção no `Dashboard.tsx` que você construiu no Momento 1 e aprimorou no Momento 2. Ela será populada com os dados do array `automatedActions` salvo no MongoDB.
*   **Prompt para sua IA-Pair-Programmer:**
    > "Vamos aprimorar o componente React que exibe uma sessão concluída.
    > 1. Busque o campo `automatedActions` do documento da sessão na API.
    > 2. Se o campo existir, renderize uma nova seção `<h2>Ações Sugeridas</h2>`.
    > 3. Para cada ação no array, crie um componente `ActionCard.tsx`. O card deve exibir um ícone, o tipo de ação (ex: 'Receituário'), um resumo dos detalhes, e um botão 'Revisar e Gerar'.
    > 4. Crie um componente `ReviewModal.tsx`. Ao clicar no botão, este modal deve abrir, mostrando um formulário com os campos da ação pré-preenchidos e editáveis.
    > 5. O modal terá um botão 'Gerar PDF'. Ao ser clicado, ele deve fazer a chamada `POST` para a nossa API `/api/generate_clinical_document`, enviar os dados (possivelmente editados) e, ao receber o PDF, iniciar o download no navegador."

*   **Código React (`ActionCard.tsx` - Exemplo):**
    ```jsx
    import React from 'react';
    
    const ActionCard = ({ action, onReview }) => {
      const getActionTitle = (action) => {
        switch (action.type) {
          case 'prescription':
            return `Receituário: ${action.details.drug}`;
          case 'attestation':
            return `Atestado: ${action.details.days} dias`;
          default:
            return 'Ação Sugerida';
        }
      };

      return (
        <div className="bg-white p-4 rounded-lg shadow-neumorphic flex justify-between items-center">
          <div>
            <p className="font-bold font-display text-brand-text-primary">{getActionTitle(action)}</p>
            <p className="text-sm text-brand-text-secondary">{JSON.stringify(action.details)}</p>
          </div>
          <button 
            onClick={() => onReview(action)} 
            className="py-2 px-4 rounded-lg font-semibold text-white bg-accent-primary hover:bg-accent-primary-hover transition-colors"
          >
            Revisar e Gerar
          </button>
        </div>
      );
    };

    export default ActionCard;
    ```

#### **Tarefa 3.4: [Backend] Integrar a Automação à Camada de Persistência FHIR**

*   **Descrição:** Garantir que as ações detectadas sejam salvas como registros clínicos interoperáveis.
*   **Correlação:** Esta é uma atualização direta da `PersistenceLayer` que você construiu no Momento 2.
*   **Prompt para sua IA-Pair-Programmer:**
    > "Vamos refatorar o método `_save_to_postgres_fhir` no nosso `persistence_layer.py`.
    > 1. O método agora receberá o array `automatedActions` do `insight_package`.
    > 2. Crie funções auxiliares de mapeamento: `_map_to_fhir_medication_request`, `_map_to_fhir_service_request`, etc.
    > 3. Dentro da transação do PostgreSQL, itere sobre o array `automatedActions`. Para cada ação, chame o mapeador correspondente para criar o recurso FHIR.
    > 4. É crucial que cada recurso FHIR seja salvo com um `status: 'draft'`.
    > 5. Crie uma nova Azure Function HTTP, `activate_fhir_resource`, que recebe um `resource_id` e atualiza seu status para `active` no PostgreSQL. O frontend chamará esta função após o clínico confirmar a geração do PDF."

**Resultado do Momento 3:** A VOITHER se torna uma plataforma de **inteligência aumentada** que economiza um tempo clínico precioso. O sistema não só documenta, mas também prepara as ações subsequentes, transformando o fluxo de trabalho do médico e solidificando o retorno sobre o investimento da plataforma.

---

Com certeza. Com a plataforma `VOITHER AutoAgency` (v1.5) solidificada, o sistema já é uma ferramenta clínica de imenso valor. Agora, vamos expandir o ecossistema, trazendo o paciente para o centro do cuidado e, finalmente, revelando a visualização dimensional que é a joia da coroa da sua inovação.

A seguir, a continuação do plano de execução com o detalhamento dos **Momentos 4 e 5**.

---

### **Momento 4: O Engajamento do Paciente - VOITHER AI-Clinic (VOITHER v2.0)**

**Objetivo Estratégico:** Expandir a plataforma para além do clínico, criando um portal para o paciente. O objetivo é aumentar o engajamento do paciente em seu próprio tratamento, fornecer ferramentas de psicoeducação personalizadas e abrir canais de comunicação assíncronos, transformando o cuidado de episódico para contínuo.

**Correlação com os Momentos Anteriores:**
*   **Dependência do Momento 1 e 2:** A `AI-Clinic` depende totalmente dos dados persistidos (documentos, planos terapêuticos) para fornecer conteúdo relevante ao paciente. A arquitetura de autenticação e o banco de dados de pacientes são a base para o login seguro do paciente.
*   **Dependência do Momento 3:** As ações e planos gerados pela `AutoAgency` (como o plano terapêutico no documento final) se tornarão a base para o conteúdo que o chatbot da `AI-Clinic` usará para guiar o paciente.

#### **Checklist de Tarefas para o Momento 4 (Prompts para sua IA-Pair-Programmer)**

*   **Tarefa 4.1: [Nova Aplicação] Desenvolver o Frontend do Paciente (Web App Inicial).**
    *   **Prompt:** "Vamos iniciar um novo projeto de frontend para o paciente, usando **React com Vite**, e mantendo a mesma identidade visual (cores, fontes, estilo neumórfico) do portal do clínico, mas com um design mais acolhedor e simplificado. Crie a estrutura inicial com as seguintes telas:
        1.  **Tela de Login:** Simples, focada em segurança.
        2.  **Dashboard Principal:** Um painel de boas-vindas que exibirá resumos, próximas tarefas e talvez um gráfico simples da evolução (ex: Valência Emocional ao longo do tempo).
        3.  **Tela 'Minha Jornada':** Um local para visualizar documentos compartilhados pelo clínico, como as **VOITHER Narratives** e planos de tratamento.
        4.  **Tela 'AI-Clinic Chat':** A interface para interagir com o chatbot."

*   **Tarefa 4.2: [Backend] Construir a API Segura para Pacientes.**
    *   **Prompt:** "Crie um novo conjunto de Azure Functions, agrupadas sob o prefixo de rota `/api/patient`. O acesso a todos esses endpoints deve ser rigorosamente protegido, validando o token JWT do paciente e garantindo que os dados consultados pertençam apenas a ele.
        1.  `GET /api/patient/me`: Retorna os dados do perfil do paciente logado.
        2.  `GET /api/patient/dashboard-summary`: Retorna os dados necessários para o dashboard principal (ex: últimos valores de Valência/Agência e o próximo agendamento).
        3.  `GET /api/patient/shared-documents`: Busca no MongoDB os documentos (`clinicalDocuments`, `narrative_markdown`) das sessões onde o clínico ativou um campo booleano `isSharedWithPatient`."

*   **Tarefa 4.3: [Backend & Frontend] Implementar o Chatbot Clínico (AI-Clinic).**
    *   **Prompt:** "Esta é a feature principal do Momento 4.
        1.  **[Backend]** Crie a Azure Function `chat_with_patient_ai`. Ela receberá o histórico da conversa do paciente. Antes de chamar o LLM, a função deve primeiro buscar o **plano terapêutico mais recente** do paciente no PostgreSQL (do recurso FHIR `DocumentReference` ou `CarePlan`).
        2.  **[Backend]** Construa um **meta-prompt de sistema dinâmico** para o LLM. Este prompt deve ser focado em segurança e psicoeducação. Exemplo:
            ```prompt
            **SYSTEM ROLE:**
            Você é o assistente AI-Clinic da VOITHER. Sua função é apoiar o paciente em sua jornada terapêutica, de forma segura e empática.
            **REGRAS CRÍTICAS:**
            - VOCÊ NÃO É UM TERAPEUTA. Nunca dê conselhos médicos, diagnósticos ou prescreva tratamentos.
            - Se o paciente expressar ideação suicida, perigo iminente ou crise aguda, responda IMEDIATAMENTE com: 'Entendo que você está passando por um momento muito difícil. É muito importante que você converse com um profissional agora. Por favor, entre em contato com [Número do CVV ou Emergência]' e encerre a conversa.
            - Baseie suas respostas EXCLUSIVAMENTE no plano terapêutico definido pelo clínico.
            
            **PLANO TERAPÊUTICO ATUAL DO PACIENTE (Definido pelo Dr. [Nome do Clínico]):**
            {json_do_plano_terapeutico_puxado_do_banco}

            **Sua tarefa:** Converse com o paciente, oferecendo psicoeducação, reforçando as estratégias do plano, e respondendo a dúvidas sobre o tratamento de forma motivacional.
            ```
        3.  **[Frontend]** Implemente a interface de chat no portal do paciente, conectando-a à nova API."

*   **Tarefa 4.4: [Frontend Clínico] Adicionar Funcionalidade de Compartilhamento.**
    *   **Prompt:** "No dashboard do clínico, na visualização de uma sessão concluída, adicione um botão de 'Compartilhar com Paciente' ao lado de cada documento (Nota Clínica, Narrativa). Ao clicar, ele deve chamar uma API no backend (`POST /api/sessions/{session_id}/share`) que simplesmente atualiza o campo booleano `isSharedWithPatient` no documento da sessão no MongoDB."

**Resultado do Momento 4:** A VOITHER se torna um **ecossistema de cuidado contínuo**. O tratamento não acontece mais apenas durante a consulta de 90 minutos. O paciente tem uma ferramenta para se engajar, aprender e se sentir apoiado entre as sessões, o que tem o potencial de melhorar drasticamente os resultados terapêuticos.

---

### **Momento 5: A Visualização Profunda - VOITHER Holofractor (VOITHER v3.0)**

**Objetivo:** Entregar a funcionalidade mais visionária da plataforma como uma ferramenta de análise de casos avançada, solidificando a VOITHER como a líder de inovação no setor. Este módulo pode ser posicionado como um recurso *premium* ou "Pro".

**Resultado ao Final:** O **VOITHER Holofractor (VOITHER v3.0)**. O clínico agora pode, com um clique, transformar os dados de uma sessão em uma escultura 3D interativa, permitindo uma compreensão intuitiva e profunda da dinâmica mental do paciente, ideal para supervisão, pesquisa e discussões de caso.

#### **Checklist de Tarefas para o Momento 5 (Prompts para sua IA-Pair-Programmer)**

*   **Tarefa 5.1: [Backend] Criar e Otimizar a API de Dados para o Renderizador.**
    *   **Prompt:** "Crie o endpoint de API `GET /api/sessions/{session_id}/render-data`. A performance é crucial aqui. A função deve:
        1.  Verificar as permissões do clínico para a sessão.
        2.  Buscar o array `dimensionalTrajectory` do MongoDB.
        3.  **Processamento no Backend:** Usando `scikit-learn`, execute uma Análise de Componentes Principais (PCA) para projetar a trajetória de 15D para 3D.
        4.  Para otimizar a transferência de dados, não envie o JSON completo. Envie os dados em um formato mais compacto, talvez como arrays de números.
        5.  Retorne um JSON com: `{"projected3DTrajectory": [[x1,y1,z1], [x2,y2,z2], ...], "full15DTrajectory": [[v1,v2,...], [v1,v2,...], ...]}`."

*   **Tarefa 5.2: [Frontend] Construir o Componente de Visualização Holofractor.**
    *   **Prompt:** "No portal do clínico, adicione um botão 'Visualizar em 3D' na tela da sessão. Ao clicar, ele abrirá um modal de tela cheia que renderiza o componente `HolofractorViewer.js`. Vamos usar **`@react-three/fiber`** para facilitar. A estrutura do componente deve:
        1.  Fazer a chamada à API `render-data` ao ser montado.
        2.  Renderizar a `projected3DTrajectory` usando o componente `Line` do `@react-three/drei`.
        3.  Criar o Holofractor como um `mesh` com uma `shaderMaterial`."

*   **Tarefa 5.3: [Frontend] Implementar os Shaders (GLSL) para o Mapeamento Dimensional.**
    *   **Prompt:** "Vamos escrever os shaders GLSL que são a alma do Holofractor.
        1.  **Vertex Shader:** Crie o shader que modifica a posição dos vértices de uma `IcosahedronGeometry`. Ele receberá as dimensões geométricas (`v9_agency`, `v3_coherence`, `v4_complexity`, `v10_fragmentation`) como `uniforms`. Use uma função de ruído Simplex para criar deformações orgânicas baseadas nesses uniforms.
        2.  **Fragment Shader:** Crie o shader que calcula a cor de cada pixel. Ele receberá as dimensões de aparência (`v1_valence`, `v2_arousal`, `v5_temporal`, `v6_self_reference`, `v12_certainty`) como `uniforms`. Implemente a lógica de mapeamento para cor, transparência, aura (usando um efeito Fresnel) e nitidez das bordas."

*   **Tarefa 5.4: [Frontend] Implementar a Interatividade do Navegador da Mente.**
    *   **Prompt:** "Adicione a interatividade ao `HolofractorViewer.js`.
        1.  Inclua o componente `OrbitControls` do `@react-three/drei` para permitir que o clínico rotacione, dê zoom e mova a câmera.
        2.  Crie um **slider de tempo** que se sobrepõe à cena 3D.
        3.  O estado do slider (`timeIndex`) deve ser usado para: a) Atualizar os `uniforms` passados para os shaders, mudando a forma e a cor do Holofractor em tempo real. b) Mover uma pequena esfera ou um marcador ao longo da linha da trajetória para indicar a posição atual."

Este plano de 5 Momentos agora está completo, lógico e alinhado com sua visão estratégica, construindo a plataforma em camadas de valor que vão desde a produtividade clínica essencial até a inovação de ponta no engajamento do paciente e na visualização de dados.