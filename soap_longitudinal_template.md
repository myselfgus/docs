# SOAP Longitudinal - Template de Preenchimento

## INSTRUÇÕES PARA IA

**Objetivo**: Documentar evolução clínica entre consultas (C1 → C2) com análise multidimensional.

**Pré-requisitos**: 
- Transcrição da consulta atual (C2)
- Dados da consulta anterior (C1) para comparação
- Intervalo de tempo entre consultas

**Metodologia**: 
- SEMPRE comparar C1 vs C2
- Identificar MUDANÇAS específicas
- Quantificar EVOLUÇÃO em escalas 0-5
- Usar PRÓPRIAS PALAVRAS do paciente

---

## CABEÇALHO

### Dados da Consulta
- **Nome**: `[EXTRAIR: Nome completo]`
- **Idade**: `[EXTRAIR: Idade atual]`
- **Prontuário**: `[USAR: Número fornecido]`
- **Data**: `[DATA: Consulta atual]`
- **Tipo Sessão**: `Follow-up (C[NÚMERO] - [DIAS] dias após C1)`
- **Profissional**: `[EXTRAIR: Nome do profissional]`

---

## S - SUBJETIVO (Análise Evolutiva)

### Narrativa Evolutiva - Transformações Discursivas

#### Evolução Linguístico-Pragmática (C1→C2)

**INSTRUÇÃO**: Compare padrões linguísticos entre consultas.

##### Frases Marcantes Comparativas

**C1 - Frase Marcante**: 
`"[BUSCAR: Frase mais significativa da consulta anterior]"`

**C2 - Frase Marcante**: 
`"[EXTRAIR: Frase mais significativa da consulta atual]"`

##### Análise Morfossintática
**INSTRUÇÃO**: Compare estruturas linguísticas.

**Elementos a analisar**:
- Complexidade das frases (simples → complexas?)
- Uso de conectivos causais ("porque", "então")
- Presença de subordinadas
- Coesão textual

**Preenchimento**:
```
C1: [Descrever padrão linguístico da consulta anterior]
C2: [Descrever padrão linguístico atual]
Evolução: [Indicar melhora, piora ou estabilidade na organização discursiva]
```

##### Code-switching/Pragmática
**INSTRUÇÃO**: Analise mudanças no registro linguístico.

**Elementos a observar**:
- Formalidade vs informalidade
- Gírias ou expressões específicas
- Adequação contextual
- Modulação do discurso

##### Metacognição
**INSTRUÇÃO**: Compare capacidade de reflexão sobre próprios processos mentais.

**Marcadores metacognitivos**:
- "Acho que", "Talvez", "Vamos dizer"
- Autocorreções
- Reconhecimento de limitações
- Insight sobre próprio comportamento

### Evolução da Queixa Principal

**INSTRUÇÃO**: Compare apresentação da queixa entre consultas.

**C1**: `[RESUMIR: Como paciente apresentou problema inicialmente]`

**C2**: `[EXTRAIR: Como paciente apresenta problema atualmente]`

**Análise Evolutiva**: `[DETERMINAR: Melhora, piora, mudança de foco, etc.]`

### Revelações/Ampliações C2

**INSTRUÇÃO**: Identifique conteúdos novos que não apareceram em C1.

#### Novos Conteúdos Revelados
**Critérios de identificação**:
- Informações sobre passado não mencionadas antes
- Sintomas que não foram relatados em C1
- Relações ou conflitos não abordados anteriormente
- Insights ou compreensões novas

#### Ampliação do Espectro Clínico
**INSTRUÇÃO**: Como o quadro clínico se expandiu ou clarificou.

---

## O - OBJETIVO (Observações Clínicas Evolutivas)

### Resposta Medicamentosa

**INSTRUÇÃO**: Avaliar resposta a medicações prescritas em C1 (se aplicável).

#### Concentração
- **C1**: `[ESTADO: Nível de concentração relatado/observado em C1]`
- **C2**: `[EXTRAIR: Nível atual de concentração da transcrição]`

#### Humor/Energia
- **C1**: `[ESTADO: Humor e energia em C1]`
- **C2**: `[EXTRAIR: Estado atual de humor e energia]`

#### Efeitos Colaterais
- **C1**: `[ESTADO: Efeitos relatados em C1]`
- **C2**: `[EXTRAIR: Efeitos atualmente relatados]`

### Mudanças Comportamentais Observadas

#### Cooperação
- **C1**: `[AVALIAR: Nível de cooperação em C1]`
- **C2**: `[OBSERVAR: Cooperação na consulta atual baseada na transcrição]`

