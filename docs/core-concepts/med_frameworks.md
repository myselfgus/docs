# SPRINT 5: MED CALIBRAÇÃO + FRAMEWORKS

## OVERVIEW
Implementar a calibração do MED com frameworks clínicos (RDoC, HiTOP, PERMA, BigFive) conforme especificado nos documentos VOITHER. Esta calibração transforma as 15 dimensões brutas em scores validados clinicamente, habilitando o VOITHER Apothecary e análises psicofarmacológicas precisas.

## DEPENDENCIES (Must exist before starting)

- [ ] ✅ **Sprint 4 completed**: MED Core com 15 dimensões funcionais
- [ ] ✅ **All dimensions tested**: Extração das 15 dimensões validada com dados reais
- [ ] ✅ **Performance benchmarks met**: MED processa <2s para análise completa
- [ ] ✅ **Storage integration working**: Resultados persistidos via DSL
- [ ] Python 3.11+ com scikit-learn, pandas, matplotlib
- [ ] Azure Machine Learning workspace configurado
- [ ] Dados clínicos anonimizados para calibração

### Pre-flight Validation Script

```bash
#!/bin/bash
# validate_sprint_4.sh
set -e

echo "🔍 Validating Sprint 4 dependencies..."

# Test MED Core functionality
python -c "
import asyncio
from src.med.dimensional_extractor import DimensionalExtractor

async def test_med():
    config = {
        'spacy_model': 'pt_core_news_lg',
        'azure': {'endpoint': 'test', 'key': 'test'},
        'dsl_runtime': {'host': 'test'}
    }
    
    med = DimensionalExtractor(config)
    
    # Test extraction
    result = await med.extract_all_dimensions(
        'Eu me sinto muito ansioso e preocupado ultimamente. Não consigo dormir direito.'
    )
    
    assert result['success'], 'MED extraction failed'
    assert len(result['dimensions']) == 15, 'Not all 15 dimensions extracted'
    assert result['total_processing_time_ms'] < 2000, 'Processing too slow'
    
    print('✅ MED Core operational with 15 dimensions')

asyncio.run(test_med())
"

# Validate framework libraries
python -c "
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
print('✅ ML frameworks available')
"

# Test Azure ML connection
python -c "
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
import os

# Test connection (will use environment variables)
try:
    ml_client = MLClient.from_config(DefaultAzureCredential())
    print('✅ Azure ML workspace accessible')
except:
    print('⚠️ Azure ML not configured, will use local calibration')
"

echo "✅ All Sprint 4 dependencies validated"
```

## IMPLEMENTATION

### 1. Project Structure

```
voither-med-frameworks/
├── src/
│   ├── __init__.py
│   ├── calibration/
│   │   ├── __init__.py
│   │   ├── framework_calibrator.py    # Main calibration engine
│   │   ├── rdoc_calibrator.py         # RDoC mapping
│   │   ├── hitop_calibrator.py        # HiTOP mapping  
│   │   ├── perma_calibrator.py        # PERMA mapping
│   │   ├── bigfive_calibrator.py      # Big Five mapping
│   │   └── neurodev_calibrator.py     # Neurodevelopmental mapping
│   ├── models/
│   │   ├── __init__.py
│   │   ├── regression_models.py       # ML models for calibration
│   │   ├── validation_models.py       # Cross-validation utilities
│   │   └── ensemble_models.py         # Ensemble calibration
│   ├── data/
│   │   ├── __init__.py
│   │   ├── clinical_data_loader.py    # Load clinical validation data
│   │   ├── framework_mappings.py      # Framework-dimension mappings
│   │   └── validation_datasets.py     # Test datasets
│   └── evaluation/
│       ├── __init__.py
│       ├── accuracy_evaluator.py      # Accuracy validation
│       ├── clinical_evaluator.py      # Clinical significance testing
│       └── performance_evaluator.py   # Performance benchmarks
├── tests/
│   ├── unit/
│   ├── integration/
│   └── clinical/
├── data/
│   ├── calibration_datasets/
│   ├── validation_datasets/
│   └── clinical_references/
├── requirements.txt
└── README.md
```

### 2. Framework Calibration Engine

