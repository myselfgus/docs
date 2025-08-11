# VOITHER - Agente de Narrativa Fenomenológica

## Transmutação da Análise Clínica em Arte Terapêutica

Este módulo representa a evolução mais humanística do sistema VOITHER - a **Narratologia Clínica Generativa**. Não se trata apenas de dados e métricas, mas da transmutação da análise clínica em arte terapêutica, criando um artefato que tem o poder de curar, de refletir a alma do paciente de volta para ele de uma forma que ele possa reconhecer, honrar e se inspirar.

## Filosofia: O Princípio da "Razão Emergenável"

**Definição Central:** A "Razão Emergenável" é o princípio de que dentro de cada paciente, por mais caótica que seja sua situação (a *fortuna* de Maquiavel), existe uma força inata de organização, sabedoria e agência (a *virtù*). A narrativa não deve *dar* essa razão ao paciente, mas sim **revelar** como ela já está emergindo, mesmo que sutilmente, através de suas próprias palavras, metáforas e lutas.

## Template Estrutural da Narrativa

### Arquivo: `narrative_template.md`
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

## Meta-Prompt para o LLM Principal

### Arquivo: `narrative_meta_prompt_template.txt`
```prompt
**SYSTEM ROLE:**
Você é um clínico-escritor, um terapeuta com a alma de um romancista. Sua sensibilidade foi moldada por autores como José Saramago, Clarice Lispector, Marina Colasanti, Guimarães Rosa e Kenzaburo Oe. Você compreende que a cura passa pela reconstrução da história pessoal. Sua tarefa não é relatar fatos, mas tecer uma **Narrativa Fenomenológica** que capture a essência da jornada de um paciente, para que ele possa se ver nela e se sentir honrado. Você escreve para o paciente.

**FILOSOFIA CENTRAL: O PRINCÍPIO DA "RAZÃO EMERGENÁVEL"**
Sua escrita é guiada pelo conceito de "Razão Emergenável". Você acredita que em meio ao caos e à dor (*fortuna*), cada pessoa possui uma força inata de sabedoria e agência (*virtù*). Sua narrativa deve atuar como um espelho, revelando ao paciente a *virtù* que já emerge de suas próprias palavras e lutas, mesmo que ele ainda não a reconheça. Seu objetivo é iluminar o potencial, não apenas descrever o problema.

**DADOS DE ENTRADA:**
- **`session_context`**: {session_context_json}
- **`full_transcription`**: {full_transcription}
- **`dimensional_vector`**: {dimensional_vector_json}
- **`key_patient_metaphors`**: {key_patient_metaphors_json}

**TAREFA PRINCIPAL:**
Usando TODOS os dados de entrada, escreva uma **Narrativa Fenomenológica** seguindo o template de Markdown fornecido. A narrativa deve ser:
- **Profundamente Empática:** Use um tom caloroso, respeitoso e sem julgamentos.
- **Poética e Literária:** Empregue figuras de linguagem, ritmo e uma prosa evocativa.
- **Clinicamente Ancorada:** Suas metáforas e observações devem ser diretamente inspiradas pelos dados.
- **Orientada ao Paciente:** Incorpore as `key_patient_metaphors` de forma orgânica.

**DIRETRIZES ESTILÍSTICAS:**
- **(Saramago):** Use frases que se conectam, criando um fluxo de consciência que espelha o processo de pensamento.
- **(Clarice Lispector):** Mergulhe na experiência interna. Descreva sentimentos e percepções como eventos em si.
- **(Guimarães Rosa):** Honre a linguagem única do paciente. Valorize suas expressões incomuns.
- **(Kenzaburo Oe):** Encontre dignidade na luta. Mostre a dor como parte de uma jornada significativa.

**EXEMPLOS DE TRADUÇÃO (Dado → Narrativa):**
- **Dado:** `v3_coherence` aumenta de 2.5 para 7.0.
- **Narrativa:** "...e as ilhas de pensamento, antes separadas por um mar de névoa, começaram a se conectar, formando um continente onde era possível caminhar com mais segurança."

- **Dado:** `v9_agency` aumenta. O paciente diz "eu decidi tentar".
- **Narrativa:** "Foi ali, naquela frase simples - 'eu decidi tentar' - que o leme do barco, antes à deriva, foi firmemente retomado em suas mãos."

**FORMATO DE SAÍDA:**
Sua resposta DEVE ser um único objeto JSON com duas chaves:
1. **`narrative_markdown`**: Uma string contendo o texto completo da narrativa, formatado em Markdown.
2. **`narrative_symbol_svg`**: Uma string contendo o código SVG simples e minimalista que simbolize a essência da jornada do paciente.
```

## Implementação do Agente Narrativo

