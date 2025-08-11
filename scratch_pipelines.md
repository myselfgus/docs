# VOITHER - DIAGRAMAS DIDÁTICOS DO PIPELINE

## 🔄 **VISÃO GERAL DO PIPELINE COMPLETO**

```
                    VOITHER PROCESSING PIPELINE
                         (3 Níveis Integrados)

INPUT                    NÍVEL 1                    NÍVEL 2                    NÍVEL 3
═════                    ═══════                    ═══════                    ═══════

🎤 Áudio              ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
   da Sessão    ────► │  ANÁLISE        │   ────► │  ANÁLISE        │   ────► │  FORMULAÇÃO     │
                      │  LINGUÍSTICA    │         │  DIMENSIONAL    │         │  INTEGRATIVA-   │
📝 Transcrição        │                 │         │                 │         │  TRAJETORIAL    │
   Automática   ────► │  47 Features    │         │  Mapeamento     │         │                 │
                      │  em 8 Domínios  │         │  Científico     │         │  Clínica +      │
🗂️ Contexto           │                 │         │  Validado       │         │  Prescrições +  │
   Clínico      ────► │  NLP + Redes    │         │                 │         │  Exames +       │
                      │  + Prosódia     │         │  RDoC/HiTOP/    │         │  Trajetória     │
                      └─────────────────┘         │  Big5/PERMA     │         └─────────────────┘
                                                  └─────────────────┘                   │
                                                                                        │
                                                                                        ▼
                                                                              ┌─────────────────┐
                                                                              │  RELATÓRIO      │
                                                                              │  CLÍNICO        │
                                                                              │  COMPLETO       │
                                                                              └─────────────────┘
```

---

## 🔬 **NÍVEL 1: ANÁLISE LINGUÍSTICA DETALHADA**

```
                          ANÁLISE LINGUÍSTICA (47 FEATURES)
                                    Nível 1

ENTRADA: Áudio + Transcrição                              SAÍDA: Vetor Linguístico
═════════════════════════                                ═══════════════════════

    🎵 Áudio                    📝 Texto
       │                          │
       ▼                          ▼
┌─────────────────┐      ┌─────────────────┐
│   PROCESSAMENTO │      │   PROCESSAMENTO │
│     PROSÓDICO   │      │      TEXTUAL    │
└─────────────────┘      └─────────────────┘
       │                          │
       ▼                          ▼

┌──────────────────────────────────────────────────────────────┐
│                    8 DOMÍNIOS DE FEATURES                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1️⃣ SINTÁTICO           │  5️⃣ COERÊNCIA TEMPORAL             │
│  ┌─────────────────┐    │  ┌─────────────────┐               │
│  │ • Complexidade  │    │  │ • Coerência     │               │
│  │ • Agency        │    │  │ • Perspectiva   │               │
│  │ • Fragmentação  │    │  │ • Sequenciamento│               │
│  └─────────────────┘    │  └─────────────────┘               │
│                         │                                    │
│  2️⃣ SEMÂNTICO           │  6️⃣ REDE CONCEITUAL               │
│  ┌─────────────────┐    │  ┌─────────────────┐               │
│  │ • Embeddings    │    │  │ • Conectividade │               │
│  │ • Campos        │    │  │ • Centralidade  │               │
│  │ • Metáforas     │    │  │ • Modularidade  │               │
│  └─────────────────┘    │  └─────────────────┘               │
│                         │                                    │
│  3️⃣ PROSÓDICO           │  7️⃣ MULTIMODAL                    │
│  ┌─────────────────┐    │  ┌─────────────────┐               │
│  │ • F0/Pitch      │    │  │ • Alinhamento   │               │
│  │ • Intensidade   │    │  │ • Contexto      │               │
│  │ • Qualidade     │    │  │ • Sincronização │               │
│  └─────────────────┘    │  └─────────────────┘               │
│                         │                                    │
│  4️⃣ PRAGMÁTICO          │  8️⃣ QUALIDADE                     │
│  ┌─────────────────┐    │  ┌─────────────────┐               │
│  │ • Atos de Fala  │    │  │ • Confiabilidade│               │
│  │ • Teoria Mente  │    │  │ • Anomalias     │               │
│  │ • Cooperação    │    │  │ • Auditoria     │               │
│  └─────────────────┘    │  └─────────────────┘               │
└──────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                        ┌─────────────────────┐
                        │  VETOR LINGUÍSTICO  │
                        │     47 Dimensões    │
                        │   [f₁, f₂, ..., f₄₇]│
                        └─────────────────────┘
```

---

## 📊 **NÍVEL 2: ANÁLISE DIMENSIONAL CIENTÍFICA**

