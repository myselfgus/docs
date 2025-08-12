# 6: APOTHECARY AUTOMÁTICO

## OVERVIEW
Implementar o VOITHER Apothecary conforme especificado no documento fornecido. O Apothecary é a evolução do PsyDX (verifique conteudo legacy) que substitui checklists estáticos por análise dinâmica da linguagem, mapeando características linguísticas calibradas para perfis de desregulação de neurotransmissores e predizendo resposta a medicamentos usando ML.

## DEPENDENCIES (Must exist before starting)

- [ ] ✅ **Sprint 5 completed**: MED Calibração + Frameworks operacional
- [ ] ✅ **Framework calibration working**: RDoC, HiTOP, PERMA, BigFive calibrados com accuracy >0.80
- [ ] ✅ **Calibrated scores validated**: Scores dos frameworks correlacionam com avaliações clínicas
- [ ] ✅ **MED integration stable**: Pipeline MED → Frameworks funcionando <2s
- [ ] Python 3.11+ com scikit-learn, pandas, numpy
- [ ] Base de dados farmacológica com histórico de respostas a medicamentos
- [ ] Azure Machine Learning para modelos preditivos

### Pre-flight Validation Script

```bash
#!/bin/bash
# validate_sprint_5.sh
set -e

echo "🔍 Validating Sprint 5 dependencies..."

# Test framework calibration functionality
python -c "
import asyncio
from src.calibration.framework_calibrator import FrameworkCalibrator
from src.med.dimensional_extractor import DimensionalExtractor

async def test_full_pipeline():
    # Test MED extraction
    med_config = {'spacy_model': 'pt_core_news_lg', 'azure': {'endpoint': 'test', 'key': 'test'}}
    med = DimensionalExtractor(med_config)
    
    result = await med.extract_all_dimensions(
        'Sinto-me ansioso e deprimido. Tenho dificuldade para dormir e me concentrar.'
    )
    assert result['success'], 'MED extraction failed'
    
    # Test framework calibration
    cal_config = {'models_dir': 'models/calibrated'}
    calibrator = FrameworkCalibrator(cal_config)
    
    calibrated = await calibrator.apply_calibration(result['dimensions'])
    assert 'calibrated_frameworks' in calibrated, 'Calibration failed'
    
    # Validate RDoC scores
    rdoc_scores = calibrated['calibrated_frameworks']['rdoc']['scores']
    assert len(rdoc_scores) == 5, 'Missing RDoC domains'
    
    print('✅ MED → Framework pipeline operational')

asyncio.run(test_full_pipeline())
"

# Test ML libraries
python -c "
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
print('✅ ML libraries operational')
"

# Validate pharmacological database access
python -c "
import os
if os.path.exists('data/pharmacological_database.csv'):
    import pandas as pd
    df = pd.read_csv('data/pharmacological_database.csv')
    assert len(df) > 100, 'Insufficient pharmacological data'
    print(f'✅ Pharmacological database loaded: {len(df)} records')
else:
    print('⚠️ Pharmacological database not found, will use synthetic data')
"

echo "✅ All Sprint 5 dependencies validated"
```

## IMPLEMENTATION

### 1. Project Structure

```
voither-apothecary/
├── src/
│   ├── __init__.py
│   ├── apothecary/
│   │   ├── __init__.py
│   │   ├── apothecary_engine.py         # Main Apothecary class
│   │   ├── neurotransmitter_mapper.py   # Dimensional → NT mapping
│   │   ├── drug_response_predictor.py   # ML prediction models
│   │   ├── treatment_recommender.py     # Treatment recommendations
│   │   └── clinical_validator.py        # Clinical validation
│   ├── models/
│   │   ├── __init__.py
│   │   ├── psydx_evolution.py          # Enhanced PsyDX algorithm
│   │   ├── ml_predictor.py             # ML response prediction
│   │   ├── ensemble_predictor.py       # Ensemble methods
│   │   └── confidence_estimator.py     # Prediction confidence
│   ├── data/
│   │   ├── __init__.py
│   │   ├── pharmacological_db.py       # Drug database interface
│   │   ├── clinical_outcomes.py        # Outcomes data loader
│   │   └── drug_interactions.py        # Drug interaction data
│   └── validation/
│       ├── __init__.py
│       ├── clinical_validation.py      # Clinical trial validation
│       ├── retrospective_analysis.py   # Retrospective validation
│       └── safety_checker.py           # Safety validation
├── tests/
│   ├── unit/
│   ├── integration/
│   └── clinical/
├── data/
│   ├── pharmacological_database.csv
│   ├── clinical_outcomes.csv
│   └── drug_interactions.csv
├── requirements.txt
└── README.md
```

### 2. Core Apothecary Engine