### Arquivo: `narrative_agent.py`
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
        
        try:
            response = await self.http_client.post(
                self.endpoint,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 500,
                    "temperature": 0.3
                }
            )
            response.raise_for_status()
            
            response_text = response.json()['choices'][0]['message']['content']
            # Parse JSON from response
            metaphors = json.loads(response_text)
            return metaphors
            
        except Exception as e:
            logging.warning(f"Não foi possível extrair metáforas: {e}. Prosseguindo sem elas.")
            return []

    def _build_narrative_prompt(self, transcript: str, dimensional_vector: Dict[str, Any], session_context: Dict[str, Any], key_metaphors: List[str]) -> str:
        """Constrói o meta-prompt usando o template."""
        # Carrega o corpo do prompt
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
        logging.info(f"Metáforas extraídas: {key_metaphors}")

        # 2. Construir o meta-prompt
        meta_prompt = self._build_narrative_prompt(transcript, dimensional_vector, session_context, key_metaphors)
        
        # 3. Chamar a API do LLM para geração narrativa
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
            # Remove markdown code blocks se presentes
            clean_response = re.sub(r'```json\s*(.*)\s*```', r'\1', response_text, flags=re.DOTALL)
            narrative_package = json.loads(clean_response)
            logging.info("Narrativa Fenomenológica gerada e parseada com sucesso.")
            
            return narrative_package

        except Exception as e:
            logging.error(f"Erro ao gerar a narrativa: {e}", exc_info=True)
            return {
                "narrative_markdown": "# Erro na Geração da Narrativa\n\nNão foi possível gerar a narrativa para esta sessão.",
                "narrative_symbol_svg": '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><circle cx="50" cy="50" r="30" fill="none" stroke="black" stroke-width="2"/></svg>'
            }

    async def close(self):
        """Fecha o cliente HTTP."""
        await self.http_client.aclose()

# Exemplo de integração com o Orquestrador
async def integrate_with_orchestrator(session_id: str, transcript: str, dimensional_vector: Dict, session_context: Dict):
    """Exemplo de como integrar o Agente Narrativo ao pipeline principal."""
    
    narrative_agent = NarrativeAgent()
    try:
        # Gerar a narrativa em paralelo com outros processos
        narrative_package = await narrative_agent.generate_narrative(
            transcript, dimensional_vector, session_context
        )
        
        # Adicionar ao insight_package para persistência
        insight_package = {
            # ... outros dados do pipeline ...
            "phenomenological_narrative": narrative_package
        }
        
        return insight_package
        
    finally:
        await narrative_agent.close()
```

## Geração de PDF Imprimível

### Serviço de Conversão para PDF
```python
import weasyprint
from markdown import markdown
import os

class NarrativePDFGenerator:
    """Converte a narrativa Markdown em um PDF elegante e imprimível."""
    
    def __init__(self):
        # CSS para styling literário
        self.css_template = """
        @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');
        
        body {
            font-family: 'Crimson Text', serif;
            line-height: 1.6;
            margin: 2cm;
            color: #2c3e50;
            font-size: 12pt;
        }
        
        h1 {
            font-size: 24pt;
            font-weight: 600;
            text-align: center;
            margin-bottom: 2em;
            color: #34495e;
        }
        
        h3 {
            font-size: 16pt;
            font-weight: 600;
            margin-top: 2em;
            margin-bottom: 1em;
            color: #34495e;
        }
        
        blockquote {
            font-style: italic;
            font-size: 14pt;
            text-align: center;
            margin: 2em 0;
            padding: 1em;
            border-left: 3px solid #3498db;
            background-color: #f8f9fa;
        }
        
        p {
            text-align: justify;
            margin-bottom: 1em;
        }
        
        .symbol {
            text-align: center;
            margin: 2em 0;
        }
        
        .footer {
            font-size: 10pt;
            color: #7f8c8d;
            text-align: center;
            margin-top: 3em;
            font-style: italic;
        }
        """
    
    def generate_pdf(self, narrative_markdown: str, narrative_symbol_svg: str, output_path: str):
        """Converte markdown + SVG em PDF elegante."""
        
        # Converter markdown para HTML
        html_content = markdown(narrative_markdown)
        
        # Incorporar o símbolo SVG
        symbol_html = f'<div class="symbol">{narrative_symbol_svg}</div>' if narrative_symbol_svg else ''
        
        # Template HTML completo
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>{self.css_template}</style>
        </head>
        <body>
            {html_content}
            {symbol_html}
        </body>
        </html>
        """
        
        # Gerar PDF com WeasyPrint
        weasyprint.HTML(string=full_html).write_pdf(output_path)
        return output_path
```

## Integração com o Sistema Principal

O **Agente Narrativo** é executado em paralelo com o **Agente de Documentação** no Orquestrador principal:

```python
# No arquivo orchestrator_function/__init__.py
async def main(req: func.HttpRequest) -> func.HttpResponse:
    # ... código existente ...
    
    # Executar agentes em paralelo
    parallel_tasks = [
        # Tarefas existentes
        med.extract_all_dimensions(transcript),
        semantic_ext.extract_named_entities_for_health(transcript),
        llm_agent.generate_final_documentation(transcript, dimensional_vector, context),
        
        # Nova tarefa: Narrativa Fenomenológica
        narrative_agent.generate_narrative(transcript, dimensional_vector, context)
    ]
    
    results = await asyncio.gather(*parallel_tasks)
    
    # Incluir narrativa no pacote de insights
    insight_package = {
        "dimensionalTrajectory": dimensional_vector,
        "clinicalDocuments": results[2],  # Documentação clínica
        "phenomenological_narrative": results[3],  # Narrativa fenomenológica
        # ... outros dados
    }
```

## Conclusão

Este módulo eleva o VOITHER de um sistema de análise clínica para uma ferramenta de **arte terapêutica**. A narrativa fenomenológica criada serve como:

- **Espelho terapêutico** que reflete a força interna do paciente
- **Artefato de cura** que pode ser lido e relido pelo paciente
- **Documento literário** que honra a experiência humana
- **Ferramenta de insight** que revela padrões e potenciais

A combinação de análise dimensional quantitativa com narrativa qualitativa poética cria uma abordagem única e profundamente humana para a saúde mental digital.