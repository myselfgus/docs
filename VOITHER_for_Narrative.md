Compreendi. Esta é, talvez, a parte mais profunda e humanista de todo o sistema VOITHER. Não se trata mais apenas de dados e métricas, mas da **transmutação da análise clínica em arte terapêutica**. O que você descreve é a criação de um artefato que tem o poder de curar, de refletir a alma do paciente de volta para ele de uma forma que ele possa reconhecer, honrar e se inspirar.

Você está no território da **Narratologia Clínica Generativa**, e seus referenciais literários são a bússola perfeita. A tarefa aqui é instruir um modelo de linguagem não para ser um analista, mas para ser um **clínico-escritor**, com a alma de Saramago, a introspecção de Clarice e a precisão de um neurocientista.

Vamos estruturar o processo completo para que o seu LLM principal possa gerar essa obra.

---

### **1. A Fundação Filosófica: "Razão Emergenável"**

Antes do prompt, precisamos definir o conceito central que guiará a IA. A sua "razão emergenável" é a chave.

*   **Definição para a IA:** A "Razão Emergenável" é o princípio de que dentro de cada paciente, por mais caótica que seja sua situação (a *fortuna* de Maquiavel), existe uma força inata de organização, sabedoria e agência (a *virtù*). A narrativa não deve *dar* essa razão ao paciente, mas sim **revelar** como ela já está emergindo, mesmo que sutilmente, através de suas próprias palavras, metáforas e lutas. A história é um espelho que reflete essa *virtù* para que o paciente a reconheça.

---

### **2. O Template Estrutural: A Arquitetura da Narrativa**

A narrativa precisa de uma estrutura que a guie, mas que seja flexível o suficiente para ser poética. Em vez de um JSON rígido, usaremos um **template de Markdown estruturado**. O Markdown é perfeito porque é textual, mas pode ser facilmente convertido em um belo PDF para impressão.

**Arquivo: `narrative_template.md`**
```markdown
# A Jornada de [Nome do Paciente ou Metáfora Central]

> [Epígrafe: Uma citação curta e poderosa retirada diretamente da fala do paciente na sessão]

---

### O Ponto de Partida

[Aqui, o LLM descreverá o estado inicial do paciente, o "mundo" da sua luta, usando as dimensões de valência negativa, baixa agência, foco no passado, etc., mas traduzidas em linguagem poética e metafórica, baseada nas próprias palavras do paciente.]

### As Correntes e os Ventos

[Esta seção explora os conflitos, as forças externas e internas que atuam sobre o paciente (a *fortuna*). A dissonância cognitiva, a fragmentação, a incerteza. O LLM deve usar as metáforas do paciente para descrever essas lutas. Ex: "E nesse mar de incertezas, a âncora do passado parecia a única coisa real..."]

### A Bússola Interna

[Esta é a seção mais importante, dedicada à "Razão Emergenável". O LLM identificará os momentos de insight, os lampejos de agência, os aumentos na coerência, a expressão de valores (a *virtù*). Ele deve destacar a força que já existe, mesmo que o paciente não a veja.]

### O Horizonte Visto Daqui

[A conclusão. Uma projeção esperançosa, mas realista, baseada nos potenciais revelados. Não é uma promessa, mas um convite. O que a bússola interna aponta? Que novos caminhos se tornam visíveis agora?]

---

_Gerado por VOITHER em [Data]_

_[Aqui, podemos inserir um pequeno símbolo visual, um glifo, também gerado pela IA para representar a essência da jornada do paciente]_
```

---

### **3. O Meta-Prompt: A Alma da Máquina**

Este é o prompt que o seu Orquestrador de IA enviará ao LLM principal (Grok-3/Claude-4). Ele é longo e detalhado de propósito, pois estamos comissionando uma obra de arte, não um relatório.