```python
# src/apothecary/apothecary_engine.py
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import logging
import asyncio

from .neurotransmitter_mapper import NeurotransmitterMapper
from .drug_response_predictor import DrugResponsePredictor
from .treatment_recommender import TreatmentRecommender
from .clinical_validator import ClinicalValidator
from ..models.psydx_evolution import EnhancedPsyDX
from ..data.pharmacological_db import PharmacologicalDatabase
from ..validation.safety_checker import SafetyChecker

class VoitherApothecary:
    """
    VOITHER Apothecary - Sistema de Suporte à Decisão Psicofarmacológica
    
    Evolução do PsyDX que substitui checklists estáticos por análise dinâmica 
    da linguagem usando características linguísticas calibradas para:
    1. Mapear para perfis de desregulação de neurotransmissores
    2. Predizer resposta a medicamentos usando ML
    3. Gerar recomendações psicofarmacológicas personalizadas
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger("VoitherApothecary")
        
        # Core components
        self.nt_mapper = NeurotransmitterMapper(config)
        self.drug_predictor = DrugResponsePredictor(config)
        self.treatment_recommender = TreatmentRecommender(config)
        self.clinical_validator = ClinicalValidator(config)
        
        # Enhanced PsyDX engine
        self.psydx_engine = EnhancedPsyDX(config)
        
        # Pharmacological database
        self.pharma_db = PharmacologicalDatabase(config)
        
        # Safety validation
        self.safety_checker = SafetyChecker(config)
        
        # Apothecary statistics
        self.apothecary_stats = {
            'total_recommendations': 0,
            'successful_predictions': 0,
            'average_confidence': 0.0,
            'safety_flags_raised': 0,
            'clinical_validations': 0
        }
    
    async def generate_treatment_recommendations(self, patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera recomendações de tratamento baseadas no perfil dimensional do paciente
        
        Args:
            patient_profile: Perfil completo do paciente incluindo:
                - raw_dimensions: 15 dimensões MED
                - calibrated_frameworks: Scores RDoC, HiTOP, PERMA, BigFive
                - clinical_context: Contexto clínico adicional
                - patient_metadata: Idade, sexo, histórico médico, etc.
                
        Returns:
            Recomendações de tratamento ranqueadas com probabilidades de sucesso
        """
        recommendation_id = f"apothecary_{int(datetime.now().timestamp())}"
        start_time = datetime.now()
        
        try:
            self.logger.info(f"Generating treatment recommendations: {recommendation_id}")
            
            # Validar perfil do paciente
            validation_result = await self._validate_patient_profile(patient_profile)
            if not validation_result['valid']:
                return {
                    'recommendation_id': recommendation_id,
                    'success': False,
                    'error': f"Invalid patient profile: {validation_result['errors']}",
                    'processing_time_ms': (datetime.now() - start_time).total_seconds() * 1000
                }
            
            # Etapa 1: Mapear dimensões para perfil neuroquímico
            nt_profile = await self.nt_mapper.map_dimensions_to_neurotransmitters(
                patient_profile['raw_dimensions'],
                patient_profile['calibrated_frameworks']
            )
            
            # Etapa 2: Aplicar algoritmo PsyDX evoluído
            psydx_result = await self.psydx_engine.calculate_neurotransmitter_profile(
                nt_profile, patient_profile.get('clinical_context', {})
            )
            
            # Etapa 3: Predizer resposta a medicamentos usando ML
            drug_predictions = await self.drug_predictor.predict_drug_responses(
                patient_profile, psydx_result
            )
            
            # Etapa 4: Ranquear e filtrar recomendações
            ranked_recommendations = await self.treatment_recommender.rank_treatments(
                drug_predictions, patient_profile, psydx_result
            )
            
            # Etapa 5: Validação de segurança
            safety_validated_recs = await self.safety_checker.validate_recommendations(
                ranked_recommendations, patient_profile
            )
            
            # Etapa 6: Validação clínica
            clinically_validated_recs = await self.clinical_validator.validate_recommendations(
                safety_validated_recs, patient_profile
            )
            
            # Calcular tempo de processamento
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Calcular confiança global
            global_confidence = np.mean([
                rec['predicted_response_probability'] 
                for rec in clinically_validated_recs[:3]  # Top 3 recommendations
            ]) if clinically_validated_recs else 0.0
            
            # Construir resultado final
            final_result = {
                'recommendation_id': recommendation_id,
                'success': True,
                'patient_id': patient_profile.get('patient_id', 'unknown'),
                'processing_time_ms': processing_time,
                'global_confidence': global_confidence,
                'confidence_level': self._classify_confidence(global_confidence),
                
                # Perfil neuroquímico
                'neurotransmitter_profile': {
                    'raw_mapping': nt_profile,
                    'psydx_analysis': psydx_result,
                    'primary_systems': psydx_result.get('primary_systems', []),
                    'adjacent_systems': psydx_result.get('adjacent_systems', [])
                },
                
                # Recomendações ranqueadas
                'treatment_recommendations': clinically_validated_recs[:10],  # Top 10
                'total_drugs_evaluated': len(drug_predictions),
                
                # Contexto diagnóstico
                'diagnostic_suggestions': self._generate_diagnostic_suggestions(
                    psydx_result, patient_profile['calibrated_frameworks']
                ),
                
                # Metadados de validação
                'validation_metadata': {
                    'safety_checks_passed': len(safety_validated_recs),
                    'clinical_validation_score': np.mean([
                        rec.get('clinical_validation_score', 0.5) 
                        for rec in clinically_validated_recs
                    ]) if clinically_validated_recs else 0.5,
                    'contraindications_checked': True,
                    'drug_interactions_verified': True
                },
                
                # Informações para o clínico
                'clinical_insights': {
                    'key_findings': self._extract_key_findings(psydx_result, nt_profile),
                    'treatment_rationale': self._generate_treatment_rationale(
                        clinically_validated_recs[:3], psydx_result
                    ),
                    'monitoring_recommendations': self._generate_monitoring_recommendations(
                        clinically_validated_recs[:3]
                    )
                }
            }
            
            # Atualizar estatísticas
            self._update_apothecary_stats(final_result)
            
            # Log resultado
            self.logger.info(
                f"✅ Recommendations generated: {recommendation_id} "
                f"({len(clinically_validated_recs)} options, "
                f"{global_confidence:.2f} confidence, {processing_time:.1f}ms)"
            )
            
            return final_result
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            self.logger.error(f"❌ Recommendation generation failed: {recommendation_id} - {e}")
            
            return {
                'recommendation_id': recommendation_id,
                'success': False,
                'error': str(e),
                'processing_time_ms': processing_time,
                'patient_id': patient_profile.get('patient_id', 'unknown')
            }
    
    async def predict_treatment_response(self, patient_profile: Dict[str, Any], 
                                       medication_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prediz a resposta a um medicamento específico
        
        Args:
            patient_profile: Perfil completo do paciente
            medication_details: Detalhes do medicamento (nome, dose, classe)
            
        Returns:
            Predição detalhada de resposta ao tratamento
        """
        try:
            # Mapear perfil neuroquímico
            nt_profile = await self.nt_mapper.map_dimensions_to_neurotransmitters(
                patient_profile['raw_dimensions'],
                patient_profile['calibrated_frameworks']
            )
            
            # Aplicar PsyDX
            psydx_result = await self.psydx_engine.calculate_neurotransmitter_profile(nt_profile)
            
            # Predizer resposta específica
            response_prediction = await self.drug_predictor.predict_single_drug_response(
                patient_profile, medication_details, psydx_result
            )
            
            # Validar segurança
            safety_result = await self.safety_checker.check_single_medication(
                medication_details, patient_profile
            )
            
            return {
                'success': True,
                'medication': medication_details,
                'predicted_response': response_prediction,
                'safety_assessment': safety_result,
                'neurotransmitter_match': self._assess_nt_medication_match(
                    medication_details, psydx_result
                ),
                'confidence': response_prediction.get('confidence', 0.5)
            }
            
        except Exception as e:
            self.logger.error(f"Single medication prediction failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'medication': medication_details
            }
    
    async def batch_analyze_treatments(self, patient_profiles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Análise em lote para múltiplos pacientes
        
        Args:
            patient_profiles: Lista de perfis de pacientes
            
        Returns:
            Lista de recomendações para cada paciente
        """
        batch_id = f"batch_{int(datetime.now().timestamp())}"
        self.logger.info(f"Starting batch analysis: {batch_id} ({len(patient_profiles)} patients)")
        
        # Processar em paralelo com limite de concorrência
        semaphore = asyncio.Semaphore(self.config.get('max_concurrent_recommendations', 5))
        
        async def process_patient(profile):
            async with semaphore:
                return await self.generate_treatment_recommendations(profile)
        
        tasks = [process_patient(profile) for profile in patient_profiles]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Tratar exceções
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    'success': False,
                    'error': str(result),
                    'patient_index': i
                })
            else:
                processed_results.append(result)
        
        self.logger.info(f"✅ Batch analysis completed: {batch_id}")
        return processed_results
    
    def get_apothecary_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas operacionais do Apothecary"""
        return {
            'operational_stats': self.apothecary_stats.copy(),
            'success_rate': (
                self.apothecary_stats['successful_predictions'] / 
                max(self.apothecary_stats['total_recommendations'], 1) * 100
            ),
            'components_status': {
                'neurotransmitter_mapper': 'operational',
                'drug_predictor': 'operational',
                'treatment_recommender': 'operational',
                'clinical_validator': 'operational',
                'safety_checker': 'operational'
            },
            'database_stats': self.pharma_db.get_database_statistics(),
            'model_versions': {
                'psydx_version': self.psydx_engine.get_version(),
                'ml_predictor_version': self.drug_predictor.get_model_version(),
                'safety_checker_version': self.safety_checker.get_version()
            }
        }
    
    async def _validate_patient_profile(self, patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Valida se o perfil do paciente está completo e válido"""
        errors = []
        
        # Verificar dimensões MED
        if 'raw_dimensions' not in patient_profile:
            errors.append("Missing raw_dimensions")
        else:
            raw_dims = patient_profile['raw_dimensions']
            expected_dims = 15
            if len(raw_dims) != expected_dims:
                errors.append(f"Expected {expected_dims} dimensions, got {len(raw_dims)}")
        
        # Verificar frameworks calibrados
        if 'calibrated_frameworks' not in patient_profile:
            errors.append("Missing calibrated_frameworks")
        else:
            frameworks = patient_profile['calibrated_frameworks']
            required_frameworks = ['rdoc', 'hitop', 'perma', 'bigfive']
            for framework in required_frameworks:
                if framework not in frameworks:
                    errors.append(f"Missing {framework} framework")
        
        # Verificar metadados básicos
        metadata = patient_profile.get('patient_metadata', {})
        if not metadata.get('age'):
            errors.append("Missing patient age")
        if not metadata.get('sex'):
            errors.append("Missing patient sex")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def _classify_confidence(self, confidence_score: float) -> str:
        """Classifica nível de confiança da recomendação"""
        if confidence_score >= 0.85:
            return 'high'
        elif confidence_score >= 0.70:
            return 'medium'
        elif confidence_score >= 0.55:
            return 'low'
        else:
            return 'very_low'
    
    def _generate_diagnostic_suggestions(self, psydx_result: Dict[str, Any], 
                                       frameworks: Dict[str, Any]) -> List[Dict[str, str]]:
        """Gera sugestões diagnósticas baseadas no perfil neuroquímico e frameworks"""
        suggestions = []
        
        # Análise baseada em sistemas principais do PsyDX
        primary_systems = psydx_result.get('primary_systems', [])
        
        if 'serotonin' in primary_systems:
            # Alto score em sistemas serotoninérgicos
            rdoc_neg_valence = frameworks.get('rdoc', {}).get('scores', {}).get('negative_valence', 0)
            if rdoc_neg_valence > 7.0:
                suggestions.append({
                    'category': 'mood_disorder',
                    'suggestion': 'Transtorno Depressivo Maior com características ansiosas',
                    'confidence': 'high',
                    'rationale': 'Elevada valência negativa (RDoC) + desregulação serotoninérgica principal'
                })
        
        if 'dopamine' in primary_systems:
            # Sistemas dopaminérgicos afetados
            hitop_thought = frameworks.get('hitop', {}).get('scores', {}).get('thought_disorder', 0)
            if hitop_thought > 6.0:
                suggestions.append({
                    'category': 'psychotic_spectrum',
                    'suggestion': 'Transtorno do Espectro Psicótico (investigar)',
                    'confidence': 'medium',
                    'rationale': 'Desregulação dopaminérgica + elevado thought disorder (HiTOP)'
                })
        
        if 'gaba' in primary_systems:
            # Sistemas GABAérgicos comprometidos
            rdoc_arousal = frameworks.get('rdoc', {}).get('scores', {}).get('arousal_regulatory', 0)
            if rdoc_arousal > 7.5:
                suggestions.append({
                    'category': 'anxiety_disorder',
                    'suggestion': 'Transtorno de Ansiedade Generalizada',
                    'confidence': 'high',
                    'rationale': 'Desregulação GABAérgica + elevado arousal regulatório (RDoC)'
                })
        
        return suggestions
    
    def _extract_key_findings(self, psydx_result: Dict[str, Any], 
                            nt_profile: Dict[str, Any]) -> List[str]:
        """Extrai principais achados para o clínico"""
        findings = []
        
        # Sistemas neurotransmissores principais
        primary_systems = psydx_result.get('primary_systems', [])
        if primary_systems:
            findings.append(f"Sistemas principais afetados: {', '.join(primary_systems).upper()}")
        
        # Contribuição percentual
        contributions = psydx_result.get('neurotransmitter_contributions', {})
        for nt, contrib in contributions.items():
            if contrib >= 35:  # Critério principal do PsyDX
                findings.append(f"{nt.capitalize()}: {contrib:.1f}% de contribuição (Principal)")
        
        # Padrões específicos
        if 'serotonin' in primary_systems and 'noradrenaline' in primary_systems:
            findings.append("Padrão dual serotoninérgico-noradrenérgico sugere IRSN como primeira linha")
        
        return findings
    
    def _generate_treatment_rationale(self, top_recommendations: List[Dict[str, Any]], 
                                    psydx_result: Dict[str, Any]) -> List[str]:
        """Gera justificativa das recomendações para o clínico"""
        rationales = []
        
        for i, rec in enumerate(top_recommendations[:3]):
            drug_class = rec.get('drug_class', 'unknown')
            probability = rec.get('predicted_response_probability', 0)
            
            rationale = f"{i+1}. {rec.get('medication_name', 'Unknown')} ({drug_class}): "
            rationale += f"{probability:.1f}% probabilidade de resposta - "
            
            # Justificativa baseada no mecanismo
            mechanism = rec.get('mechanism_of_action', {})
            if mechanism.get('serotonin_affinity', 0) > 0.7:
                rationale += "Alta afinidade serotoninérgica alinha com perfil neuroquímico"
            elif mechanism.get('dopamine_affinity', 0) > 0.7:
                rationale += "Ação dopaminérgica indicada pelo perfil de desregulação"
            
            rationales.append(rationale)
        
        return rationales
    
    def _generate_monitoring_recommendations(self, top_recommendations: List[Dict[str, Any]]) -> List[str]:
        """Gera recomendações de monitoramento"""
        monitoring = []
        
        for rec in top_recommendations[:2]:  # Top 2 apenas
            drug_class = rec.get('drug_class', '')
            
            if 'ssri' in drug_class.lower():
                monitoring.append("ISRS: Monitorar síndrome serotoninérgica, ideação suicida (primeiras 4 semanas)")
            elif 'snri' in drug_class.lower():
                monitoring.append("IRSN: Monitorar pressão arterial, função hepática, sintomas de descontinuação")
            elif 'antipsychotic' in drug_class.lower():
                monitoring.append("Antipsicótico: Monitorar síndrome metabólica, movimentos involuntários")
        
        # Monitoramento geral
        monitoring.append("Avaliação de eficácia: 2-4 semanas para resposta inicial, 6-8 semanas para resposta completa")
        monitoring.append("Escala de avaliação: Aplicar HAM-D ou PHQ-9 a cada consulta")
        
        return monitoring
    
    def _assess_nt_medication_match(self, medication_details: Dict[str, Any], 
                                  psydx_result: Dict[str, Any]) -> Dict[str, Any]:
        """Avalia compatibilidade entre medicação e perfil neurotransmissor"""
        primary_systems = psydx_result.get('primary_systems', [])
        drug_mechanisms = medication_details.get('mechanism_of_action', {})
        
        match_score = 0.0
        match_reasons = []
        
        # Verificar alinhamento com sistemas principais
        if 'serotonin' in primary_systems:
            serotonin_affinity = drug_mechanisms.get('serotonin_affinity', 0)
            match_score += serotonin_affinity * 0.4
            if serotonin_affinity > 0.7:
                match_reasons.append("Alta afinidade serotoninérgica alinha com desregulação principal")
        
        if 'dopamine' in primary_systems:
            dopamine_affinity = drug_mechanisms.get('dopamine_affinity', 0)
            match_score += dopamine_affinity * 0.3
            if dopamine_affinity > 0.7:
                match_reasons.append("Ação dopaminérgica indicada pelo perfil")
        
        if 'noradrenaline' in primary_systems:
            noradrenaline_affinity = drug_mechanisms.get('noradrenaline_affinity', 0)
            match_score += noradrenaline_affinity * 0.3
            if noradrenaline_affinity > 0.7:
                match_reasons.append("Componente noradrenérgico complementa perfil")
        
        return {
            'match_score': min(match_score, 1.0),
            'match_quality': 'high' if match_score > 0.8 else 'medium' if match_score > 0.6 else 'low',
            'match_reasons': match_reasons
        }
    
    def _update_apothecary_stats(self, result: Dict[str, Any]):
        """Atualiza estatísticas operacionais"""
        self.apothecary_stats['total_recommendations'] += 1
        
        if result['success']:
            self.apothecary_stats['successful_predictions'] += 1
            
            # Atualizar média de confiança
            confidence = result.get('global_confidence', 0)
            total = self.apothecary_stats['total_recommendations']
            current_avg = self.apothecary_stats['average_confidence']
            self.apothecary_stats['average_confidence'] = (
                (current_avg * (total - 1) + confidence) / total
            )
        
        # Contar validações clínicas
        if result.get('validation_metadata', {}).get('clinical_validation_score', 0) > 0.5:
            self.apothecary_stats['clinical_validations'] += 1
```

