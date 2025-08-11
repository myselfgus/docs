---
title: "Frequently Asked Questions"
description: "Common questions and answers about VOITHER system"
version: "1.0"
last_updated: "2025-01-19"
audience: ["all"]
priority: "medium"
reading_time: "10 minutes"
tags: ["faq", "support", "questions"]
---

# Frequently Asked Questions (FAQ)

## General Questions

### What is VOITHER?
VOITHER is an AI-powered system for dimensional analysis of mental health consultations. It transcribes medical consultations in real-time and provides 15-dimensional analysis of patient mental states, automated clinical documentation, and 3D visualization of mental space.

### Who can use VOITHER?
- **Mental health professionals**: Psychiatrists, psychologists, therapists
- **Healthcare institutions**: Hospitals, clinics, private practices
- **Researchers**: Academic institutions studying mental health
- **Developers**: Technical teams implementing the system

### Is VOITHER HIPAA compliant?
Yes, VOITHER is designed with HIPAA compliance in mind, including:
- End-to-end encryption
- Access controls and audit logging
- Data minimization principles
- Secure cloud infrastructure (Azure)

## Technical Questions

### What languages does VOITHER support?
Currently, VOITHER primarily supports:
- **Portuguese** (primary language)
- **English** (secondary support)
- Additional languages planned for future releases

### What audio formats are supported?
VOITHER supports:
- **Live microphone input** via WebRTC
- **WAV files** (16kHz, mono preferred)
- **MP3 files** (converted automatically)
- **Real-time streaming** from devices

### What are the minimum system requirements?
See our [System Requirements](system-requirements.md) for detailed specifications:
- 8GB RAM minimum
- Modern web browser with WebRTC support
- Stable internet connection
- Azure service subscriptions

### Can VOITHER work offline?
No, VOITHER requires internet connectivity for:
- Azure Speech Services for transcription
- AI services for dimensional analysis
- Cloud database storage
- Real-time collaboration features

## Clinical Questions

### How accurate is the transcription?
Transcription accuracy depends on:
- **Audio quality**: 95%+ with good audio
- **Language clarity**: Affected by accents, speech patterns
- **Background noise**: Reduced accuracy with noise
- **Technical setup**: Proper microphone configuration improves results

### What are the 15 dimensions?
The 15 dimensions analyze:
1. Emotional valence
2. Arousal/activation
3. Narrative coherence
4. Syntactic complexity
5. Temporal orientation
6. Self-reference density
7. Social language
8. Discursive flexibility
9. Dominance/agency
10. Discourse fragmentation
11. Semantic density
12. Certainty/uncertainty markers
13. Connectivity patterns
14. Pragmatic communication
15. Emotional prosody

See [15 Dimensions](../core-concepts/15-dimensions.md) for detailed explanations.

### How should I interpret dimensional scores?
- **Scores are relative**: Compare to patient's baseline
- **Trends matter more**: Look for patterns over time
- **Clinical context is key**: Combine with professional judgment
- **Not diagnostic**: Dimensions support, don't replace clinical assessment

### Can VOITHER diagnose mental health conditions?
**No.** VOITHER is a **support tool** that:
- Provides dimensional analysis
- Identifies patterns and trends
- Generates documentation
- **Does not replace clinical judgment**
- **Does not provide diagnoses**

## Privacy & Security

### How is patient data protected?
- **Encryption**: All data encrypted in transit and at rest
- **Access controls**: Role-based permissions
- **Audit logging**: Complete activity tracking
- **Data minimization**: Only necessary data collected
- **Geographic controls**: Data stays in specified regions

### Who has access to the data?
Access is strictly controlled:
- **Treating clinician**: Full access to their patients
- **Authorized staff**: Role-based limited access
- **System administrators**: Technical access only, no clinical data
- **Patients**: Can access their own data (where legally permitted)

### How long is data retained?
Data retention follows healthcare regulations:
- **Clinical records**: As per local healthcare laws
- **Audio files**: Configurable retention period
- **System logs**: 90 days by default
- **Backups**: Follow organizational policies