```python
# src/calibration/framework_calibrator.py
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import logging
import joblib
from pathlib import Path

from .rdoc_calibrator import RDoCCalibrator
from .hitop_calibrator import HiTOPCalibrator
from .perma_calibrator import PERMACalibrator
from .bigfive_calibrator import BigFiveCalibrator
from .neurodev_calibrator import NeuroDevelopmentalCalibrator
from ..models.regression_models import CalibratedRegressionModel
from ..data.clinical_data_loader import ClinicalDataLoader
from ..evaluation.accuracy_evaluator import AccuracyEvaluator

class FrameworkCalibrator:
    """
    Calibração das 15 dimensões MED para frameworks clínicos validados
    
    Transforma dimensões brutas em scores calibrados para:
    - RDoC (Research Domain Criteria)
    - HiTOP (Hierarchical Taxonomy of Psychopathology)  
    - PERMA (Well-being model)
    - Big Five (Personality traits)
    - Neurodevelopmental markers
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger("FrameworkCalibrator") 
        
        # Initialize framework-specific calibrators
        self.rdoc_calibrator = RDoCCalibrator(config)
        self.hitop_calibrator = HiTOPCalibrator(config)
        self.perma_calibrator = PERMACalibrator(config)
        self.bigfive_calibrator = BigFiveCalibrator(config)
        self.neurodev_calibrator = NeuroDevelopmentalCalibrator(config)
        
        # Data loader for clinical validation
        self.data_loader = ClinicalDataLoader(config)
        
        # Evaluation utilities
        self.accuracy_evaluator = AccuracyEvaluator(config)
        
        # Calibration models storage
        self.models_dir = Path(config.get('models_dir', 'models/calibrated'))
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        # Calibration status
        self.calibration_status = {
            'rdoc': {'calibrated': False, 'accuracy': 0.0, 'last_updated': None},
            'hitop': {'calibrated': False, 'accuracy': 0.0, 'last_updated': None},
            'perma': {'calibrated': False, 'accuracy': 0.0, 'last_updated': None},
            'bigfive': {'calibrated': False, 'accuracy': 0.0, 'last_updated': None},
            'neurodev': {'calibrated': False, 'accuracy': 0.0, 'last_updated': None}
        }
        
        # Load existing calibration models if available
        self._load_existing_models()
    
    async def calibrate_all_frameworks(self, clinical_data_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Calibra todos os frameworks usando dados clínicos de validação
        
        Args:
            clinical_data_path: Caminho para dados clínicos (opcional)
            
        Returns:
            Resultado da calibração para todos os frameworks
        """
        start_time = datetime.now()
        calibration_id = f"calibration_{int(start_time.timestamp())}"
        
        self.logger.info(f"Starting full framework calibration: {calibration_id}")
        
        try:
            # Load clinical validation data
            if clinical_data_path:
                clinical_data = await self.data_loader.load_clinical_data(clinical_data_path)
            else:
                clinical_data = await self.data_loader.load_default_clinical_data()
            
            self.logger.info(f"Loaded {len(clinical_data)} clinical samples for calibration")
            
            # Prepare dimensional features and framework targets
            features, targets = self._prepare_calibration_data(clinical_data)
            
            # Calibrate each framework
            calibration_results = {}
            
            # RDoC Calibration
            self.logger.info("Calibrating RDoC framework...")
            rdoc_result = await self._calibrate_framework(
                'rdoc', features, targets['rdoc'], self.rdoc_calibrator
            )
            calibration_results['rdoc'] = rdoc_result
            
            # HiTOP Calibration  
            self.logger.info("Calibrating HiTOP framework...")
            hitop_result = await self._calibrate_framework(
                'hitop', features, targets['hitop'], self.hitop_calibrator
            )
            calibration_results['hitop'] = hitop_result
            
            # PERMA Calibration
            self.logger.info("Calibrating PERMA framework...")
            perma_result = await self._calibrate_framework(
                'perma', features, targets['perma'], self.perma_calibrator
            )
            calibration_results['perma'] = perma_result
            
            # Big Five Calibration
            self.logger.info("Calibrating Big Five framework...")
            bigfive_result = await self._calibrate_framework(
                'bigfive', features, targets['bigfive'], self.bigfive_calibrator
            )
            calibration_results['bigfive'] = bigfive_result
            
            # Neurodevelopmental Calibration
            self.logger.info("Calibrating Neurodevelopmental framework...")
            neurodev_result = await self._calibrate_framework(
                'neurodev', features, targets['neurodev'], self.neurodev_calibrator
            )
            calibration_results['neurodev'] = neurodev_result
            
            # Calculate overall calibration quality
            overall_accuracy = np.mean([
                result['accuracy'] for result in calibration_results.values()
            ])
            
            calibration_time = (datetime.now() - start_time).total_seconds()
            
            final_result = {
                'calibration_id': calibration_id,
                'success': True,
                'overall_accuracy': overall_accuracy,
                'calibration_time_seconds': calibration_time,
                'frameworks_calibrated': len(calibration_results),
                'clinical_samples_used': len(clinical_data),
                'framework_results': calibration_results,
                'calibration_timestamp': start_time.isoformat(),
                'model_versions': self._get_model_versions()
            }
            
            # Save calibration results
            await self._save_calibration_results(final_result)
            
            self.logger.info(f"✅ Full calibration completed: {overall_accuracy:.3f} accuracy")
            return final_result
            
        except Exception as e:
            self.logger.error(f"Calibration failed: {e}")
            return {
                'calibration_id': calibration_id,
                'success': False,
                'error': str(e),
                'calibration_time_seconds': (datetime.now() - start_time).total_seconds()
            }
    
    async def apply_calibration(self, raw_dimensions: Dict[str, float], 
                              frameworks: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Aplica calibração às dimensões brutas para obter scores dos frameworks
        
        Args:
            raw_dimensions: Dimensões brutas do MED (15 dimensões)
            frameworks: Lista de frameworks a aplicar (None = todos)
            
        Returns:
            Scores calibrados para cada framework
        """
        if frameworks is None:
            frameworks = ['rdoc', 'hitop', 'perma', 'bigfive', 'neurodev']
        
        calibrated_scores = {}
        
        # Preparar features das dimensões
        dimension_features = self._prepare_dimension_features(raw_dimensions)
        
        # Aplicar calibração para cada framework solicitado
        for framework in frameworks:
            if framework not in self.calibration_status:
                continue
            
            if not self.calibration_status[framework]['calibrated']:
                self.logger.warning(f"Framework {framework} not calibrated, skipping")
                continue
            
            try:
                if framework == 'rdoc':
                    scores = await self.rdoc_calibrator.apply_calibration(dimension_features)
                elif framework == 'hitop':
                    scores = await self.hitop_calibrator.apply_calibration(dimension_features)
                elif framework == 'perma':
                    scores = await self.perma_calibrator.apply_calibration(dimension_features)
                elif framework == 'bigfive':
                    scores = await self.bigfive_calibrator.apply_calibration(dimension_features)
                elif framework == 'neurodev':
                    scores = await self.neurodev_calibrator.apply_calibration(dimension_features)
                
                calibrated_scores[framework] = {
                    'scores': scores,
                    'accuracy': self.calibration_status[framework]['accuracy'],
                    'last_updated': self.calibration_status[framework]['last_updated']
                }
                
            except Exception as e:
                self.logger.error(f"Failed to apply {framework} calibration: {e}")
                calibrated_scores[framework] = {
                    'error': str(e),
                    'scores': {}
                }
        
        return {
            'raw_dimensions': raw_dimensions,
            'calibrated_frameworks': calibrated_scores,
            'calibration_applied_at': datetime.now().isoformat()
        }
    
    async def validate_calibration_accuracy(self, validation_data_path: str) -> Dict[str, Any]:
        """
        Valida a acurácia da calibração usando dados independentes
        
        Args:
            validation_data_path: Caminho para dados de validação
            
        Returns:
            Resultado da validação de acurácia
        """
        try:
            # Load validation data
            validation_data = await self.data_loader.load_clinical_data(validation_data_path)
            self.logger.info(f"Loaded {len(validation_data)} validation samples")
            
            # Prepare features and targets
            features, targets = self._prepare_calibration_data(validation_data)
            
            # Validate each framework
            validation_results = {}
            
            for framework_name in ['rdoc', 'hitop', 'perma', 'bigfive', 'neurodev']:
                if not self.calibration_status[framework_name]['calibrated']:
                    continue
                
                framework_targets = targets[framework_name]
                framework_predictions = await self._predict_framework_scores(
                    framework_name, features
                )
                
                # Calculate accuracy metrics
                accuracy_metrics = self.accuracy_evaluator.evaluate_predictions(
                    framework_targets, framework_predictions
                )
                
                validation_results[framework_name] = accuracy_metrics
            
            # Calculate overall validation score
            overall_accuracy = np.mean([
                result['accuracy'] for result in validation_results.values()
                if 'accuracy' in result
            ])
            
            return {
                'success': True,
                'overall_validation_accuracy': overall_accuracy,
                'framework_validations': validation_results,
                'validation_samples': len(validation_data),
                'validated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_calibration_status(self) -> Dict[str, Any]:
        """Retorna status atual da calibração"""
        return {
            'calibration_status': self.calibration_status.copy(),
            'models_directory': str(self.models_dir),
            'available_frameworks': ['rdoc', 'hitop', 'perma', 'bigfive', 'neurodev'],
            'total_calibrated_frameworks': sum(
                1 for status in self.calibration_status.values() 
                if status['calibrated']
            )
        }
    
    async def _calibrate_framework(self, framework_name: str, features: np.ndarray, 
                                 targets: np.ndarray, calibrator) -> Dict[str, Any]:
        """Calibra um framework específico"""
        try:
            # Perform calibration
            calibration_result = await calibrator.calibrate(features, targets)
            
            # Evaluate accuracy
            accuracy = calibration_result.get('accuracy', 0.0)
            
            # Update status
            self.calibration_status[framework_name] = {
                'calibrated': True,
                'accuracy': accuracy,
                'last_updated': datetime.now().isoformat()
            }
            
            # Save model
            model_path = self.models_dir / f"{framework_name}_calibration_model.joblib"
            joblib.dump(calibration_result['model'], model_path)
            
            return {
                'framework': framework_name,
                'success': True,
                'accuracy': accuracy,
                'model_path': str(model_path),
                'calibration_metrics': calibration_result.get('metrics', {}),
                'feature_importance': calibration_result.get('feature_importance', [])
            }
            
        except Exception as e:
            self.logger.error(f"Failed to calibrate {framework_name}: {e}")
            return {
                'framework': framework_name,
                'success': False,
                'error': str(e)
            }
    
    def _prepare_calibration_data(self, clinical_data: List[Dict[str, Any]]) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
        """Prepara dados clínicos para calibração"""
        
        # Extract dimensional features (15 dimensions)
        dimension_names = [
            'v1_valence_emotional', 'v2_arousal_activation', 'v3_narrative_coherence',
            'v4_syntactic_complexity', 'v5_temporal_orientation', 'v6_self_reference_density',
            'v7_social_language', 'v8_cognitive_flexibility', 'v9_dominance_agency',
            'v10_discourse_fragmentation', 'v11_semantic_density', 'v12_certainty_markers',
            'v13_connectivity_patterns', 'v14_pragmatic_competence', 'v15_prosodic_variation'
        ]
        
        features = []
        targets = {
            'rdoc': [], 'hitop': [], 'perma': [], 'bigfive': [], 'neurodev': []
        }
        
        for sample in clinical_data:
            # Extract dimensional features
            sample_features = [
                sample.get('dimensions', {}).get(dim, 0.0) 
                for dim in dimension_names
            ]
            features.append(sample_features)
            
            # Extract framework target scores
            targets['rdoc'].append(self._extract_rdoc_targets(sample))
            targets['hitop'].append(self._extract_hitop_targets(sample))
            targets['perma'].append(self._extract_perma_targets(sample))
            targets['bigfive'].append(self._extract_bigfive_targets(sample))
            targets['neurodev'].append(self._extract_neurodev_targets(sample))
        
        return (
            np.array(features),
            {key: np.array(value) for key, value in targets.items()}
        )
    
    def _prepare_dimension_features(self, raw_dimensions: Dict[str, float]) -> np.ndarray:
        """Prepara features das dimensões para aplicação de calibração"""
        dimension_names = [
            'v1_valence_emotional', 'v2_arousal_activation', 'v3_narrative_coherence',
            'v4_syntactic_complexity', 'v5_temporal_orientation', 'v6_self_reference_density',
            'v7_social_language', 'v8_cognitive_flexibility', 'v9_dominance_agency',
            'v10_discourse_fragmentation', 'v11_semantic_density', 'v12_certainty_markers',
            'v13_connectivity_patterns', 'v14_pragmatic_competence', 'v15_prosodic_variation'
        ]
        
        features = [raw_dimensions.get(dim, 0.0) for dim in dimension_names]
        return np.array(features).reshape(1, -1)
    
    def _extract_rdoc_targets(self, sample: Dict[str, Any]) -> List[float]:
        """Extrai targets do RDoC de uma amostra clínica"""
        rdoc_data = sample.get('rdoc_scores', {})
        return [
            rdoc_data.get('negative_valence', 0.0),
            rdoc_data.get('positive_valence', 0.0),
            rdoc_data.get('cognitive_systems', 0.0),
            rdoc_data.get('social_processes', 0.0),
            rdoc_data.get('arousal_regulatory', 0.0)
        ]
    
    def _extract_hitop_targets(self, sample: Dict[str, Any]) -> List[float]:
        """Extrai targets do HiTOP de uma amostra clínica"""
        hitop_data = sample.get('hitop_scores', {})
        return [
            hitop_data.get('internalizing', 0.0),
            hitop_data.get('externalizing', 0.0),
            hitop_data.get('thought_disorder', 0.0)
        ]
    
    def _extract_perma_targets(self, sample: Dict[str, Any]) -> List[float]:
        """Extrai targets do PERMA de uma amostra clínica"""
        perma_data = sample.get('perma_scores', {})
        return [
            perma_data.get('positive_emotions', 0.0),
            perma_data.get('engagement', 0.0),
            perma_data.get('relationships', 0.0),
            perma_data.get('meaning', 0.0),
            perma_data.get('accomplishment', 0.0)
        ]
    
    def _extract_bigfive_targets(self, sample: Dict[str, Any]) -> List[float]:
        """Extrai targets do Big Five de uma amostra clínica"""
        bigfive_data = sample.get('bigfive_scores', {})
        return [
            bigfive_data.get('openness', 0.0),
            bigfive_data.get('conscientiousness', 0.0),
            bigfive_data.get('extraversion', 0.0),
            bigfive_data.get('agreeableness', 0.0),
            bigfive_data.get('neuroticism', 0.0)
        ]
    
    def _extract_neurodev_targets(self, sample: Dict[str, Any]) -> List[float]:
        """Extrai targets neurodesenvolvimentais de uma amostra clínica"""
        neurodev_data = sample.get('neurodev_scores', {})
        return [
            neurodev_data.get('attention_regulation', 0.0),
            neurodev_data.get('executive_function', 0.0),
            neurodev_data.get('social_cognition', 0.0),
            neurodev_data.get('language_development', 0.0),
            neurodev_data.get('motor_coordination', 0.0)
        ]
    
    async def _predict_framework_scores(self, framework_name: str, features: np.ndarray) -> np.ndarray:
        """Prediz scores de um framework usando modelo calibrado"""
        model_path = self.models_dir / f"{framework_name}_calibration_model.joblib"
        
        if not model_path.exists():
            raise FileNotFoundError(f"Calibration model not found: {model_path}")
        
        model = joblib.load(model_path)
        predictions = model.predict(features)
        
        return predictions
    
    def _load_existing_models(self):
        """Carrega modelos de calibração existentes"""
        for framework_name in ['rdoc', 'hitop', 'perma', 'bigfive', 'neurodev']:
            model_path = self.models_dir / f"{framework_name}_calibration_model.joblib"
            
            if model_path.exists():
                try:
                    # Load model to verify it works
                    model = joblib.load(model_path)
                    
                    # Update status
                    self.calibration_status[framework_name]['calibrated'] = True
                    self.calibration_status[framework_name]['last_updated'] = datetime.fromtimestamp(
                        model_path.stat().st_mtime
                    ).isoformat()
                    
                    self.logger.info(f"Loaded existing {framework_name} calibration model")
                    
                except Exception as e:
                    self.logger.warning(f"Failed to load {framework_name} model: {e}")
    
    def _get_model_versions(self) -> Dict[str, str]:
        """Retorna versões dos modelos calibrados"""
        versions = {}
        for framework_name in ['rdoc', 'hitop', 'perma', 'bigfive', 'neurodev']:
            if self.calibration_status[framework_name]['calibrated']:
                versions[framework_name] = self.calibration_status[framework_name]['last_updated']
        return versions
    
    async def _save_calibration_results(self, results: Dict[str, Any]):
        """Salva resultados da calibração"""
        results_path = self.models_dir / f"calibration_results_{results['calibration_id']}.json"
        
        import json
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        self.logger.info(f"Calibration results saved: {results_path}")
```

