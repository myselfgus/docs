# VOITHER - FORMULAÇÃO INTEGRATIVA-TRAJETORIAL (NÍVEL 3)
## Síntese Clínica Dimensional + Prescrições + Trajetória

### 🎯 **1. INTEGRAÇÃO DIMENSIONAL CLÍNICA**
**Input:** Perfis RDoC + HiTOP + Big5 + PERMA  
**Output:** Formulação clínica narrativa estruturada

#### 1.1 Síntese de Perfil Atual
```python
class IntegrativeFormulation:
    def synthesize_current_profile(self, dimensional_results):
        """Integra todos os frameworks em narrativa clínica coerente"""
        
        profile_integration = {
            'dominant_patterns': self.identify_dominant_patterns(dimensional_results),
            'convergent_indicators': self.find_cross_framework_convergence(dimensional_results),
            'discrepant_findings': self.flag_inconsistencies(dimensional_results),
            'clinical_phenotype': self.generate_phenotype_description(dimensional_results)
        }
        
        # Exemplo de integração
        if (dimensional_results['RDoC']['negative_valence'] > 7.0 and 
            dimensional_results['HiTOP']['internalizing'] > 7.5 and
            dimensional_results['Big5']['neuroticism'] > 7.0):
            
            primary_pattern = {
                'clinical_presentation': 'Internalizing pattern with high negative valence',
                'neurobiological_substrate': 'Hyperactive threat detection systems',
                'behavioral_manifestation': 'Avoidance, rumination, emotional dysregulation',
                'functional_impact': self.assess_functional_impact(dimensional_results)
            }
        
        return profile_integration
```

#### 1.2 Mapeamento Dimensional → Fenótipo Clínico
```python
def map_dimensions_to_clinical_phenotype(self, dimensional_profile):
    """Traduz perfil dimensional em descrição clínica útil"""
    
    clinical_phenotypes = {
        # Padrão Internalizante Alto
        'high_internalizing': {
            'criteria': {
                'RDoC_negative_valence': '>7.0',
                'HiTOP_internalizing': '>7.5', 
                'Big5_neuroticism': '>7.0',
                'PERMA_positive_emotions': '<3.0'
            },
            'phenotype': {
                'primary_presentation': 'Síndrome internalizante com hiperativação de sistemas de ameaça',
                'core_features': [
                    'Processamento enviesado para ameaças',
                    'Rumination patterns estabelecidos',
                    'Déficit em regulação emocional positiva',
                    'Reatividade aumentada a estressores'
                ],
                'functional_domains_affected': [
                    'Relacionamentos interpessoais (evitação)',
                    'Performance acadêmica/profissional',
                    'Qualidade do sono e energia',
                    'Tomada de decisão (paralisia por análise)'
                ]
            }
        },
        
        # Padrão Externalizante Alto  
        'high_externalizing': {
            'criteria': {
                'HiTOP_externalizing': '>7.0',
                'RDoC_cognitive_control': '<4.0',
                'Big5_conscientiousness': '<4.0'
            },
            'phenotype': {
                'primary_presentation': 'Síndrome externalizante com déficit de controle inibitório',
                'core_features': [
                    'Impulsividade comportamental aumentada',
                    'Dificuldade de planejamento e organização', 
                    'Externalização de responsabilidade',
                    'Busca por estimulação/novidade'
                ]
            }
        },
        
        # Padrão Thought Disorder
        'thought_disorder': {
            'criteria': {
                'HiTOP_thought_disorder': '>6.0',
                'RDoC_cognitive_control': '<5.0'
            },
            'phenotype': {
                'primary_presentation': 'Desorganização do pensamento com fragmentação cognitiva',
                'core_features': [
                    'Incoerência semântica progressiva',
                    'Associações livres/frouxas',
                    'Fragmentação sintática do discurso',
                    'Déficit de integração executiva'
                ],
                'risk_factors': [
                    'Progressão para sintomas psicóticos',
                    'Deterioração funcional cognitiva',
                    'Isolamento social secundário'
                ]
            }
        }
    }
    
    return self.match_profile_to_phenotype(dimensional_profile, clinical_phenotypes)
```

---

### 📈 **2. ANÁLISE TRAJETORIAL TEMPORAL**
**Onde estava → Onde está → Para onde vai**