#### Insight
- **C1**: `[ESTADO: Nível de insight demonstrado em C1]`
- **C2**: `[EXTRAIR: Evidências de insight na transcrição atual]`

#### Motivação
- **C1**: `[ESTADO: Motivação para tratamento em C1]`
- **C2**: `[AVALIAR: Motivação atual baseada na transcrição]`

### Status Uso de Substâncias

**INSTRUÇÃO**: Atualizar status de uso baseado na consulta atual.

- **Tempo de abstinência**: `[EXTRAIR: Período mencionado na transcrição]`
- **Contexto**: `[IDENTIFICAR: Internação, ambulatorial, etc.]`
- **Sintomas de abstinência**: `[EXTRAIR: Sintomas relatados]`
- **Fissura/Compulsão**: `[AVALIAR: Intensidade e frequência mencionadas]`

---

## A - AVALIAÇÃO (Análise Dimensional Longitudinal)

### Evolução Multidimensional VOITHER (Escala 0-5)

**INSTRUÇÃO**: Pontuar cada dimensão com base nas evidências das transcrições.

**Escala de Pontuação**:
- 0: Gravemente comprometido
- 1: Severamente comprometido  
- 2: Moderadamente comprometido
- 3: Levemente comprometido
- 4: Funcional com limitações menores
- 5: Plenamente funcional

#### Temporal
**Definição**: Relação com passado, presente e futuro.
- **C1**: `[PONTUAR: 0-5 baseado em C1]`
- **C2**: `[EXTRAIR: Evidências da transcrição e pontuar 0-5]`

#### Relacional  
**Definição**: Qualidade dos vínculos e relações interpessoais.
- **C1**: `[PONTUAR: 0-5 baseado em C1]`
- **C2**: `[AVALIAR: Relações mencionadas na transcrição atual]`

#### Espacial
**Definição**: Relação com territórios e espaços físicos.
- **C1**: `[PONTUAR: 0-5 baseado em C1]`
- **C2**: `[EXTRAIR: Como paciente se relaciona com espaços]`

#### Linguística
**Definição**: Organização, coerência e expressividade discursiva.
- **C1**: `[PONTUAR: 0-5 baseado em C1]`
- **C2**: `[AVALIAR: Qualidade discursiva da transcrição]`

#### Emocional
**Definição**: Regulação e expressão afetiva.
- **C1**: `[PONTUAR: 0-5 baseado em C1]`
- **C2**: `[EXTRAIR: Estados emocionais relatados/observados]`

#### Cognitiva
**Definição**: Funcionamento executivo, atenção, memória.
- **C1**: `[PONTUAR: 0-5 baseado em C1]`
- **C2**: `[AVALIAR: Evidências cognitivas na transcrição]`

#### Comportamental
**Definição**: Padrões de ação e tomada de decisão.
- **C1**: `[PONTUAR: 0-5 baseado em C1]`
- **C2**: `[EXTRAIR: Comportamentos relatados na consulta]`

#### Existencial
**Definição**: Sentido de propósito e significado na vida.
- **C1**: `[PONTUAR: 0-5 baseado em C1]`
- **C2**: `[IDENTIFICAR: Expressões de propósito ou desesperança]`

#### Somática
**Definição**: Manifestações corporais e saúde física.
- **C1**: `[PONTUAR: 0-5 baseado em C1]`
- **C2**: `[EXTRAIR: Sintomas físicos mencionados]`

#### Transcendente
**Definição**: Capacidade de ir além de limitações atuais.
- **C1**: `[PONTUAR: 0-5 baseado em C1]`
- **C2**: `[AVALIAR: Esperança, espiritualidade, crescimento]`

### Análise de Trajetória Evolutiva

#### CONSULTA 1 (Baseline)
- **Passado**: `[RESUMIR: Como C1 abordou questões do passado]`
- **Presente**: `[RESUMIR: Estado presente em C1]`
- **Futuro**: `[RESUMIR: Perspectivas futuras em C1]`
- **Resistências**: `[IDENTIFICAR: Resistências observadas em C1]`

#### CONSULTA 2 (X dias)
- **Passado**: `[EXTRAIR: Nova abordagem do passado na transcrição]`
- **Presente**: `[EXTRAIR: Estado presente atual]`
- **Futuro**: `[EXTRAIR: Perspectivas futuras atuais]`
- **Resistências**: `[IDENTIFICAR: Resistências atuais]`

### Diagnóstico Evolutivo

#### Mantidos
`[LISTAR: Diagnósticos que permanecem inalterados]`