### 3. RDoC Framework Calibrator

```python
# src/calibration/rdoc_calibrator.py
import numpy as np
from typing import Dict, Any, List, Tuple
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error

class RDoCCalibrator:
    """
    Calibrador para Research Domain Criteria (RDoC)
    
    Mapeia 15 dimensões MED para 5 domínios RDoC:
    - Negative Valence Systems (Sistemas de Valência Negativa)
    - Positive Valence Systems (Sistemas de Valência Positiva)  
    - Cognitive Systems (Sistemas Cognitivos)
    - Social Processes (Processos Sociais)
    - Arousal and Regulatory Systems (Sistemas de Arousal e Regulação)
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # RDoC domain definitions and dimensional mappings
        self.rdoc_mappings = {
            'negative_valence': {
                'primary_dimensions': ['v1_valence_emotional', 'v2_arousal_activation', 'v12_certainty_markers'],
                'secondary_dimensions': ['v10_discourse_fragmentation', 'v6_self_reference_density'],
                'weights': {'primary': 0.7, 'secondary': 0.3}
            },
            'positive_valence': {
                'primary_dimensions': ['v1_valence_emotional', 'v7_social_language', 'v8_cognitive_flexibility'],
                'secondary_dimensions': ['v3_narrative_coherence', 'v9_dominance_agency'],
                'weights': {'primary': 0.8, 'secondary': 0.2}
            },
            'cognitive_systems': {
                'primary_dimensions': ['v4_syntactic_complexity', 'v8_cognitive_flexibility', 'v11_semantic_density'],
                'secondary_dimensions': ['v3_narrative_coherence', 'v13_connectivity_patterns', 'v14_pragmatic_competence'],
                'weights': {'primary': 0.6, 'secondary': 0.4}
            },
            'social_processes': {
                'primary_dimensions': ['v7_social_language', 'v14_pragmatic_competence', 'v9_dominance_agency'],
                'secondary_dimensions': ['v6_self_reference_density', 'v13_connectivity_patterns'],
                'weights': {'primary': 0.75, 'secondary': 0.25}
            },
            'arousal_regulatory': {
                'primary_dimensions': ['v2_arousal_activation', 'v15_prosodic_variation', 'v10_discourse_fragmentation'],
                'secondary_dimensions': ['v5_temporal_orientation', 'v12_certainty_markers'],
                'weights': {'primary': 0.65, 'secondary': 0.35}
            }
        }
        
        # Calibration models for each RDoC domain
        self.domain_models = {}
        self.feature_scaler = StandardScaler()
        self.is_calibrated = False
    
    async def calibrate(self, features: np.ndarray, targets: np.ndarray) -> Dict[str, Any]:
        """
        Calibra mapeamento das dimensões MED para domínios RDoC
        
        Args:
            features: Array das 15 dimensões MED [n_samples, 15]
            targets: Array dos 5 domínios RDoC [n_samples, 5]
            
        Returns:
            Resultado da calibração com métricas de acurácia
        """
        
        # Normalize features
        features_scaled = self.feature_scaler.fit_transform(features)
        
        # Train multi-output model for all RDoC domains
        self.multi_output_model = MultiOutputRegressor(
            RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
        )
        
        # Fit model
        self.multi_output_model.fit(features_scaled, targets)
        
        # Calculate predictions for accuracy assessment
        predictions = self.multi_output_model.predict(features_scaled)
        
        # Calculate metrics for each domain
        domain_names = ['negative_valence', 'positive_valence', 'cognitive_systems', 
                       'social_processes', 'arousal_regulatory']
        
        domain_metrics = {}
        for i, domain_name in enumerate(domain_names):
            domain_targets = targets[:, i]
            domain_predictions = predictions[:, i]
            
            # Calculate R² score
            r2 = r2_score(domain_targets, domain_predictions)
            mse = mean_squared_error(domain_targets, domain_predictions)
            
            # Cross-validation score
            cv_scores = cross_val_score(
                RandomForestRegressor(n_estimators=50, random_state=42),
                features_scaled, domain_targets, cv=5, scoring='r2'
            )
            
            domain_metrics[domain_name] = {
                'r2_score': r2,
                'mse': mse,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std()
            }
        
        # Calculate overall accuracy
        overall_r2 = r2_score(targets, predictions)
        
        # Feature importance analysis
        feature_importance = self._calculate_feature_importance()
        
        self.is_calibrated = True
        
        return {
            'model': self.multi_output_model,  # Return trained model
            'accuracy': overall_r2,
            'domain_metrics': domain_metrics,
            'feature_importance': feature_importance,
            'calibration_samples': len(features),
            'rdoc_domains': domain_names
        }
    
    async def apply_calibration(self, dimension_features: np.ndarray) -> Dict[str, float]:
        """
        Aplica calibração para converter dimensões em scores RDoC
        
        Args:
            dimension_features: Array das 15 dimensões [1, 15]
            
        Returns:
            Scores dos 5 domínios RDoC
        """
        if not self.is_calibrated:
            raise ValueError("RDoC calibrator not trained. Call calibrate() first.")
        
        # Normalize features
        features_scaled = self.feature_scaler.transform(dimension_features)
        
        # Predict RDoC scores
        rdoc_predictions = self.multi_output_model.predict(features_scaled)[0]
        
        # Map predictions to domain names
        domain_names = ['negative_valence', 'positive_valence', 'cognitive_systems', 
                       'social_processes', 'arousal_regulatory']
        
        rdoc_scores = {
            domain_name: float(score) 
            for domain_name, score in zip(domain_names, rdoc_predictions)
        }
        
        # Apply domain-specific post-processing
        rdoc_scores = self._apply_domain_constraints(rdoc_scores)
        
        return rdoc_scores
    
    def _calculate_feature_importance(self) -> Dict[str, float]:
        """Calcula importância das features para cada domínio RDoC"""
        
        if not hasattr(self.multi_output_model, 'estimators_'):
            return {}
        
        dimension_names = [
            'v1_valence_emotional', 'v2_arousal_activation', 'v3_narrative_coherence',
            'v4_syntactic_complexity', 'v5_temporal_orientation', 'v6_self_reference_density',
            'v7_social_language', 'v8_cognitive_flexibility', 'v9_dominance_agency',
            'v10_discourse_fragmentation', 'v11_semantic_density', 'v12_certainty_markers',
            'v13_connectivity_patterns', 'v14_pragmatic_competence', 'v15_prosodic_variation'
        ]
        
        domain_names = ['negative_valence', 'positive_valence', 'cognitive_systems', 
                       'social_processes', 'arousal_regulatory']
        
        feature_importance = {}
        
        for i, domain_name in enumerate(domain_names):
            estimator = self.multi_output_model.estimators_[i]
            importances = estimator.feature_importances_
            
            domain_importance = {
                dim_name: float(importance)
                for dim_name, importance in zip(dimension_names, importances)
            }
            
            # Sort by importance
            domain_importance = dict(
                sorted(domain_importance.items(), key=lambda x: x[1], reverse=True)
            )
            
            feature_importance[domain_name] = domain_importance
        
        return feature_importance
    
    def _apply_domain_constraints(self, rdoc_scores: Dict[str, float]) -> Dict[str, float]:
        """Aplica restrições específicas dos domínios RDoC"""
        
        # Constraint: Negative and Positive Valence should be somewhat anti-correlated
        neg_val = rdoc_scores['negative_valence']
        pos_val = rdoc_scores['positive_valence']
        
        # If both are very high, moderate them
        if neg_val > 7.0 and pos_val > 7.0:
            adjustment = 0.8
            rdoc_scores['negative_valence'] = neg_val * adjustment
            rdoc_scores['positive_valence'] = pos_val * adjustment
        
        # Ensure all scores are within valid ranges (0-10 for RDoC)
        for domain in rdoc_scores:
            rdoc_scores[domain] = np.clip(rdoc_scores[domain], 0.0, 10.0)
        
        return rdoc_scores
    
    def get_rdoc_interpretation(self, rdoc_scores: Dict[str, float]) -> Dict[str, str]:
        """
        Fornece interpretação clínica dos scores RDoC
        
        Args:
            rdoc_scores: Scores dos domínios RDoC
            
        Returns:
            Interpretação clínica para cada domínio
        """
        interpretations = {}
        
        # Negative Valence Systems
        neg_val = rdoc_scores['negative_valence']
        if neg_val >= 7.0:
            interpretations['negative_valence'] = "Elevado: Forte presença de emoções negativas, ansiedade, medo ou estresse"
        elif neg_val >= 4.0:
            interpretations['negative_valence'] = "Moderado: Alguma presença de emoções negativas, dentro de faixas adaptativas"
        else:
            interpretations['negative_valence'] = "Baixo: Pouca presença de emoções negativas, possível estado de bem-estar"
        
        # Positive Valence Systems
        pos_val = rdoc_scores['positive_valence']
        if pos_val >= 7.0:
            interpretations['positive_valence'] = "Elevado: Forte capacidade de recompensa, motivação e emoções positivas"
        elif pos_val >= 4.0:
            interpretations['positive_valence'] = "Moderado: Capacidade adequada para prazer e motivação"
        else:
            interpretations['positive_valence'] = "Baixo: Possível anedonia, redução na capacidade de sentir prazer"
        
        # Cognitive Systems
        cog_sys = rdoc_scores['cognitive_systems']
        if cog_sys >= 7.0:
            interpretations['cognitive_systems'] = "Elevado: Excelente funcionamento cognitivo, atenção e controle executivo"
        elif cog_sys >= 4.0:
            interpretations['cognitive_systems'] = "Moderado: Funcionamento cognitivo adequado com possíveis limitações menores"
        else:
            interpretations['cognitive_systems'] = "Baixo: Possíveis dificuldades atencionais ou executivas significativas"
        
        # Social Processes
        social = rdoc_scores['social_processes']
        if social >= 7.0:
            interpretations['social_processes'] = "Elevado: Forte competência social, empatia e comunicação interpessoal"
        elif social >= 4.0:
            interpretations['social_processes'] = "Moderado: Habilidades sociais adequadas com possíveis áreas de melhoria"
        else:
            interpretations['social_processes'] = "Baixo: Possíveis dificuldades significativas na interação social"
        
        # Arousal and Regulatory Systems
        arousal = rdoc_scores['arousal_regulatory']
        if arousal >= 7.0:
            interpretations['arousal_regulatory'] = "Elevado: Possível hiperativação, dificuldade de regulação emocional"
        elif arousal >= 4.0:
            interpretations['arousal_regulatory'] = "Moderado: Nível adequado de ativação e regulação emocional"
        else:
            interpretations['arousal_regulatory'] = "Baixo: Possível hipoativação, redução na responsividade emocional"
        
        return interpretations
```