### Can data be exported?
Yes, data can be exported in standard formats:
- **FHIR R4** for interoperability
- **PDF** for clinical reports
- **JSON** for technical integration
- **CSV** for analysis

## Implementation Questions

### How long does implementation take?
Implementation timeline varies:
- **Pilot deployment**: 2-4 weeks
- **Full deployment**: 1-3 months
- **Staff training**: 2-4 weeks
- **Integration**: Depends on existing systems

### What training is required?
Training needs by role:
- **Clinicians**: 4-6 hours (system use, interpretation)
- **IT staff**: 1-2 days (technical setup, maintenance)
- **Administrators**: 2-4 hours (user management, reporting)

### Can VOITHER integrate with existing EHR systems?
Yes, through:
- **FHIR R4** standard integration
- **API endpoints** for custom integration
- **Data export/import** capabilities
- **Custom connectors** (development required)

### What's the cost structure?
Contact sales for pricing information. Factors include:
- Number of concurrent users
- Azure service usage
- Storage requirements
- Support level needed

## Troubleshooting

### The transcription isn't working. What should I do?
Check common issues:
1. **Microphone permissions** in browser
2. **Internet connectivity** stability
3. **Azure service status** 
4. **Browser compatibility** (Chrome/Edge recommended)

See [Troubleshooting Guide](troubleshooting.md) for detailed solutions.

### The analysis seems incorrect. Why?
Possible causes:
- **Poor audio quality** affecting transcription
- **Background noise** or interruptions
- **Non-standard speech patterns** 
- **Language mixing** (multiple languages)
- **Technical issues** with AI services

### How do I interpret unusual dimensional scores?
- **Very high/low scores**: May indicate technical issues or extreme states
- **Inconsistent patterns**: Check audio quality and context
- **Sudden changes**: Consider external factors or session events
- **Contact support**: For persistent interpretation issues

## Feature Questions

### Can I customize the dimensional analysis?
Currently limited customization:
- **Thresholds**: Can be adjusted
- **Reporting format**: Multiple options available
- **Custom rules**: Available for enterprise customers
- **Future releases**: More customization planned

### Is real-time visualization available?
Yes, VOITHER includes:
- **3D Holofractor**: Real-time mental space visualization
- **Live dimensional tracking**: During consultation
- **Interactive exploration**: Post-session analysis
- **Export capabilities**: For presentations

### Can multiple people use the system simultaneously?
Yes, VOITHER supports:
- **Concurrent sessions**: Multiple clinicians
- **Shared access**: Team collaboration
- **Role-based permissions**: Different access levels
- **Audit trails**: Track all activities

## Support

### How do I get help?
Support resources:
1. **Documentation**: Comprehensive guides available
2. **Troubleshooting**: Step-by-step problem solving
3. **Community**: User forums and discussions
4. **Technical support**: Professional assistance available

### What if I find a bug?
Report bugs through:
1. **Bug report form**: Detailed issue submission
2. **Support ticket**: Direct technical assistance
3. **Documentation**: Include steps to reproduce
4. **Logs**: Provide relevant error messages

### How often is VOITHER updated?
Update schedule:
- **Security patches**: As needed
- **Bug fixes**: Monthly
- **Feature updates**: Quarterly
- **Major releases**: Annually

### Is training available?
Yes, training options include:
- **Online documentation**: Self-paced learning
- **Video tutorials**: Step-by-step guides
- **Live training sessions**: Interactive workshops
- **Certification programs**: Professional credentials

## Getting Started

### What's the quickest way to try VOITHER?
1. Review [System Requirements](system-requirements.md)
2. Follow [Installation Guide](installation.md)
3. Complete [Clinician Quick Start](clinician-quickstart.md)
4. Try with test audio files
5. Contact support for assistance

### Where can I learn more?
Additional resources:
- **[Knowledge Graph](../docs/VOITHER_Knowledge_Graph_Updated.md)**: Complete system overview
- **[System Architecture](../architecture/voither_system_architecture.md)**: Technical details
- **[Developer Guide](developer-guide.md)**: Implementation guidance
- **[Research Papers](../research/)**: Scientific foundations