#### Melhorados  
`[LISTAR: Condições que apresentaram melhora]`

#### Novos/Emergentes
`[IDENTIFICAR: Novos sintomas ou condições que emergiram]`

#### Fatores Complexificadores
`[EXTRAIR: Elementos que complicam o quadro ou tratamento]`

---

## P - PLANO (Ajustes Terapêuticos Baseados na Evolução)

### Ajustes Medicamentosos

**INSTRUÇÃO**: Baseado na resposta observada, ajustar medicação.

- **Medicação atual**: `[LISTAR: Medicações em uso]`
- **Resposta observada**: `[AVALIAR: Eficácia e tolerabilidade]`
- **Ajustes necessários**: `[PROPOR: Mudanças de dose, medicação ou adição]`
- **Monitoramento**: `[DEFINIR: O que acompanhar nos próximos encontros]`

### Mudanças no Plano Terapêutico

#### Frequência Consultas
- **C1**: `[ESTADO: Frequência estabelecida inicialmente]`
- **C2**: `[AJUSTAR: Nova frequência baseada na evolução]`

#### Modalidades
- **C1**: `[ESTADO: Modalidades terapêuticas em C1]`
- **C2**: `[AJUSTAR: Modalidades atuais ou novas]`

#### Objetivos
- **C1**: `[ESTADO: Objetivos estabelecidos em C1]`
- **C2**: `[REVISAR: Objetivos ajustados baseados na evolução]`

### Intervenções Específicas Baseadas na Evolução

**INSTRUÇÃO**: Marcar intervenções apropriadas baseadas na análise evolutiva.

- ☐ Manter plano atual (evolução favorável)
- ☐ Intensificar tratamento (evolução insuficiente)
- ☐ Reduzir intensidade (evolução adequada)
- ☐ Mudar estratégia (evolução desfavorável)
- ☐ Incluir família/rede apoio
- ☐ Avaliação especializada adicional
- ☐ Grupo terapêutico
- ☐ Atividades ocupacionais
- ☐ Outro: `[ESPECIFICAR baseado na necessidade identificada]`

### Próximos Passos

#### Curto prazo (próxima semana)
`[DEFINIR: Ações imediatas baseadas na consulta]`

#### Médio prazo (próximo mês)  
`[PLANEJAR: Objetivos de médio prazo]`

#### Reavaliação
- **Data**: `[AGENDAR: Próxima consulta]`
- **Objetivo**: `[DEFINIR: Foco da próxima avaliação]`

### Alertas e Monitoramento

#### SINAIS DE ALERTA IDENTIFICADOS
`[EXTRAIR: Sinais de risco mencionados ou observados na transcrição]`

#### INDICADORES DE PROGRESSO
`[IDENTIFICAR: Marcadores de melhora a acompanhar]`

#### CRITÉRIOS PARA MUDANÇA DE ESTRATÉGIA
`[DEFINIR: Quando mudar abordagem terapêutica]`

---

## SÍNTESE EVOLUTIVA

### Prognóstico e Trajetória

#### DIREÇÃO DA EVOLUÇÃO
- ☐ Favorável `[JUSTIFICAR: Baseado em quais evidências]`
- ☐ Estável `[JUSTIFICAR: Baseado em quais evidências]`
- ☐ Desfavorável `[JUSTIFICAR: Baseado em quais evidências]`

#### FATORES PROGNÓSTICOS IDENTIFICADOS
`[LISTAR: Fatores que influenciam positiva ou negativamente o prognóstico]`

#### PREVISÃO TRAJETORIAL
`[ESTIMAR: Curso provável baseado na evolução observada]`

#### RECOMENDAÇÕES ESTRATÉGICAS
`[PROPOR: Estratégias de longo prazo baseadas na análise]`

---

## METADADOS PARA PROCESSAMENTO

### Indicadores de Evolução Favorável:
- Maior organização discursiva
- Aumento de insight
- Melhora da regulação emocional
- Expansão de perspectivas futuras
- Fortalecimento de vínculos

### Indicadores de Evolução Desfavorável:
- Desorganização crescente
- Perda de insight
- Desregulação emocional
- Visão catastrófica do futuro
- Isolamento social

### Padrões Linguísticos de Melhora:
- Code-switching mais adequado
- Maior uso de conectivos causais
- Presença de modalizadores de incerteza saudável
- Metacognição aumentada
- Narrativa mais coesa

### Sinais de Alerta para Escalation:
- Ideação suicida emergente
- Sintomas psicóticos novos
- Descompensação comportamental
- Abandono de cuidados básicos
- Isolamento social extremo