# VOITHER - ANÁLISE LINGUÍSTICA (NÍVEL 1)
## Pipeline de Extração de Features Linguísticas

### 🔧 **1. ANÁLISE SINTÁTICA ESTRUTURAL**
**Objetivo:** Extrair características de organização e complexidade cognitiva

#### 1.1 Complexidade Sintática
```python
# Features extraídas
{
    'tree_depth': max_dependency_depth,
    'subordination_ratio': subordinate_clauses / total_clauses,
    'syntactic_entropy': shannon_entropy(syntactic_patterns),
    'mean_sentence_length': tokens_per_sentence,
    'clause_complexity': embedded_structures_count,
    'coordination_ratio': coordinate_structures / total_structures
}
```

#### 1.2 Padrões de Agency
```python
{
    'active_voice_ratio': active_structures / total_structures,
    'first_person_density': first_person_pronouns / total_pronouns,
    'modal_verb_usage': modal_verbs / total_verbs,
    'agency_markers': explicit_agency_expressions,
    'passive_constructions': passive_voice_count
}
```

#### 1.3 Fragmentação vs. Integração
```python
{
    'incomplete_sentences': fragments / total_sentences,
    'false_starts': restarted_utterances,
    'self_corrections': correction_markers,
    'syntactic_fluency': fluent_transitions / total_transitions,
    'parsing_breaks': unparseable_segments
}
```

---

### 🧠 **2. ANÁLISE SEMÂNTICA MULTIDIMENSIONAL**
**Objetivo:** Capturar conteúdo conceitual e emocional

#### 2.1 Embeddings Contextuais
```python
# Modelos state-of-the-art
{
    'sentence_embeddings': use_multilingual_E5_large(),
    'word_embeddings': bert_portuguese_base(),
    'clinical_embeddings': clinicalbert_pt(),
    'contextual_similarity': cosine_similarity_matrix,
    'semantic_density': unique_concepts / total_words
}
```

#### 2.2 Campos Semânticos Clínicos
```python
{
    'emotional_lexicon': {
        'negative_valence': fear_anxiety_sadness_words,
        'positive_valence': joy_hope_enthusiasm_words,
        'arousal_markers': energy_activation_words,
        'dominance_markers': control_power_agency_words
    },
    'cognitive_lexicon': {
        'executive_function': planning_organization_words,
        'memory_markers': recall_forgetting_words,
        'attention_markers': focus_distraction_words,
        'metacognition': thinking_about_thinking
    },
    'social_lexicon': {
        'relationship_words': family_friends_social,
        'cooperation_markers': helping_sharing_words,
        'conflict_markers': arguing_fighting_words,
        'theory_of_mind': perspective_taking_words
    }
}
```

#### 2.3 Análise de Metáforas e Analogias
```python
{
    'metaphor_detection': identify_metaphorical_language(),
    'conceptual_mappings': source_to_target_domains,
    'embodied_cognition': body_based_metaphors,
    'spatial_metaphors': up_down_in_out_mappings,
    'temporal_metaphors': time_as_space_movement
}
```

---

### 🎵 **3. ANÁLISE PROSÓDICA AVANÇADA**
**Objetivo:** Capturar características acústicas e neurobiológicas

#### 3.1 Características Fundamentais
```python
{
    'f0_statistics': {
        'mean_pitch': fundamental_frequency_mean,
        'pitch_variance': f0_standard_deviation,
        'pitch_range': max_f0 - min_f0,
        'pitch_slope': linear_regression_slope
    },
    'intensity_features': {
        'mean_intensity': rms_energy_mean,
        'intensity_variance': energy_fluctuations,
        'dynamic_range': max_intensity - min_intensity
    },
    'timing_features': {
        'speech_rate': syllables_per_second,
        'pause_statistics': pause_duration_distribution,
        'rhythm_metrics': normalized_pairwise_variability,
        'articulation_rate': phonemes_per_speech_time
    }
}
```

#### 3.2 Qualidade Vocal
```python
{
    'voice_quality': {
        'jitter': pitch_perturbation,
        'shimmer': amplitude_perturbation,
        'harmonics_noise_ratio': hnr_ratio,
        'spectral_tilt': high_freq_energy / low_freq_energy
    },
    'emotional_prosody': {
        'stress_patterns': emphasis_distribution,
        'intonation_contours': pitch_movement_patterns,
        'vocal_effort': strain_tension_markers,
        'breathiness': spectral_noise_markers
    }
}
```

---

### 💬 **4. ANÁLISE PRAGMÁTICA CONTEXTUAL**
**Objetivo:** Processar uso funcional da linguagem

#### 4.1 Classificação de Atos de Fala
```python
{
    'speech_acts': {
        'assertives': statements_about_reality,
        'directives': attempts_to_influence,
        'commissives': commitments_to_action,
        'expressives': psychological_state_expressions,
        'declarations': status_changing_utterances
    },
    'illocutionary_force': strength_of_communicative_intent,
    'perlocutionary_effects': intended_audience_impact
}
```

