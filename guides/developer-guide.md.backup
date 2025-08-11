# Developer Guide - VOITHER Implementation

*Complete guide for developers implementing and extending VOITHER*

## 🛠️ Development Environment Setup

### Prerequisites
- **Node.js** 18+ or **Python** 3.11+
- **Azure Account** with AI services enabled
- **MongoDB Atlas** account (free tier available)
- **Git** and **Docker** (optional but recommended)

### Quick Setup (15 minutes)

```bash
# Clone the repository
git clone https://github.com/myselfgus/docs
cd docs

# Install dependencies (Node.js path)
npm install

# Or Python path
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Azure keys

# Run development server
npm run dev
# Or python app.py
```

## 🏗️ Architecture Overview

### System Components

```mermaid
graph TD
    A[Frontend - React/Next.js] --> B[API Gateway]
    B --> C[Core Services]
    C --> D[MED Engine - Dimensional Extraction]
    C --> E[Transcription Service]
    C --> F[FHIR Service Layer]
    
    D --> G[MongoDB Atlas - Insights]
    F --> H[PostgreSQL - FHIR Resources]
    E --> I[Azure Blob Storage - Audio]
    
    J[Azure AI Services] --> D
    J --> E
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React 19 + TypeScript | User interface and 3D visualization |
| **Real-time** | Azure SignalR | WebSocket connections for live transcription |
| **Backend** | Node.js/Express or Python/FastAPI | API services and business logic |
| **AI Processing** | Azure AI Studio + Custom Models | Dimensional analysis and NLP |
| **Data Storage** | MongoDB Atlas + PostgreSQL | Hybrid storage architecture |
| **File Storage** | Azure Blob Storage | Audio files and media |
| **Orchestration** | Azure Functions | Serverless processing |

## 🧠 Core Components

### 1. MED Engine (Motor de Extração Dimensional)

The heart of VOITHER - extracts 15 psychological dimensions from text.

```python
from voither.med import DimensionalExtractor

# Initialize the MED engine
med = DimensionalExtractor({
    'azure_key': 'your-azure-key',
    'azure_endpoint': 'your-endpoint',
    'spacy_model': 'pt_core_news_lg'
})

# Extract dimensions from text
result = await med.extract_dimensions(
    text="Patient expresses feeling anxious about the future...",
    speaker="patient"
)

# Result structure
{
    'dimensions': {
        'v1_valence': -2.3,
        'v2_arousal': 7.2,
        'v3_coherence': 6.8,
        # ... all 15 dimensions
    },
    'metadata': {
        'processing_time': 1.2,
        'confidence_scores': {...}
    }
}
```

### 2. Real-time Transcription Pipeline

```javascript
// Frontend transcription setup
import { ConversationTranscriber } from './services/transcription';

const transcriber = new ConversationTranscriber({
    subscriptionKey: process.env.AZURE_SPEECH_KEY,
    region: process.env.AZURE_SPEECH_REGION,
    language: 'pt-BR'
});

// Start real-time transcription
transcriber.startContinuousRecognition();

transcriber.on('transcribed', (result) => {
    // Send to backend for dimensional analysis
    socket.emit('analyze_segment', {
        text: result.text,
        speaker: result.speaker,
        timestamp: result.offset
    });
});
```

### 3. FHIR Integration Layer

```python
from voither.fhir import FHIRMapper

# Map VOITHER data to FHIR resources
mapper = FHIRMapper()

# Convert dimensional data to FHIR Observations
fhir_observations = mapper.dimensions_to_observations(
    dimensions=session_data['dimensions'],
    patient_id='patient-123',
    practitioner_id='practitioner-456'
)