## DEPLOYMENT

### Deployment Script

```bash
#!/bin/bash
# deploy_med_frameworks.sh

set -e

echo "🚀 Deploying VOITHER MED Framework Calibration"

# Validate Sprint 4 dependencies
echo "🔍 Validating dependencies..."
./validate_sprint_4.sh

# Install ML dependencies
echo "📦 Installing ML dependencies..."
pip install -r requirements.txt
pip install scikit-learn==1.3.0 pandas==2.0.3 matplotlib==3.7.1 seaborn==0.12.2

# Download clinical calibration datasets
echo "📊 Setting up calibration datasets..."
python scripts/download_clinical_datasets.py

# Create calibration models directory
mkdir -p models/calibrated

# Run calibration process
echo "🧠 Starting framework calibration..."
python -c "
import asyncio
from src.calibration.framework_calibrator import FrameworkCalibrator

async def run_calibration():
    config = {
        'models_dir': 'models/calibrated',
        'azure': {'endpoint': '${AZURE_ENDPOINT}', 'key': '${AZURE_KEY}'},
        'max_concurrent_extractions': 3
    }
    
    calibrator = FrameworkCalibrator(config)
    result = await calibrator.calibrate_all_frameworks()
    
    print(f'Calibration completed: {result[\"overall_accuracy\"]:.3f} accuracy')
    print(f'Frameworks calibrated: {result[\"frameworks_calibrated\"]}')

asyncio.run(run_calibration())
"

# Validate calibration results
echo "✅ Validating calibration..."
python tests/integration/test_framework_calibration.py

# Build Docker image
echo "🐳 Building Docker image..."
docker build -t voither-med-frameworks:latest .

# Deploy to production
echo "☸️ Deploying to production..."
kubectl apply -f k8s/med-frameworks-deployment.yaml
kubectl rollout status deployment/voither-med-frameworks

echo "✅ MED Framework Calibration deployment completed!"
```

