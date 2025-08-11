"""
TEMPLATE VOITHER - 1ª CONSULTA MÉDICA
Otimizado para LLM
Objetivo: Extrair informações dimensionais da transcrição e gerar prontuário estruturado
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Union
from dataclasses import dataclass

@dataclass
class DimensionalProfile:
    """Perfil dimensional extraído da transcrição"""
    valence_emotional: float  # -5 a +5
    arousal_activation: float  # 0 a 10
    narrative_coherence: float  # 0 a 10
    syntactic_complexity: float  # 0 a 10
    temporal_orientation: Dict[str, float]  # past, present, future %
    self_reference_density: float  # 0 a 10
    social_language: float  # 0 a 10
    discursive_flexibility: float  # 0 a 10
    dominance_agency: float  # 0 a 10
    discourse_fragmentation: float  # 0 a 10
    semantic_density: float  # 0 a 10
    certainty_markers: float  # -5 a +5
    connectivity_patterns: float  # 0 a 10
    pragmatic_communication: float  # 0 a 10
    emotional_prosody: float  # 0 a 10 (se áudio disponível)

class VoitherPrimeiraConsulta:
    """
    Template para primeira consulta médica com análise dimensional
    """
    
    def __init__(self):
        self.template = {
            "metadata": {
                "template_type": "primeira_consulta",
                "version": "2.0",
                "created_at": datetime.now().isoformat(),
                "llm_instructions": "Siga rigorosamente este template para extrair informações da transcrição médica"
            },
            
            "llm_instructions": {
                "overview": """
                Você é um especialista em análise dimensional de saúde mental. Sua tarefa é:
                1. Analisar a transcrição da primeira consulta médica
                2. Extrair as 15 dimensões fundamentais
                3. Gerar um registro clínico humanizado
                4. Sugerir plano terapêutico inicial baseado no perfil dimensional
                
                IMPORTANTE: NUNCA mencione números ou termos técnicos no registro clínico.
                Traduza sempre em linguagem natural e profissional.
                """,
                
                "step_by_step_process": [
                    "1. Leia a transcrição completa",
                    "2. Identifique seções: anamnese, exame mental, queixa principal",
                    "3. Extraia cada uma das 15 dimensões usando os prompts específicos",
                    "4. Valide consistência entre dimensões",
                    "5. Gere registro clínico humanizado",
                    "6. Sugira plano terapêutico baseado no perfil",
                    "7. Estruture saída nos formatos especificados"
                ],
                
                "critical_rules": [
                    "NUNCA invente informações não presentes na transcrição",
                    "SEMPRE use citações diretas do paciente (aspas)",
                    "MANTENHA tom profissional mas caloroso",
                    "FOQUE em observações comportamentais concretas",
                    "EVITE listas - escreva em prosa fluida"
                ]
            },
            
            "dimensional_extraction_prompts": {
                "valence_emotional": {
                    "prompt": """
                    Analise as palavras emocionais na transcrição:
                    - Identifique expressões de sentimentos positivos vs negativos
                    - Observe adjetivos emocionais usados pelo paciente
                    - Considere o tom geral da narrativa
                    - Escala: -5 (muito negativo) a +5 (muito positivo)
                    """,
                    "indicators": {
                        "positive": ["feliz", "alegre", "esperançoso", "satisfeito", "bem", "ótimo"],
                        "negative": ["triste", "angustiado", "desesperado", "deprimido", "mal", "péssimo"],
                        "neutral": ["ok", "normal", "estável", "neutro"]
                    },
                    "translation": {
                        "muito_negativo": "humor persistentemente rebaixado, com predomínio de afetos negativos",
                        "negativo": "humor subdeprimido, com momentos de tristeza",
                        "neutro": "humor estável, afetos equilibrados",
                        "positivo": "humor adequado, com momentos de alegria apropriada",
                        "muito_positivo": "humor elevado, com expressão consistente de bem-estar"
                    }
                },
                
                "arousal_activation": {
                    "prompt": """
                    Avalie o nível de energia/ativação:
                    - Velocidade da fala (rápida/lenta)
                    - Palavras indicativas de energia (agitado, calmo, etc.)
                    - Descrição de atividade física
                    - Relatos de sono e apetite
                    - Escala: 0 (muito baixo) a 10 (muito alto)
                    """,
                    "indicators": {
                        "high": ["agitado", "acelerado", "nervoso", "inquieto", "hiperativo"],
                        "low": ["letárgico", "lento", "preguiçoso", "sem energia", "cansado"],
                        "normal": ["normal", "adequado", "equilibrado"]
                    },
                    "translation": {
                        "muito_baixo": "apresenta sinais de hipoativação, com lentificação psicomotora",
                        "baixo": "energia reduzida, com alguma lentificação",
                        "normal": "nível de ativação adequado",
                        "alto": "apresenta sinais de hiperativação",
                        "muito_alto": "estado de intensa ativação, com possível agitação psicomotora"
                    }
                },
                
                "narrative_coherence": {
                    "prompt": """
                    Avalie a organização lógica do discurso:
                    - Uso de conectores lógicos (porque, então, portanto, assim)
                    - Sequência temporal clara nos relatos
                    - Capacidade de manter o fio da meada
                    - Conexões entre ideias
                    - Escala: 0 (muito fragmentado) a 10 (muito coerente)
                    """,
                    "indicators": {
                        "high": ["porque", "então", "portanto", "assim", "consequentemente", "por isso"],
                        "low": ["não sei", "esqueci", "perdido", "confuso", "não consegue explicar"],
                        "fragmented": ["eh...", "tipo...", "sabe?", "não sei explicar"]
                    },
                    "translation": {
                        "muito_baixo": "discurso significativamente fragmentado, com dificuldade em organizar ideias",
                        "baixo": "alguma desorganização do pensamento, com ocasionais perdas do fio condutor",
                        "normal": "discurso organizado, consegue conectar ideias adequadamente",
                        "alto": "excelente organização narrativa, com sequência lógica clara",
                        "muito_alto": "discurso extremamente bem estruturado e coerente"
                    }
                }
            },
            
            "clinical_sections": {
                "identificacao": {
                    "prompt": "Extraia dados demográficos básicos mencionados na transcrição (idade, sexo, escolaridade, profissão, estado civil)",
                    "required_fields": ["idade", "sexo", "escolaridade", "profissao", "estado_civil"]
                },
                
                "queixa_principal": {
                    "prompt": "Identifique a queixa principal do paciente. Use citação direta se disponível.",
                    "format": "Em suas palavras: '[citação]'. [Elaboração clínica]"
                },
                
                "historia_doenca_atual": {
                    "prompt": "Construa cronologia da doença atual baseada no relato",
                    "components": ["inicio_sintomas", "evolucao", "fatores_desencadeantes", "impacto_funcional"]
                },
                
                "exame_mental": {
                    "prompt": "Baseado nas dimensões extraídas, descreva o exame mental em linguagem clínica natural",
                    "domains": ["aparencia", "comportamento", "humor_afeto", "pensamento", "percepcao", "cognicao", "juizo_critica"]
                },
                
                "avaliacao_risco": {
                    "prompt": "Avalie risco suicida, homicida e de autolesão baseado no discurso",
                    "components": ["ideacao_suicida", "plano_suicida", "meios_acesso", "fatores_protecao", "fatores_risco"]
                },
                
                "impressao_diagnostica": {
                    "prompt": "Formule hipóteses diagnósticas baseadas no perfil dimensional",
                    "format": "Hipótese principal: [CID-11]. Diagnósticos diferenciais: [lista]. Justificativa dimensional: [explicação]"
                },
                
                "plano_terapeutico": {
                    "prompt": "Sugira plano terapêutico baseado no perfil dimensional específico",
                    "components": ["medicamentoso", "psicoterapeutico", "psicossocial", "followup"]
                }
            },
            
            "output_format": {
                "structured_data": {
                    "session_metadata": {
                        "session_id": "UUID",
                        "patient_id": "UUID",
                        "date": "ISO_DATE",
                        "duration_minutes": "INTEGER",
                        "session_type": "primeira_consulta"
                    },
                    "dimensional_scores": {
                        "valence_emotional": "FLOAT",
                        "arousal_activation": "FLOAT",
                        "narrative_coherence": "FLOAT",
                        "syntactic_complexity": "FLOAT",
                        "temporal_orientation": {"past": "FLOAT", "present": "FLOAT", "future": "FLOAT"},
                        "self_reference_density": "FLOAT",
                        "social_language": "FLOAT",
                        "discursive_flexibility": "FLOAT",
                        "dominance_agency": "FLOAT",
                        "discourse_fragmentation": "FLOAT",
                        "semantic_density": "FLOAT",
                        "certainty_markers": "FLOAT",
                        "connectivity_patterns": "FLOAT",
                        "pragmatic_communication": "FLOAT",
                        "emotional_prosody": "FLOAT_OR_NULL"
                    }
                },
                
                "clinical_narrative": {
                    "format": "Texto em prosa fluida seguindo formato DAP/BIRP",
                    "sections": [
                        "abertura_contextual",
                        "dados_observacao",
                        "avaliacao_clinica",
                        "plano_intervencao",
                        "fechamento_reflexivo"
                    ],
                    "style": "Profissional mas caloroso, como clínico experiente escrevendo"
                }
            },
            
            "validation_checklist": [
                "Todas as 15 dimensões foram avaliadas?",
                "Há citações diretas do paciente?",
                "O registro está em linguagem natural (sem números)?",
                "As sugestões terapêuticas são específicas ao perfil?",
                "O plano é factível e realista?",
                "Há avaliação de risco adequada?",
                "O tom é profissional mas humanizado?"
            ]
        }
    
    def generate_llm_system_prompt(self) -> str:
        """Gera prompt completo para instruir o LLM"""
        return f"""
        Você é um especialista em análise dimensional de saúde mental usando o sistema VOITHER. 
        
        Sua tarefa é analisar a transcrição de uma primeira consulta médica e extrair:
        1. Perfil dimensional completo (15 dimensões)
        2. Informações clínicas estruturadas
        3. Registro clínico humanizado
        4. Plano terapêutico baseado no perfil dimensional
        
        TEMPLATE COMPLETO:
        {json.dumps(self.template, indent=2, ensure_ascii=False)}
        """

# Exemplo de uso
if __name__ == "__main__":
    template = VoitherPrimeiraConsulta()
    llm_prompt = template.generate_llm_system_prompt()
    print("Template para 1ª consulta criado com sucesso!")