# Save to PostgreSQL FHIR store
fhir_store.save_resources(fhir_observations)
```

## 🔧 Implementation Patterns

### 1. Dimensional Analysis Pipeline

```python
class DimensionalPipeline:
    """Complete pipeline for processing therapy sessions"""
    
    def __init__(self, config):
        self.transcription_service = TranscriptionService(config.azure)
        self.med_engine = DimensionalExtractor(config.med)
        self.fhir_mapper = FHIRMapper(config.fhir)
        self.storage = StorageService(config.storage)
    
    async def process_session(self, audio_stream, patient_id):
        """Process complete therapy session"""
        
        # 1. Transcribe audio with diarization
        transcript = await self.transcription_service.transcribe(
            audio_stream,
            enable_diarization=True
        )
        
        # 2. Extract dimensions from each speaker segment
        dimensions_timeline = []
        for segment in transcript.segments:
            dims = await self.med_engine.extract_dimensions(
                text=segment.text,
                speaker=segment.speaker
            )
            dimensions_timeline.append({
                'timestamp': segment.start_time,
                'dimensions': dims,
                'speaker': segment.speaker
            })
        
        # 3. Generate clinical documentation
        clinical_doc = await self.generate_clinical_notes(
            transcript, dimensions_timeline
        )
        
        # 4. Map to FHIR resources
        fhir_resources = self.fhir_mapper.session_to_fhir(
            patient_id=patient_id,
            session_data={
                'transcript': transcript,
                'dimensions': dimensions_timeline,
                'clinical_notes': clinical_doc
            }
        )
        
        # 5. Store everything
        session_id = await self.storage.save_session({
            'mongodb': {  # Rich, unstructured data
                'transcript': transcript,
                'dimensions_timeline': dimensions_timeline,
                'clinical_notes': clinical_doc
            },
            'postgresql': {  # Structured FHIR data
                'resources': fhir_resources
            },
            'blob_storage': {  # Original audio
                'audio_file': audio_stream
            }
        })
        
        return session_id
```

### 2. Real-time Processing with WebSockets

```javascript
// Backend WebSocket handler
class RealTimeProcessor {
    constructor(io) {
        this.io = io;
        this.activeSessions = new Map();
    }
    
    handleConnection(socket) {
        socket.on('start_session', async (data) => {
            const sessionId = generateSessionId();
            
            // Initialize session state
            this.activeSessions.set(sessionId, {
                patientId: data.patientId,
                startTime: Date.now(),
                segments: [],
                dimensions: []
            });
            
            socket.join(sessionId);
            socket.emit('session_started', { sessionId });
        });
        
        socket.on('audio_chunk', async (data) => {
            const { sessionId, audioChunk } = data;
            
            // Process audio chunk
            const transcription = await this.transcribeChunk(audioChunk);
            
            if (transcription.text) {
                // Extract dimensions in real-time
                const dimensions = await this.extractDimensions(
                    transcription.text
                );
                
                // Update session state
                const session = this.activeSessions.get(sessionId);
                session.segments.push(transcription);
                session.dimensions.push(dimensions);
                
                // Send real-time updates to client
                this.io.to(sessionId).emit('transcription_update', {
                    text: transcription.text,
                    speaker: transcription.speaker,
                    dimensions: dimensions
                });
            }
        });
    }
}
```

### 3. Holofractor 3D Visualization

```javascript
// React Three Fiber component for 3D visualization
import { Canvas, useFrame } from '@react-three/fiber';
import { useState, useRef } from 'react';