## VALIDATION

### Success Criteria (Binary Validation)

1. **Framework Calibration**
   - [ ] All 5 frameworks (RDoC, HiTOP, PERMA, BigFive, Neurodev) calibrated successfully
   - [ ] Overall calibration accuracy >0.80 for each framework
   - [ ] Cross-validation R² scores >0.75 across all domains
   - [ ] Feature importance analysis shows logical dimensional mappings

2. **Clinical Validation**
   - [ ] Calibrated scores correlate with clinical assessments (r >0.70)
   - [ ] Framework scores show expected inter-correlations
   - [ ] Clinical interpretations align with expert evaluations
   - [ ] Validation on independent dataset confirms accuracy

3. **Performance Requirements**
   - [ ] Calibration application <50ms per sample
   - [ ] Batch processing supports 1000+ samples efficiently
   - [ ] Memory usage <1GB during calibration training
   - [ ] Models save/load correctly for production deployment

4. **Integration Testing**
   - [ ] MED Core → Framework Calibration pipeline functional
   - [ ] Calibrated scores persist correctly via DSL integration
   - [ ] Real-time calibration works with live MED extractions
   - [ ] Error handling graceful for edge cases

### Integration Tests

```python
# tests/integration/test_framework_calibration.py
import pytest
import asyncio
import numpy as np
from src.calibration.framework_calibrator import FrameworkCalibrator
from src.med.dimensional_extractor import DimensionalExtractor

@pytest.mark.asyncio
async def test_full_calibration_pipeline():
    """Test complete MED → Framework calibration pipeline"""
    
    # Setup MED extractor
    med_config = {
        'spacy_model': 'pt_core_news_lg',
        'azure': {'endpoint': 'test', 'key': 'test'}
    }
    med = DimensionalExtractor(med_config)
    
    # Setup framework calibrator
    cal_config = {
        'models_dir': 'test_models',
        'max_concurrent_extractions': 2
    }
    calibrator = FrameworkCalibrator(cal_config)
    
    # Test text samples
    test_texts = [
        "Eu me sinto muito ansioso e deprimido ultimamente. Não consigo me concentrar no trabalho.",
        "Estou muito feliz com minha vida. Tenho ótimos relacionamentos e me sinto realizado.",
        "Às vezes fico confuso e não consigo organizar meus pensamentos direito."
    ]
    
    # Extract dimensions
    dimension_results = []
    for text in test_texts:
        result = await med.extract_all_dimensions(text)
        assert result['success'], f"MED extraction failed for: {text[:50]}..."
        dimension_results.append(result['dimensions'])
    
    # Apply calibration (should work with pre-trained models or mock data)
    for dimensions in dimension_results:
        calibrated = await calibrator.apply_calibration(dimensions)
        
        # Validate structure
        assert 'calibrated_frameworks' in calibrated
        assert 'rdoc' in calibrated['calibrated_frameworks']
        assert 'hitop' in calibrated['calibrated_frameworks']
        assert 'perma' in calibrated['calibrated_frameworks']
        assert 'bigfive' in calibrated['calibrated_frameworks']
        
        # Validate score ranges
        rdoc_scores = calibrated['calibrated_frameworks']['rdoc']['scores']
        for domain, score in rdoc_scores.items():
            assert 0.0 <= score <= 10.0, f"RDoC {domain} score {score} out of range"

@pytest.mark.asyncio 
async def test_calibration_accuracy():
    """Test calibration accuracy with known clinical data"""
    
    # Load test clinical data
    test_clinical_data = [
        {
            'dimensions': {
                'v1_valence_emotional': -3.2,  # Very negative
                'v2_arousal_activation': 8.1,   # High arousal
                'v3_narrative_coherence': 4.2,
                'v7_social_language': 2.1,     # Low social
                # ... other dimensions
            },
            'rdoc_scores': {
                'negative_valence': 8.5,        # Expected high
                'positive_valence': 2.1,        # Expected low
                'social_processes': 3.2,        # Expected low
                # ... other scores
            }
        }
        # ... more test samples
    ]
    
    config = {'models_dir': 'test_models'}
    calibrator = FrameworkCalibrator(config)
    
    # Test calibration accuracy
    validation_result = await calibrator.validate_calibration_accuracy('test_data.json')
    
    assert validation_result['success']
    assert validation_result['overall_validation_accuracy'] > 0.75
```

## OUTPUTS GENERATED

Upon successful completion, this sprint generates:

1. **Calibrated Framework Models**
   - RDoC calibration model with 5 domain mappings
   - HiTOP calibration model with hierarchical structure
   - PERMA calibration model for well-being assessment
   - Big Five calibration model for personality traits
   - Neurodevelopmental calibration model

2. **Clinical Validation Results**
   - Accuracy metrics for each framework (R², MSE, CV scores)
   - Feature importance analysis showing dimensional contributions
   - Clinical interpretation guidelines for each framework
   - Validation reports with independent dataset testing

3. **Production-Ready Calibration Service**
   - Real-time calibration API for live MED integration
   - Batch processing capabilities for historical data
   - Model versioning and update mechanisms
   - Performance monitoring and alerting

4. **Integration Components**
   - Seamless integration with MED Core from Sprint 4
   - DSL integration for persistent storage of calibrated scores
   - Preparation for VOITHER Apothecary (Sprint 6)
   - Clinical dashboard data feed

**This sprint enables the transformation of raw MED dimensions into clinically validated framework scores, forming the foundation for precise psychopharmacological recommendations in the VOITHER Apothecary.**