#### 2.1 Reconstrução da Trajetória Histórica
```python
def reconstruct_historical_trajectory(self, current_profile, historical_data=None):
    """Reconstrói trajetória baseada em perfil atual + dados históricos"""
    
    trajectory_reconstruction = {
        'developmental_trajectory': {
            # Inferência baseada em padrões estabelecidos
            'early_patterns': self.infer_early_development(current_profile),
            'adolescent_patterns': self.infer_adolescent_trajectory(current_profile),
            'adult_consolidation': self.analyze_current_consolidation(current_profile)
        },
        
        'critical_transitions': {
            # Pontos de inflexão prováveis baseados no perfil
            'vulnerability_periods': self.identify_vulnerability_windows(current_profile),
            'protective_factors': self.identify_historical_protections(current_profile),
            'trauma_signatures': self.detect_trauma_linguistic_signatures(current_profile)
        },
        
        'stability_vs_change_patterns': {
            'stable_traits': self.identify_stable_dimensional_patterns(current_profile),
            'state_dependent_features': self.identify_changeable_features(current_profile),
            'intervention_responsive_domains': self.predict_treatment_responsiveness(current_profile)
        }
    }
    
    return trajectory_reconstruction

# Exemplo de inferência trajetorial
def infer_early_development(self, current_profile):
    """Infere padrões de desenvolvimento precoce baseado no perfil atual"""
    
    if (current_profile['Big5']['neuroticism'] > 7.0 and 
        current_profile['RDoC']['social_processes'] < 4.0):
        
        return {
            'likely_early_pattern': 'Temperamento inibido com sensibilidade social aumentada',
            'developmental_vulnerabilities': [
                'Ansiedade de separação provável',
                'Timidez comportamental persistente',
                'Sensibilidade a críticas/rejeição'
            ],
            'protective_factors_needed': [
                'Ambiente familiar seguro/previsível',
                'Exposições sociais graduais e seguras',
                'Validação emocional consistente'
            ]
        }
```

#### 2.2 Predição Trajetorial Futura
```python
def predict_future_trajectory(self, current_profile, intervention_plan=None):
    """Prediz trajetórias prováveis com/sem intervenção"""
    
    trajectory_models = {
        'natural_history': {
            # Sem intervenção - baseado em estudos longitudinais
            'short_term_6_months': self.predict_natural_6month(current_profile),
            'medium_term_2_years': self.predict_natural_2year(current_profile),
            'long_term_5_years': self.predict_natural_5year(current_profile)
        },
        
        'intervention_modified': {
            # Com intervenção - baseado em RCTs e effectiveness studies
            'optimistic_scenario': self.predict_optimal_response(current_profile, intervention_plan),
            'realistic_scenario': self.predict_typical_response(current_profile, intervention_plan),
            'pessimistic_scenario': self.predict_poor_response(current_profile, intervention_plan)
        },
        
        'risk_stratification': {
            'deterioration_risk': self.calculate_deterioration_probability(current_profile),
            'maintenance_probability': self.calculate_stability_probability(current_profile),
            'improvement_likelihood': self.calculate_improvement_probability(current_profile, intervention_plan)
        }
    }
    
    return trajectory_models

# Exemplo de predição específica
def predict_optimal_response(self, current_profile, intervention_plan):
    """Predição otimista baseada em fatores prognósticos positivos"""
    
    positive_prognostic_factors = []
    
    if current_profile['PERMA']['relationships'] > 6.0:
        positive_prognostic_factors.append('Strong social support network')
    
    if current_profile['Big5']['conscientiousness'] > 6.0:
        positive_prognostic_factors.append('High treatment adherence likelihood')
    
    if current_profile['RDoC']['cognitive_control'] > 5.0:
        positive_prognostic_factors.append('Preserved executive function for skill learning')
    
    return {
        'timeline': '6-12 months',
        'expected_changes': {
            'RDoC_negative_valence': f"Reduction from {current_profile['RDoC']['negative_valence']:.1f} to ~4.5",
            'PERMA_positive_emotions': f"Increase from {current_profile['PERMA']['positive_emotions']:.1f} to ~6.5",
            'functional_improvement': 'Significant improvement in 3+ life domains'
        },
        'positive_factors': positive_prognostic_factors,
        'success_probability': self.calculate_success_probability(positive_prognostic_factors)
    }
```

---

