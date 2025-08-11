# 4: MED CORE (15 DIMENSÕES)

## Atencao: as 4 DSLs foram unificadas na linguagem .ee (verificar conteúdo)

## OVERVIEW
Implementar o Motor de Extração Dimensional (MED) conforme especificado em `voither_med_implementation.md`. O MED é o núcleo de inteligência do VOITHER que processa texto e áudio para extrair 15 dimensões comportamentais, habilitando análise objetiva do estado mental em tempo real.

## DEPENDENCIES (Must exist before starting)

- [ ] ✅ **Sprint 3 completed**: DSL Runtime (.Re) funcional e operacional
- [ ] ✅ **All DSLs working**: .aje/.ire/.e parsers + runtime executando corretamente
- [ ] ✅ **Storage backends operational**: TimescaleDB, MongoDB, Neo4j acessíveis
- [ ] ✅ **Runtime engine tested**: .Re engine passa todos os testes de integração
- [ ] Python 3.11+ com spaCy, numpy, scikit-learn
- [ ] Azure Cognitive Services (Language Service, Speech Service)
- [ ] Modelo spaCy pt_core_news_lg instalado

### Pre-flight Validation Script

```bash
#!/bin/bash
# validate_sprint_3.sh
set -e

echo "🔍 Validating Sprint 3 dependencies..."

# Test .Re runtime is operational
python -c "
import asyncio
from src.runtime.re_engine import ReEngine

async def test_runtime():
    config = {'redis': {'host': 'redis-service', 'port': 6379}}
    engine = ReEngine(config)
    
    assert await engine.start(), '.Re engine failed to start'
    
    # Test DSL execution
    result = await engine.execute_dsl_command('aje', 'Re{test}.aje:{\"test\": true}')
    assert result['success'], 'DSL execution failed'
    
    await engine.stop()
    print('✅ .Re runtime engine operational')

asyncio.run(test_runtime())
"

# Validate Azure services connectivity
python -c "
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os

endpoint = os.getenv('AZURE_LANGUAGE_ENDPOINT')
key = os.getenv('AZURE_LANGUAGE_KEY')

if not endpoint or not key:
    raise ValueError('Azure Language Service credentials not configured')
    
client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
response = client.analyze_sentiment(documents=['test'])
print('✅ Azure Language Service accessible')
"

# Test spaCy model availability
python -c "
import spacy
nlp = spacy.load('pt_core_news_lg')
doc = nlp('Este é um teste do modelo de linguagem.')
assert len(doc) > 0, 'spaCy model not working'
print('✅ spaCy model pt_core_news_lg loaded')
"

echo "✅ All Sprint 3 dependencies validated"
```

## IMPLEMENTATION

### 1. Project Structure

```
voither-med-core/
├── src/
│   ├── __init__.py
│   ├── med/
│   │   ├── __init__.py
│   │   ├── dimensional_extractor.py    # Main MED class
│   │   ├── extractors/
│   │   │   ├── __init__.py
│   │   │   ├── emotional_core.py       # v1-v3: Valence, Arousal, Coherence
│   │   │   ├── cognitive_linguistic.py # v4-v6: Complexity, Temporal, Self-ref
│   │   │   ├── social_communicative.py # v7-v9: Social, Flexibility, Agency
│   │   │   ├── structural_prosodic.py  # v10-v15: Fragmentation, Density, etc
│   │   │   └── base_extractor.py       # Abstract base for extractors
│   │   ├── analyzers/
│   │   │   ├── __init__.py
│   │   │   ├── text_analyzer.py        # Text-based analysis
│   │   │   ├── audio_analyzer.py       # Audio feature extraction
│   │   │   └── hybrid_analyzer.py      # Combined text+audio
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── linguistic_utils.py     # spaCy utilities
│   │       ├── audio_utils.py          # Audio processing utilities
│   │       └── math_utils.py           # Mathematical operations
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── azure_integration.py        # Azure Cognitive Services
│   │   ├── dsl_integration.py          # Integration with .Re runtime
│   │   └── storage_integration.py      # Database persistence
│   └── config/
│       ├── __init__.py
│       ├── dimensions_config.py        # 15 dimensions configuration
│       └── models_config.py            # ML models configuration
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── requirements.txt
└── README.md
```

### 2. Core MED Dimensional Extractor