function HolofractorMesh({ dimensions }) {
    const meshRef = useRef();
    
    // Create custom shader material
    const shaderMaterial = useMemo(() => ({
        vertexShader: `
            uniform float u_valence;
            uniform float u_arousal;
            uniform float u_coherence;
            
            void main() {
                vec3 pos = position;
                
                // Modulate geometry based on dimensions
                float displacement = sin(pos.x * u_coherence) * 0.1;
                pos += normal * displacement;
                
                gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
            }
        `,
        fragmentShader: `
            uniform float u_valence;
            uniform float u_arousal;
            
            void main() {
                // Color based on valence and arousal
                vec3 color = vec3(
                    (u_valence + 5.0) / 10.0,  // Red component
                    u_arousal / 10.0,          // Green component
                    0.5                        // Blue component
                );
                
                gl_FragColor = vec4(color, 0.8);
            }
        `,
        uniforms: {
            u_valence: { value: dimensions.v1_valence },
            u_arousal: { value: dimensions.v2_arousal },
            u_coherence: { value: dimensions.v3_coherence }
        }
    }), [dimensions]);
    
    // Animate the holofractor
    useFrame(() => {
        if (meshRef.current) {
            meshRef.current.rotation.y += 0.01;
        }
    });
    
    return (
        <mesh ref={meshRef}>
            <icosahedronGeometry args={[1, 2]} />
            <shaderMaterial {...shaderMaterial} />
        </mesh>
    );
}
```

## 📊 Data Models

### MongoDB Document Structure

```javascript
// Session document in MongoDB
{
    "_id": ObjectId("..."),
    "patientId": ObjectId("..."),
    "sessionDate": ISODate("2024-01-15"),
    "durationMinutes": 90,
    
    // Complete transcription
    "transcript": {
        "fullText": "Doctor: How are you feeling? Patient: I'm anxious...",
        "segments": [
            {
                "speaker": "doctor",
                "text": "How are you feeling?",
                "startTime": 0,
                "endTime": 2.5,
                "confidence": 0.95
            }
        ]
    },
    
    // Dimensional trajectory over time
    "dimensionalTrajectory": [
        {
            "timestamp": 0,
            "dimensions": {
                "v1_valence": -2.3,
                "v2_arousal": 7.2,
                // ... all 15 dimensions
            },
            "speaker": "patient"
        }
    ],
    
    // Generated clinical documentation
    "clinicalNotes": {
        "soapNote": "Subjective: Patient reports anxiety...",
        "phenomenologicalNarrative": "The session reveals...",
        "treatmentRecommendations": [...]
    },
    
    // Metadata
    "processingMetadata": {
        "transcriptionModel": "azure-speech-v3.1",
        "medVersion": "v2.0",
        "processingTime": 125.6
    }
}
```

### PostgreSQL FHIR Schema

```sql
-- FHIR Patient resource
CREATE TABLE fhir_patients (
    id UUID PRIMARY KEY,
    resource JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- FHIR Observation resource (for dimensions)
CREATE TABLE fhir_observations (
    id UUID PRIMARY KEY,
    patient_id UUID REFERENCES fhir_patients(id),
    code VARCHAR(100) NOT NULL,  -- Dimension code
    value_quantity DECIMAL(10,2),
    effective_datetime TIMESTAMP,
    resource JSONB NOT NULL
);

-- Indexes for performance
CREATE INDEX idx_observations_patient_code 
ON fhir_observations(patient_id, code);

CREATE INDEX idx_observations_datetime 
ON fhir_observations(effective_datetime);
```

## 🧪 Testing Strategy

### Unit Tests

```python
import pytest
from voither.med import DimensionalExtractor

@pytest.fixture
def med_engine():
    return DimensionalExtractor({
        'azure_key': 'test-key',
        'azure_endpoint': 'test-endpoint'
    })

async def test_valence_extraction(med_engine):
    """Test emotional valence extraction"""
    
    # Test positive text
    result = await med_engine.extract_dimensions(
        "I feel really happy and excited about life!"
    )
    assert result['dimensions']['v1_valence'] > 2.0
    
    # Test negative text
    result = await med_engine.extract_dimensions(
        "I'm feeling depressed and hopeless"
    )
    assert result['dimensions']['v1_valence'] < -2.0

async def test_coherence_extraction(med_engine):
    """Test narrative coherence detection"""
    
    # Coherent text
    coherent_text = """
    I woke up this morning feeling anxious about my presentation.
    I prepared thoroughly yesterday, but I still worry about forgetting something.
    Despite my preparation, I think I'll do well because I know the material.
    """
    
    result = await med_engine.extract_dimensions(coherent_text)
    assert result['dimensions']['v3_coherence'] > 6.0
    
    # Incoherent text
    incoherent_text = """
    Morning anxiety presentation. Yesterday forgot material.
    Worry preparation... well material know think.
    """
    
    result = await med_engine.extract_dimensions(incoherent_text)
    assert result['dimensions']['v3_coherence'] < 4.0
```

### Integration Tests

```python
async def test_full_pipeline():
    """Test complete session processing pipeline"""
    
    # Mock audio file
    audio_file = create_test_audio("test_session.wav")
    
    # Process through complete pipeline
    pipeline = DimensionalPipeline(test_config)
    session_id = await pipeline.process_session(audio_file, "test-patient")
    
    # Verify MongoDB storage
    session = await mongodb.sessions.find_one({"_id": session_id})
    assert session is not None
    assert len(session['dimensionalTrajectory']) > 0
    
    # Verify FHIR storage
    observations = await postgres.query(
        "SELECT * FROM fhir_observations WHERE session_id = ?",
        session_id
    )
    assert len(observations) > 0
    
    # Verify blob storage
    audio_url = session['audioFileUrl']
    assert await blob_storage.exists(audio_url)
```

### Performance Tests

```python
import time
import asyncio

async def test_realtime_performance():
    """Ensure real-time processing meets latency requirements"""
    
    med_engine = DimensionalExtractor(config)
    
    # Test single extraction speed
    start_time = time.time()
    result = await med_engine.extract_dimensions(
        "This is a test sentence for performance measurement."
    )
    processing_time = time.time() - start_time
    
    # Must process under 500ms for real-time use
    assert processing_time < 0.5
    
    # Test concurrent processing
    texts = ["Test sentence {}".format(i) for i in range(10)]
    
    start_time = time.time()
    results = await asyncio.gather(*[
        med_engine.extract_dimensions(text) for text in texts
    ])
    concurrent_time = time.time() - start_time
    
    # Concurrent processing should be faster than sequential
    assert concurrent_time < (processing_time * 10)
```

## 🚀 Deployment Guide

### Docker Configuration

```dockerfile
# Dockerfile for VOITHER backend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download pt_core_news_lg

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Start application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Azure Deployment

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'

variables:
  azureSubscription: 'your-subscription'
  resourceGroup: 'voither-rg'
  webAppName: 'voither-api'

stages:
- stage: Build
  jobs:
  - job: BuildJob
    steps:
    - task: Docker@2
      inputs:
        containerRegistry: 'voither-acr'
        repository: 'voither/api'
        command: 'buildAndPush'
        Dockerfile: '**/Dockerfile'

- stage: Deploy
  jobs:
  - deployment: DeployJob
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureWebAppContainer@1
            inputs:
              azureSubscription: $(azureSubscription)
              appName: $(webAppName)
              containers: 'voither-acr.azurecr.io/voither/api:latest'
```

### Environment Configuration

```bash
# Production environment variables
AZURE_SPEECH_KEY=your-azure-speech-key
AZURE_SPEECH_REGION=brazilsouth
AZURE_AI_KEY=your-azure-ai-key
AZURE_AI_ENDPOINT=https://your-ai-endpoint.cognitiveservices.azure.com/

MONGODB_CONNECTION_STRING=mongodb+srv://username:password@cluster.mongodb.net/
POSTGRES_CONNECTION_STRING=postgresql://username:password@host:5432/database

AZURE_STORAGE_ACCOUNT=voitherstorage
AZURE_STORAGE_KEY=your-storage-key

REDIS_URL=redis://voither-redis.redis.cache.windows.net:6380
REDIS_PASSWORD=your-redis-password

# Application settings
NODE_ENV=production
LOG_LEVEL=info
MAX_SESSION_DURATION=7200  # 2 hours
MAX_CONCURRENT_SESSIONS=100
```

## 🔧 Development Tools

### VS Code Extensions
- **Python/Node.js** language support
- **Azure Tools** for Azure integration
- **Docker** for containerization
- **Thunder Client** for API testing
- **MongoDB** for database management

### Recommended Tools
- **Azure Data Studio** for PostgreSQL management
- **MongoDB Compass** for MongoDB exploration
- **Postman** for API testing
- **Azure Storage Explorer** for blob storage
- **Redis Insight** for Redis monitoring

## 📈 Monitoring & Logging

### Application Insights

```python
from applicationinsights import TelemetryClient

# Initialize telemetry
tc = TelemetryClient(os.environ['APPINSIGHTS_CONNECTION_STRING'])

# Track dimensional extraction performance
def track_med_extraction(text_length, processing_time, dimensions):
    tc.track_event('med_extraction', {
        'text_length': text_length,
        'processing_time': processing_time,
        'valence': dimensions['v1_valence'],
        'arousal': dimensions['v2_arousal']
    })

# Track errors
def track_error(error, context):
    tc.track_exception(error, properties=context)
```

### Health Checks

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint"""
    
    checks = {
        'api': 'healthy',
        'database': await check_database_connection(),
        'azure_ai': await check_azure_ai_services(),
        'storage': await check_blob_storage(),
        'redis': await check_redis_connection()
    }
    
    overall_status = 'healthy' if all(
        status == 'healthy' for status in checks.values()
    ) else 'unhealthy'
    
    return JSONResponse({
        'status': overall_status,
        'checks': checks,
        'timestamp': datetime.utcnow().isoformat()
    })
```

## 🔒 Security Best Practices

### Authentication & Authorization

```python
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication

# JWT-based authentication
SECRET = os.environ['JWT_SECRET']
jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600)

# Role-based access control
@app.get("/sessions/{session_id}")
async def get_session(
    session_id: str,
    user: User = Depends(get_current_user)
):
    # Verify user can access this session
    if not can_access_session(user, session_id):
        raise HTTPException(403, "Insufficient permissions")
    
    return await get_session_data(session_id)
```

### Data Protection

```python
from cryptography.fernet import Fernet

class DataEncryption:
    """Encrypt sensitive patient data"""
    
    def __init__(self):
        self.key = os.environ['ENCRYPTION_KEY'].encode()
        self.cipher = Fernet(self.key)
    
    def encrypt_transcript(self, transcript):
        """Encrypt transcript text"""
        return self.cipher.encrypt(transcript.encode())
    
    def decrypt_transcript(self, encrypted_transcript):
        """Decrypt transcript text"""
        return self.cipher.decrypt(encrypted_transcript).decode()
```

## 🤝 Contributing Guidelines

### Code Style

```python
# Use type hints
from typing import List, Dict, Optional

async def extract_dimensions(
    text: str,
    speaker: Optional[str] = None,
    context: Optional[Dict] = None
) -> Dict[str, float]:
    """Extract psychological dimensions from text.
    
    Args:
        text: Input text to analyze
        speaker: Speaker identifier (optional)
        context: Additional context (optional)
        
    Returns:
        Dictionary mapping dimension names to values
    """
    pass

# Use docstrings for documentation
# Follow PEP 8 style guidelines
# Use meaningful variable names
```

### Pull Request Process

1. **Create feature branch**: `git checkout -b feature/new-dimension`
2. **Write tests**: Ensure 90%+ code coverage
3. **Update documentation**: Include relevant docs updates
4. **Submit PR**: Use provided template
5. **Code review**: Address feedback promptly
6. **Merge**: Squash commits for clean history

### Testing Requirements

- **Unit tests**: 90%+ coverage required
- **Integration tests**: Critical paths covered
- **Performance tests**: Latency requirements met
- **Security tests**: Vulnerability scanning passed

---

## 📞 Developer Support

### Community
- **GitHub Discussions**: Technical questions and feature requests
- **Discord**: Real-time developer chat
- **Stack Overflow**: Tag questions with `voither`

### Resources
- **API Documentation**: Auto-generated from code
- **Architecture Diagrams**: Always kept up-to-date
- **Code Examples**: Comprehensive example repository
- **Video Tutorials**: Step-by-step implementation guides

*Ready to build the future of mental health AI? Let's code!* 🚀