```
                      MAPEAMENTO BASEADO EM EVIDÊNCIA CIENTÍFICA
                                      Nível 2

ENTRADA: Vetor Linguístico                               SAÍDA: Perfil Dimensional
══════════════════════                                  ═══════════════════════

┌─────────────────────┐
│  VETOR LINGUÍSTICO  │
│     47 Features     │
└─────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      BANCO DE CORRELAÇÕES VALIDADAS                          │
│                             (500+ Estudos)                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  📚 EVIDÊNCIA CIENTÍFICA:                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ • Covington 2005: Sintaxe ↔ Executivo (r=0.74)                    │   │
│  │ • Pennebaker 1996: Semântica ↔ Depressão (r=0.68)                 │   │
│  │ • Scherer 2003: Prosódia ↔ Arousal (r=0.81)                       │   │
│  │ • Bedi 2015: Coerência ↔ Psicose (r=0.83)                         │   │
│  │ • Meta-análises validadas + replicações                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        4 FRAMEWORKS CIENTÍFICOS                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  🧬 RDoC                   🎭 HiTOP                                         │
│  ┌─────────────────┐      ┌─────────────────┐                              │
│  │ • Negative      │      │ • Internalizing │                              │
│  │   Valence      │      │ • Externalizing │                              │
│  │ • Positive      │      │ • Thought       │                              │
│  │   Valence      │      │   Disorder      │                              │
│  │ • Cognitive     │      │ • Detachment    │                              │
│  │   Control      │      │ • Disinhibition │                              │
│  │ • Social        │      │ • Antagonism    │                              │
│  │   Processes    │      └─────────────────┘                              │
│  │ • Arousal       │                                                       │
│  └─────────────────┘                                                       │
│                                                                             │
│  🌟 Big Five               🌈 PERMA                                         │
│  ┌─────────────────┐      ┌─────────────────┐                              │
│  │ • Neuroticism   │      │ • Positive      │                              │
│  │ • Extraversion  │      │   Emotions      │                              │
│  │ • Openness      │      │ • Engagement    │                              │
│  │ • Agreeableness │      │ • Relationships │                              │
│  │ • Conscientious │      │ • Meaning       │                              │
│  └─────────────────┘      │ • Accomplishment│                              │
│                           └─────────────────┘                              │
└─────────────────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────┐
│ PERFIL DIMENSIONAL  │
│   Multi-Framework   │
│                     │
│ • RDoC: [5 scores]  │
│ • HiTOP: [6 scores] │
│ • Big5: [5 scores]  │
│ • PERMA: [5 scores] │
│                     │
│ + Confidence scores │
│ + Evidence trails   │
└─────────────────────┘
```

---

## 🏥 **NÍVEL 3: FORMULAÇÃO INTEGRATIVA-TRAJETORIAL**

```
                        FORMULAÇÃO CLÍNICA COMPLETA
                                  Nível 3

ENTRADA: Perfil Dimensional                              SAÍDA: Relatório Clínico
═══════════════════════                                 ══════════════════════

┌─────────────────────┐
│ PERFIL DIMENSIONAL  │
│   Multi-Framework   │
└─────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           INTEGRAÇÃO CLÍNICA                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  🎯 SÍNTESE DE PERFIL        📈 ANÁLISE TRAJETORIAL                         │
│  ┌─────────────────┐       ┌─────────────────┐                              │
│  │ • Padrões       │       │ • Onde estava   │                              │
│  │   Dominantes    │       │ • Onde está     │                              │
│  │ • Convergências │       │ • Para onde vai │                              │
│  │ • Fenótipo      │       │ • Fatores risco │                              │
│  │   Clínico       │       │ • Prognóstico   │                              │
│  └─────────────────┘       └─────────────────┘                              │
│                                                                             │
│  💊 PRESCRIÇÕES            🔬 EXAMES COMPLEMENTARES                          │
│  ┌─────────────────┐       ┌─────────────────┐                              │
│  │ • Farmacoterapia│       │ • Neuroimagem   │                              │
│  │   Dimensional   │       │ • Biomarcadores │                              │
│  │ • Psicoterapia  │       │ • Avaliação     │                              │
│  │   Específica    │       │   Cognitiva     │                              │
│  │ • Apps/Digital  │       │ • Farmacogenôm. │                              │
│  └─────────────────┘       └─────────────────┘                              │
│                                                                             │
│  📊 MONITORAMENTO          🎯 TARGETS TERAPÊUTICOS                          │
│  ┌─────────────────┐       ┌─────────────────┐                              │
│  │ • Frequência    │       │ • Alvos         │                              │
│  │ • Métrics       │       │   Primários     │                              │
│  │ • Segurança     │       │ • Alvos         │                              │
│  │ • Progresso     │       │   Secundários   │                              │
│  └─────────────────┘       │ • Cronograma    │                              │
│                           └─────────────────┘                              │
└─────────────────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RELATÓRIO CLÍNICO FINAL                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  📋 FORMULAÇÃO NARRATIVA                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ "Paciente apresenta padrão predominantemente internalizante         │   │
│  │ (HiTOP=7.8) com hiperativação de sistemas de ameaça (RDoC          │   │
│  │ Negative Valence=8.2) e déficit em controle executivo (RDoC        │   │
│  │ Cognitive Control=3.1). Perfil sugere vulnerabilidade a            │   │
│  │ episódios depressivo-ansiosos recorrentes..."                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  💊 PRESCRIÇÕES:                                                            │
│  • Escitalopram 10-20mg/dia (target: RDoC Negative Valence)                │
│  • CBT protocolo internalizing (16 sessões)                                │
│  • MindShift app para ansiedade (3x/dia)                                   │
│                                                                             │
│  🔬 EXAMES SOLICITADOS:                                                     │
│  • Cortisol matinal + curva (HPA axis)                                     │
│  • Inflammatory markers (CRP, IL-6)                                        │
│  • Executive function battery                                              │
│                                                                             │
│  📊 MONITORAMENTO:                                                          │
│  • Retorno 2 semanas (ajuste dose)                                         │
│  • Reavaliação dimensional 6 semanas                                       │
│  • Target: Negative Valence <5.0 em 8 semanas                              │
│                                                                             │
│  📈 PROGNÓSTICO:                                                            │
│  • Curto prazo: Melhora esperada 6-8 semanas                               │
│  • Longo prazo: Bom (fatores sociais preservados)                          │
│  • Risco recaída: Moderado (neuroticism alto)                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 **FLUXO DE DADOS DETALHADO**

```
                            PIPELINE DE PROCESSAMENTO
                               (Fluxo de Dados)

┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   INPUT     │    │   NÍVEL 1   │    │   NÍVEL 2   │    │   NÍVEL 3   │
│             │    │             │    │             │    │             │
│ 🎤 Audio    │───▶│ 🔤 Features │───▶│ 📊 Dimensões│───▶│ 🏥 Clínica  │
│ 📝 Texto    │    │             │    │             │    │             │
│ 🗂️ Context  │    │ Linguísticas│    │ Científicas │    │ Formulação  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │                   │                   │                   │
   Dados Brutos        47 Features       21 Construtos       Relatório
   Multimodais         Estruturadas      Dimensionais        Clínico
                                                            Completo

TEMPO:    ~0 min          ~2-3 min         ~1-2 min         ~1 min
PROCESSO: Captura         NLP + ML         Correlações      Template +
          Automática      Avançado         Científicas      Narrativa
```

---

## 🎛️ **ARQUITETURA TÉCNICA SIMPLIFICADA**

```
                          INFRAESTRUTURA VOITHER

┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  👨‍⚕️ Interface Psiquiatra  │  📱 Dashboard Paciente  │  📊 Relatórios        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  🤖 Claude API          🎵 Whisper API         🧠 NLP Models                │
│  (Análise dimensional)  (Speech-to-text)      (Features linguísticas)       │
│                                                                             │
│  📚 Evidence Bank       🔄 Pipeline Engine     💾 Database                  │
│  (500+ estudos)        (Orquestração)         (Pacientes + resultados)     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             INTEGRAÇÃO                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  🏥 Prontuário Eletrônico  │  💊 Sistema Prescrição  │  📋 Relatórios        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 **DIFERENCIAL COMPETITIVO VISUAL**

```
                      VOITHER vs. ABORDAGENS TRADICIONAIS

TRADICIONAL                              VOITHER
═══════════                              ═══════

📝 Observação Subjetiva          ───▶    🔬 Análise Objetiva (47 features)
❓ Diagnóstico Categorial        ───▶    📊 Perfil Dimensional Científico  
🎯 "Feeling" Clínico             ───▶    📚 Baseado em 500+ estudos validados
💊 Trial-and-error               ───▶    🎯 Prescrições dimensionalmente orientadas
📅 Follow-up irregular           ───▶    📊 Monitoramento dimensional contínuo
❌ Sem rastreabilidade           ───▶    🔍 Evidence trail completo

RESULTADO:                               RESULTADO:
• Diagnósticos inconsistentes            • Perfis dimensionais reprodutíveis
• Tratamentos genéricos                  • Intervenções personalizadas  
• Prognóstico impreciso                  • Predições baseadas em trajetória
• Baixa accountability                   • Auditabilidade científica total
```

**🎯 VOITHER = Psiquiatria Científica + Tecnologia + Personalização Dimensional**