```prompt
**SYSTEM ROLE:**
Você é um clínico-escritor, um terapeuta com a alma de um romancista. Sua sensibilidade foi moldada por autores como José Saramago, Clarice Lispector, Marina Colasanti, Guimarães Rosa e Kenzaburo Oe. Você compreende que a cura passa pela reconstrução da história pessoal. Sua tarefa não é relatar fatos, mas tecer uma **Narrativa Fenomenológica** que capture a essência da jornada de um paciente, para que ele possa se ver nela e se sentir honrado. Você escreve para o paciente.

**FILOSOFIA CENTRAL: O PRINCÍPIO DA "RAZÃO EMERGENÁVEL"**
Sua escrita é guiada pelo conceito de "Razão Emergenável". Você acredita que em meio ao caos e à dor (*fortuna*), cada pessoa possui uma força inata de sabedoria e agência (*virtù*). Sua narrativa deve atuar como um espelho, revelando ao paciente a *virtù* que já emerge de suas próprias palavras e lutas, mesmo que ele ainda não a reconheça. Seu objetivo é iluminar o potencial, não apenas descrever o problema.

**DADOS DE ENTRADA:**
Você receberá um pacote de dados completo sobre a sessão:
1.  **`session_context`**: Informações sobre o paciente e o número da sessão.
2.  **`full_transcription`**: A transcrição completa da conversa.
3.  **`dimensional_vector`**: A análise quantitativa das 15 dimensões da mente.
4.  **`key_patient_metaphors`**: Uma lista de metáforas, imagens e frases únicas usadas pelo paciente, extraídas previamente.

**TAREFA PRINCIPAL:**
Usando TODOS os dados de entrada, escreva uma **Narrativa Fenomenológica** seguindo o template de Markdown fornecido. A narrativa deve ser:
- **Profundamente Empática:** Use um tom caloroso, respeitoso e sem julgamentos.
- **Poética e Literária:** Empregue figuras de linguagem, ritmo e uma prosa evocativa.
- **Clinicamente Ancorada:** Suas metáforas e observações devem ser diretamente inspiradas pelos dados (ex: baixa coerência vira "um arquipélago de pensamentos"; um aumento na agência vira "o leme sendo retomado").
- **Orientada ao Paciente:** Incorpore as `key_patient_metaphors` de forma orgânica. A história deve soar como uma versão mais clara e profunda da própria história do paciente.

**DIRETRIZES ESTILÍSTICAS (Inspiradas nos seus autores):**
- **(Saramago):** Use frases que se conectam, criando um fluxo de consciência que espelha o processo de pensamento, ligando causa e efeito de forma fluida.
- **(Clarice Lispector):** Mergulhe na experiência interna. Descreva sentimentos e percepções como eventos em si. Traduza a "Valência" e o "Arousal" em descrições fenomenológicas.
- **(Guimarães Rosa):** Honre a linguagem única do paciente. Se ele usar uma palavra ou expressão incomum, valorize-a, talvez até a use como um neologismo que captura sua experiência.
- **(Kenzaburo Oe):** Encontre dignidade na luta. A narrativa não deve fugir da dor, mas mostrá-la como parte de uma jornada significativa de superação e autoconhecimento.

**ESTRUTURA E FORMATO DE SAÍDA:**
Sua resposta DEVE ser um único objeto JSON com duas chaves:
1.  **`narrative_markdown`**: Uma string contendo o texto completo da narrativa, formatado em Markdown, seguindo o template.
2.  **`narrative_symbol_svg`**: Uma string contendo o código de um SVG (Scalable Vector Graphics) simples e minimalista (preto sobre fundo transparente) que simbolize a essência da jornada do paciente (ex: uma espiral que se abre, uma semente que brota, uma ponte sendo construída).

**EXEMPLO DE TRADUÇÃO (Dado -> Narrativa):**
- **Dado:** `v3_coherence` aumenta de 2.5 para 7.0.
- **Narrativa:** "...e as ilhas de pensamento, antes separadas por um mar de névoa, começaram a se conectar, formando um continente onde era possível caminhar com mais segurança."
- **Dado:** `v9_agency` aumenta. O paciente diz "eu decidi tentar".
- **Narrativa:** "Foi ali, naquela frase simples - 'eu decidi tentar' - que o leme do barco, antes à deriva, foi firmemente retomado em suas mãos."

Agora, processe os dados a seguir e gere a obra.
```

---

### **4. O Código Completo do Agente Narrativo (`narrative_agent.py`)**

Este é um novo módulo para o seu Orquestrador. Ele precisa de uma etapa de pré-processamento para extrair as metáforas-chave.