### 💊 **3. PRESCRIÇÕES E INTERVENÇÕES DIMENSIONALMENTE ORIENTADAS**

#### 3.1 Farmacoterapia Dimensional
```python
def generate_dimensional_pharmacotherapy(self, dimensional_profile):
    """Prescrições baseadas em perfil dimensional específico"""
    
    pharmacotherapy_recommendations = {
        'primary_targets': [],
        'medication_classes': [],
        'dosing_considerations': [],
        'monitoring_parameters': []
    }
    
    # Alvo: RDoC Negative Valence System
    if dimensional_profile['RDoC']['negative_valence'] > 7.0:
        pharmacotherapy_recommendations['primary_targets'].append({
            'target': 'Hyperactive threat detection (amygdala-ACC)',
            'mechanism': 'Serotonergic modulation + GABAergic enhancement',
            'first_line': {
                'medication': 'Escitalopram 10-20mg/dia',
                'rationale': 'Selective 5-HT reuptake inhibition reduces threat sensitivity',
                'timeline': '4-6 weeks for full effect',
                'dimensional_target': 'Reduce negative valence to <5.0'
            },
            'augmentation_if_needed': {
                'medication': 'Pregabalina 150-300mg/dia',
                'rationale': 'GABAergic enhancement for residual anxiety/rumination',
                'timing': 'If <50% improvement at 8 weeks'
            }
        })
    
    # Alvo: RDoC Cognitive Control Deficits
    if dimensional_profile['RDoC']['cognitive_control'] < 4.0:
        pharmacotherapy_recommendations['primary_targets'].append({
            'target': 'Executive function enhancement (dlPFC)',
            'mechanism': 'Dopaminergic/noradrenergic optimization', 
            'first_line': {
                'medication': 'Bupropiona XR 150-300mg/dia',
                'rationale': 'NDRI mechanism enhances cognitive control circuits',
                'timeline': '2-4 weeks for cognitive effects',
                'dimensional_target': 'Improve cognitive control to >6.0'
            }
        })
    
    # Alvo: HiTOP Internalizing + Big5 Neuroticism
    if (dimensional_profile['HiTOP']['internalizing'] > 7.5 and 
        dimensional_profile['Big5']['neuroticism'] > 7.0):
        
        pharmacotherapy_recommendations['medication_classes'].append({
            'class': 'SSRI + CBT combination',
            'evidence_base': 'RCT evidence for dimensional internalizing spectrum',
            'specific_recommendation': {
                'medication': 'Sertralina 50-150mg/dia',
                'psychotherapy': 'CBT protocols for emotional regulation',
                'rationale': 'Synergistic neuroplastic effects on emotional circuits'
            }
        })
    
    return pharmacotherapy_recommendations
```

#### 3.2 Psicoterapia Dimensionalmente Orientada
```python
def generate_dimensional_psychotherapy(self, dimensional_profile):
    """Protocolos terapêuticos baseados no perfil dimensional"""
    
    psychotherapy_plan = {
        'primary_modality': None,
        'specific_protocols': [],
        'session_frequency': None,
        'duration_estimate': None,
        'outcome_metrics': []
    }
    
    # CBT para Cognitive Control + Internalizing
    if (dimensional_profile['RDoC']['cognitive_control'] < 5.0 and
        dimensional_profile['HiTOP']['internalizing'] > 6.0):
        
        psychotherapy_plan['primary_modality'] = 'Cognitive-Behavioral Therapy'
        psychotherapy_plan['specific_protocols'] = [
            {
                'protocol': 'Cognitive Restructuring for Threat Bias',
                'target': 'RDoC Negative Valence reduction',
                'techniques': [
                    'Thought record with probability estimation',
                    'Behavioral experiments for safety behaviors', 
                    'Attention bias modification training'
                ],
                'duration': '8-12 sessions'
            },
            {
                'protocol': 'Executive Function Skills Training',
                'target': 'RDoC Cognitive Control enhancement',
                'techniques': [
                    'Problem-solving training',
                    'Attention and working memory exercises',
                    'Planning and organization strategies'
                ],
                'duration': '6-8 sessions'
            }
        ]
    
    # DBT para Emotional Dysregulation + High Neuroticism
    if (dimensional_profile['Big5']['neuroticism'] > 8.0 and
        dimensional_profile['PERMA']['positive_emotions'] < 3.0):
        
        psychotherapy_plan['specific_protocols'].append({
            'protocol': 'Dialectical Behavior Therapy Skills',
            'target': 'Emotional regulation + distress tolerance',
            'modules': [
                'Mindfulness (present-moment awareness)',
                'Distress tolerance (crisis survival)',
                'Emotion regulation (understanding and changing emotions)',
                'Interpersonal effectiveness (maintaining relationships)'
            ],
            'format': 'Individual therapy + skills group',
            'duration': '6 months standard protocol'
        })
    
    return psychotherapy_plan
```