```python
# src/med/dimensional_extractor.py
import spacy
import numpy as np
import asyncio
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import time
import logging

from .extractors.emotional_core import EmotionalCoreExtractor
from .extractors.cognitive_linguistic import CognitiveLinguisticExtractor
from .extractors.social_communicative import SocialCommunicativeExtractor
from .extractors.structural_prosodic import StructuralProsodicExtractor
from .analyzers.text_analyzer import TextAnalyzer
from .analyzers.audio_analyzer import AudioAnalyzer
from .analyzers.hybrid_analyzer import HybridAnalyzer
from ..integration.azure_integration import AzureLanguageIntegration
from ..integration.dsl_integration import DSLIntegration
from ..config.dimensions_config import DIMENSIONS_CONFIG

class DimensionalExtractor:
    """
    Motor de Extração Dimensional (MED) - Núcleo do VOITHER
    
    Extrai 15 dimensões comportamentais do espaço mental ℳ:
    - Núcleo Emocional (v1-v3): Valência, Arousal, Coerência
    - Cognitivo-Linguístico (v4-v6): Complexidade, Temporal, Autoreferência
    - Social-Comunicativo (v7-v9): Social, Flexibilidade, Agência
    - Estrutural-Prosódico (v10-v15): Fragmentação, Densidade, Certeza, etc.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger("DimensionalExtractor")
        
        # Load spaCy model
        self.nlp = spacy.load(config.get('spacy_model', 'pt_core_news_lg'))
        self.logger.info(f"Loaded spaCy model: {self.nlp.meta['name']}")
        
        # Initialize analyzers
        self.text_analyzer = TextAnalyzer(self.nlp, config)
        self.audio_analyzer = AudioAnalyzer(config)
        self.hybrid_analyzer = HybridAnalyzer(config)
        
        # Initialize dimensional extractors
        self.emotional_extractor = EmotionalCoreExtractor(config)
        self.cognitive_extractor = CognitiveLinguisticExtractor(config)
        self.social_extractor = SocialCommunicativeExtractor(config)
        self.structural_extractor = StructuralProsodicExtractor(config)
        
        # Initialize integrations
        self.azure_integration = AzureLanguageIntegration(config.get('azure', {}))
        self.dsl_integration = DSLIntegration(config.get('dsl_runtime', {}))
        
        # Extraction statistics
        self.extraction_stats = {
            'total_extractions': 0,
            'successful_extractions': 0,
            'average_processing_time_ms': 0.0,
            'dimension_accuracy_scores': {dim: 0.0 for dim in DIMENSIONS_CONFIG.keys()}
        }
        
        # Confidence thresholds for each dimension
        self.confidence_thresholds = {
            'high': 0.85,
            'medium': 0.70,
            'low': 0.50
        }
    
    async def extract_all_dimensions(self, text: str, 
                                   audio_features: Optional[Dict[str, Any]] = None,
                                   context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extrai todas as 15 dimensões de uma transcrição e características de áudio
        
        Args:
            text: Transcrição completa da sessão
            audio_features: Características extraídas do áudio (opcional)
            context: Contexto adicional (patient_id, session_id, etc.)
            
        Returns:
            Dict com as 15 dimensões + metadados de confiança
        """
        start_time = time.time()
        extraction_id = f"med_{int(time.time() * 1000)}"
        
        try:
            self.logger.info(f"Starting dimensional extraction: {extraction_id}")
            
            # Preparar contexto de extração
            extraction_context = {
                'extraction_id': extraction_id,
                'text_length': len(text),
                'has_audio': audio_features is not None,
                'timestamp': datetime.utcnow().isoformat(),
                **(context or {})
            }
            
            # Análise inicial do texto
            doc = self.nlp(text)
            sentences = list(doc.sents)
            tokens = [token for token in doc]
            
            self.logger.debug(f"Processed {len(sentences)} sentences, {len(tokens)} tokens")
            
            # Simular características de áudio se não fornecidas
            if audio_features is None:
                audio_features = self._simulate_audio_features(doc)
                extraction_context['audio_simulated'] = True
            
            # Análise híbrida (texto + áudio)
            hybrid_features = await self.hybrid_analyzer.analyze(text, audio_features)
            
            # Extração por grupos de dimensões
            dimensions = {}
            confidence_scores = {}
            processing_times = {}
            
            # Grupo 1: Núcleo Emocional (v1-v3)
            start_group = time.time()
            emotional_dims = await self.emotional_extractor.extract_dimensions(
                doc, sentences, tokens, audio_features, hybrid_features
            )
            dimensions.update(emotional_dims['dimensions'])
            confidence_scores.update(emotional_dims['confidence_scores'])
            processing_times['emotional_core'] = (time.time() - start_group) * 1000
            
            # Grupo 2: Cognitivo-Linguístico (v4-v6)
            start_group = time.time()
            cognitive_dims = await self.cognitive_extractor.extract_dimensions(
                doc, sentences, tokens, audio_features, hybrid_features
            )
            dimensions.update(cognitive_dims['dimensions'])
            confidence_scores.update(cognitive_dims['confidence_scores'])
            processing_times['cognitive_linguistic'] = (time.time() - start_group) * 1000
            
            # Grupo 3: Social-Comunicativo (v7-v9)
            start_group = time.time()
            social_dims = await self.social_extractor.extract_dimensions(
                doc, sentences, tokens, audio_features, hybrid_features
            )
            dimensions.update(social_dims['dimensions'])
            confidence_scores.update(social_dims['confidence_scores'])
            processing_times['social_communicative'] = (time.time() - start_group) * 1000
            
            # Grupo 4: Estrutural-Prosódico (v10-v15)
            start_group = time.time()
            structural_dims = await self.structural_extractor.extract_dimensions(
                doc, sentences, tokens, audio_features, hybrid_features
            )
            dimensions.update(structural_dims['dimensions'])
            confidence_scores.update(structural_dims['confidence_scores'])
            processing_times['structural_prosodic'] = (time.time() - start_group) * 1000
            
            # Validação dimensional
            validated_dimensions = self._validate_dimensions(dimensions)
            
            # Cálculo de confiança global
            global_confidence = np.mean(list(confidence_scores.values()))
            
            # Tempo total de processamento
            total_processing_time = (time.time() - start_time) * 1000
            
            # Resultado final
            result = {
                'extraction_id': extraction_id,
                'success': True,
                'dimensions': validated_dimensions,
                'confidence_scores': confidence_scores,
                'global_confidence': global_confidence,
                'confidence_level': self._classify_confidence(global_confidence),
                'processing_times': processing_times,
                'total_processing_time_ms': total_processing_time,
                'extraction_context': extraction_context,
                'validation_results': self._get_validation_summary(validated_dimensions),
                'metadata': {
                    'text_stats': {
                        'characters': len(text),
                        'words': len(tokens),
                        'sentences': len(sentences),
                        'avg_words_per_sentence': len(tokens) / len(sentences) if sentences else 0
                    },
                    'audio_stats': self._get_audio_stats(audio_features),
                    'model_versions': {
                        'spacy_model': self.nlp.meta['name'],
                        'med_version': '1.0.0'
                    }
                }
            }
            
            # Persistir resultados via DSL
            await self._persist_extraction_results(result, context)
            
            # Atualizar estatísticas
            self._update_extraction_stats(total_processing_time, True, confidence_scores)
            
            self.logger.info(f"✅ Extraction completed: {extraction_id} ({total_processing_time:.1f}ms)")
            return result
            
        except Exception as e:
            total_processing_time = (time.time() - start_time) * 1000
            self._update_extraction_stats(total_processing_time, False, {})
            
            error_result = {
                'extraction_id': extraction_id,
                'success': False,
                'error': str(e),
                'total_processing_time_ms': total_processing_time,
                'extraction_context': extraction_context
            }
            
            self.logger.error(f"❌ Extraction failed: {extraction_id} - {e}")
            return error_result
    
    async def extract_single_dimension(self, dimension_name: str, text: str,
                                     audio_features: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extrai uma única dimensão específica
        
        Args:
            dimension_name: Nome da dimensão (v1_valence, v2_arousal, etc.)
            text: Texto para análise
            audio_features: Características de áudio (opcional)
            
        Returns:
            Resultado da extração da dimensão específica
        """
        if dimension_name not in DIMENSIONS_CONFIG:
            raise ValueError(f"Unknown dimension: {dimension_name}")
        
        start_time = time.time()
        
        # Processar texto
        doc = self.nlp(text)
        sentences = list(doc.sents)
        tokens = [token for token in doc]
        
        # Simular áudio se necessário
        if audio_features is None:
            audio_features = self._simulate_audio_features(doc)
        
        # Análise híbrida
        hybrid_features = await self.hybrid_analyzer.analyze(text, audio_features)
        
        # Determinar extrator apropriado
        extractor = self._get_extractor_for_dimension(dimension_name)
        
        # Extrair dimensão específica
        result = await extractor.extract_single_dimension(
            dimension_name, doc, sentences, tokens, audio_features, hybrid_features
        )
        
        processing_time = (time.time() - start_time) * 1000
        
        return {
            'dimension_name': dimension_name,
            'value': result['value'],
            'confidence': result['confidence'],
            'processing_time_ms': processing_time,
            'metadata': result.get('metadata', {}),
            'success': True
        }
    
    async def batch_extract_dimensions(self, text_samples: List[str],
                                     audio_samples: Optional[List[Dict[str, Any]]] = None,
                                     context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Extração em lote para múltiplas amostras
        
        Args:
            text_samples: Lista de textos para análise
            audio_samples: Lista de características de áudio (opcional)
            context: Contexto compartilhado
            
        Returns:
            Lista de resultados de extração
        """
        if audio_samples and len(audio_samples) != len(text_samples):
            raise ValueError("Audio samples count must match text samples count")
        
        tasks = []
        for i, text in enumerate(text_samples):
            audio_features = audio_samples[i] if audio_samples else None
            sample_context = {
                'batch_id': context.get('batch_id', 'batch_' + str(int(time.time()))),
                'sample_index': i,
                'total_samples': len(text_samples),
                **(context or {})
            }
            
            task = self.extract_all_dimensions(text, audio_features, sample_context)
            tasks.append(task)
        
        # Executar extrações em paralelo (limitado para evitar sobrecarga)
        batch_size = min(len(tasks), self.config.get('max_concurrent_extractions', 5))
        results = []
        
        for i in range(0, len(tasks), batch_size):
            batch_tasks = tasks[i:i + batch_size]
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            
            for result in batch_results:
                if isinstance(result, Exception):
                    results.append({
                        'success': False,
                        'error': str(result),
                        'batch_index': i
                    })
                else:
                    results.append(result)
        
        return results
    
    def get_extraction_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas de extração"""
        return {
            'total_extractions': self.extraction_stats['total_extractions'],
            'successful_extractions': self.extraction_stats['successful_extractions'],
            'success_rate': (
                self.extraction_stats['successful_extractions'] / 
                max(self.extraction_stats['total_extractions'], 1) * 100
            ),
            'average_processing_time_ms': self.extraction_stats['average_processing_time_ms'],
            'dimension_accuracy_scores': self.extraction_stats['dimension_accuracy_scores'].copy(),
            'confidence_thresholds': self.confidence_thresholds.copy()
        }
    
    def _simulate_audio_features(self, doc) -> Dict[str, Any]:
        """Simula características de áudio baseadas no texto"""
        text_length = len(doc.text)
        word_count = len([token for token in doc if not token.is_space])
        
        # Estimativa de velocidade de fala baseada no comprimento do texto
        estimated_speech_rate = min(max(word_count / (text_length / 150.0), 80), 220)
        
        return {
            'speech_rate': estimated_speech_rate,
            'pitch_variance': np.random.uniform(1.0, 4.0),
            'jitter': np.random.uniform(0.1, 1.5),
            'shimmer': np.random.uniform(0.1, 1.5),
            'voice_quality': np.random.uniform(0.3, 0.9),
            'pause_duration_avg': np.random.uniform(0.2, 1.0),
            'simulated': True
        }
    
    def _validate_dimensions(self, dimensions: Dict[str, float]) -> Dict[str, float]:
        """Valida e normaliza valores dimensionais"""
        validated = {}
        
        for dim_name, value in dimensions.items():
            if dim_name not in DIMENSIONS_CONFIG:
                self.logger.warning(f"Unknown dimension: {dim_name}")
                continue
            
            config = DIMENSIONS_CONFIG[dim_name]
            min_val = config.get('min_value', -10.0)
            max_val = config.get('max_value', 10.0)
            
            # Clamp value to valid range
            validated_value = np.clip(value, min_val, max_val)
            
            # Handle NaN/inf values
            if not np.isfinite(validated_value):
                validated_value = config.get('default_value', 0.0)
                self.logger.warning(f"Invalid value for {dim_name}, using default: {validated_value}")
            
            validated[dim_name] = float(validated_value)
        
        return validated
    
    def _classify_confidence(self, confidence_score: float) -> str:
        """Classifica nível de confiança"""
        if confidence_score >= self.confidence_thresholds['high']:
            return 'high'
        elif confidence_score >= self.confidence_thresholds['medium']:
            return 'medium'
        elif confidence_score >= self.confidence_thresholds['low']:
            return 'low'
        else:
            return 'very_low'
    
    def _get_validation_summary(self, dimensions: Dict[str, float]) -> Dict[str, Any]:
        """Retorna resumo da validação dimensional"""
        return {
            'dimensions_extracted': len(dimensions),
            'expected_dimensions': len(DIMENSIONS_CONFIG),
            'completion_rate': len(dimensions) / len(DIMENSIONS_CONFIG) * 100,
            'value_ranges_valid': all(
                DIMENSIONS_CONFIG[dim]['min_value'] <= val <= DIMENSIONS_CONFIG[dim]['max_value']
                for dim, val in dimensions.items()
                if dim in DIMENSIONS_CONFIG
            )
        }
    
    def _get_audio_stats(self, audio_features: Dict[str, Any]) -> Dict[str, Any]:
        """Retorna estatísticas das características de áudio"""
        if not audio_features:
            return {'available': False}
        
        return {
            'available': True,
            'simulated': audio_features.get('simulated', False),
            'speech_rate': audio_features.get('speech_rate', 0),
            'pitch_variance': audio_features.get('pitch_variance', 0),
            'voice_quality': audio_features.get('voice_quality', 0)
        }
    
    def _get_extractor_for_dimension(self, dimension_name: str):
        """Retorna o extrator apropriado para uma dimensão"""
        if dimension_name.startswith('v1_') or dimension_name.startswith('v2_') or dimension_name.startswith('v3_'):
            return self.emotional_extractor
        elif dimension_name.startswith('v4_') or dimension_name.startswith('v5_') or dimension_name.startswith('v6_'):
            return self.cognitive_extractor
        elif dimension_name.startswith('v7_') or dimension_name.startswith('v8_') or dimension_name.startswith('v9_'):
            return self.social_extractor
        else:
            return self.structural_extractor
    
    async def _persist_extraction_results(self, result: Dict[str, Any], context: Optional[Dict[str, Any]]):
        """Persiste resultados via integração DSL"""
        try:
            # Criar evento .aje para armazenar resultado
            aje_event = {
                'action': 'dimensional_extraction',
                'extraction_id': result['extraction_id'],
                'dimensions': result['dimensions'],
                'confidence_scores': result['confidence_scores'],
                'processing_time_ms': result['total_processing_time_ms'],
                'context': context or {}
            }
            
            await self.dsl_integration.store_aje_event(aje_event)
            
            # Se tiver correlações significativas, criar padrão .ire
            if result['global_confidence'] > 0.8:
                ire_pattern = {
                    'pattern_name': 'high_confidence_extraction',
                    'extraction_id': result['extraction_id'],
                    'threshold': 0.8,
                    'dimensions': result['dimensions']
                }
                
                await self.dsl_integration.store_ire_pattern(ire_pattern)
            
        except Exception as e:
            self.logger.error(f"Failed to persist extraction results: {e}")
    
    def _update_extraction_stats(self, processing_time: float, success: bool, 
                                confidence_scores: Dict[str, float]):
        """Atualiza estatísticas de extração"""
        self.extraction_stats['total_extractions'] += 1
        
        if success:
            self.extraction_stats['successful_extractions'] += 1
            
            # Atualizar média de tempo de processamento
            total = self.extraction_stats['total_extractions']
            current_avg = self.extraction_stats['average_processing_time_ms']
            self.extraction_stats['average_processing_time_ms'] = (
                (current_avg * (total - 1) + processing_time) / total
            )
            
            # Atualizar scores de acurácia das dimensões
            for dim_name, confidence in confidence_scores.items():
                if dim_name in self.extraction_stats['dimension_accuracy_scores']:
                    current_score = self.extraction_stats['dimension_accuracy_scores'][dim_name]
                    # Média móvel simples
                    self.extraction_stats['dimension_accuracy_scores'][dim_name] = (
                        (current_score * 0.9) + (confidence * 0.1)
                    )
```

