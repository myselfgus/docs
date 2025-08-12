# VOITHER - AI-Powered Mental Health Analysis Platform

<div align="center">

<img src="assets/icon.png" alt="VOITHER Logo" width="200"/>

**Geometry of Mental Spaces Through Dimensional AI Analysis**

[![Documentation](https://img.shields.io/badge/docs-comprehensive-blue)](.)
[![Status](https://img.shields.io/badge/status-active%20development-green)](.)
[![Language](https://img.shields.io/badge/language-portuguese%20%2B%20english-orange)](.)

---

*Revolutionary AI system for real-time mental health analysis using 15-dimensional psychological space mapping and 3D visualization*

</div>

## 🧠 What is VOITHER?

VOITHER is a cutting-edge AI platform that transforms mental health practice through:

- **Real-time transcription** of therapeutic sessions with speaker diarization
- **15-dimensional analysis** of psychological states using advanced NLP
- **3D visualization** of mental spaces through the Holofractor Mental Renderer
- **Automated clinical documentation** with intelligent trigger detection
- **Interoperable FHIR integration** for seamless EHR connectivity

## 🎯 Repository Scope & Purpose

**This repository focuses on:**
- 📚 **Documentation & Knowledge Organization**: Systematizing all knowledge that originated and forms VOITHER
- 📖 **Content Organization**: Structuring and organizing conceptual content
- 🗂️ **Documentation Workflows**: How this repository works and documentation processes
- 🧭 **Navigation & Discovery**: Helping users find and understand VOITHER concepts

**For actual construction/implementation**, see:
- 🏗️ **[VOITHER Architecture Specifications](voither_architecture_specs/)**: Real construction blueprints for building VOITHER components
- 🔧 **Construction Repositories**: Separate repositories for each VOITHER component implementation

## 🚀 Quick Start

### 📖 **Start Here - Unified Manual**
- **🎯 Technical Compendium**: [Complete System Manual](docs/VOITHER_TECHNICAL_COMPENDIUM.md) - **NEW: Unified integration of all content**
- **📋 How Automations Work**: [Automation Status & Monitoring](docs/AUTOMATION_STATUS.md) - **NEW: Complete automation overview**

### For Clinicians
- **Getting Started**: [Clinical Quick Start Guide](guides/clinician-quickstart.md)
- **Core Concepts**: [Understanding the 15 Dimensions](core-concepts/15-dimensions.md)
- **System Architecture**: [How VOITHER Works](architecture/voither_system_architecture.md)

### For Developers
- **Technical Overview**: [System Architecture](architecture/voither_system_architecture.md)
- **Implementation Guide**: [Development Setup](guides/developer-guide.md)
- **🏗️ Construction Specs**: [VOITHER Architecture Specifications](voither_architecture_specs/) ⭐ **NEW: Real implementation blueprints**
- **API Documentation**: [Technical Pipeline](architecture/voither_technical_pipeline.md)

### For Researchers
- **Research Background**: [Dimensional Psychology](research/geometria_afetos_cognicao.md)
- **Knowledge Graph**: [Complete System Overview](docs/VOITHER_Knowledge_Graph_Updated.md)
- **Academic Papers**: [Publications](research/)

## 📚 Documentation Structure

### 📁 **Repository Organization**
```
docs/
├── 📁 architecture/         # System design & technical architecture (CONCEPTUAL)
├── 📁 assets/              # Media files, icons, videos
├── 📁 core-concepts/       # Core AI concepts & frameworks
├── 📁 database/            # Database design & ideas  
├── 📁 docs/                # Main documentation files
│   ├── 📁 architecture/    # Advanced architecture blueprints (CONCEPTUAL)
│   ├── 📁 core-concepts/   # Enhanced core concepts
│   ├── 📁 database/        # Database implementation details
│   ├── 📁 dsl/            # Domain-specific language files
│   ├── 📁 pipelines/      # Data processing pipelines
│   ├── 📁 reengine/       # ReEngine framework sections
│   ├── 📁 visualflows_charts/ # 📊 Complete visual workflows - DOCUMENTATION FOCUS
│   └── 📁 voither-system/ # VOITHER system components (CONCEPTUAL)
├── 📁 guides/              # User guides & tutorials
├── 📁 raw/                 # Unprocessed backup archive
├── 📁 research/            # Academic papers & research
├── 📁 scripts/             # 🤖 Documentation automation scripts
├── 📁 templates/           # Clinical templates & forms
├── 📁 workflows/           # 🔄 Documentation workflow diagrams
└── 📁 voither_architecture_specs/ # 🏗️ **REAL CONSTRUCTION SPECS** (NEW)
    ├── 📁 medicalscribe/    # Medical Scribe implementation specs
    ├── 📁 autoagency/       # Auto-Agency system specs
    ├── 📁 apothecary/       # Apothecary component specs
    ├── 📁 peer_ai/          # Peer-AI specifications
    ├── 📁 holofractor/      # Holofractor renderer specs
    ├── 📁 brre_engine/      # BRRE engine specifications
    ├── 📁 a2a_orchestration/ # A2A coordination specs
    ├── 📁 enterprise_integration/ # GitHub Enterprise specs
    └── 📁 clinical_workflows/ # Real clinical implementation
```

### 🏗️ **Architecture & System Design**
| Document | Description | Audience | Type |
|----------|-------------|----------|------|
| [System Architecture](architecture/voither_system_architecture.md) | Complete technical architecture overview | Developers, Architects | CONCEPTUAL |
| [🏗️ Architecture Specifications](voither_architecture_specs/) | **NEW**: Real construction blueprints for all VOITHER components | Implementers, Engineers | CONSTRUCTION |
| [Implementation Plan](docs/voither-system/voither_implementation_plan.md) | Development roadmap and milestones | Project Managers, Developers | CONCEPTUAL |
| [Technical Pipeline](architecture/voither_technical_pipeline.md) | Data flow and processing pipeline | Technical Teams | CONCEPTUAL |

### 📊 **Visual Workflows & Charts - Documentation Focus**
| Chart | Focus Area | Description | Type |
|-------|------------|-------------|------|
| [Visual Flows Index](docs/visualflows_charts/README.md) | Complete visual documentation suite | All audiences | DOCUMENTATION |
| [System Architecture Chart](docs/visualflows_charts/01_voither_system_architecture.md) | Core foundation & .ee DSL integration | Technical Leadership | DOCUMENTATION |
| [Clinical Workflow Pipeline](docs/visualflows_charts/02_clinical_workflow_pipeline.md) | Healthcare processes & AI integration | Clinical Teams | DOCUMENTATION |
| [Development Lifecycle](docs/visualflows_charts/03_development_lifecycle.md) | DevOps, CI/CD, quality assurance | Development Teams | DOCUMENTATION |
| [AI Model Integration](docs/visualflows_charts/04_ai_model_integration.md) | ML pipeline & inference architecture | AI/ML Engineers | DOCUMENTATION |
| [Data Architecture](docs/visualflows_charts/05_data_architecture.md) | Knowledge graphs & data flow | Data Engineers | DOCUMENTATION |
| [Security & Compliance](docs/visualflows_charts/06_security_compliance.md) | Zero-trust security & regulatory compliance | Security Teams | DOCUMENTATION |
| [Deployment Infrastructure](docs/visualflows_charts/07_deployment_infrastructure.md) | Cloud-native deployment & scalability | Infrastructure Teams | DOCUMENTATION |

> **Note**: These visual flows explain VOITHER concepts and documentation organization. For construction-ready specifications, see [Architecture Specifications](voither_architecture_specs/).

### 🧩 **Core Components**
| Component | Description | Status |
|-----------|-------------|--------|
| [MED Core](core-concepts/med_core.md) | Motor de Extração Dimensional (15 dimensions) | ✅ Implemented |
| [Apothecary Engine](core-concepts/apothecary_engine.md) | Automated medication analysis | 🔄 Development |
| [AutoAgency](core-concepts/autoagency.md) | Clinical automation system | 📋 Planned |
| [Holofractor](voither-system/voither_dimensional_holofractor.md) | 3D mental space visualization | 🔄 Development |

### 🔧 **Technical Implementation**
| Document | Focus Area | Complexity | Type |
|----------|------------|------------|------|
| [MED Implementation](docs/voither-system/voither_med_implementation.md) | Dimensional extraction engine | Advanced | CONCEPTUAL |
| [Framework Integration](docs/core-concepts/med_frameworks.md) | RDoC, HiTOP, Big Five integration | Intermediate | CONCEPTUAL |
| [FHIR Integration](docs/voither-system/voither_orchestrator_doc.md) | Healthcare interoperability | Advanced | CONCEPTUAL |
| [🏗️ Architecture Specifications](voither_architecture_specs/) | Real construction blueprints | Advanced | CONSTRUCTION |

### 📚 **Documentation & Organization Systems**
| Document | Description | Status | Type |
|----------|-------------|--------|------|
| [Automation Pipeline](docs/AUTOMATION_PIPELINE.md) | Documentation automation overview | ✅ Active | DOCUMENTATION |
| [Automation Status Monitor](docs/AUTOMATION_STATUS.md) | Documentation validation monitoring | ✅ Active | DOCUMENTATION |
| [Technical Compendium](docs/VOITHER_TECHNICAL_COMPENDIUM.md) | **Unified manual**: Complete content integration | ✅ Comprehensive | DOCUMENTATION |
| [🏗️ Architecture Specifications](voither_architecture_specs/) | Real implementation specifications | 📋 Available | CONSTRUCTION |

### 🔬 **Research & Theory**
| Document | Topic | Type |
|----------|--------|------|
| [Mental Space Geometry](research/geometria_afetos_cognicao.md) | Theoretical foundation | Research Paper |
| [Emergence Enabled Systems](core-concepts/emergence_enabled_ee.md) | AI-native architecture | Technical Spec |
| [ReEngine Framework](reengine/ReEngine_Sec_01.md) | Bergsonian-Rhizomatic reasoning | Philosophical-Technical |

## 🌟 Key Features - Documentation Repository

### 📚 **Documentation Organization & Content Management**
- **Unified Knowledge Systematization**: Complete organization of all VOITHER conceptual content
- **Multi-Audience Navigation**: Structured access for clinicians, developers, and researchers  
- **Version-Controlled Documentation**: Git-based documentation lifecycle management
- **Content Validation Systems**: Automated verification of documentation integrity

### 🏗️ **Architecture Specifications (Separated)**
- **Real Construction Blueprints**: Detailed specifications for actual VOITHER implementation
- **Component-Based Organization**: Separated specs for each VOITHER system component
- **Implementation-Ready Documentation**: Technical specifications designed for construction teams
- **Construction-Documentation Bridge**: Clear separation between conceptual and implementation content
- **Composable Architecture**: Sequential, parallel, and hierarchical agent composition patterns

### 🎯 **Real-Time Analysis**
- Live transcription with Azure Speech Services / Google Cloud Speech-to-Text
- Instant dimensional analysis during sessions
- Real-time 3D visualization of mental states
- WebSocket-based streaming architecture

### 📊 **15-Dimensional Framework**
VOITHER analyzes mental states across 15 validated dimensions:

1. **Valência Emocional** - Emotional polarity (-5 to +5)
2. **Arousal/Ativação** - Energy level (0 to 10)
3. **Coerência Narrativa** - Logical organization (0 to 10)
4. **Complexidade Sintática** - Thought elaboration (0 to 10)
5. **Orientação Temporal** - Past/present/future focus
6. **Densidade Autoreferência** - Self-reference frequency
7. **Linguagem Social** - Social interaction references
8. **Flexibilidade Discursiva** - Perspective adaptability
9. **Dominância/Agência** - Sense of control
10. **Fragmentação do Discurso** - Speech disorganization
11. **Densidade Semântica** - Meaningful content richness
12. **Marcadores Certeza/Incerteza** - Confidence vs doubt
13. **Padrões de Conectividade** - Logical connector usage
14. **Comunicação Pragmática** - Social communication adequacy
15. **Prosódia Emocional** - Speech melody and rhythm

### 🏥 **Clinical Integration**
- Automated SOAP/DAP note generation
- FHIR-compliant data structures
- Integration with existing EHR systems
- Prescription and scheduling automation

## 🗺️ **System Versions & Roadmap**

| Version | Focus | Status | Key Features |
|---------|--------|---------|---------------|
| **v0.1** | [Geometry Visualization](voither-system/voither_implementation_plan.md#v01) | ✅ Complete | Three.js 3D rendering, simulated data |
| **v1.0** | [Medical Scribe](voither-system/voither_implementation_plan.md#v10) | 🔄 Development | Real-time transcription, dimensional analysis |
| **v1.5** | [AutoAgency](voither-system/voither_implementation_plan.md#v15) | 📋 Planned | Clinical automation, trigger detection |
| **v2.0** | [AI-Clinic](voither-system/voither_implementation_plan.md#v20) | 📋 Planned | Patient portal, continuous care |
| **v3.0** | [Holofractor Premium](voither-system/voither_implementation_plan.md#v30) | 🔮 Future | NVIDIA Omniverse integration |

## 🛠️ **Technology Stack - Conceptual Overview**

### **Core Technologies (Conceptual)**
- **Unified .ee DSL**: AI-native programming language for healthcare
- **BRRE Engine**: Bergsonian-Rhizomatic Reasoning for clinical intelligence
- **Emergenability Framework**: Detection and facilitation of therapeutic emergence

### **Frontend Technologies**
- React/Next.js with TypeScript
- Three.js for 3D visualization
- Real-time communication protocols

### **Backend Architecture**
- Cloud-native microservices
- Dimensional data storage
- FHIR-compliant data handling
- Secure audio processing

### **AI & Analytics**
- Multi-modal AI integration
- Custom dimensional extraction models
- Clinical decision support systems

### **Healthcare Standards**
- FHIR R4 compliance
- HIPAA security standards
- EU AI Act compliance

> **For Implementation Details**: See [Architecture Specifications](voither_architecture_specs/) for construction-ready technical specifications.

## 🏗️ **Architecture Overview - Documentation Focus**

```mermaid
graph TD
    subgraph "Documentation Repository Scope"
        DR[📚 Documentation Repository]
        DO[🗂️ Documentation Organization]
        KS[🧭 Knowledge Systematization]
        CF[🔄 Content Flows]
    end
    
    subgraph "VOITHER Conceptual Architecture"
        CI[Clinician Interface]
        DA[Dimensional Analysis]
        HL[Holofractor Layer]
        CD[Clinical Documentation]
        FS[FHIR Storage]
    end
    
    subgraph "Construction Specifications"
        AS[🏗️ Architecture Specs]
        MS[Medical Scribe Specs]
        HF[Holofractor Specs]
        BE[BRRE Engine Specs]
        A2A[A2A Orchestration Specs]
    end
    
    DR --> DO
    DO --> KS
    KS --> CF
    
    CI --> DA
    DA --> HL
    HL --> CD
    CD --> FS
    
    AS --> MS
    AS --> HF
    AS --> BE
    AS --> A2A
    
    CF -.-> AS
    
    style DR fill:#e8f5e8,stroke:#2e7d32,stroke-width:3px
    style AS fill:#fff3e0,stroke:#ef6c00,stroke-width:3px
    style CI fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
```

**Architecture Layers**:
- **📚 Green**: Documentation & knowledge organization (this repository's primary focus)
- **🟠 Orange**: Construction specifications (for implementation repositories)  
- **🔵 Blue**: VOITHER conceptual system (documented here, implemented elsewhere)
    AO --> AM
    
    AO --> B[Real-time Transcription]
    B --> C[Dimensional Analysis Engine]
    C --> D[3D Visualization]
    C --> E[Clinical Documentation]
    E --> F[FHIR Integration]
    F --> G[EHR Systems]
    
    subgraph "Data Storage"
        H[MongoDB Atlas]
        I[Azure PostgreSQL / Google Cloud SQL]
        J[Azure Blob Storage / Google Cloud Storage]
    end
    
    subgraph "Enterprise Infrastructure (NEW)"
        K[GitHub Enterprise Organizations]
        L[Automation Pipeline]
        M[Quality Monitoring]
    end
    
    C --> H
    F --> I
    B --> J
    AO --> K
    AO --> L
    L --> M
```

## 🤝 **Contributing**

We welcome contributions! Please see our [Contribution Guidelines](docs/CONTRIBUTING.md) for:
- Code standards and practices
- Documentation guidelines
- Pull request procedures
- Issue reporting

### **Documentation Maintenance**
Use our built-in tools for maintaining documentation quality:

```bash
# Quick validation
make validate-quick

# Full link checking
make validate

# Statistics
make stats

# Spell checking (if tools installed)
make spell-check
```

### **Development Setup**
```bash
# Install documentation tools
make dev-setup

# Install Git hooks for automatic validation
make install-hooks

# Validate documentation structure
python scripts/validate-docs.py

# Run content verification
python scripts/ai-content-verifier.py
```

> **For Implementation Setup**: See [Architecture Specifications](voither_architecture_specs/) for construction-ready setup instructions.

## 📄 **License & Compliance**

- **Healthcare Compliance**: HIPAA, GDPR, LGPD compliant
- **Medical Device**: IEC 62304 Class B certification planned
- **AI Regulation**: EU AI Act compliance
- **Interoperability**: FHIR R4 standard implementation

## 🆘 **Support & Resources**

### **Documentation Index**
- 📖 [Complete Knowledge Graph](docs/VOITHER_Knowledge_Graph_Updated.md)
- 🎯 [Technical Compendium - Unified Manual](docs/VOITHER_TECHNICAL_COMPENDIUM.md) ⭐ **Documentation Focus**
- 📊 [Visual Workflows Charts](docs/visualflows_charts/README.md) ⭐ **Documentation Focus**
- 🏗️ [Architecture Specifications](voither_architecture_specs/) ⭐ **Construction Focus**
- 🔄 [Automation Pipeline Status](docs/AUTOMATION_STATUS.md) ⭐ **Documentation Focus**
- 🎯 [Implementation Templates](templates/voither_primeira_consulta_template.py)
- 🔗 [Pipeline Documentation](docs/voither-system/VOITHER_files_pipeline.md)

### **Quick Links**
- [System Requirements](guides/system-requirements.md)
- [Installation Guide](guides/installation.md)
- [🏗️ Architecture Specifications](voither_architecture_specs/) ⭐ **For Implementation Teams**
- [Troubleshooting](guides/troubleshooting.md)
- [FAQ](guides/faq.md)

### **Community**
- Issues: [GitHub Issues](https://github.com/myselfgus/docs/issues)
- Discussions: [GitHub Discussions](https://github.com/myselfgus/docs/discussions)

### **Documentation Tools**
- **Validation**: `make validate` - Check links and structure
- **Statistics**: `make stats` - Documentation metrics
- **Local Server**: `make serve` - Preview documentation locally
- **Help**: `make help` - See all available commands

---

<div align="center">

**Made with ❤️ for advancing mental health through AI**

*Transforming psychological care through computational intelligence*

[🚀 Get Started](#-quick-start) • [📚 Documentation](#-documentation-structure) • [🤝 Contribute](#-contributing)

</div>