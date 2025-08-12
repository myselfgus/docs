---
title: "Getting Started with VOITHER - Overview"
description: "Quick orientation guide to help you navigate VOITHER documentation and choose the right path"
version: "1.0"
last_updated: "2024-01-15"
audience: ["all"]
priority: "essential"
reading_time: "10 minutes"
tags: ["getting_started", "overview", "navigation", "beginner"]
---

# Getting Started with VOITHER

*Your guide to navigating the future of AI-powered mental health analysis*

## 🎯 What Brings You Here?

Choose your path based on your role and immediate needs:

### 👩‍⚕️ **I'm a Clinician**
*"I want to understand how VOITHER can improve my practice"*

**Start Here:** [Clinician Quick Start](../guides/clinician-quickstart.md) (30 min)
- Learn the 15-dimensional analysis framework
- See real clinical applications
- Understand the AI co-pilot approach
- Get hands-on with the first session

**Then Explore:**
- [System Overview](VOITHER_Knowledge_Graph_Updated.md) - Complete picture
- [15 Dimensions Deep Dive](../core-concepts/med_core.md) - Understanding the science
- [Clinical Templates](guides/research/voither_primeira_consulta_template.py) - Practical examples

### 👨‍💻 **I'm a Developer**
*"I need to implement, integrate, or extend VOITHER"*

**Start Here:** [Developer Guide](../guides/developer-guide.md) (45 min)
- Complete implementation walkthrough
- Code examples and patterns
- Testing and deployment strategies
- API references and integrations

**Then Explore:**
- [System Architecture](../architecture/voither_system_architecture.md) - Technical foundation
- [MED Engine Implementation](docs/voither-system/voither_med_implementation.md) - Core AI system
- [Technical Pipeline](../architecture/voither_technical_pipeline.md) - Data flow details

### 🔬 **I'm a Researcher**
*"I want to understand the science and methodology behind VOITHER"*

**Start Here:** [Knowledge Graph](VOITHER_Knowledge_Graph_Updated.md) (15 min)
- Complete system overview
- Research foundations
- Validation frameworks
- Academic applications

**Then Explore:**
- [Mental Geometry](guides/research/geometria_afetos_cognicao.md) - Theoretical foundation
- [Framework Integration](../core-concepts/med_frameworks.md) - RDoC, HiTOP, Big Five
- [ReEngine Framework](docs/reengine/ReEngine_Sec_01.md) - Advanced AI reasoning

### 🏗️ **I'm a System Architect**
*"I need to plan infrastructure and integration strategy"*

**Start Here:** [System Architecture](../architecture/voither_system_architecture.md) (30 min)
- Complete technical architecture
- Hybrid data storage approach
- Scalability and security design
- Azure integration patterns

**Then Explore:**
- [Files Pipeline](docs/voither-system/VOITHER_files_pipeline.md) - Data architecture
- [Orchestrator](docs/voither-system/voither_orchestrator_doc.md) - System coordination
- [Database Design](docs/database/DB_ideas.md) - Storage strategy

### 📊 **I'm a Project Manager**
*"I need to understand scope, timeline, and resource requirements"*

**Start Here:** [README](../README.md) + [Implementation Plan](docs/voither-system/voither_implementation_plan.md) (30 min)
- Project vision and scope
- Development roadmap
- Resource requirements
- Risk assessment

**Then Explore:**
- [Documentation Index](DOCUMENTATION_INDEX.md) - Complete scope
- [Knowledge Graph](VOITHER_Knowledge_Graph_Updated.md) - System complexity
- [Developer Guide](../guides/developer-guide.md) - Technical requirements

## 🚀 Quick Start Paths