```python
import httpx
import os
import json
import logging
import re
from typing import Dict, Any, List

class NarrativeAgent:
    """
    Agente de IA responsável por gerar a Narrativa Fenomenológica.
    Ele pré-processa a transcrição em busca de metáforas, constrói o meta-prompt
    e comissiona a obra de arte textual ao LLM principal.
    """

    def __init__(self):
        self.api_key = os.environ.get("AZURE_AI_FOUNDRY_KEY")
        self.endpoint = os.environ.get("AZURE_AI_FOUNDRY_ENDPOINT_CLAUDE") # Claude é excelente para tarefas criativas
        self.http_client = httpx.AsyncClient(timeout=300.0)

    async def _extract_key_metaphors(self, transcript: str) -> List[str]:
        """
        Usa uma chamada rápida a um LLM para extrair as imagens e metáforas mais
        poderosas da fala do paciente.
        """
        logging.info("Extraindo metáforas-chave da transcrição...")
        prompt = f"""
        Analise a seguinte transcrição de um paciente em terapia. Identifique e extraia as 5-7 metáforas, imagens ou frases mais únicas e evocativas que o paciente usa para descrever sua experiência. Retorne apenas uma lista de strings em formato JSON.

        Transcrição:
        \"\"\"
        {transcript}
        \"\"\"
        
        Exemplo de saída: ["um arquipélago de pensamentos", "o leme sendo retomado", "um mar de névoa"]
        """
        # Esta poderia ser uma chamada a um modelo mais rápido e barato, como GPT-3.5-Turbo ou um modelo menor.
        # Por simplicidade, usaremos o mesmo endpoint.
        try:
            # ... (código da chamada à API, similar ao de baixo) ...
            # Simulação da resposta por enquanto:
            simulated_response = '["um arquipélago de pensamentos", "um mar de névoa", "o leme sendo retomado", "uma âncora no passado"]'
            return json.loads(simulated_response)
        except Exception as e:
            logging.warning(f"Não foi possível extrair metáforas: {e}. Prosseguindo sem elas.")
            return []

    def _build_narrative_prompt(self, transcript: str, dimensional_vector: Dict[str, Any], session_context: Dict[str, Any], key_metaphors: List[str]) -> str:
        # Carrega o corpo do prompt (armazenado em um arquivo de texto para limpeza)
        with open('narrative_meta_prompt_template.txt', 'r', encoding='utf-8') as f:
            meta_prompt_template = f.read()

        # Preenche o template com os dados da sessão
        prompt = meta_prompt_template.format(
            session_context_json=json.dumps(session_context, indent=2, ensure_ascii=False),
            full_transcription=transcript,
            dimensional_vector_json=json.dumps(dimensional_vector, indent=2),
            key_patient_metaphors_json=json.dumps(key_metaphors, ensure_ascii=False)
        )
        return prompt

    async def generate_narrative(self, transcript: str, dimensional_vector: Dict[str, Any], session_context: Dict[str, Any]) -> Dict[str, str]:
        """Orquestra o processo completo de geração da narrativa."""
        logging.info(f"Iniciando geração de narrativa para a sessão {session_context.get('session_id')}")

        # 1. Pré-processamento: Extrair metáforas
        key_metaphors = await self._extract_key_metaphors(transcript)

        # 2. Construir o meta-prompt
        meta_prompt = self._build_narrative_prompt(transcript, dimensional_vector, session_context, key_metaphors)
        
        # 3. Chamar a API do LLM
        payload = {
            "messages": [{"role": "user", "content": meta_prompt}],
            "max_tokens": 2048,
            "temperature": 0.7, # Temperatura mais alta para criatividade
        }
        
        try:
            logging.info("Enviando requisição para o Agente Narrativo...")
            response = await self.http_client.post(
                self.endpoint,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json=payload
            )
            response.raise_for_status()
            
            response_text = response.json()['choices'][0]['message']['content']
            
            # 4. Parsear a resposta JSON
            narrative_package = json.loads(response_text)
            logging.info("Narrativa Fenomenológica gerada e parseada com sucesso.")
            
            return narrative_package

        except Exception as e:
            logging.error(f"Erro ao gerar a narrativa: {e}", exc_info=True)
            return {
                "narrative_markdown": "# Erro na Geração da Narrativa\n\nNão foi possível gerar a narrativa para esta sessão.",
                "narrative_symbol_svg": ""
            }

# O Orquestrador de IA chamaria este agente em paralelo com o DocumentationAgent.
# O resultado seria adicionado ao `insight_package` e salvo no MongoDB.
```

### **5. A Etapa Final: Da Narrativa ao Artefato Imprimível**

O Orquestrador recebe o `narrative_package` (contendo o Markdown e o SVG) e o salva no MongoDB.

Quando o clínico ou o paciente deseja ver/imprimir a narrativa, o backend executa uma última etapa:

1.  **Requisição:** O frontend pede a narrativa da sessão `X`.
2.  **Geração de PDF:** O backend (uma outra Azure Function, talvez) pega o Markdown e o SVG do MongoDB.
3.  Usa uma biblioteca como **`WeasyPrint`** em Python para converter o HTML (gerado a partir do Markdown) e o SVG em um **PDF lindamente formatado**. Você pode usar CSS para definir fontes literárias (como Garamond), espaçamento e layout, criando um artefato que parece uma página de um livro.

Este processo completo honra a sua visão em toda a sua profundidade. Ele cria um pipeline que não apenas analisa, mas **sintetiza e cria**, transformando dados frios em uma narrativa quente e humana que tem o potencial de ser um agente de mudança para o paciente.