#### 3.3 Intervenções Digitais/Apps Personalizadas
```python
def generate_digital_interventions(self, dimensional_profile):
    """Apps e intervenções digitais baseadas no perfil"""
    
    digital_recommendations = []
    
    # Para RDoC Negative Valence alto
    if dimensional_profile['RDoC']['negative_valence'] > 7.0:
        digital_recommendations.append({
            'app': 'MindShift (Anxiety Canada)',
            'target': 'Real-time anxiety management',
            'usage_protocol': '3x/day during anxiety spikes',
            'features_to_use': [
                'Thought record functionality',
                'Relaxation audio guides', 
                'Behavioral experiment planning'
            ],
            'monitoring': 'Track anxiety ratings pre/post use'
        })
    
    # Para PERMA Positive Emotions baixo
    if dimensional_profile['PERMA']['positive_emotions'] < 4.0:
        digital_recommendations.append({
            'app': 'Happify (evidence-based positive psychology)',
            'target': 'Increase positive affect and engagement',
            'usage_protocol': '15-20 min daily exercises',
            'tracks_recommended': [
                'Savor track (mindful appreciation)',
                'Gratitude journaling',
                'Strengths identification and use'
            ]
        })
    
    return digital_recommendations
```

---

### 🔬 **4. EXAMES COMPLEMENTARES DIMENSIONALMENTE ORIENTADOS**

#### 4.1 Neuroimagem Estrutural/Funcional
```python
def recommend_neuroimaging(self, dimensional_profile, clinical_context):
    """Neuroimagem quando clinicamente indicada pelo perfil dimensional"""
    
    imaging_recommendations = []
    
    # fMRI para Cognitive Control severo
    if (dimensional_profile['RDoC']['cognitive_control'] < 3.0 and
        clinical_context['functional_impairment'] == 'severe'):
        
        imaging_recommendations.append({
            'modality': 'fMRI task-based',
            'specific_protocol': 'N-back working memory task + Stroop',
            'target_networks': [
                'Central Executive Network (dlPFC-parietal)',
                'Anterior Cingulate Cortex activation',
                'Default Mode Network deactivation'
            ],
            'clinical_utility': 'Objective measure of cognitive control deficits',
            'insurance_justification': 'Severe functional impairment with unclear etiology'
        })
    
    # DTI para Thought Disorder
    if dimensional_profile['HiTOP']['thought_disorder'] > 7.0:
        imaging_recommendations.append({
            'modality': 'Diffusion Tensor Imaging (DTI)',
            'target_tracts': [
                'Uncinate fasciculus (semantic processing)',
                'Superior longitudinal fasciculus (working memory)',
                'Corpus callosum (interhemispheric communication)'
            ],
            'clinical_utility': 'White matter integrity assessment',
            'differential_diagnosis': 'Rule out early neurodegenerative processes'
        })
    
    return imaging_recommendations
```

