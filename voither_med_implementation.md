# Motor de Extração Dimensional (MED): Implementação Completa em Python
## Código Real e Prático para Extração das 15 Dimensões do Espaço Mental ℳ

---

## Arquitetura: O Motor de Extração Dimensional (MED)

A melhor abordagem não é pensar em 15 "agentes" de IA independentes, o que seria computacionalmente caro e complexo de orquestrar. Em vez disso, construímos um sistema unificado que chamaremos de **Motor de Extração Dimensional (MED)**.

O **MED** é uma classe ou serviço no seu backend que, ao receber a transcrição e os dados de áudio, executa uma série de **Módulos de Extração Dimensional (MED-i)**. Cada módulo é uma função especializada responsável por calcular uma única dimensão.

### Tipos de Módulos

- **Alguns módulos são algorítmicos:** Rápidos, baseados em regras e linguística computacional clássica (usando bibliotecas como `spaCy`).
- **Outros são baseados em ML/DL:** Mais sofisticados, usando modelos de machine learning pré-treinados ou serviços de IA (como o Azure Language Service) para tarefas que exigem compreensão de contexto.

Esta arquitetura modular é eficiente, escalável e permite que você aprimore cada módulo individualmente no futuro.

---

## Pré-requisitos de Instalação

Antes de rodar, instale as bibliotecas necessárias no seu ambiente Python:

```bash
pip install spacy numpy
python -m spacy download pt_core_news_lg
```

*Nota: Para dimensões baseadas em áudio (Arousal, Prosódia), o ideal é usar bibliotecas como `librosa`. No código abaixo, simularemos a entrada dessas características, mas o local para integrá-las estará claramente marcado.*

---