### 3. Emotional Core Extractor (v1-v3)

```python
# src/med/extractors/emotional_core.py
import numpy as np
from typing import Dict, Any, List
from .base_extractor import BaseExtractor
from ..utils.linguistic_utils import LinguisticUtils
from ...integration.azure_integration import AzureLanguageIntegration

class EmotionalCoreExtractor(BaseExtractor):
    """
    Extrator do Núcleo Emocional (v1-v3)
    - v1_valence_emotional: Valência emocional (-5 a +5)
    - v2_arousal_activation: Nível de ativação/arousal (0 a 10)
    - v3_narrative_coherence: Coerência narrativa (0 a 10)
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.azure_integration = AzureLanguageIntegration(config.get('azure', {}))
        self.linguistic_utils = LinguisticUtils()
        
        # Dicionários de palavras para análise lexical
        self.valence_words = {
            # Palavras positivas
            'feliz': 2.5, 'bem': 1.8, 'ótimo': 3.0, 'maravilhoso': 3.5, 'alegre': 2.2,
            'satisfeito': 2.0, 'contente': 1.9, 'animado': 2.8, 'tranquilo': 1.5,
            'esperançoso': 2.3, 'orgulhoso': 2.1, 'grato': 2.4, 'aliviado': 1.7,
            
            # Palavras negativas  
            'triste': -2.5, 'mal': -1.8, 'péssimo': -3.0, 'terrível': -3.5, 'deprimido': -3.2,
            'ansioso': -2.0, 'preocupado': -1.8, 'estressado': -2.3, 'irritado': -2.1,
            'desesperançoso': -3.1, 'envergonhado': -2.2, 'culpado': -2.4, 'frustrado': -2.0,
            'raiva': -2.8, 'medo': -2.5, 'pânico': -3.3, 'desespero': -3.4
        }
        
        self.arousal_words = {
            # Alto arousal
            'agitado': 8.5, 'ansioso': 8.0, 'nervoso': 7.5, 'excitado': 8.2, 'eufórico': 9.0,
            'irritado': 7.8, 'furioso': 9.2, 'pânico': 9.5, 'frenético': 9.1, 'hiperativo': 8.8,
            'tenso': 7.2, 'estressado': 7.6, 'alarmado': 8.3, 'perturbado': 7.4,
            
            # Baixo arousal
            'calmo': 2.0, 'relaxado': 1.8, 'sereno': 1.5, 'tranquilo': 2.2, 'pacífico': 1.6,
            'cansado': 2.5, 'sonolento': 1.8, 'letárgico': 1.2, 'apático': 1.0, 'entediado': 2.8,
            'desanimado': 2.4, 'melancólico': 2.6, 'resignado': 2.3, 'passivo': 1.9
        }
    
    async def extract_dimensions(self, doc, sentences, tokens, audio_features, hybrid_features) -> Dict[str, Any]:
        """Extrai as 3 dimensões do núcleo emocional"""
        
        # v1: Valência Emocional
        valence_result = await self._extract_valence_emotional(doc, sentences, tokens, audio_features)
        
        # v2: Arousal/Ativação
        arousal_result = await self._extract_arousal_activation(doc, sentences, tokens, audio_features)
        
        # v3: Coerência Narrativa
        coherence_result = await self._extract_narrative_coherence(doc, sentences, tokens)
        
        return {
            'dimensions': {
                'v1_valence_emotional': valence_result['value'],
                'v2_arousal_activation': arousal_result['value'],
                'v3_narrative_coherence': coherence_result['value']
            },
            'confidence_scores': {
                'v1_valence_emotional': valence_result['confidence'],
                'v2_arousal_activation': arousal_result['confidence'],
                'v3_narrative_coherence': coherence_result['confidence']
            },
            'metadata': {
                'valence_metadata': valence_result['metadata'],
                'arousal_metadata': arousal_result['metadata'],
                'coherence_metadata': coherence_result['metadata']
            }
        }
    
    async def _extract_valence_emotional(self, doc, sentences, tokens, audio_features) -> Dict[str, Any]:
        """Extrai valência emocional usando múltiplas abordagens"""
        
        # Abordagem 1: Análise lexical com dicionário
        lexical_valence = self._compute_lexical_valence(tokens)
        
        # Abordagem 2: Azure Language Service (mais robusta)
        azure_valence = await self._compute_azure_valence(doc.text)
        
        # Abordagem 3: Análise de polaridade por sentença
        sentence_valences = []
        for sent in sentences:
            if len(sent.text.strip()) > 5:  # Ignorar sentenças muito curtas
                sent_valence = self._compute_sentence_valence(sent)
                sentence_valences.append(sent_valence)
        
        sentence_valence_avg = np.mean(sentence_valences) if sentence_valences else 0.0
        
        # Combinação ponderada das abordagens
        weights = {
            'lexical': 0.3,
            'azure': 0.5,
            'sentence': 0.2
        }
        
        combined_valence = (
            weights['lexical'] * lexical_valence +
            weights['azure'] * azure_valence +
            weights['sentence'] * sentence_valence_avg
        )
        
        # Normalizar para escala -5 a +5
        final_valence = np.clip(combined_valence, -5.0, 5.0)
        
        # Calcular confiança baseada na consistência entre abordagens
        valence_values = [lexical_valence, azure_valence, sentence_valence_avg]
        confidence = self._calculate_confidence_from_consistency(valence_values)
        
        return {
            'value': final_valence,
            'confidence': confidence,
            'metadata': {
                'lexical_valence': lexical_valence,
                'azure_valence': azure_valence,
                'sentence_valence_avg': sentence_valence_avg,
                'sentence_count': len(sentence_valences),
                'method': 'hybrid_lexical_azure_sentence'
            }
        }
    
    async def _extract_arousal_activation(self, doc, sentences, tokens, audio_features) -> Dict[str, Any]:
        """Extrai nível de arousal/ativação"""
        
        # Abordagem 1: Análise lexical
        lexical_arousal = self._compute_lexical_arousal(tokens)
        
        # Abordagem 2: Características prosódicas do áudio
        audio_arousal = self._compute_audio_arousal(audio_features)
        
        # Abordagem 3: Indicadores textuais de ativação
        textual_arousal = self._compute_textual_arousal_indicators(doc, tokens)
        
        # Combinação ponderada (áudio tem peso maior se disponível)
        if not audio_features.get('simulated', False):
            weights = {'lexical': 0.25, 'audio': 0.50, 'textual': 0.25}
        else:
            weights = {'lexical': 0.40, 'audio': 0.20, 'textual': 0.40}
        
        combined_arousal = (
            weights['lexical'] * lexical_arousal +
            weights['audio'] * audio_arousal +
            weights['textual'] * textual_arousal
        )
        
        # Normalizar para escala 0 a 10
        final_arousal = np.clip(combined_arousal, 0.0, 10.0)
        
        # Confiança baseada na consistência
        arousal_values = [lexical_arousal, audio_arousal, textual_arousal]
        confidence = self._calculate_confidence_from_consistency(arousal_values, scale_factor=0.1)
        
        return {
            'value': final_arousal,
            'confidence': confidence,
            'metadata': {
                'lexical_arousal': lexical_arousal,
                'audio_arousal': audio_arousal,
                'textual_arousal': textual_arousal,
                'audio_simulated': audio_features.get('simulated', False),
                'method': 'hybrid_lexical_audio_textual'
            }
        }
    
    async def _extract_narrative_coherence(self, doc, sentences, tokens) -> Dict[str, Any]:
        """Extrai coerência narrativa"""
        
        if len(sentences) < 2:
            return {
                'value': 10.0,  # Texto muito curto é considerado coerente
                'confidence': 0.5,
                'metadata': {'method': 'insufficient_sentences', 'sentence_count': len(sentences)}
            }
        
        # Abordagem 1: Similaridade semântica entre sentenças consecutivas
        semantic_coherence = self._compute_semantic_coherence(sentences)
        
        # Abordagem 2: Conectivos lógicos e coesão textual
        cohesion_coherence = self._compute_cohesion_coherence(doc, sentences)
        
        # Abordagem 3: Consistência temática
        thematic_coherence = self._compute_thematic_coherence(sentences)
        
        # Combinação das abordagens
        weights = {'semantic': 0.5, 'cohesion': 0.3, 'thematic': 0.2}
        
        combined_coherence = (
            weights['semantic'] * semantic_coherence +
            weights['cohesion'] * cohesion_coherence +
            weights['thematic'] * thematic_coherence
        )
        
        # Normalizar para escala 0 a 10
        final_coherence = np.clip(combined_coherence, 0.0, 10.0)
        
        # Confiança baseada na quantidade de sentenças e consistência
        coherence_values = [semantic_coherence, cohesion_coherence, thematic_coherence]
        base_confidence = self._calculate_confidence_from_consistency(coherence_values, scale_factor=0.1)
        
        # Ajustar confiança baseado no número de sentenças
        sentence_factor = min(len(sentences) / 10.0, 1.0)  # Mais sentenças = maior confiança
        final_confidence = base_confidence * sentence_factor
        
        return {
            'value': final_coherence,
            'confidence': final_confidence,
            'metadata': {
                'semantic_coherence': semantic_coherence,
                'cohesion_coherence': cohesion_coherence,
                'thematic_coherence': thematic_coherence,
                'sentence_count': len(sentences),
                'method': 'semantic_cohesion_thematic'
            }
        }
    
    def _compute_lexical_valence(self, tokens) -> float:
        """Computa valência baseada em dicionário lexical"""
        total_valence = 0.0
        valence_words_found = 0
        
        for token in tokens:
            if token.lemma_.lower() in self.valence_words:
                total_valence += self.valence_words[token.lemma_.lower()]
                valence_words_found += 1
        
        if valence_words_found == 0:
            return 0.0
        
        return total_valence / valence_words_found
    
    async def _compute_azure_valence(self, text: str) -> float:
        """Computa valência usando Azure Language Service"""
        try:
            sentiment_result = await self.azure_integration.analyze_sentiment(text)
            
            if sentiment_result and 'confidence_scores' in sentiment_result:
                positive_score = sentiment_result['confidence_scores'].get('positive', 0)
                negative_score = sentiment_result['confidence_scores'].get('negative', 0)
                
                # Converter para escala -5 a +5
                valence = (positive_score - negative_score) * 5
                return np.clip(valence, -5.0, 5.0)
        
        except Exception as e:
            self.logger.warning(f"Azure sentiment analysis failed: {e}")
        
        return 0.0
    
    def _compute_sentence_valence(self, sentence) -> float:
        """Computa valência de uma sentença específica"""
        sentence_tokens = [token for token in sentence if not token.is_space]
        return self._compute_lexical_valence(sentence_tokens)
    
    def _compute_lexical_arousal(self, tokens) -> float:
        """Computa arousal baseado em dicionário lexical"""
        total_arousal = 0.0
        arousal_words_found = 0
        
        for token in tokens:
            if token.lemma_.lower() in self.arousal_words:
                total_arousal += self.arousal_words[token.lemma_.lower()]
                arousal_words_found += 1
        
        if arousal_words_found == 0:
            return 5.0  # Arousal neutro
        
        return total_arousal / arousal_words_found
    
    def _compute_audio_arousal(self, audio_features) -> float:
        """Computa arousal baseado em características de áudio"""
        if not audio_features:
            return 5.0
        
        # Velocidade de fala como indicador de arousal
        speech_rate = audio_features.get('speech_rate', 120)
        speech_arousal = min(max((speech_rate - 100) / 20, 0), 10)
        
        # Variância de pitch como indicador
        pitch_variance = audio_features.get('pitch_variance', 2.0)
        pitch_arousal = min(pitch_variance * 2, 10)
        
        # Jitter/shimmer como indicadores de tensão vocal
        jitter = audio_features.get('jitter', 0.5)
        shimmer = audio_features.get('shimmer', 0.5)
        tension_arousal = min((jitter + shimmer) * 3, 10)
        
        # Combinação ponderada
        combined_arousal = (
            0.4 * speech_arousal +
            0.3 * pitch_arousal +
            0.3 * tension_arousal
        )
        
        return np.clip(combined_arousal, 0.0, 10.0)
    
    def _compute_textual_arousal_indicators(self, doc, tokens) -> float:
        """Computa indicadores textuais de arousal"""
        
        # Indicadores de alta ativação textual
        indicators = {
            'exclamation_marks': doc.text.count('!') * 0.5,
            'question_marks': doc.text.count('?') * 0.3,
            'capitalization': sum(1 for token in tokens if token.text.isupper() and len(token.text) > 2) * 0.4,
            'repetition': self._count_repetitions(tokens) * 0.6,
            'interruptions': doc.text.count('...') * 0.3
        }
        
        # Soma ponderada dos indicadores
        total_textual_arousal = sum(indicators.values())
        
        # Normalizar baseado no comprimento do texto
        text_length_factor = len(tokens) / 100.0  # Normalizar por 100 palavras
        normalized_arousal = total_textual_arousal / max(text_length_factor, 0.1)
        
        # Adicionar arousal base de 5.0 e limitar a 10.0
        return min(5.0 + normalized_arousal, 10.0)
    
    def _compute_semantic_coherence(self, sentences) -> float:
        """Computa coerência semântica entre sentenças"""
        if len(sentences) < 2:
            return 10.0
        
        similarities = []
        for i in range(len(sentences) - 1):
            sent1, sent2 = sentences[i], sentences[i + 1]
            
            # Verificar se as sentenças têm vetores e conteúdo suficiente
            if (sent1.has_vector and sent2.has_vector and 
                len(sent1.text.strip()) > 3 and len(sent2.text.strip()) > 3):
                
                similarity = sent1.similarity(sent2)
                if not np.isnan(similarity):
                    similarities.append(similarity)
        
        if not similarities:
            return 5.0  # Coerência neutra se não conseguir calcular
        
        # Converter similaridade (0-1) para escala de coerência (0-10)
        avg_similarity = np.mean(similarities)
        coherence_score = avg_similarity * 10
        
        return np.clip(coherence_score, 0.0, 10.0)
    
    def _compute_cohesion_coherence(self, doc, sentences) -> float:
        """Computa coerência baseada em conectivos e coesão"""
        
        # Conectivos que indicam coerência
        connectives = {
            'porque', 'portanto', 'então', 'assim', 'consequentemente', 'logo',
            'entretanto', 'contudo', 'porém', 'todavia', 'no entanto',
            'além disso', 'também', 'igualmente', 'da mesma forma',
            'por exemplo', 'ou seja', 'isto é', 'em outras palavras'
        }
        
        # Contar conectivos
        text_lower = doc.text.lower()
        connective_count = sum(text_lower.count(conn) for conn in connectives)
        
        # Normalizar pelo número de sentenças
        connective_density = connective_count / max(len(sentences), 1)
        
        # Converter para escala 0-10 (densidade ideal é cerca de 0.2-0.3)
        cohesion_score = min(connective_density * 30, 10)
        
        # Penalizar ausência total de conectivos em textos longos
        if connective_count == 0 and len(sentences) > 3:
            cohesion_score = max(cohesion_score, 3.0)
        
        return cohesion_score
    
    def _compute_thematic_coherence(self, sentences) -> float:
        """Computa consistência temática"""
        
        # Extrair entidades nomeadas de cada sentença
        sentence_entities = []
        for sent in sentences:
            entities = set(ent.lemma_.lower() for ent in sent.ents if ent.label_ in ['PER', 'ORG', 'LOC'])
            if entities:
                sentence_entities.append(entities)
        
        if len(sentence_entities) < 2:
            return 7.0  # Assumir coerência razoável se não há entidades suficientes
        
        # Calcular sobreposição de entidades entre sentenças
        overlaps = []
        for i in range(len(sentence_entities) - 1):
            entities1, entities2 = sentence_entities[i], sentence_entities[i + 1]
            
            if entities1 and entities2:
                intersection = len(entities1.intersection(entities2))
                union = len(entities1.union(entities2))
                overlap = intersection / union if union > 0 else 0
                overlaps.append(overlap)
        
        if not overlaps:
            return 7.0
        
        # Converter para escala 0-10
        avg_overlap = np.mean(overlaps)
        thematic_score = 5.0 + (avg_overlap * 5.0)  # Base de 5, até 10
        
        return np.clip(thematic_score, 0.0, 10.0)
    
    def _count_repetitions(self, tokens) -> int:
        """Conta repetições de palavras como indicador de arousal"""
        word_counts = {}
        for token in tokens:
            if not token.is_stop and not token.is_punct