#### 4.2 Biomarcadores Laboratoriais
```python
def recommend_laboratory_workup(self, dimensional_profile):
    """Labs baseados no perfil dimensional e fatores de risco"""
    
    lab_recommendations = {
        'routine_screening': [],
        'targeted_biomarkers': [],
        'pharmacogenomics': []
    }
    
    # Para profiles de alto Neuroticism + baixo Positive Emotions
    if (dimensional_profile['Big5']['neuroticism'] > 7.5 and 
        dimensional_profile['PERMA']['positive_emotions'] < 3.0):
        
        lab_recommendations['targeted_biomarkers'] = [
            {
                'test': 'Cortisol matinal + curva',
                'rationale': 'HPA axis dysregulation common in chronic stress/depression',
                'interpretation': 'Correlate with RDoC Negative Valence scores'
            },
            {
                'test': 'Inflammatory markers (CRP, IL-6, TNF-α)',
                'rationale': 'Neuroinflammation associated with internalizing disorders',
                'treatment_implications': 'May indicate adjunctive anti-inflammatory approaches'
            },
            {
                'test': 'BDNF serum levels',
                'rationale': 'Neuroplasticity marker, prognostic for treatment response',
                'monitoring': 'Recheck after 3 months of treatment'
            }
        ]
    
    # Pharmacogenomics para casos complexos
    if dimensional_profile['treatment_resistance_risk'] > 0.7:
        lab_recommendations['pharmacogenomics'] = [
            {
                'test': 'CYP2D6, CYP2C19 genotyping',
                'rationale': 'Optimize SSRI/antipsychotic dosing',
                'clinical_utility': 'Reduce trial-and-error prescribing'
            },
            {
                'test': 'COMT genotype', 
                'rationale': 'Dopamine metabolism affects cognitive interventions',
                'treatment_implications': 'May influence stimulant/cognitive enhancer response'
            }
        ]
    
    return lab_recommendations
```

#### 4.3 Avaliações Cognitivas Objetivas
```python
def recommend_cognitive_testing(self, dimensional_profile):
    """Testes neuropsicológicos baseados no perfil dimensional"""
    
    cognitive_battery = []
    
    # Para RDoC Cognitive Control < 4.0
    if dimensional_profile['RDoC']['cognitive_control'] < 4.0:
        cognitive_battery.append({
            'domain': 'Executive Functions',
            'tests': [
                'Wisconsin Card Sorting Test (cognitive flexibility)',
                'Stroop Color-Word Test (inhibitory control)',
                'N-back task (working memory)',
                'Tower of London (planning)'
            ],
            'purpose': 'Quantify specific executive deficits',
            'treatment_planning': 'Target specific cognitive domains in therapy'
        })
    
    # Para HiTOP Thought Disorder > 6.0
    if dimensional_profile['HiTOP']['thought_disorder'] > 6.0:
        cognitive_battery.append({
            'domain': 'Language and Semantic Processing',
            'tests': [
                'Category fluency (semantic organization)',
                'Boston Naming Test (lexical access)',
                'Discourse comprehension tasks',
                'Semantic priming paradigms'
            ],
            'purpose': 'Assess semantic network integrity',
            'monitoring': 'Track cognitive decline vs. stability'
        })
    
    return cognitive_battery
```

---

### 📋 **5. FORMULAÇÃO CLÍNICA INTEGRATIVA FINAL**

#### 5.1 Template de Formulação Estruturada
```python
def generate_integrated_formulation(self, dimensional_profile, trajectory_analysis, 
                                   interventions, exam_recommendations):
    """Formulação clínica narrativa final integrando todos os elementos"""
    
    formulation = {
        'presenting_concerns': self.synthesize_chief_complaints(dimensional_profile),
        'dimensional_profile_summary': self.create_profile_narrative(dimensional_profile),
        'historical_trajectory': self.narrative_trajectory(trajectory_analysis),
        'current_functioning': self.assess_current_function(dimensional_profile),
        'risk_assessment': self.comprehensive_risk_assessment(dimensional_profile),
        'prognostic_factors': self.identify_prognostic_indicators(dimensional_profile),
        'treatment_plan': self.integrate_treatment_recommendations(interventions),
        'monitoring_plan': self.create_monitoring_strategy(exam_recommendations),
        'case_complexity': self.rate_case_complexity(dimensional_profile)
    }
    
    return self.format_clinical_narrative(formulation)

# Exemplo de narrativa gerada
def create_profile_narrative(self, dimensional_profile):
    """Converte perfil dimensional em narrativa clínica legível"""
    
    narrative = f"""
    PERFIL DIMENSIONAL ATUAL:
    
    Apresenta padrão predominantemente internalizante (HiTOP Internalizing = {dimensional_profile['HiTOP']['internalizing']:.1f}) 
    caracterizado por hiperativação de sistemas de detecção de ameaças (RDoC Negative Valence = {dimensional_profile['RDoC']['negative_valence']:.1f}) 
    e déficit moderado em controle cognitivo (RDoC Cognitive Control = {dimensional_profile['RDoC']['cognitive_control']:.1f}).
    
    O perfil de personalidade revela alta instabilidade emocional (Big5 Neuroticism = {dimensional_profile['Big5']['neuroticism']:.1f}) 
    com preservação relativa de capacidades sociais (RDoC Social Processes = {dimensional_profile['RDoC']['social_processes']:.1f}).
    
    Recursos de bem-estar psicológico significativamente comprometidos, particularmente em emoções positivas 
    (PERMA Positive Emotions = {dimensional_profile['PERMA']['positive_emotions']:.1f}) e senso de significado 
    (PERMA Meaning = {dimensional_profile['PERMA']['meaning']:.1f}).
    
    IMPLICAÇÕES FUNCIONAIS:
    Este perfil dimensional sugere vulnerabilidade a episódios depressivo-ansiosos recorrentes, com risco de 
    cronificação caso não haja intervenção adequada. A preservação do funcionamento social constitui fator 
    protetor importante para o prognóstico.
    """
    
    return narrative
```

