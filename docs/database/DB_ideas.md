## 🏗️ ARQUITETURA DE DADOS VOITHER: ESTRUTURA DIMENSIONAL COMPLETA
### 📊 VISÃO GERAL: ARQUITETURA HÍBRIDA
```
┌─────────────────────────────────────────────────────────┐
│ CAMADA DE INGESTÃO │
├─────────────────┬──────────────────┬───────────────────┤
│ PostgreSQL │ TimescaleDB │ MongoDB/S3 │
│ (Estruturado) │ (Séries Temp) │ (Não-Estrut) │
├─────────────────┴──────────────────┴───────────────────┤
│ CAMADA ANALÍTICA │
│ Apache Spark + Databricks │
├─────────────────────────────────────────────────────────┤
│ CAMADA DE SERVING │
│ Redis (Cache) + API │
└─────────────────────────────────────────────────────────┘
```
## 1️⃣ POSTGRESQL - DADOS ESTRUTURADOS CORE
### **Tabela: patients**
```sql
CREATE TABLE patients (
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
caps_id INTEGER NOT NULL,
encrypted_cpf VARCHAR(256) UNIQUE,
-- Dados demográficos (anonimizados)
age_range VARCHAR(10), -- '18-25', '26-35', etc
gender VARCHAR(20),
education_level VARCHAR(50),
socioeconomic_score INTEGER,
-- Dados clínicos iniciais
primary_diagnosis_icd11 VARCHAR(10),
secondary_diagnoses JSONB,
medication_history JSONB,
trauma_scores JSONB, -- ACE scores, etc
-- Metadados
consent_date TIMESTAMP,
consent_research BOOLEAN,
created_at TIMESTAMP DEFAULT NOW(),
updated_at TIMESTAMP DEFAULT NOW()
);
-- Índices para performance
CREATE INDEX idx_patients_caps ON patients(caps_id);
CREATE INDEX idx_patients_diagnosis ON patients(primary_diagnosis_icd11);
```
### **Tabela: sessions**
```sql
CREATE TABLE sessions (
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
patient_id UUID REFERENCES patients(id),
therapist_id UUID REFERENCES therapists(id),
-- Contexto da sessão
session_number INTEGER,
session_type VARCHAR(50), -- 'individual', 'group', 'assessment'
duration_minutes INTEGER,
setting VARCHAR(50), -- 'in-person', 'teletherapy'
-- Referências aos dados brutos
audio_storage_key VARCHAR(512), -- S3/Blob key
transcript_storage_key VARCHAR(512),
-- Status
processing_status VARCHAR(50),
quality_score FLOAT, -- Qualidade do áudio/transcrição
-- Timestamps
session_datetime TIMESTAMP,
created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_sessions_patient ON sessions(patient_id);
CREATE INDEX idx_sessions_datetime ON sessions(session_datetime);
```
### **Tabela: interventions**
```sql
CREATE TABLE interventions (
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
patient_id UUID REFERENCES patients(id),
session_id UUID REFERENCES sessions(id),
-- Tipo e detalhes
intervention_type VARCHAR(100), -- 'medication_change', 'therapy_modality'
intervention_details JSONB,
-- Para rastreabilidade
prescribed_by UUID REFERENCES therapists(id),
prescribed_at TIMESTAMP,
-- Acompanhamento
adherence_score FLOAT,
patient_feedback JSONB
);
```
## 2️⃣ TIMESCALEDB - SÉRIES TEMPORAIS DIMENSIONAIS
### **Hypertable: dimensional_measurements**
```sql
CREATE TABLE dimensional_measurements (
time TIMESTAMPTZ NOT NULL,
patient_id UUID NOT NULL,
session_id UUID,
measurement_source VARCHAR(50), -- 'session', 'app', 'daily_check'
-- 15 Dimensões Core
valence_emotional FLOAT,
arousal_activation FLOAT,
narrative_coherence FLOAT,
syntactic_complexity FLOAT,
temporal_orientation_past FLOAT,
temporal_orientation_present FLOAT,
temporal_orientation_future FLOAT,
self_reference_density FLOAT,
social_language FLOAT,
cognitive_flexibility FLOAT,
dominance_agency FLOAT,
discourse_fragmentation FLOAT,
semantic_density FLOAT,
certainty_markers FLOAT,
emotional_prosody FLOAT,
-- Frameworks Integrados
rdoc_negative_valence FLOAT,
rdoc_cognitive_control FLOAT,
rdoc_social_processes FLOAT,
rdoc_arousal_regulatory FLOAT,
hitop_internalizing FLOAT,
hitop_externalizing FLOAT,
hitop_thought_disorder FLOAT,
big5_neuroticism FLOAT,
big5_extraversion FLOAT,
big5_openness FLOAT,
big5_agreeableness FLOAT,
big5_conscientiousness FLOAT,
perma_positive_emotions FLOAT,
perma_engagement FLOAT,
perma_relationships FLOAT,
perma_meaning FLOAT,
perma_accomplishment FLOAT,
-- Metadados de qualidade
confidence_score FLOAT,
processing_version VARCHAR(20)
);
-- Converter para hypertable
SELECT create_hypertable('dimensional_measurements', 'time');
-- Índices otimizados
CREATE INDEX ON dimensional_measurements (patient_id, time DESC);
CREATE INDEX ON dimensional_measurements (session_id, time DESC);
-- Política de retenção (mantém dados detalhados por 2 anos)
SELECT add_retention_policy('dimensional_measurements', INTERVAL '2 years');
```
### **Continuous Aggregates para Performance**
```sql
-- Agregado diário
CREATE MATERIALIZED VIEW daily_dimensions
WITH (timescaledb.continuous) AS
SELECT
time_bucket('1 day', time) AS day,
patient_id,
AVG(valence_emotional) as avg_valence,
AVG(arousal_activation) as avg_arousal,
AVG(narrative_coherence) as avg_coherence,
-- ... todas as dimensões
COUNT(*) as measurement_count
FROM dimensional_measurements
GROUP BY day, patient_id;
-- Agregado semanal
CREATE MATERIALIZED VIEW weekly_dimensions
WITH (timescaledb.continuous) AS
SELECT
time_bucket('1 week', time) AS week,
patient_id,
AVG(valence_emotional) as avg_valence,
STDDEV(valence_emotional) as std_valence,
-- tendência
regr_slope(valence_emotional, extract(epoch from time)) as valence_trend,
-- ... todas as dimensões
FROM dimensional_measurements
GROUP BY week, patient_id;
```
## 3️⃣ MONGODB - DADOS NÃO-ESTRUTURADOS
### **Collection: session_transcripts**
```javascript
{
"_id": ObjectId("..."),
"session_id": "uuid-session",
"patient_id": "uuid-patient",
"transcript": {
"full_text": "Completo texto da sessão...",
"segments": [
{
"speaker": "patient",
"start_time": 0.0,
"end_time": 15.3,
"text": "Essa semana foi difícil...",
"prosody": {
"pitch_mean": 195.2,
"pitch_variance": 45.3,
"speech_rate": 3.2,
"pause_ratio": 0.15
},
"linguistic_features": {
"pos_tags": ["DET", "NOUN", "VERB", "ADJ"],
"dependency_tree": {...},
"entities": ["semana", "difícil"]
}
}
],
"analysis": {
"themes": ["trabalho", "família", "ansiedade"],
"key_moments": [
{
"timestamp": 523.4,
"type": "breakthrough",
"description": "Paciente reconheceu padrão",
"dimensional_shift": {
"coherence": +1.2,
"valence": +0.8
}
}
],
"therapeutic_markers": {
"resistance_moments": [...],
"insight_moments": [...],
"emotional_peaks": [...]
}
}
},
"metadata": {
"processing_timestamp": ISODate("..."),
"llm_version": "claude-3-opus",
"quality_metrics": {
"transcription_confidence": 0.94,
"speaker_diarization_accuracy": 0.89
}
}
}
```
### **Collection: dimensional_analysis_snapshots**
```javascript
{
"_id": ObjectId("..."),
"patient_id": "uuid-patient",
"analysis_date": ISODate("2025-07-17"),
"dimensional_profile": {
"current_state": {
"primary_concerns": ["ruminação", "isolamento"],
"dimensional_clusters": {
"depressive_pattern": {
"dimensions": ["valence", "self_reference", "past_orientation"],
"severity": 7.8
}
}
},
"trajectory_analysis": {
"trend": "improving",
"velocity": 0.3, // rate of change
"volatility": 0.15, // estabilidade
"predicted_state_30d": {...}
},
"intervention_effectiveness": {
"cbt_response": 0.72,
"medication_response": 0.45,
"group_therapy_response": 0.88
}
},
"population_comparison": {
"percentile_ranks": {
"valence": 15, // pior que 85% dos pacientes
"coherence": 45,
"recovery_speed": 72 // melhor que 72%
},
"similar_profiles": ["patient_ids..."], // para análise de cohort
"successful_interventions_in_similar": [...]
}
}
```
## 4️⃣ REDIS - CACHE E REAL-TIME
### **Estruturas de Dados em Tempo Real**
```python
# Estado atual do paciente (TTL 1 hora)
redis.hset(f"patient:{patient_id}:current", {
"valence": -2.3,
"coherence": 4.5,
"last_session": "2025-07-17",
"risk_score": 0.25,
"active_interventions": json.dumps(["CBT", "Medication"])
})
# Fila de processamento
redis.lpush("processing_queue", json.dumps({
"session_id": session_id,
"priority": "high",
"requested_at": timestamp
}))
# Rankings em tempo real
redis.zadd("coherence_improvements_weekly", {
patient_id: improvement_score
})
```
## 5️⃣ DATA LAKE (S3/AZURE BLOB/GOOGLE CLOUD STORAGE)
### **Estrutura de Pastas**
```
/voither-data-lake/
├── /raw/
│ ├── /audio/
│ │ └── /2025/07/17/{session_id}.wav
│ ├── /transcripts/
│ │ └── /2025/07/17/{session_id}.json
│ └── /app_data/
│ └── /2025/07/17/{patient_id}_interactions.json
│
├── /processed/
│ ├── /dimensional_extracts/
│ │ └── /2025/07/17/{session_id}_dimensions.parquet
│ ├── /population_analytics/
│ │ └── /2025/07/cohort_analysis.parquet
│ └── /ml_features/
│ └── /2025/07/training_data_v2.parquet
│
└── /models/
├── /dimensional_extraction/
│ └── /v2.1/model.pkl
└── /prediction/
└── /risk_model_v1.5/
```
## 6️⃣ ESQUEMA DE INTEGRAÇÃO
### **Pipeline de Dados**
```python
# Exemplo de fluxo de processamento
async def process_session(session_id):
# 1. Salva áudio no S3
audio_key = await save_to_s3(audio_file)
# 2. Registra sessão no PostgreSQL
session = await create_session_record(session_id, audio_key)
# 3. Processa transcrição
transcript = await transcribe_audio(audio_key)
await save_to_mongodb(session_id, transcript)
# 4. Extrai dimensões
dimensions = await extract_dimensions(transcript)
# 5. Salva série temporal
await save_to_timescale(session_id, dimensions)
# 6. Atualiza cache
await update_redis_cache(patient_id, dimensions)
# 7. Trigger análises populacionais
await queue_population_analysis(patient_id)
```
## 7️⃣ SEGURANÇA E COMPLIANCE
### **Estratégias de Proteção**
```sql
-- Criptografia em repouso
CREATE EXTENSION IF NOT EXISTS pgcrypto;
-- Função para CPF
CREATE OR REPLACE FUNCTION encrypt_cpf(cpf TEXT)
RETURNS TEXT AS $$
BEGIN
RETURN encode(encrypt(cpf::bytea, 'encryption_key', 'aes'), 'base64');
END;
$$ LANGUAGE plpgsql;
-- Row Level Security
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
CREATE POLICY caps_isolation ON patients
FOR ALL
USING (caps_id = current_setting('app.current_caps_id')::int);
-- Auditoria
CREATE TABLE audit_log (
id SERIAL PRIMARY KEY,
user_id UUID,
action VARCHAR(50),
table_name VARCHAR(50),
record_id UUID,
changes JSONB,
timestamp TIMESTAMP DEFAULT NOW()
);
```
## 8️⃣ QUERIES ANALÍTICAS EXEMPLO
### **Trajetória Individual**
```sql
SELECT
date_trunc('week', time) as week,
AVG(valence_emotional) as avg_valence,
AVG(narrative_coherence) as avg_coherence,
regr_slope(valence_emotional, extract(epoch from time)) as trend
FROM dimensional_measurements
WHERE patient_id = $1
AND time > NOW() - INTERVAL '3 months'
GROUP BY week
ORDER BY week;
```
### **Análise Populacional**
```sql
WITH patient_improvements AS (
SELECT
p.caps_id,
p.primary_diagnosis_icd11,
dm.patient_id,
MAX(dm.valence_emotional) - MIN(dm.valence_emotional) as valence_improvement
FROM dimensional_measurements dm
JOIN patients p ON p.id = dm.patient_id
WHERE dm.time > NOW() - INTERVAL '6 months'
GROUP BY p.caps_id, p.primary_diagnosis_icd11, dm.patient_id
)
SELECT
caps_id,
primary_diagnosis_icd11,
AVG(valence_improvement) as avg_improvement,
PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY valence_improvement) as median_improvement
FROM patient_improvements
GROUP BY caps_id, primary_diagnosis_icd11;
```
## 🚀 IMPLEMENTAÇÃO RECOMENDADA
### **Fase 1: MVP (Já fazer certo)**
- PostgreSQL + TimescaleDB (essenciais)
- S3 para áudios
- Redis básico
### **Fase 2: Escala**
- MongoDB para análises complexas
- Data Lake estruturado
- Apache Spark para população
### **Fase 3: Avançado**
- Real-time streaming (Kafka)
- MLflow para modelos
- Databricks para analytics
Essa arquitetura suporta de 100 a 1 milhão de pacientes sem mudanças fundamentais! 🎯​​​​​​​​​​​​​​​​