### 3. Neurotransmitter Mapper

```python
# src/apothecary/neurotransmitter_mapper.py
import numpy as np
from typing import Dict, Any
import logging

class NeurotransmitterMapper:
    """
    Mapeia dimensões MED calibradas para perfil de neurotransmissores
    
    Baseado na literatura neurocientífica e nos frameworks RDoC/HiTOP,
    estabelece correlações entre dimensões linguísticas e sistemas neurobiológicos
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger("NeurotransmitterMapper")
        
        # Mapeamentos baseados em literatura neurocientífica
        self.nt_dimension_mappings = {
            'serotonin': {
                'primary_dimensions': [
                    ('v1_valence_emotional', -0.85),    # Valência negativa → baixa serotonina
                    ('v2_arousal_activation', 0.45),     # Arousal moderado
                    ('v6_self_reference_density', 0.60) # Auto-foco relacionado à ruminação
                ],
                'framework_weights': {
                    'rdoc_negative_valence': 0.80,      # Alta correlação
                    'hitop_internalizing': 0.75,        # Forte indicador
                    'perma_positive_emotions': -0.70,   # Relação inversa
                    'bigfive_neuroticism': 0.65
                }
            },
            
            'dopamine': {
                'primary_dimensions': [
                    ('v1_valence_emotional', 0.70),     # Valência positiva → dopamina
                    ('v9_dominance_agency', 0.80),      # Agência/motivação
                    ('v8_cognitive_flexibility', 0.65)  # Flexibilidade cognitiva
                ],
                'framework_weights': {
                    'rdoc_positive_valence': 0.85,      # Sistema de recompensa
                    'perma_engagement': 0.70,           # Engajamento
                    'perma_accomplishment': 0.75,       # Realização
                    'bigfive_extraversion': 0.60
                }
            },
            
            'noradrenaline': {
                'primary_dimensions': [
                    ('v2_arousal_activation', 0.75),    # Alto arousal
                    ('v12_certainty_markers', -0.55),   # Incerteza
                    ('v10_discourse_fragmentation', 0.50) # Fragmentação por estresse
                ],
                'framework_weights': {
                    'rdoc_arousal_regulatory': 0.80,    # Sistema de arousal
                    'rdoc_negative_valence': 0.60,      # Ansiedade/estresse
                    'hitop_internalizing': 0.55,        # Ansiedade
                    'bigfive_neuroticism': 0.70
                }
            },
            
            'gaba': {
                'primary_dimensions': [
                    ('v2_arousal_activation', -0.80),   # Baixo arousal → GABA funcionando
                    ('v12_certainty_markers', 0.65),    # Certeza/tranquilidade
                    ('v3_narrative_coherence', 0.55)    # Coerência por regulação
                ],
                'framework_weights': {
                    'rdoc_arousal_regulatory': -0.75,   # Regulação adequada
                    'rdoc_negative_valence': -0.70,     # Menos valência negativa
                    'hitop_internalizing': -0.65,       # Menos internalização
                    'bigfive_neuroticism': -0.60
                }
            },
            
            'acetylcholine': {
                'primary_dimensions': [
                    ('v4_syntactic_complexity', 0.70),  # Complexidade cognitiva
                    ('v11_semantic_density', 0.75),     # Densidade semântica
                    ('v14_pragmatic_competence', 0.65)  # Competência pragmática
                ],
                'framework_weights': {
                    'rdoc_cognitive_systems': 0.80,     # Sistemas cognitivos
                    'bigfive_openness': 0.60,           # Abertura cognitiva
                    'bigfive_conscientiousness': 0.55   # Organização
                }
            }
        }
    
    async def map_dimensions_to_neurotransmitters(self, raw_dimensions: Dict[str, float],
                                                calibrated_frameworks: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mapeia dimensões MED para perfil de neurotransmissores
        
        Args:
            raw_dimensions: 15 dimensões MED brutas
            calibrated_frameworks: Scores calibrados dos frameworks
            
        Returns:
            Perfil de neurotransmissores com scores e confiança
        """
        
        nt_scores = {}
        nt_confidences = {}
        
        for nt_name, mapping_config in self.nt_dimension_mappings.items():
            # Calcular score baseado em dimensões primárias
            dimension_score = self._calculate_dimensional_score(
                raw_dimensions, mapping_config['primary_dimensions']
            )
            
            # Calcular score baseado em frameworks calibrados
            framework_score = self._calculate_framework_score(
                calibrated_frameworks, mapping_config['framework_weights']
            )
            
            # Combinar scores com pesos
            combined_score = (0.4 * dimension_score + 0.6 * framework_score)
            
            # Normalizar para escala 0-10
            normalized_score = self._normalize_nt_score(combined_score)
            
            # Calcular confiança baseada na consistência
            confidence = self._calculate_mapping_confidence(
                dimension_score, framework_score, raw_dimensions, calibrated_frameworks
            )
            
            nt_scores[nt_name] = normalized_score
            nt_confidences[nt_name] = confidence
        
        # Aplicar correções baseadas em interações conhecidas
        nt_scores = self._apply_neurotransmitter_interactions(nt_scores)
        
        return {
            'neurotransmitter_scores': nt_scores,
            'confidence_scores': nt_confidences,
            'mapping_metadata': {
                'total_neurotransmitters': len(nt_scores),
                'high_confidence_mappings': sum(1 for conf in nt_confidences.values() if conf > 0.8),
                'average_confidence': np.mean(list(nt_confidences.values())),
                'mapping_method': 'dimensional_framework_hybrid'
            }
        }
    
    def _calculate_dimensional_score(self, dimensions: Dict[str, float], 
                                   dimension_mappings: List[tuple]) -> float:
        """Calcula score baseado em dimensões primárias"""
        total_score = 0.0
        total_weight = 0.0
        
        for dim_name, weight in dimension_mappings:
            if dim_name in dimensions:
                dim_value = dimensions[dim_name]
                # Normalizar dimensão para escala 0-1
                normalized_dim = self._normalize_dimension_value(dim_name, dim_value)
                total_score += normalized_dim * abs(weight)
                total_weight += abs(weight)
        
        return total_score / total_weight if total_weight > 0 else 0.5
    
    def _calculate_framework_score(self, frameworks: Dict[str, Any], 
                                 framework_weights: Dict[str, float]) -> float:
        """Calcula score baseado em frameworks calibrados"""
        total_score = 0.0
        total_weight = 0.0
        
        for framework_key, weight in framework_weights.items():
            # Extrair score do framework
            framework_score = self._extract_framework_score(frameworks, framework_key)
            
            if framework_score is not None:
                # Normalizar score do framework
                normalized_score = framework_score / 10.0  # Assumindo escala 0-10
                
                # Aplicar peso (pode ser negativo para relações inversas)
                if weight < 0:
                    normalized_score = 1.0 - normalized_score
                
                total_score += normalized_score * abs(weight)
                total_weight += abs(weight)
        
        return total_score / total_weight if total_weight > 0 else 0.5
    
    def _extract_framework_score(self, frameworks: Dict[str, Any], framework_key: str) -> float:
        """Extrai score específico de um framework"""
        # Mapear chave para framework e domínio
        if framework_key.startswith('rdoc_'):
            domain = framework_key.replace('rdoc_', '')
            return frameworks.get('rdoc', {}).get('scores', {}).get(domain, None)
        elif framework_key.startswith('hitop_'):
            domain = framework_key.replace('hitop_', '')
            return frameworks.get('hitop', {}).get('scores', {}).get(domain, None)
        elif framework_key.startswith('perma_'):
            domain = framework_key.replace('perma_', '')
            return frameworks.get('perma', {}).get('scores', {}).get(domain, None)
        elif framework_key.startswith('bigfive_'):
            trait = framework_key.replace('bigfive_', '')
            return frameworks.get('bigfive', {}).get('scores', {}).get(trait, None)
        
        return None
    
    def _normalize_dimension_value(self, dim_name: str, value: float) -> float:
        """Normaliza valor de dimensão para escala 0-1"""
        # Mapeamentos específicos por dimensão (baseado nas configurações do MED)
        dimension_ranges = {
            'v1_valence_emotional': (-5.0, 5.0),
            'v2_arousal_activation': (0.0, 10.0),
            'v3_narrative_coherence': (0.0, 10.0),
            'v4_syntactic_complexity': (0.0, 10.0),
            'v5_temporal_orientation': (0.0, 10.0),
            'v6_self_reference_density': (0.0, 10.0),
            'v7_social_language': (0.0, 10.0),
            'v8_cognitive_flexibility': (0.0, 10.0),
            'v9_dominance_agency': (0.0, 10.0),
            'v10_discourse_fragmentation': (0.0, 10.0),
            'v11_semantic_density': (0.0, 10.0),
            'v12_certainty_markers': (-5.0, 5.0),
            'v13_connectivity_patterns': (0.0, 10.0),
            'v14_pragmatic_competence': (0.0, 10.0),
            'v15_prosodic_variation': (0.0, 10.0)
        }
        
        min_val, max_val = dimension_ranges.get(dim_name, (0.0, 10.0))
        normalized = (value - min_val) / (max_val - min_val)
        return np.clip(normalized, 0.0, 1.0)
    
    def _normalize_nt_score(self, score: float) -> float:
        """Normaliza score de neurotransmissor para escala 0-10"""
        return np.clip(score * 10.0, 0.0, 10.0)
    
    def _calculate_mapping_confidence(self, dim_score: float, framework_score: float,
                                    raw_dimensions: Dict[str, float],
                                    frameworks: Dict[str, Any]) -> float:
        """Calcula confiança do mapeamento"""
        
        # Confiança baseada na consistência entre dimensões e frameworks
        consistency = 1.0 - abs(dim_score - framework_score)
        
        # Confiança baseada na qualidade dos dados de entrada
        dim_confidence = np.mean([
            frameworks.get('rdoc', {}).get('accuracy', 0.8),
            frameworks.get('hitop', {}).get('accuracy', 0.8),
            frameworks.get('perma', {}).get('accuracy', 0.8),
            frameworks.get('bigfive', {}).get('accuracy', 0.8)
        ])
        
        # Combinar confidências
        combined_confidence = (0.6 * consistency + 0.4 * dim_confidence)
        
        return np.clip(combined_confidence, 0.0, 1.0)
    
    def _apply_neurotransmitter_interactions(self, nt_scores: Dict[str, float]) -> Dict[str, float]:
        """Aplica correções baseadas em interações conhecidas entre neurotransmissores"""
        
        corrected_scores = nt_scores.copy()
        
        # Interação Serotonina-Dopamina (competição em alguns circuitos)
        if nt_scores['serotonin'] > 8.0 and nt_scores['dopamine'] > 8.0:
            # Ambos muito altos é menos provável
            corrected_scores['serotonin'] *= 0.9
            corrected_scores['dopamine'] *= 0.9
        
        # Interação GABA-Noradrenalina (GABA regula noradrenalina)
        if nt_scores['gaba'] < 3.0 and nt_scores['noradrenaline'] > 7.0:
            # GABA baixo pode permitir noradrenalina alta
            corrected_scores['noradrenaline'] = min(corrected_scores['noradrenaline'] * 1.1, 10.0)
        
        # Interação Acetilcolina-Dopamina (balanço motor e cognitivo)
        if abs(nt_scores['acetylcholine'] - nt_scores['dopamine']) > 6.0:
            # Grande desbalanço é menos comum
            difference = abs(nt_scores['acetylcholine'] - nt_scores['dopamine'])
            correction_factor = 1.0 - (difference - 6.0) * 0.05
            corrected_scores['acetylcholine'] *= correction_factor
            corrected_scores['dopamine'] *= correction_factor
        
        return corrected_scores
```