## Implementação Completa: dimensional_extractor.py

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
        """Extrai a Valência Emocional (v₁)"""
        # Em produção, isso seria uma chamada para um serviço de análise de sentimento mais robusto (Azure Language Service)
        # O spaCy com vetores dá uma aproximação.
        valence_words = {"feliz": 2, "bem": 1.5, "melhorar": 1, "triste": -2, "mal": -1.5, "difícil": -1}
        score = sum(valence_words.get(token.lemma_, 0) for token in doc)
        return np.clip(score, -5, 5)

    def _extract_arousal(self, doc, audio_features):
        """Extrai o Arousal/Ativação (v₂)"""
        # Combina análise de áudio (primária) e texto (secundária)
        text_arousal_words = {"agitado": 9, "ansioso": 8, "energia": 7, "calmo": 2, "cansado": 1, "lento": 1}
        text_score = np.mean([text_arousal_words.get(token.lemma_, 5) for token in doc if token.lemma_ in text_arousal_words]) if any(t.lemma_ in text_arousal_words for t in doc) else 5.0
        
        # A velocidade da fala (do áudio) é um forte indicador
        speech_rate_score = np.clip((audio_features['speech_rate'] - 120) / 10, 0, 10) # Normaliza em torno de 120 palavras/min
        
        # Média ponderada dando mais peso ao áudio
        return np.clip(0.7 * speech_rate_score + 0.3 * text_score, 0, 10)

    def _extract_coherence(self, sentences):
        """Extrai a Coerência Narrativa (v₃)"""
        if len(sentences) < 2: return 10.0
        similarities = []
        for i in range(len(sentences) - 1):
            if sentences[i].has_vector and sentences[i+1].has_vector and len(sentences[i]) > 1 and len(sentences[i+1]) > 1:
                similarities.append(sentences[i].similarity(sentences[i+1]))
        
        return np.mean(similarities) * 10 if similarities else 5.0

    def _extract_complexity(self, doc):
        """Extrai a Complexidade Sintática (v₄)"""
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
        """Extrai a Orientação Temporal (v₅)"""
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
        """Extrai a Densidade de Autoreferência (v₆)"""
        first_person_pronouns = {"eu", "meu", "minha", "mim", "comigo"}
        all_pronouns = [token for token in tokens if token.pos_ == 'PRON']
        if not all_pronouns: return 0.0
        
        first_person_count = sum(1 for token in all_pronouns if token.lemma_.lower() in first_person_pronouns)
        return (first_person_count / len(all_pronouns)) * 10

    def _extract_social_language(self, doc):
        """Extrai a Linguagem Social (v₇)"""
        social_count = sum(1 for token in doc if token.lemma_.lower() in self.social_words)
        num_sentences = len(list(doc.sents))
        return np.clip((social_count / num_sentences if num_sentences > 0 else 0) * 5, 0, 10)

    def _extract_flexibility(self, sentences, chunk_size=5):
        """Extrai a Flexibilidade Discursiva (v₈)"""
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
        """Extrai a Dominância/Agência (v₉)"""
        agency_count = sum(1 for token in doc if token.lemma_.lower() in self.agency_words)
        active_voice_count = sum(1 for token in doc if token.dep_ == 'nsubj' and token.pos_ == 'PRON' and 'Person=1' in token.morph)
        num_sentences = len(list(doc.sents))
        
        score = ((agency_count + active_voice_count) / num_sentences if num_sentences > 0 else 0) * 4
        return np.clip(score, 0, 10)

    def _extract_fragmentation(self, text, tokens):
        """Extrai a Fragmentação do Discurso (v₁₀)"""
        # Contagem de disfluências simples
        disfluencies = text.lower().count(" ah ") + text.lower().count(" uhm ")
        
        # Variância do comprimento da sentença
        sent_lengths = [len(sent) for sent in nlp(text).sents]
        variance = np.var(sent_lengths) if sent_lengths else 0
        
        score = (disfluencies * 2) + (variance / 10)
        return np.clip(score, 0, 10)

    def _extract_semantic_density(self, tokens):
        """Extrai a Densidade Semântica (v₁₁)"""
        content_pos = {'NOUN', 'VERB', 'ADJ', 'ADV'}
        content_words = sum(1 for token in tokens if token.pos_ in content_pos)
        return (content_words / len(tokens) if tokens else 0) * 10

    def _extract_certainty(self, doc):
        """Extrai os Marcadores de Certeza/Incerteza (v₁₂)"""
        certain_count = sum(1 for token in doc if token.lemma_ in self.certainty_words)
        uncertain_count = sum(1 for token in doc if token.lemma_ in self.uncertainty_words)
        
        total = certain_count + uncertain_count
        if total == 0: return 0.0
        
        return ((certain_count - uncertain_count) / total) * 5

    def _extract_connectivity(self, doc):
        """Extrai os Padrões de Conectividade (v₁₃)"""
        connective_count = sum(1 for token in doc if token.lemma_ in self.connective_words)
        num_sentences = len(list(doc.sents))
        return np.clip((connective_count / num_sentences if num_sentences > 0 else 0) * 5, 0, 10)

    def _extract_pragmatics(self, doc):
        """Extrai a Comunicação Pragmática (v₁₄)"""
        # MÓDULO COMPLEXO: Em produção, seria um modelo de ML treinado (ex: fine-tuning de um LLM)
        # para classificar atos de fala e sua adequação.
        # Simulação: Mede a proporção de perguntas, que é um ato de fala interativo.
        question_count = sum(1 for token in doc if token.text == '?')
        num_sentences = len(list(doc.sents))
        return np.clip((question_count / num_sentences if num_sentences > 0 else 0) * 10, 0, 10)

    def _extract_prosody(self, audio_features):
        """Extrai a Prosódia Emocional (v₁₅)"""
        # A prosódia é um vetor. Aqui, combinamos em um único score de "variação".
        # Jitter e shimmer altos, e variância de pitch alta indicam alta variação prosódica.
        score = (audio_features['pitch_variance'] * 0.5) + (audio_features['jitter'] * 2) + (audio_features['shimmer'] * 2)
        return np.clip(score, 0, 10)

    def _simulate_audio_features(self, doc):
        """
        Esta função simula a extração de características do áudio com base no texto.
        Em uma implementação real, você usaria uma biblioteca como Librosa no arquivo de áudio.
        """
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
    print(json.dumps(dimensional_vector, indent=2, ensure_ascii=False))
