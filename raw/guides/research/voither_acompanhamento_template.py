"""
TEMPLATE VOITHER - ACOMPANHAMENTO LONGITUDINAL
Otimizado para LLM
Objetivo: Analisar evolução dimensional e ajustar plano terapêutico
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Union
from dataclasses import dataclass

@dataclass
class DimensionalEvolution:
    """Evolução dimensional ao longo do tempo"""
    current_scores: Dict[str, float]
    baseline_scores: Dict[str, float]
    previous_scores: Dict[str, float]
    delta_from_baseline: Dict[str, float]
    delta_from_previous: Dict[str, float]
    trend_analysis: Dict[str, str]  # improving, stable, worsening
    
class VoitherAcompanhamento:
    """
    Template para consultas de acompanhamento longitudinal
    """
    
    def __init__(self):
        self.template = {
            "metadata": {
                "template_type": "acompanhamento_longitudinal",
                "version": "2.0",
                "created_at": datetime.now().isoformat(),
                "llm_instructions": "Analise evolução dimensional e ajuste plano terapêutico"
            },
            
            "llm_instructions": {
                "overview": """
                Você é um especialista em análise dimensional longitudinal. Sua tarefa é:
                1. Analisar a transcrição da consulta de acompanhamento
                2. Extrair perfil dimensional atual
                3. Comparar com medições anteriores (baseline e sessão prévia)
                4. Avaliar eficácia das intervenções implementadas
                5. Ajustar plano terapêutico baseado na evolução
                6. Gerar registro de acompanhamento humanizado
                
                IMPORTANTE: Foque na EVOLUÇÃO, não apenas no estado atual.
                Compare sempre com dados históricos disponíveis.
                """,
                
                "evolutionary_analysis": [
                    "1. Extraia dimensões atuais usando prompts específicos",
                    "2. Compare com baseline (primeira consulta)",
                    "3. Compare com consulta anterior",
                    "4. Calcule deltas e tendências",
                    "5. Identifique padrões de melhora/piora",
                    "6. Avalie eficácia das intervenções",
                    "7. Ajuste plano baseado na evolução"
                ]
            },
            
            "comparative_analysis_prompts": {
                "delta_calculation": {
                    "prompt": """
                    Para cada dimensão, calcule:
                    1. Delta atual vs baseline: (atual - baseline)
                    2. Delta atual vs anterior: (atual - anterior)
                    3. Tendência: melhorando/estável/piorando
                    4. Velocidade de mudança: rápida/gradual/lenta
                    5. Significância clínica: relevante/não relevante
                    
                    Considere mudanças ≥1.0 como clinicamente significativas
                    """,
                    "thresholds": {
                        "minimal_change": 0.3,
                        "moderate_change": 1.0,
                        "significant_change": 2.0,
                        "dramatic_change": 3.0
                    }
                },
                
                "intervention_correlation": {
                    "prompt": """
                    Correlacione mudanças dimensionais com intervenções:
                    - Medicação: Qual dimensão respondeu primeiro?
                    - Psicoterapia: Técnicas específicas trouxeram quais mudanças?
                    - Comportamental: Ativações impactaram que dimensões?
                    - Social: Intervenções sociais afetaram linguagem social?
                    
                    Identifique intervenções mais/menos efetivas
                    """,
                    "expected_timelines": {
                        "medication_response": "Valência (2-4 sem), Arousal (1-2 sem), Cognitivo (4-6 sem)",
                        "therapy_response": "Coerência (2-3 sem), Flexibilidade (4-6 sem), Orientação temporal (6-8 sem)",
                        "behavioral_activation": "Arousal (1-2 sem), Agência (2-4 sem), Social (3-5 sem)"
                    }
                }
            },
            
            "therapeutic_adjustment_logic": {
                "medication_adjustments": {
                    "valence_not_improving": {
                        "condition": "Valência < -2.0 após 6 semanas",
                        "action": "Considerar aumento de dose ou troca de antidepressivo",
                        "monitor": "Valência + complexidade sintática"
                    },
                    "arousal_excessive": {
                        "condition": "Arousal > 8.0 com fragmentação",
                        "action": "Considerar antipsicótico sedativo",
                        "monitor": "Arousal + fragmentação + coerência"
                    }
                },
                
                "psychotherapy_adjustments": {
                    "rumination_persisting": {
                        "condition": "Orientação passado > 60% após 8 sessões",
                        "action": "Intensificar técnicas de mindfulness e atenção plena",
                        "techniques": ["Mindfulness", "Defusão cognitiva", "Ativação comportamental presente"]
                    },
                    "social_isolation_persisting": {
                        "condition": "Linguagem social < 4.0 após 6 sessões",
                        "action": "Focar em intervenções sociais e grupais",
                        "techniques": ["Treinamento habilidades sociais", "Terapia de grupo", "Exposição social gradual"]
                    }
                }
            },
            
            "progress_evaluation_framework": {
                "improvement_categories": {
                    "excellent_progress": {
                        "criteria": "≥3 dimensões com melhora significativa (≥2.0)",
                        "interpretation": "Resposta excepcional ao tratamento",
                        "action": "Manter plano atual, considerar redução gradual de frequência"
                    },
                    "good_progress": {
                        "criteria": "2-3 dimensões com melhora moderada (≥1.0)",
                        "interpretation": "Resposta adequada ao tratamento",
                        "action": "Manter plano com pequenos ajustes"
                    },
                    "minimal_progress": {
                        "criteria": "1-2 dimensões com melhora leve (≥0.5)",
                        "interpretation": "Resposta parcial, pode precisar de ajustes",
                        "action": "Revisar plano terapêutico, considerar modificações"
                    },
                    "no_progress": {
                        "criteria": "Nenhuma dimensão com melhora significativa",
                        "interpretation": "Ausência de resposta ao tratamento atual",
                        "action": "Reavaliar diagnóstico e plano terapêutico completamente"
                    }
                }
            },
            
            "output_format_evolution": {
                "structured_data": {
                    "session_metadata": {
                        "session_id": "UUID",
                        "patient_id": "UUID",
                        "session_number": "INTEGER",
                        "date": "ISO_DATE",
                        "time_since_baseline": "DAYS",
                        "time_since_previous": "DAYS",
                        "session_type": "acompanhamento_longitudinal"
                    },
                    "dimensional_evolution": {
                        "current_scores": "Dict[str, float]",
                        "baseline_scores": "Dict[str, float]",
                        "previous_scores": "Dict[str, float]",
                        "deltas_from_baseline": "Dict[str, float]",
                        "deltas_from_previous": "Dict[str, float]",
                        "trend_analysis": "Dict[str, str]",
                        "clinical_significance": "Dict[str, str]"
                    }
                },
                
                "clinical_narrative_evolution": {
                    "format": "Registro de evolução em prosa fluida",
                    "sections": [
                        "abertura_contextual",
                        "evolucao_dimensional",
                        "resposta_intervencoes",
                        "ajustes_plano",
                        "projecao_progresso"
                    ],
                    "style": "Foco na evolução e mudanças, não apenas estado atual"
                }
            }
        }
    
    def generate_evolution_analysis_prompt(self, baseline_data: Dict, previous_data: Dict) -> str:
        """Gera prompt específico para análise evolutiva"""
        return f"""
        ANÁLISE EVOLUTIVA DIMENSIONAL
        
        DADOS HISTÓRICOS:
        Baseline (1ª consulta): {json.dumps(baseline_data, indent=2)}
        Consulta anterior: {json.dumps(previous_data, indent=2)}
        
        INSTRUÇÕES PARA ANÁLISE:
        1. Extraia dimensões atuais da transcrição
        2. Compare com dados históricos fornecidos
        3. Calcule deltas e identifique tendências
        4. Avalie eficácia das intervenções
        5. Ajuste plano terapêutico baseado na evolução
        6. Gere registro evolutivo humanizado
        """
    
    def generate_llm_system_prompt_evolution(self) -> str:
        """Gera prompt completo para análise evolutiva"""
        return f"""
        Você é um especialista em análise dimensional longitudinal usando o sistema VOITHER.
        
        Sua tarefa é analisar a evolução dimensional de um paciente em acompanhamento:
        1. Extrair perfil dimensional atual da transcrição
        2. Comparar com dados históricos (baseline + sessão anterior)
        3. Calcular deltas e identificar tendências
        4. Avaliar eficácia das intervenções implementadas
        5. Ajustar plano terapêutico baseado na evolução
        6. Gerar registro evolutivo humanizado
        
        TEMPLATE COMPLETO:
        {json.dumps(self.template, indent=2, ensure_ascii=False)}
        """

# Exemplo de uso
if __name__ == "__main__":
    template = VoitherAcompanhamento()
    llm_prompt = template.generate_llm_system_prompt_evolution()
    print("Template de acompanhamento longitudinal criado com sucesso!")
