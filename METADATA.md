# VOITHER Documentation Metadata

*Machine-readable metadata for all documentation files*

## Document Classification

```yaml
documentation_structure:
  version: "2.0"
  last_updated: "2024-01-15"
  total_documents: 29
  total_lines: 23845
  
  categories:
    getting_started:
      priority: high
      audience: ["all"]
      documents:
        - README.md
        - TABLE_OF_CONTENTS.md
        - DOCUMENTATION_INDEX.md
        
    user_guides:
      priority: high
      audience: ["clinicians", "developers", "administrators"]
      documents:
        - guides/clinician-quickstart.md
        - guides/developer-guide.md
        
    core_architecture:
      priority: essential
      audience: ["developers", "architects"]
      documents:
        - voither_system_architecture.md
        - voither_implementation_plan.md
        - voither_technical_pipeline.md
        - VOITHER_files_pipeline.md
        
    core_intelligence:
      priority: essential
      audience: ["developers", "researchers", "clinicians"]
      documents:
        - VOITHER_Knowledge_Graph_Updated.md
        - med_core.md
        - voither_med_implementation.md
        - med_frameworks.md
        
    ai_automation:
      priority: important
      audience: ["developers", "architects"]
      status: mixed
      documents:
        - autoagency.md
        - apothecary_engine.md
        - voither_orchestrator_doc.md
        - voither_narrative_agent.md
        
    visualization:
      priority: medium
      audience: ["developers", "ux_designers"]
      documents:
        - voither_dimensional_holofractor.md
        - voither_navigate.md
        - VOITHER_for_Narrative.md
        
    research_theory:
      priority: medium
      audience: ["researchers", "academics"]
      documents:
        - geometria_afetos_cognicao.md
        - espaco_mental_paper.md
        - emergence_enabled_ee.md
        
    technical_infrastructure:
      priority: advanced
      audience: ["architects", "DevOps"]
      documents:
        - iser_pipelines.md
        - DB_ideas.md
        
    reengine_framework:
      priority: specialized
      audience: ["researchers", "advanced_developers"]
      complexity: expert
      documents:
        - ReEngine_Sec_01.md
        - ReEngine_Sec_02.md
        - ReEngine_Sec_03.md
        - ReEngine_Sec_04.md
        
    implementation_templates:
      priority: practical
      audience: ["developers"]
      format: code
      documents:
        - voither_primeira_consulta_template.py
        - voither_acompanhamento_template.py
        - PlanoTerapeutico.ini
        
    media_assets:
      priority: low
      format: binary
      documents:
        - icon.png
        - icon.ico
        - Logo_Montado_em_Vídeo_Animado.mp4
        - gemini_generated_video_49FF70E7.mov
        - "Screenshot 2025-07-19 095235.png"
        - "Screenshot 2025-07-19 095429.png"
        - .ee
```

## Document Status Tracking

```yaml
implementation_status:
  complete:
    - README.md
    - VOITHER_Knowledge_Graph_Updated.md
    - med_core.md
    - voither_med_implementation.md
    - med_frameworks.md
    - voither_system_architecture.md
    - ReEngine_Sec_01.md
    - ReEngine_Sec_02.md
    - ReEngine_Sec_03.md
    - ReEngine_Sec_04.md
    - emergence_enabled_ee.md
    
  in_development:
    - voither_dimensional_holofractor.md
    - voither_orchestrator_doc.md
    - apothecary_engine.md
    - voither_narrative_agent.md
    - voither_navigate.md
    - VOITHER_files_pipeline.md
    
  planned:
    - VOITHER_for_Narrative.md
    
  needs_update:
    - autoagency.md
    
  newly_created:
    - guides/clinician-quickstart.md
    - guides/developer-guide.md
    - TABLE_OF_CONTENTS.md
    - DOCUMENTATION_INDEX.md
    - METADATA.md
```

## Audience Mapping

```yaml
audiences:
  clinicians:
    primary_documents:
      - README.md
      - guides/clinician-quickstart.md
      - VOITHER_Knowledge_Graph_Updated.md
      - med_core.md
    reading_time: "2-4 hours"
    priority_level: high
    
  developers:
    primary_documents:
      - README.md
      - guides/developer-guide.md
      - voither_system_architecture.md
      - voither_med_implementation.md
      - voither_technical_pipeline.md
    reading_time: "4-8 hours"
    priority_level: high
    
  researchers:
    primary_documents:
      - VOITHER_Knowledge_Graph_Updated.md
      - geometria_afetos_cognicao.md
      - med_frameworks.md
      - emergence_enabled_ee.md
      - ReEngine_Sec_01.md
    reading_time: "6-12 hours"
    priority_level: medium
    
  architects:
    primary_documents:
      - voither_system_architecture.md
      - VOITHER_files_pipeline.md
      - voither_orchestrator_doc.md
      - iser_pipelines.md
    reading_time: "4-6 hours"
    priority_level: high
    
  project_managers:
    primary_documents:
      - README.md
      - VOITHER_Knowledge_Graph_Updated.md
      - voither_implementation_plan.md
      - DOCUMENTATION_INDEX.md
    reading_time: "2-3 hours"
    priority_level: medium
```