```

---

## Integração com Azure Language Service

Para dimensões que exigem análise mais sofisticada (como Valência Emocional), você pode substituir as implementações básicas por chamadas ao Azure Language Service:

```python
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def _extract_valence_azure(self, text):
    """Versão aprimorada usando Azure Language Service"""
    # Configurar cliente do Azure
    endpoint = "https://your-resource.cognitiveservices.azure.com/"
    key = "your-api-key"
    
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, 
        credential=AzureKeyCredential(key)
    )
    
    # Análise de sentimento
    response = text_analytics_client.analyze_sentiment(documents=[text])[0]
    
    # Converter para escala -5 a +5
    positive_score = response.confidence_scores.positive
    negative_score = response.confidence_scores.negative
    
    valence = (positive_score - negative_score) * 5
    return np.clip(valence, -5, 5)
```

---

## Integração com Análise de Áudio Real

Para características de áudio reais, você pode usar a biblioteca `librosa`:

```python
import librosa

def extract_audio_features_real(self, audio_file_path):
    """Extração real de características de áudio usando librosa"""
    # Carregar o arquivo de áudio
    y, sr = librosa.load(audio_file_path)
    
    # Características prosódicas
    pitch, _ = librosa.piptrack(y=y, sr=sr)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    
    # Características espectrais
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    
    return {
        'speech_rate': tempo,
        'pitch_variance': np.var(pitch[pitch > 0]),
        'jitter': np.std(np.diff(pitch[pitch > 0])) if len(pitch[pitch > 0]) > 1 else 0,
        'shimmer': np.std(spectral_centroids)
    }
```

---

## Uso no Pipeline VOITHER

Este código se integra perfeitamente ao pipeline VOITHER:

```python
# No seu Orquestrador de IA (Azure Function)
def process_session_analysis(session_id, transcription_text, audio_file_url):
    # 1. Instanciar o Motor de Extração Dimensional
    med = DimensionalExtractor()
    
    # 2. Extrair características de áudio (se disponível)
    audio_features = None
    if audio_file_url:
        audio_features = extract_audio_features_real(audio_file_url)
    
    # 3. Extrair todas as dimensões
    dimensional_vector = med.extract_all_dimensions(transcription_text, audio_features)
    
    # 4. Converter para formato de série temporal Ψ(t)
    timestamp_vector = {
        "timestamp": 0,  # Para análise da sessão completa
        "vector": [
            dimensional_vector["v1_valence"],
            dimensional_vector["v2_arousal"],
            dimensional_vector["v3_coherence"],
            # ... todas as 15 dimensões
        ]
    }
    
    # 5. Salvar no MongoDB
    session_document = {
        "sessionId": session_id,
        "dimensionalTrajectory": [timestamp_vector],
        "fullTranscription": transcription_text,
        "extractedDimensions": dimensional_vector
    }
    
    return session_document
```

---

## Conclusão: Da Teoria à Prática

Este código representa o **primeiro protótipo funcional do seu Motor de Extração Dimensional**. Ele é a ponte entre a sua arquitetura teórica e a engenharia de software real.

### Características Principais

- **Modularidade:** Cada função `_extract_...` é um módulo que pode ser testado, validado e aprimorado de forma independente.
- **Hibridismo:** Ele combina regras linguísticas (`spaCy`), estatísticas (`numpy`) e placeholders para ML/DL, exatamente como a arquitetura ideal deveria ser.
- **Pronto para o Pipeline:** A função `extract_all_dimensions` é o ponto de entrada que seu Orquestrador de IA (a Azure Function) irá chamar, passando a transcrição e recebendo o vetor `Ψ(t)` para salvar nos bancos de dados.

### Próximos Passos

1. **Integrar ao backend** VOITHER
2. **Substituir placeholders** por serviços de IA reais (Azure Language Service)
3. **Adicionar análise de áudio real** usando `librosa`
4. **Alimentar o VOITHER MentalRender** com os dados gerados
5. **Validar com dados clínicos** reais

Você tem agora o blueprint completo para construir o núcleo de inteligência do seu sistema.