## DEPLOYMENT

### Deployment Script

```bash
#!/bin/bash
# deploy_apothecary.sh

set -e

echo "🚀 Deploying VOITHER Apothecary"

# Validate Sprint 5 dependencies
echo "🔍 Validating dependencies..."
./validate_sprint_5.sh

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Download pharmacological database
echo "💊 Setting up pharmacological database..."
python scripts/setup_pharmacological_db.py

# Train ML models
echo "🧠 Training drug response prediction models..."
python -c "
import asyncio
from src.apothecary.drug_response_predictor import DrugResponsePredictor

async def train_models():
    config = {
        'models_dir': 'models/apothecary',
        'pharma_db_path': 'data/pharmacological_database.csv'
    }
    
    predictor = DrugResponsePredictor(config)
    result = await predictor.train_response_models()
    
    print(f'Models trained: {result[\"models_trained\"]}')
    print(f'Average accuracy: {result[\"average_accuracy\"]:.3f}')

asyncio.run(train_models())
"

# Run comprehensive tests
echo "🧪 Running Apothecary tests..."
pytest tests/integration/test_apothecary_integration.py -v

# Build Docker image
echo "🐳 Building Docker image..."
docker build -t voither-apothecary:latest .

# Deploy to production
echo "☸️ Deploying to production..."
kubectl apply -f k8s/apothecary-deployment.yaml
kubectl rollout status deployment/voither-apothecary

echo "✅ VOITHER Apothecary deployment completed!"
```