## Content Tags

```yaml
tags:
  technology:
    ai_ml: [med_core.md, apothecary_engine.md, emergence_enabled_ee.md]
    azure: [voither_system_architecture.md, guides/developer-guide.md]
    mongodb: [voither_system_architecture.md, DB_ideas.md]
    react: [voither_dimensional_holofractor.md, guides/developer-guide.md]
    python: [voither_med_implementation.md, med_core.md]
    
  functionality:
    transcription: [voither_system_architecture.md, guides/developer-guide.md]
    dimensional_analysis: [med_core.md, voither_med_implementation.md]
    visualization: [voither_dimensional_holofractor.md]
    automation: [autoagency.md, apothecary_engine.md]
    documentation: [voither_narrative_agent.md]
    
  domain:
    healthcare: [guides/clinician-quickstart.md, med_frameworks.md]
    psychology: [geometria_afetos_cognicao.md, espaco_mental_paper.md]
    psychiatry: [apothecary_engine.md, med_core.md]
    ai_research: [emergence_enabled_ee.md, ReEngine_Sec_01.md]
    
  complexity:
    beginner: [README.md, guides/clinician-quickstart.md]
    intermediate: [voither_system_architecture.md, med_core.md]
    advanced: [VOITHER_files_pipeline.md, emergence_enabled_ee.md]
    expert: [ReEngine_Sec_04.md, voither_orchestrator_doc.md]
```

## Document Relationships

```yaml
dependencies:
  README.md:
    references:
      - VOITHER_Knowledge_Graph_Updated.md
      - voither_system_architecture.md
      - guides/clinician-quickstart.md
      - guides/developer-guide.md
    
  med_core.md:
    dependencies:
      - voither_med_implementation.md
      - med_frameworks.md
    references:
      - VOITHER_Knowledge_Graph_Updated.md
    
  voither_system_architecture.md:
    references:
      - voither_technical_pipeline.md
      - VOITHER_files_pipeline.md
      - med_core.md
    
  autoagency.md:
    dependencies:
      - med_core.md
      - voither_orchestrator_doc.md
    status: needs_update
    
  guides/developer-guide.md:
    references:
      - voither_system_architecture.md
      - voither_med_implementation.md
      - med_core.md
```

## Search Index

```yaml
search_terms:
  voither: [README.md, VOITHER_Knowledge_Graph_Updated.md]
  ai: [med_core.md, apothecary_engine.md, emergence_enabled_ee.md]
  mental_health: [guides/clinician-quickstart.md, geometria_afetos_cognicao.md]
  dimensions: [med_core.md, voither_med_implementation.md]
  architecture: [voither_system_architecture.md, VOITHER_files_pipeline.md]
  visualization: [voither_dimensional_holofractor.md]
  automation: [autoagency.md, apothecary_engine.md]
  transcription: [voither_system_architecture.md, guides/developer-guide.md]
  azure: [voither_system_architecture.md, guides/developer-guide.md]
  fhir: [voither_system_architecture.md, voither_orchestrator_doc.md]
  mongodb: [voither_system_architecture.md, DB_ideas.md]
  react: [voither_dimensional_holofractor.md, guides/developer-guide.md]
  three_js: [voither_dimensional_holofractor.md, voither_implementation_plan.md]
  reengine: [ReEngine_Sec_01.md, ReEngine_Sec_02.md, ReEngine_Sec_03.md, ReEngine_Sec_04.md]
  emergence: [emergence_enabled_ee.md, ReEngine_Sec_01.md]
  holofractor: [voither_dimensional_holofractor.md, voither_implementation_plan.md]
```

## Quality Metrics

```yaml
documentation_quality:
  completeness:
    total_documents: 29
    documented_features: 15
    completion_percentage: 85
    
  accessibility:
    beginner_friendly: 4
    intermediate_level: 8
    advanced_level: 12
    expert_level: 5
    
  maintenance:
    last_updated: "2024-01-15"
    outdated_documents: 1
    maintenance_needed: ["autoagency.md"]
    
  coverage:
    user_guides: 2
    technical_docs: 15
    research_papers: 3
    implementation_guides: 4
    api_docs: 0  # needs improvement
    tutorials: 2
```

## Automation Hooks

```yaml
automation:
  build_triggers:
    - on_file_change: ["*.md", "*.py"]
    - on_schedule: "daily"
    
  validation_rules:
    - check_links: true
    - spell_check: true
    - markdown_lint: true
    - broken_references: true
    
  generation_tasks:
    - update_toc: "TABLE_OF_CONTENTS.md"
    - update_index: "DOCUMENTATION_INDEX.md"
    - update_metadata: "METADATA.md"
    - generate_api_docs: planned
    
  notification_targets:
    - slack_channel: "#docs"
    - email: "docs-team@voither.com"
```

---

*This metadata file is automatically generated and maintained. Last updated: Current session*