#### 5.2 Plano de Monitoramento Dimensional
```python
def create_monitoring_strategy(self, dimensional_profile, interventions):
    """Estratégia de acompanhamento baseada no perfil e intervenções"""
    
    monitoring_plan = {
        'frequency': self.determine_follow_up_frequency(dimensional_profile),
        'dimensional_tracking': {
            'primary_targets': self.identify_primary_monitoring_dimensions(dimensional_profile),
            'measurement_tools': self.select_measurement_instruments(dimensional_profile),
            'change_thresholds': self.define_significant_change_criteria(dimensional_profile)
        },
        'safety_monitoring': {
            'risk_indicators': self.define_risk_monitoring_parameters(dimensional_profile),
            'crisis_protocols': self.establish_crisis_response_plan(dimensional_profile),
            'escalation_triggers': self.define_escalation_criteria(dimensional_profile)
        },
        'treatment_response_indicators': {
            'early_response_markers': 'Improvements in sleep, energy, concentration (2-4 weeks)',
            'intermediate_markers': 'Mood stabilization, reduced anxiety (6-8 weeks)', 
            'long_term_markers': 'Functional improvement, relationship quality (3-6 months)'
        }
    }
    
    return monitoring_plan
```

---

### 📊 **6. OUTPUT FINAL ESTRUTURADO**

```python
class VoitherClinicalFormulation:
    def generate_complete_formulation(self, patient_data):
        """Pipeline completo: Linguística → Dimensional → Formulação Clínica"""
        
        # Pipeline integrado
        linguistic_analysis = self.analyze_linguistics(patient_data['session_transcript'])
        dimensional_profile = self.analyze_dimensions(linguistic_analysis)
        trajectory_analysis = self.analyze_trajectory(dimensional_profile, patient_data['history'])
        
        # Formulação clínica final
        clinical_formulation = {
            'patient_id': patient_data['id'],
            'assessment_date': datetime.now(),
            
            'dimensional_profile': dimensional_profile,
            'trajectory_analysis': trajectory_analysis,
            
            'clinical_formulation': self.generate_integrated_formulation(
                dimensional_profile, trajectory_analysis
            ),
            
            'treatment_recommendations': {
                'pharmacotherapy': self.generate_dimensional_pharmacotherapy(dimensional_profile),
                'psychotherapy': self.generate_dimensional_psychotherapy(dimensional_profile),
                'digital_interventions': self.generate_digital_interventions(dimensional_profile)
            },
            
            'diagnostic_workup': {
                'neuroimaging': self.recommend_neuroimaging(dimensional_profile),
                'laboratory': self.recommend_laboratory_workup(dimensional_profile),
                'cognitive_testing': self.recommend_cognitive_testing(dimensional_profile)
            },
            
            'monitoring_plan': self.create_monitoring_strategy(dimensional_profile),
            
            'prognosis': {
                'short_term': self.predict_short_term_trajectory(dimensional_profile),
                'long_term': self.predict_long_term_trajectory(dimensional_profile),
                'prognostic_factors': self.identify_prognostic_factors(dimensional_profile)
            },
            
            'case_complexity_rating': self.rate_complexity(dimensional_profile),
            'confidence_intervals': self.calculate_formulation_confidence(dimensional_profile)
        }
        
        return clinical_formulation
```

**Output:** Formulação clínica completa, cientificamente fundamentada, com prescrições específicas, exames orientados e monitoramento dimensional estruturado - o mais próximo de um "diagnóstico" dimensional útil clinicamente.