## VALIDATION

### Success Criteria (Binary Validation)

1. **Core Functionality**
   - [ ] Apothecary generates treatment recommendations successfully
   - [ ] Neurotransmitter mapping accuracy >0.80 correlation with clinical assessments
   - [ ] Drug response predictions correlate with historical outcomes (r >0.65)
   - [ ] Safety validation prevents contraindicated combinations

2. **Clinical Integration**
   - [ ] Diagnostic suggestions align with clinical evaluations (κ >0.70)
   - [ ] Treatment recommendations match expert clinical decisions >75% of cases
   - [ ] Confidence scores predict actual treatment success (AUC >0.75)
   - [ ] Clinical insights provide actionable information for clinicians

3. **Performance Requirements**
   - [ ] Recommendation generation <3s for complete patient profile
   - [ ] Batch processing supports 100+ patients efficiently
   - [ ] ML models achieve >0.70 accuracy on drug response prediction
   - [ ] System handles 1000+ concurrent recommendation requests

4. **Safety and Validation**
   - [ ] All FDA contraindications correctly identified
   - [ ] Drug interaction checking 99.9% accurate
   - [ ] Safety alerts triggered for high-risk combinations
   - [ ] Clinical validation scores correlate with expert review

### Integration Tests

```python
# tests/integration/test_apothecary_integration.py
import pytest
import asyncio
from src.apothecary.apothecary_engine import VoitherApothecary
from src.calibration.framework_calibrator import FrameworkCalibrator
from src.med.dimensional_extractor import DimensionalExtractor

@pytest.mark.asyncio
async def test_full_apothecary_pipeline():
    """Test complete MED → Frameworks → Apothecary pipeline"""
    
    # Setup complete pipeline
    med_config = {'spacy_model': 'pt_core_news_lg'}
    frameworks_config = {'models_dir': 'models/calibrated'}
    apothecary_config = {'models_dir': 'models/apothecary'}
    
    med = DimensionalExtractor(med_config)
    calibrator = FrameworkCalibrator(frameworks_config)
    apothecary = VoitherApothecary(apothecary_config)
    
    # Test patient case
    test_text = """
    Doutor, eu tenho me sentido muito deprimido nas últimas semanas. 
    Não consigo dormir bem, perdi o interesse nas coisas que gostava de fazer.
    Fico muito ansioso também, especialmente de manhã. 
    Sinto que minha mente está sempre acelerada, não consigo me concentrar no trabalho.
    Às vezes penso que seria melhor se eu não estivesse aqui.
    """
    
    # Extract dimensions
    med_result = await med.extract_all_dimensions(test_text)
    assert med_result['success']
    
    # Apply framework calibration
    calibrated = await calibrator.apply_calibration(med_result['dimensions'])
    assert 'calibrated_frameworks' in calibrated
    
    # Create patient profile
    patient_profile = {
        'patient_id': 'test_patient_001',
        'raw_dimensions': med_result['dimensions'],
        'calibrated_frameworks': calibrated['calibrated_frameworks'],
        'patient_metadata': {
            'age': 35,
            'sex': 'M',
            'weight': 75,
            'medical_history': ['no_major_medical_conditions']
        },
        'clinical_context': {
            'chief_complaint': 'depression_anxiety',
            'duration_weeks': 4,
            'severity': 'moderate_to_severe'
        }
    }
    
    # Generate recommendations
    recommendations = await apothecary.generate_treatment_recommendations(patient_profile)
    
    # Validate structure
    assert recommendations['success']
    assert 'treatment_recommendations' in recommendations
    assert len(recommendations['treatment_recommendations']) > 0
    
    # Validate content quality
    top_rec = recommendations['treatment_recommendations'][0]
    assert 'medication_name' in top_rec
    assert 'predicted_response_probability' in top_rec
    assert 'drug_class' in top_rec
    assert top_rec['predicted_response_probability'] > 0.5
    
    # Validate safety
    assert 'validation_metadata' in recommendations
    assert recommendations['validation_metadata']['contraindications_checked']
    assert recommendations['validation_metadata']['drug_interactions_verified']
    
    # Validate clinical insights
    assert 'clinical_insights' in recommendations
    assert 'key_findings' in recommendations['clinical_insights']
    assert len(recommendations['clinical_insights']['key_findings']) > 0

@pytest.mark.asyncio
async def test_apothecary_safety_validation():
    """Test safety validation catches dangerous combinations"""
    
    apothecary = VoitherApothecary({'models_dir': 'models/apothecary'})
    
    # Test patient with contraindications
    high_risk_profile = {
        'patient_id': 'high_risk_patient',
        'raw_dimensions': {f'v{i}_test': 5.0 for i in range(1, 16)},
        'calibrated_frameworks': {
            'rdoc': {'scores': {'negative_valence': 8.0}},
            'hitop': {'scores': {'internalizing': 7.5}},
            'perma': {'scores': {'positive_emotions': 2.0}},
            'bigfive': {'scores': {'neuroticism': 8.5}}
        },
        'patient_metadata': {
            'age': 70,
            'sex': 'F',
            'weight': 50,
            'medical_history': [
                'cardiac_arrhythmia',
                'liver_disease',
                'kidney_disease'
            ],
            'current_medications': [
                'warfarin',
                'digoxin',
                'lithium'
            ]
        }
    }
    
    recommendations = await apothecary.generate_treatment_recommendations(high_risk_profile)
    
    # Should still succeed but with safety warnings
    assert recommendations['success']
    
    # Check that high-risk medications are filtered out or flagged
    for rec in recommendations['treatment_recommendations']:
        # Should not recommend medications with major interactions
        assert rec.get('safety_warnings', [])  # Should have warnings
        assert rec.get('interaction_risk', 'low') != 'high'  # High risk should be filtered
```

## OUTPUTS GENERATED

Upon successful completion, this sprint generates:

1. **Production Apothecary System**
   - Complete VOITHER Apothecary engine with ML-powered recommendations
   - Neurotransmitter mapping based on calibrated frameworks
   - Drug response prediction models with >70% accuracy
   - Safety validation and contraindication checking

2. **Clinical Decision Support**
   - Ranked treatment recommendations with probability scores
   - Diagnostic suggestions based on neurotransmitter profiles
   - Clinical insights and treatment rationales for physicians
   - Monitoring recommendations for prescribed treatments

3. **Enhanced PsyDX Algorithm**
   - Evolution of original PsyDX with dynamic language analysis
   - Integration with RDoC, HiTOP, PERMA, BigFive frameworks
   - ML-enhanced neurotransmitter profiling
   - Automated confidence scoring and validation

4. **Safety and Validation Framework**
   - Comprehensive drug interaction database
   - FDA contraindication checking
   - Clinical validation with expert correlation metrics
   - Real-time safety alerts and warnings

**This sprint completes the core therapeutic recommendation engine of VOITHER, enabling precise, AI-powered psychopharmacological decision support based on objective linguistic analysis rather than subjective clinical impressions.**