### ⚡ **5-Minute Overview**
Just need the basics?
1. [README](../README.md) - Project overview
2. [Knowledge Graph Summary](VOITHER_Knowledge_Graph_Updated.md#entidades-principais) - Key components

### 📚 **30-Minute Deep Dive**
Ready to understand the full system?
1. [README](../README.md) (10 min)
2. [Knowledge Graph](VOITHER_Knowledge_Graph_Updated.md) (15 min)
3. [System Architecture Overview](../architecture/voither_system_architecture.md#1-princípios-fundamentais-da-arquitetura-voither) (5 min)

### 🎓 **2-Hour Comprehensive Study**
Want to become a VOITHER expert?
1. Complete 30-minute path above
2. Your role-specific deep dive documentation
3. Hands-on exploration with relevant templates/examples

## 🧠 Core Concepts You Should Know

### **The 15 Dimensions**
VOITHER analyzes mental states across 15 validated psychological dimensions:
- **Emotional** (Valence, Arousal)
- **Cognitive** (Coherence, Complexity, Semantic Density)
- **Social** (Social Language, Pragmatic Communication)
- **Temporal** (Past/Present/Future orientation)
- **Self-Perception** (Self-reference, Agency)
- **Organization** (Flexibility, Fragmentation, Connectivity)
- **Expression** (Certainty, Prosody)

### **Real-Time Processing**
- Live transcription with speaker identification
- Instant dimensional analysis during sessions
- 3D visualization of mental state evolution
- Automated clinical documentation

### **Hybrid Architecture**
- **MongoDB**: Rich, unstructured insights and trajectories
- **PostgreSQL**: Structured FHIR-compliant clinical data
- **Azure**: Scalable cloud infrastructure with AI services
- **Real-time**: WebSocket streaming for live processing

### **AI Co-Pilot Approach**
VOITHER enhances rather than replaces clinical judgment:
- Objective measurements complement subjective assessment
- Automated tasks free time for patient interaction
- Pattern recognition reveals insights human eyes might miss
- Final decisions always remain with the clinician

## 🗺️ Understanding the Ecosystem

### **Version Roadmap**
| Version | Status | Focus | Key Features |
|---------|---------|--------|---------------|
| **v0.1** | ✅ Complete | 3D Visualization | Three.js rendering, simulated data |
| **v1.0** | 🔄 Development | Medical Scribe | Real-time transcription, dimensional analysis |
| **v1.5** | 📋 Planned | AutoAgency | Clinical automation, trigger detection |
| **v2.0** | 📋 Planned | AI-Clinic | Patient portal, continuous care |
| **v3.0** | 🔮 Future | Holofractor Premium | NVIDIA Omniverse integration |

### **Key Components**
- **MED Engine**: 15-dimensional extraction from speech/text
- **Holofractor**: 3D mental space visualization
- **AutoAgency**: Automated clinical tasks and documentation
- **AI-Clinic**: Patient engagement and continuous care
- **FHIR Integration**: Healthcare interoperability

## 🎯 Success Metrics

After exploring VOITHER documentation, you should be able to:

### **For Clinicians**
- [ ] Explain how VOITHER enhances clinical practice
- [ ] Understand the 15-dimensional analysis framework
- [ ] Navigate the user interface confidently
- [ ] Interpret dimensional scores and visualizations

### **For Developers**
- [ ] Set up a development environment
- [ ] Understand the system architecture
- [ ] Implement basic integrations
- [ ] Extend the MED engine capabilities

### **For Researchers**
- [ ] Understand the theoretical foundations
- [ ] Evaluate the validation frameworks
- [ ] Design research applications
- [ ] Contribute to the academic literature

### **For Architects**
- [ ] Design integration strategies
- [ ] Plan infrastructure requirements
- [ ] Ensure security and compliance
- [ ] Scale the system appropriately

## 🆘 When You Get Stuck

### **Common Questions**
- **"Where do I start coding?"** → [Developer Guide](../guides/developer-guide.md)
- **"How does the AI work?"** → [MED Core](../core-concepts/med_core.md)
- **"What about data privacy?"** → [System Architecture - Security](../architecture/voither_system_architecture.md#13-segurança-e-conformidade-por-design)
- **"Can this integrate with our EHR?"** → [FHIR Integration](docs/voither-system/voither_orchestrator_doc.md)

### **Finding Specific Information**
- **Complete document list**: [Documentation Index](DOCUMENTATION_INDEX.md)
- **Navigation guide**: [Table of Contents](TABLE_OF_CONTENTS.md)
- **Technical specifications**: [System Architecture](../architecture/voither_system_architecture.md)
- **Research foundations**: [Knowledge Graph](VOITHER_Knowledge_Graph_Updated.md)

### **Getting Help**
- **Documentation issues**: Create GitHub issue
- **Technical questions**: Check [Developer Guide](../guides/developer-guide.md)
- **Clinical questions**: See [Clinician Quick Start](../guides/clinician-quickstart.md)
- **General discussion**: GitHub Discussions

## 🌟 Ready to Begin?

Choose your adventure:

| Time Available | Recommended Path |
|----------------|------------------|
| **5 minutes** | [README](../README.md) → Quick overview |
| **30 minutes** | [Your role-specific quick start](#what-brings-you-here) |
| **2+ hours** | [Comprehensive study path](#2-hour-comprehensive-study) |
| **I'm lost** | [Table of Contents](TABLE_OF_CONTENTS.md) → Find your way |

---

*Welcome to the future of mental health AI. Let's build something amazing together.* 🚀