#### 4.2 Teoria da Mente e Competência Social
```python
{
    'perspective_taking': others_mental_states_references,
    'social_deixis': context_dependent_references,
    'politeness_strategies': face_saving_behaviors,
    'cooperative_principles': grice_maxims_adherence,
    'conversational_repair': error_correction_strategies
}
```

---

### 🕰️ **5. ANÁLISE DE COERÊNCIA TEMPORAL**
**Objetivo:** Avaliar integração narrativa e temporal

#### 5.1 Coerência Narrativa
```python
{
    'thematic_coherence': topic_consistency_across_segments,
    'causal_coherence': logical_connection_strength,
    'temporal_coherence': chronological_organization,
    'referential_coherence': pronoun_reference_clarity,
    'global_coherence': overall_story_integration
}
```

#### 5.2 Perspectiva Temporal
```python
{
    'temporal_orientation': {
        'past_focus': past_tense_verbs + past_time_references,
        'present_focus': present_tense + immediate_context,
        'future_focus': future_tense + planning_language
    },
    'temporal_sequencing': chronological_order_accuracy,
    'temporal_distance': psychological_time_perception
}
```

---

### 🕸️ **6. ANÁLISE DE REDE CONCEITUAL**
**Objetivo:** Mapear conectividade e estrutura conceitual

#### 6.1 Rede Semântica
```python
{
    'concept_network': {
        'nodes': unique_semantic_concepts,
        'edges': semantic_associations,
        'centrality_measures': betweenness_closeness_eigenvector,
        'clustering_coefficient': local_connectivity,
        'path_length': average_shortest_path
    },
    'network_metrics': {
        'density': actual_connections / possible_connections,
        'modularity': community_structure_strength,
        'small_world_index': clustering / path_length,
        'degree_distribution': connectivity_pattern
    }
}
```

#### 6.2 Dinâmica de Ativação
```python
{
    'activation_patterns': {
        'spreading_activation': concept_to_concept_flow,
        'semantic_priming': facilitation_effects,
        'inhibition_effects': concept_suppression,
        'resonance_patterns': self_reinforcing_loops
    },
    'network_evolution': temporal_changes_in_connectivity
}
```

---

### 🔊 **7. ANÁLISE MULTIMODAL INTEGRADA**
**Objetivo:** Combinar texto, áudio e contexto

#### 7.1 Alinhamento Texto-Áudio
```python
{
    'multimodal_features': {
        'text_audio_synchrony': alignment_accuracy,
        'prosody_semantic_match': emotional_congruence,
        'emphasis_content_correlation': stress_importance_match,
        'pause_syntax_alignment': boundary_correspondence
    }
}
```

#### 7.2 Features de Contexto
```python
{
    'contextual_features': {
        'session_position': early_middle_late_session,
        'interaction_history': prior_exchanges_influence,
        'therapeutic_alliance': rapport_indicators,
        'environmental_factors': setting_noise_interruptions
    }
}
```

---

### 📊 **8. MÉTRICAS DE QUALIDADE E CONFIABILIDADE**

#### 8.1 Scores de Confiabilidade
```python
{
    'reliability_metrics': {
        'transcription_confidence': speech_to_text_accuracy,
        'parsing_confidence': syntactic_analysis_certainty,
        'semantic_confidence': embedding_stability,
        'overall_quality_score': weighted_composite_reliability
    }
}
```

#### 8.2 Detecção de Anomalias
```python
{
    'anomaly_detection': {
        'outlier_features': statistical_deviations,
        'processing_errors': failed_analyses,
        'data_quality_flags': corrupted_segments,
        'attention_flags': segments_requiring_review
    }
}
```

---

### 🔄 **PIPELINE DE PROCESSAMENTO**

```python
class VoitherLinguisticAnalysis:
    def __init__(self):
        self.processors = {
            'syntactic': SyntacticProcessor(),
            'semantic': SemanticProcessor(),
            'prosodic': ProsodicProcessor(),
            'pragmatic': PragmaticProcessor(),
            'coherence': CoherenceProcessor(),
            'network': NetworkProcessor(),
            'multimodal': MultimodalProcessor(),
            'quality': QualityProcessor()
        }
    
    def analyze(self, audio_file, transcript):
        results = {}
        
        # Processamento paralelo de features
        for processor_name, processor in self.processors.items():
            results[processor_name] = processor.extract_features(
                audio_file, transcript
            )
        
        # Integração cross-modal
        results['integrated'] = self.integrate_modalities(results)
        
        # Quality assessment
        results['quality'] = self.assess_quality(results)
        
        return LanguisticFeatureVector(results)
```

**Total: 47 features principais organizadas em 8 domínios**

**Output:** Vetor linguístico multidimensional pronto para mapeamento dimensional