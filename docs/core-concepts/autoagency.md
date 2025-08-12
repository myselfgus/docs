# 7: AUTOAGENCY + WORKFLOWS ADMINISTRATIVOS

## OVERVIEW
Implementar o sistema AUTOAGENCY que automatiza tarefas administrativas clínicas usando workflows .e executados pelo runtime .Re, com detecção inteligente de necessidades baseada no MED. O AUTOAGENCY transforma processos manuais em automação inteligente, liberando profissionais para foco no cuidado direto ao paciente.

## ATENCAO: .e .Re estao integradas em .ee e no BRRE.

## DEPENDENCIES (Must exist before starting)

- [ ] ✅ **Sprint 6 completed**: VOITHER Apothecary operacional com recomendações automáticas
- [ ] ✅ **DSL Runtime functional**: .Re engine executando workflows .e corretamente
- [ ] ✅ **MED detection working**: Sistema detecta necessidades baseado em análise dimensional
- [ ] ✅ **Integration tested**: Pipeline completo MED → Frameworks → Apothecary funcionando
- [ ] Python 3.11+ com asyncio, celery, redis
- [ ] Sistema de templates para documentação clínica
- [ ] Integração com sistemas FHIR para interoperabilidade

### Pre-flight Validation Script

```bash
#!/bin/bash
# validate_sprint_6.sh
set -e

echo "🔍 Validating Sprint 6 dependencies..."

# Test Apothecary functionality
python -c "
import asyncio
from src.apothecary.apothecary_engine import VoitherApothecary
from src.med.dimensional_extractor import DimensionalExtractor

async def test_apothecary():
    # Test MED extraction
    med = DimensionalExtractor({'spacy_model': 'pt_core_news_lg'})
    result = await med.extract_all_dimensions('Sinto-me deprimido e ansioso.')
    assert result['success'], 'MED extraction failed'
    
    # Test Apothecary
    apothecary = VoitherApothecary({'models_dir': 'models/apothecary'})
    patient_profile = {
        'patient_id': 'test',
        'raw_dimensions': result['dimensions'],
        'calibrated_frameworks': {'rdoc': {'scores': {'negative_valence': 7.0}}},
        'patient_metadata': {'age': 30, 'sex': 'M'}
    }
    
    recommendations = await apothecary.generate_treatment_recommendations(patient_profile)
    assert recommendations['success'], 'Apothecary failed'
    
    print('✅ Apothecary operational')

asyncio.run(test_apothecary())
"

# Test DSL Runtime
python -c "
import asyncio
from src.runtime.re_engine import ReEngine

async def test_dsl_runtime():
    config = {'redis': {'host': 'redis-service', 'port': 6379}}
    engine = ReEngine(config)
    
    assert await engine.start(), '.Re engine failed to start'
    
    # Test workflow execution
    result = await engine.execute_dsl_command(
        'e', 
        'execute workflow administrative_task',
        {'task_type': 'documentation'}
    )
    assert result['success'], 'Workflow execution failed'
    
    await engine.stop()
    print('✅ DSL Runtime operational')

asyncio.run(test_dsl_runtime())
"

# Test async task queue
python -c "
import redis
r = redis.Redis(host='redis-service', port=6379)
r.ping()
print('✅ Redis task queue available')
"

echo "✅ All Sprint 6 dependencies validated"
```

## IMPLEMENTATION

### 1. Project Structure

```
voither-autoagency/
├── src/
│   ├── __init__.py
│   ├── autoagency/
│   │   ├── __init__.py
│   │   ├── agency_engine.py           # Main AUTOAGENCY class
│   │   ├── task_detector.py           # Intelligent task detection
│   │   ├── workflow_orchestrator.py   # Workflow management
│   │   ├── document_automator.py      # Documentation automation
│   │   └── administrative_assistant.py # Administrative tasks
│   ├── workflows/
│   │   ├── __init__.py
│   │   ├── clinical_workflows.py      # Clinical workflow definitions
│   │   ├── documentation_workflows.py # Documentation workflows
│   │   ├── scheduling_workflows.py    # Scheduling automation
│   │   └── billing_workflows.py       # Billing automation
│   ├── templates/
│   │   ├── __init__.py
│   │   ├── template_engine.py         # Template processing
│   │   ├── clinical_templates.py      # Clinical document templates
│   │   └── report_templates.py        # Report generation
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── fhir_integration.py        # FHIR interoperability
│   │   ├── ehr_integration.py         # EHR system integration
│   │   └── scheduling_integration.py  # Scheduling system integration
│   └── tasks/
│       ├── __init__.py
│       ├── async_tasks.py             # Celery async tasks
│       ├── task_scheduler.py          # Task scheduling
│       └── task_monitor.py            # Task monitoring
├── tests/
│   ├── unit/
│   ├── integration/
│   └── workflow/
├── templates/
│   ├── clinical/
│   ├── administrative/
│   └── reports/
├── requirements.txt
└── README.md
```

### 2. Core AUTOAGENCY Engine

```python
# src/autoagency/agency_engine.py
import asyncio
import uuid
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass, field

from .task_detector import IntelligentTaskDetector
from .workflow_orchestrator import WorkflowOrchestrator
from .document_automator import DocumentAutomator
from .administrative_assistant import AdministrativeAssistant
from ..workflows.clinical_workflows import ClinicalWorkflows
from ..integrations.fhir_integration import FHIRIntegration
from ..tasks.async_tasks import AsyncTaskManager
from ...runtime.re_engine import ReEngine

@dataclass
class AutomationTask:
    """Represents an automated task"""
    task_id: str
    task_type: str
    priority: int
    patient_id: Optional[str]
    session_id: Optional[str]
    triggered_by: str
    automation_context: Dict[str, Any]
    estimated_time_minutes: int
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    errors: List[str] = field(default_factory=list)

class VoitherAutoAgency:
    """
    VOITHER AUTOAGENCY - Sistema de Automação Administrativa Inteligente
    
    Automatiza tarefas administrativas clínicas usando:
    1. Detecção inteligente de necessidades baseada no MED
    2. Workflows .e orquestrados pelo runtime .Re
    3. Geração automática de documentação clínica
    4. Integração com sistemas FHIR/EHR
    5. Agendamento inteligente e gerenciamento de tarefas
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger("VoitherAutoAgency")
        
        # Core components
        self.task_detector = IntelligentTaskDetector(config)
        self.workflow_orchestrator = WorkflowOrchestrator(config)
        self.document_automator = DocumentAutomator(config)
        self.admin_assistant = AdministrativeAssistant(config)
        
        # Workflow definitions
        self.clinical_workflows = ClinicalWorkflows(config)
        
        # External integrations
        self.fhir_integration = FHIRIntegration(config.get('fhir', {}))
        
        # Task management
        self.async_task_manager = AsyncTaskManager(config)
        
        # DSL Runtime engine for workflow execution
        self.dsl_runtime = ReEngine(config.get('dsl_runtime', {}))
        
        # Active automation tasks
        self.active_tasks: Dict[str, AutomationTask] = {}
        
        # Automation statistics
        self.automation_stats = {
            'total_tasks_automated': 0,
            'successful_automations': 0,
            'average_task_time_minutes': 0.0,
            'time_saved_hours': 0.0,
            'most_common_automations': {},
            'error_rate': 0.0
        }
        
        # Automation rules and triggers
        self.automation_rules = self._initialize_automation_rules()
    
    async def start_automation_engine(self) -> bool:
        """Inicia o motor de automação"""
        try:
            self.logger.info("Starting VOITHER AUTOAGENCY Engine")
            
            # Start DSL runtime
            if not await self.dsl_runtime.start():
                raise Exception("Failed to start DSL runtime")
            
            # Start async task manager
            await self.async_task_manager.start()
            
            # Initialize integrations
            await self.fhir_integration.initialize()
            
            # Start task monitoring
            asyncio.create_task(self._automation_monitoring_loop())
            
            self.logger.info("✅ AUTOAGENCY Engine started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start AUTOAGENCY Engine: {e}")
            return False
    
    async def stop_automation_engine(self) -> bool:
        """Para o motor de automação graciosamente"""
        try:
            self.logger.info("Stopping VOITHER AUTOAGENCY Engine")
            
            # Complete active tasks
            await self._complete_active_tasks()
            
            # Stop components
            await self.async_task_manager.stop()
            await self.dsl_runtime.stop()
            
            self.logger.info("✅ AUTOAGENCY Engine stopped successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error stopping AUTOAGENCY Engine: {e}")
            return False
    
    async def process_clinical_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa uma sessão clínica e executa automações necessárias
        
        Args:
            session_data: Dados completos da sessão incluindo:
                - med_analysis: Análise MED completa
                - apothecary_recommendations: Recomendações do Apothecary
                - patient_profile: Perfil completo do paciente
                - session_metadata: Metadados da sessão
                
        Returns:
            Resultado do processamento automático
        """
        automation_id = f"auto_{int(datetime.now().timestamp())}"
        start_time = datetime.now()
        
        try:
            self.logger.info(f"Processing clinical session automation: {automation_id}")
            
            # Detectar tarefas necessárias baseado na análise
            detected_tasks = await self.task_detector.detect_automation_needs(session_data)
            
            if not detected_tasks:
                return {
                    'automation_id': automation_id,
                    'tasks_detected': 0,
                    'message': 'No automation tasks detected for this session'
                }
            
            # Executar tarefas em paralelo com priorização
            automation_results = await self._execute_detected_tasks(
                detected_tasks, session_data, automation_id
            )
            
            # Calcular métricas de automação
            processing_time = (datetime.now() - start_time).total_seconds()
            time_saved = self._calculate_time_saved(automation_results)
            
            # Resultado final
            final_result = {
                'automation_id': automation_id,
                'session_id': session_data.get('session_metadata', {}).get('session_id'),
                'patient_id': session_data.get('patient_profile', {}).get('patient_id'),
                'success': True,
                'processing_time_seconds': processing_time,
                'tasks_detected': len(detected_tasks),
                'tasks_completed': len([r for r in automation_results if r.get('success', False)]),
                'time_saved_minutes': time_saved,
                'automation_results': automation_results,
                'automated_outputs': {
                    'clinical_documentation': self._extract_clinical_docs(automation_results),
                    'administrative_tasks': self._extract_admin_tasks(automation_results),
                    'system_integrations': self._extract_integrations(automation_results)
                }
            }
            
            # Atualizar estatísticas
            self._update_automation_stats(final_result)
            
            self.logger.info(
                f"✅ Session automation completed: {automation_id} "
                f"({len(automation_results)} tasks, {time_saved:.1f}min saved)"
            )
            
            return final_result
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"❌ Session automation failed: {automation_id} - {e}")
            
            return {
                'automation_id': automation_id,
                'success': False,
                'error': str(e),
                'processing_time_seconds': processing_time
            }
    
    async def execute_manual_automation(self, task_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa automação manual solicitada pelo usuário
        
        Args:
            task_type: Tipo de tarefa ('documentation', 'scheduling', 'billing', etc.)
            context: Contexto da automação
            
        Returns:
            Resultado da execução manual
        """
        task_id = f"manual_{task_type}_{int(datetime.now().timestamp())}"
        
        try:
            # Criar tarefa manual
            manual_task = AutomationTask(
                task_id=task_id,
                task_type=task_type,
                priority=1,  # Alta prioridade para tarefas manuais
                patient_id=context.get('patient_id'),
                session_id=context.get('session_id'),
                triggered_by='manual_request',
                automation_context=context,
                estimated_time_minutes=self._estimate_task_time(task_type)
            )
            
            # Executar tarefa
            result = await self._execute_single_task(manual_task)
            
            return {
                'task_id': task_id,
                'success': result.get('success', False),
                'task_type': task_type,
                'execution_result': result,
                'time_saved_minutes': self._calculate_single_task_time_saved(task_type, result)
            }
            
        except Exception as e:
            self.logger.error(f"Manual automation failed: {task_type} - {e}")
            return {
                'task_id': task_id,
                'success': False,
                'error': str(e)
            }
    
    async def get_automation_recommendations(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera recomendações de automação baseadas no contexto
        
        Args:
            context: Contexto para análise (sessão, paciente, histórico)
            
        Returns:
            Recomendações de automação
        """
        try:
            # Analisar potencial de automação
            automation_potential = await self.task_detector.analyze_automation_potential(context)
            
            # Gerar recomendações específicas
            recommendations = []
            
            for potential_task in automation_potential:
                recommendation = {
                    'task_type': potential_task['type'],
                    'description': potential_task['description'],
                    'estimated_time_saved_minutes': potential_task['time_savings'],
                    'automation_confidence': potential_task['confidence'],
                    'prerequisites': potential_task.get('prerequisites', []),
                    'impact_level': self._classify_impact_level(potential_task['time_savings'])
                }
                recommendations.append(recommendation)
            
            return {
                'success': True,
                'total_recommendations': len(recommendations),
                'potential_time_savings_hours': sum(r['estimated_time_saved_minutes'] for r in recommendations) / 60,
                'recommendations': recommendations,
                'automation_readiness_score': np.mean([r['automation_confidence'] for r in recommendations]) if recommendations else 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Failed to generate automation recommendations: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_automation_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas de automação"""
        return {
            'operational_stats': self.automation_stats.copy(),
            'active_tasks': len(self.active_tasks),
            'task_queue_length': self.async_task_manager.get_queue_length(),
            'automation_rules': len(self.automation_rules),
            'system_status': {
                'dsl_runtime': 'operational' if self.dsl_runtime.status.value == 'idle' else 'busy',
                'fhir_integration': 'connected' if self.fhir_integration.is_connected() else 'disconnected',
                'async_tasks': 'operational'
            },
            'efficiency_metrics': {
                'automation_rate': self._calculate_automation_rate(),
                'error_rate': self.automation_stats['error_rate'],
                'average_time_savings_per_session': self._calculate_avg_time_savings()
            }
        }
    
    async def _execute_detected_tasks(self, detected_tasks: List[Dict[str, Any]], 
                                    session_data: Dict[str, Any], 
                                    automation_id: str) -> List[Dict[str, Any]]:
        """Executa tarefas detectadas em paralelo com priorização"""
        
        # Converter em AutomationTask objects
        automation_tasks = []
        for task_data in detected_tasks:
            task = AutomationTask(
                task_id=f"{automation_id}_{task_data['type']}_{len(automation_tasks)}",
                task_type=task_data['type'],
                priority=task_data.get('priority', 5),
                patient_id=session_data.get('patient_profile', {}).get('patient_id'),
                session_id=session_data.get('session_metadata', {}).get('session_id'),
                triggered_by='intelligent_detection',
                automation_context={**task_data, 'session_data': session_data},
                estimated_time_minutes=task_data.get('estimated_time', 5)
            )
            automation_tasks.append(task)
        
        # Ordenar por prioridade (menor número = maior prioridade)
        automation_tasks.sort(key=lambda t: t.priority)
        
        # Executar tarefas com limitação de concorrência
        semaphore = asyncio.Semaphore(self.config.get('max_concurrent_automations', 3))
        
        async def execute_with_semaphore(task):
            async with semaphore:
                return await self._execute_single_task(task)
        
        # Executar em paralelo
        tasks_futures = [execute_with_semaphore(task) for task in automation_tasks]
        results = await asyncio.gather(*tasks_futures, return_exceptions=True)
        
        # Processar resultados
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    'task_id': automation_tasks[i].task_id,
                    'success': False,
                    'error': str(result),
                    'task_type': automation_tasks[i].task_type
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def _execute_single_task(self, task: AutomationTask) -> Dict[str, Any]:
        """Executa uma única tarefa de automação"""
        
        task.started_at = datetime.now()
        task.status = "executing"
        self.active_tasks[task.task_id] = task
        
        try:
            self.logger.debug(f"Executing automation task: {task.task_id} ({task.task_type})")
            
            # Roteamento baseado no tipo de tarefa
            if task.task_type == 'clinical_documentation':
                result = await self._execute_documentation_task(task)
            elif task.task_type == 'administrative_scheduling':
                result = await self._execute_scheduling_task(task)
            elif task.task_type == 'billing_coding':
                result = await self._execute_billing_task(task)
            elif task.task_type == 'fhir_integration':
                result = await self._execute_fhir_task(task)
            elif task.task_type == 'follow_up_automation':
                result = await self._execute_followup_task(task)
            else:
                # Tarefa genérica usando workflow .e
                result = await self._execute_generic_workflow_task(task)
            
            # Atualizar status da tarefa
            task.completed_at = datetime.now()
            task.status = "completed"
            task.result = result
            
            return {
                'task_id': task.task_id,
                'success': result.get('success', False),
                'task_type': task.task_type,
                'execution_time_minutes': (task.completed_at - task.started_at).total_seconds() / 60,
                'result': result
            }
            
        except Exception as e:
            task.completed_at = datetime.now()
            task.status = "failed"
            task.errors.append(str(e))
            
            self.logger.error(f"Task execution failed: {task.task_id} - {e}")
            
            return {
                'task_id': task.task_id,
                'success': False,
                'error': str(e),
                'task_type': task.task_type
            }
        
        finally:
            # Cleanup active task
            if task.task_id in self.active_tasks:
                del self.active_tasks[task.task_id]
    
    async def _execute_documentation_task(self, task: AutomationTask) -> Dict[str, Any]:
        """Executa tarefa de documentação clínica"""
        
        context = task.automation_context
        session_data = context.get('session_data', {})
        
        # Gerar documentação usando o DocumentAutomator
        documentation_result = await self.document_automator.generate_clinical_documentation(
            session_data.get('med_analysis', {}),
            session_data.get('apothecary_recommendations', {}),
            session_data.get('patient_profile', {}),
            context.get('documentation_type', 'session_note')
        )
        
        # Salvar no sistema FHIR se configurado
        if self.fhir_integration.is_connected() and documentation_result.get('success'):
            fhir_result = await self.fhir_integration.store_clinical_document(
                documentation_result['document'],
                session_data.get('patient_profile', {})
            )
            documentation_result['fhir_stored'] = fhir_result.get('success', False)
        
        return documentation_result
    
    async def _execute_scheduling_task(self, task: AutomationTask) -> Dict[str, Any]:
        """Executa tarefa de agendamento automático"""
        
        context = task.automation_context
        session_data = context.get('session_data', {})
        
        # Usar o Administrative Assistant para agendamento
        scheduling_result = await self.admin_assistant.auto_schedule_followup(
            session_data.get('patient_profile', {}),
            session_data.get('apothecary_recommendations', {}),
            context.get('scheduling_preferences', {})
        )
        
        return scheduling_result
    
    async def _execute_billing_task(self, task: AutomationTask) -> Dict[str, Any]:
        """Executa tarefa de codificação e faturamento"""
        
        context = task.automation_context
        session_data = context.get('session_data', {})
        
        # Gerar códigos de faturamento baseados na sessão
        billing_result = await self.admin_assistant.generate_billing_codes(
            session_data.get('med_analysis', {}),
            session_data.get('apothecary_recommendations', {}),
            context.get('billing_context', {})
        )
        
        return billing_result
    
    async def _execute_fhir_task(self, task: AutomationTask) -> Dict[str, Any]:
        """Executa tarefa de integração FHIR"""
        
        context = task.automation_context
        session_data = context.get('session_data', {})
        
        # Sincronizar dados com sistema FHIR
        fhir_result = await self.fhir_integration.sync_session_data(
            session_data,
            context.get('sync_options', {})
        )
        
        return fhir_result
    
    async def _execute_followup_task(self, task: AutomationTask) -> Dict[str, Any]:
        """Executa tarefa de follow-up automático"""
        
        context = task.automation_context
        session_data = context.get('session_data', {})
        
        # Criar tarefas de follow-up baseadas nas recomendações
        followup_result = await self.admin_assistant.create_followup_tasks(
            session_data.get('apothecary_recommendations', {}),
            session_data.get('patient_profile', {}),
            context.get('followup_timeline', {})
        )
        
        return followup_result
    
    async def _execute_generic_workflow_task(self, task: AutomationTask) -> Dict[str, Any]:
        """Executa tarefa genérica usando workflow .e"""
        
        # Construir comando de workflow baseado no tipo de tarefa
        workflow_command = f"execute workflow {task.task_type}_automation"
        
        # Executar via DSL Runtime
        dsl_result = await self.dsl_runtime.execute_dsl_command(
            'e',
            workflow_command,
            task.automation_context
        )
        
        return dsl_result
    
    def _initialize_automation_rules(self) -> Dict[str, Any]:
        """Inicializa regras de automação padrão"""
        return {
            'documentation_threshold': 0.8,  # Confiança mínima para doc automática
            'scheduling_priority_score': 7.0,  # Score mínimo para agendamento prioritário
            'billing_automation_enabled': True,
            'fhir_sync_automatic': True,
            'followup_auto_creation': True,
            'max_concurrent_tasks': 5,
            'task_timeout_minutes': 30
        }
    
    def _calculate_time_saved(self, automation_results: List[Dict[str, Any]]) -> float:
        """Calcula tempo total economizado pelas automações"""
        time_savings_map = {
            'clinical_documentation': 15,  # minutos economizados
            'administrative_scheduling': 10,
            'billing_coding': 8,
            'fhir_integration': 5,
            'follow_up_automation': 12
        }
        
        total_saved = 0.0
        for result in automation_results:
            if result.get('success', False):
                task_type = result.get('task_type', '')
                total_saved += time_savings_map.get(task_type, 5)  # 5min default
        
        return total_saved
    
    def _extract_clinical_docs(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extrai documentos clínicos gerados"""
        docs = []
        for result in results:
            if (result.get('task_type') == 'clinical_documentation' and 
                result.get('success') and 
                'result' in result):
                docs.append(result['result'])
        return docs
    
    def _extract_admin_tasks(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extrai tarefas administrativas executadas"""
        admin_tasks = []
        admin_types = ['administrative_scheduling', 'billing_coding', 'follow_up_automation']
        
        for result in results:
            if (result.get('task_type') in admin_types and 
                result.get('success') and 
                'result' in result):
                admin_tasks.append(result['result'])
        return admin_tasks
    
    def _extract_integrations(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extrai integrações de sistema executadas"""
        integrations = []
        for result in results:
            if (result.get('task_type') == 'fhir_integration' and 
                result.get('success') and 
                'result' in result):
                integrations.append(result['result'])
        return integrations
    
    def _update_automation_stats(self, result: Dict[str, Any]):
        """Atualiza estatísticas de automação"""
        self.automation_stats['total_tasks_automated'] += result.get('tasks_detected', 0)
        self.automation_stats['successful_automations'] += result.get('tasks_completed', 0)
        
        # Atualizar tempo médio
        if result.get('tasks_completed', 0) > 0:
            avg_time = result.get('time_saved_minutes', 0) / result.get('tasks_completed', 1)
            total_tasks = self.automation_stats['total_tasks_automated']
            current_avg = self.automation_stats['average_task_time_minutes']
            
            self.automation_stats['average_task_time_minutes'] = (
                (current_avg * (total_tasks - result.get('tasks_detected', 0)) + 
                 avg_time * result.get('tasks_detected', 0)) / total_tasks
            )
        
        # Atualizar tempo total economizado
        self.automation_stats['time_saved_hours'] += result.get('time_saved_minutes', 0) / 60
        
        # Atualizar taxa de erro
        total_attempted = self.automation_stats['total_tasks_automated']
        successful = self.automation_stats['successful_automations']
        self.automation_stats['error_rate'] = (
            (total_attempted - successful) / max(total_attempted, 1) * 100
        )
    
    async def _automation_monitoring_loop(self):
        """Loop de monitoramento de automações"""
        while True:
            try:
                # Monitorar tarefas que estão executando há muito tempo
                current_time = datetime.now()
                timeout_minutes = self.automation_rules['task_timeout_minutes']
                
                for task_id, task in list(self.active_tasks.items()):
                    if (task.started_at and 
                        (current_time - task.started_at).total_seconds() > timeout_minutes * 60):
                        
                        self.logger.warning(f"Task timeout: {task_id}")
                        task.status = "timeout"
                        task.errors.append("Task exceeded timeout limit")
                        del self.active_tasks[task_id]
                
                # Aguardar antes da próxima verificação
                await asyncio.sleep(60)  # Verificar a cada minuto
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Monitoring loop error: {e}")
                await asyncio.sleep(60)
    
    async def _complete_active_tasks(self):
        """Completa tarefas ativas de forma graciosa"""
        if not self.active_tasks:
            return
        
        self.logger.info(f"Completing {len(self.active_tasks)} active tasks...")
        
        # Aguardar conclusão com timeout
        timeout_seconds = 300  # 5 minutos
        start_wait = datetime.now()
        
        while self.active_tasks and (datetime.now() - start_wait).total_seconds() < timeout_seconds:
            await asyncio.sleep(1)
        
        # Forçar finalização de tarefas que não completaram
        for task_id, task in self.active_tasks.items():
            task.status = "force_completed"
            task.completed_at = datetime.now()
            self.logger.warning(f"Force completed task: {task_id}")
        
        self.active_tasks.clear()
    
    def _estimate_task_time(self, task_type: str) -> int:
        """Estima tempo de execução para um tipo de tarefa"""
        time_estimates = {
            'clinical_documentation': 5,
            'administrative_scheduling': 3,
            'billing_coding': 4,
            'fhir_integration': 2,
            'follow_up_automation': 3
        }
        return time_estimates.get(task_type, 5)
    
    def _calculate_single_task_time_saved(self, task_type: str, result: Dict[str, Any]) -> float:
        """Calcula tempo economizado para uma tarefa específica"""
        if not result.get('success', False):
            return 0.0
        
        time_savings_map = {
            'clinical_documentation': 15,
            'administrative_scheduling': 10,
            'billing_coding': 8,
            'fhir_integration': 5,
            'follow_up_automation': 12
        }
        
        return time_savings_map.get(task_type, 5)
    
    def _classify_impact_level(self, time_savings: float) -> str:
        """Classifica nível de impacto baseado no tempo economizado"""
        if time_savings >= 20:
            return 'high'
        elif time_savings >= 10:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_automation_rate(self) -> float:
        """Calcula taxa de automação (% de tarefas automatizadas)"""
        total = self.automation_stats['total_tasks_automated']
        if total == 0:
            return 0.0
        return (self.automation_stats['successful_automations'] / total) * 100
    
    def _calculate_avg_time_savings(self) -> float:
        """Calcula economia média de tempo por sessão"""
        total_hours = self.automation_stats['time_saved_hours']
        total_automations = self.automation_stats['successful_automations']
        if total_automations == 0:
            return 0.0
        return (total_hours / total_automations) * 60  # Retorna em minutos
```

### 3. Intelligent Task Detector

```python
# src/autoagency/task_detector.py
import numpy as np
from typing import Dict, Any, List, Optional
import logging

class IntelligentTaskDetector:
    """
    Detector Inteligente de Tarefas
    
    Analisa dados de sessão clínica (MED + Apothecary) para detectar
    automaticamente quais tarefas administrativas podem ser automatizadas
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger("IntelligentTaskDetector")
        
        # Regras de detecção baseadas em padrões clínicos
        self.detection_rules = {
            'clinical_documentation': {
                'triggers': [
                    ('med_confidence', '>', 0.8),
                    ('session_completeness', '>', 0.9),
                    ('apothecary_recommendations', 'exists', True)
                ],
                'priority': 1,
                'estimated_time': 5
            },
            
            'administrative_scheduling': {
                'triggers': [
                    ('apothecary_confidence', '>', 0.7),
                    ('treatment_recommendations', 'count', '>', 0),
                    ('follow_up_needed', '==', True)
                ],
                'priority': 2,
                'estimated_time': 3
            },
            
            'billing_coding': {
                'triggers': [
                    ('session_duration', '>', 30),  # minutos
                    ('diagnostic_confidence', '>', 0.6),
                    ('med_analysis_complete', '==', True)
                ],
                'priority': 3,
                'estimated_time': 4
            },
            
            'fhir_integration': {
                'triggers': [
                    ('patient_profile_complete', '==', True),
                    ('med_dimensions_valid', '==', True),
                    ('system_integration_enabled', '==', True)
                ],
                'priority': 4,
                'estimated_time': 2
            },
            
            'follow_up_automation': {
                'triggers': [
                    ('treatment_started', '==', True),
                    ('monitoring_required', '==', True),
                    ('apothecary_recommendations', 'has_monitoring', True)
                ],
                'priority': 2,
                'estimated_time': 3
            }
        }
    
    async def detect_automation_needs(self, session_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detecta necessidades de automação baseadas nos dados da sessão
        
        Args:
            session_data: Dados completos da sessão clínica
            
        Returns:
            Lista de tarefas detectadas para automação
        """
        
        detected_tasks = []
        
        # Extrair métricas relevantes dos dados da sessão
        session_metrics = self._extract_session_metrics(session_data)
        
        # Aplicar regras de detecção
        for task_type, rule_config in self.detection_rules.items():
            if self._evaluate_task_triggers(session_metrics, rule_config['triggers']):
                
                # Calcular confiança da detecção
                detection_confidence = self._calculate_detection_confidence(
                    session_metrics, rule_config['triggers']
                )
                
                # Criar task detected
                detected_task = {
                    'type': task_type,
                    'description': self._get_task_description(task_type),
                    'priority': rule_config['priority'],
                    'estimated_time': rule_config['estimated_time'],
                    'detection_confidence': detection_confidence,
                    'triggering_factors': self._get_triggering_factors(
                        session_metrics, rule_config['triggers']
                    ),
                    'automation_context': {
                        'session_metrics': session_metrics,
                        'detection_metadata': {
                            'rule_version': '1.0',
                            'detection_timestamp': datetime.now().isoformat()
                        }
                    }
                }
                
                detected_tasks.append(detected_task)
        
        # Ordenar por prioridade e confiança
        detected_tasks.sort(key=lambda t: (t['priority'], -t['detection_confidence']))
        
        self.logger.info(
            f"Detected {len(detected_tasks)} automation tasks: "
            f"{[t['type'] for t in detected_tasks]}"
        )
        
        return detected_tasks
    
    async def analyze_automation_potential(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analisa potencial de automação para um contexto específico
        
        Args:
            context: Contexto para análise (pode incluir histórico, preferências, etc.)
            
        Returns:
            Lista de potenciais automações com benefícios estimados
        """
        
        potential_automations = []
        
        # Analisar padrões históricos se disponível
        if 'historical_data' in context:
            historical_patterns = self._analyze_historical_patterns(context['historical_data'])
            
            for pattern in historical_patterns:
                if pattern['frequency'] >= 3:  # Tarefas que ocorrem 3+ vezes
                    potential_automation = {
                        'type': pattern['task_type'],
                        'description': f"Automação de {pattern['task_type']} (executada {pattern['frequency']}x)",
                        'frequency': pattern['frequency'],
                        'time_savings': pattern['avg_time_spent'] * pattern['frequency'] * 0.8,  # 80% economia
                        'confidence': min(pattern['frequency'] / 10.0, 1.0),  # Max confidence at 10 occurrences
                        'implementation_effort': self._estimate_implementation_effort(pattern['task_type']),
                        'roi_score': self._calculate_automation_roi(
                            pattern['avg_time_spent'] * pattern['frequency'], 
                            self._estimate_implementation_effort(pattern['task_type'])
                        )
                    }
                    potential_automations.append(potential_automation)
        
        # Analisar contexto atual
        if 'current_session' in context:
            current_potential = await self.detect_automation_needs(context['current_session'])
            
            for task in current_potential:
                potential_automation = {
                    'type': task['type'],
                    'description': f"Automação imediata: {task['description']}",
                    'time_savings': task['estimated_time'] * 0.9,  # 90% economia para tarefas detectadas
                    'confidence': task['detection_confidence'],
                    'implementation_effort': 'immediate',
                    'roi_score': task['estimated_time'] * 0.9  # ROI imediato
                }
                potential_automations.append(potential_automation)
        
        # Ordenar por ROI score
        potential_automations.sort(key=lambda a: a['roi_score'], reverse=True)
        
        return potential_automations
    
    def _extract_session_metrics(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai métricas relevantes dos dados da sessão"""
        
        metrics = {}
        
        # Métricas do MED
        med_analysis = session_data.get('med_analysis', {})
        if med_analysis:
            metrics['med_confidence'] = med_analysis.get('global_confidence', 0.0)
            metrics['med_dimensions_valid'] = len(med_analysis.get('dimensions', {})) == 15
            metrics['med_analysis_complete'] = med_analysis.get('success', False)
        
        # Métricas do Apothecary
        apothecary_data = session_data.get('apothecary_recommendations', {})
        if apothecary_data:
            metrics['apothecary_confidence'] = apothecary_data.get('global_confidence', 0.0)
            recommendations = apothecary_data.get('treatment_recommendations', [])
            metrics['treatment_recommendations'] = len(recommendations)
            metrics['apothecary_recommendations'] = len(recommendations) > 0
            
            # Verificar se há necessidade de monitoramento
            metrics['monitoring_required'] = any(
                'monitoring' in rec.get('clinical_considerations', {}) 
                for rec in recommendations
            )
            
            # Verificar recomendações de follow-up
            metrics['follow_up_needed'] = any(
                rec.get('follow_up_recommended', False) 
                for rec in recommendations
            )
        
        # Métricas do perfil do paciente
        patient_profile = session_data.get('patient_profile', {})
        if patient_profile:
            metadata = patient_profile.get('patient_metadata', {})
            metrics['patient_profile_complete'] = all([
                metadata.get('age'),
                metadata.get('sex'),
                patient_profile.get('raw_dimensions')
            ])
        
        # Métricas da sessão
        session_metadata = session_data.get('session_metadata', {})
        if session_metadata:
            metrics['session_duration'] = session_metadata.get('duration_minutes', 0)
            metrics['session_completeness'] = session_metadata.get('completeness_score', 0.0)
        
        # Métricas de diagnóstico
        diagnostic_data = session_data.get('diagnostic_suggestions', [])
        if diagnostic_data:
            high_conf_diagnostics = [d for d in diagnostic_data if d.get('confidence') == 'high']
            metrics['diagnostic_confidence'] = len(high_conf_diagnostics) / max(len(diagnostic_data), 1)
        else:
            metrics['diagnostic_confidence'] = 0.0
        
        # Configurações do sistema
        metrics['system_integration_enabled'] = self.config.get('fhir_enabled', False)
        metrics['treatment_started'] = bool(apothecary_data.get('treatment_recommendations'))
        
        return metrics
    
    def _evaluate_task_triggers(self, metrics: Dict[str, Any], triggers: List[tuple]) -> bool:
        """Avalia se os triggers de uma tarefa foram satisfeitos"""
        
        for trigger in triggers:
            metric_name, operator, expected_value = trigger
            
            if metric_name not in metrics:
                return False
            
            metric_value = metrics[metric_name]
            
            # Aplicar operador
            if operator == '>':
                if not (metric_value > expected_value):
                    return False
            elif operator == '>=':
                if not (metric_value >= expected_value):
                    return False
            elif operator == '<':
                if not (metric_value < expected_value):
                    return False
            elif operator == '<=':
                if not (metric_value <= expected_value):
                    return False
            elif operator == '==':
                if not (metric_value == expected_value):
                    return False
            elif operator == '!=':
                if not (metric_value != expected_value):
                    return False
            elif operator == 'exists':
                if expected_value and not metric_value:
                    return False
                elif not expected_value and metric_value:
                    return False
            elif operator == 'count':
                # Especial para contagem
                next_op, next_val = triggers[triggers.index(trigger) + 1][1:3]
                if next_op == '>':
                    if not (metric_value > next_val):
                        return False
                # Skip next trigger since we processed it
                triggers.remove(triggers[triggers.index(trigger) + 1])
            elif operator == 'has_monitoring':
                # Especial para verificar monitoramento
                if expected_value and not self._check_monitoring_needed(metrics):
                    return False
        
        return True
    
    def _calculate_detection_confidence(self, metrics: Dict[str, Any], triggers: List[tuple]) -> float:
        """Calcula confiança da detecção baseada na força dos triggers"""
        
        total_confidence = 0.0
        trigger_count = 0
        
        for trigger in triggers:
            metric_name, operator, expected_value = trigger
            
            if metric_name not in metrics:
                continue
            
            metric_value = metrics[metric_name]
            
            # Calcular confiança baseada na "força" do trigger
            if operator in ['>', '>=', '<', '<=']:
                if isinstance(metric_value, (int, float)) and isinstance(expected_value, (int, float)):
                    if operator in ['>', '>=']:
                        strength = min(metric_value / expected_value, 2.0)  # Cap at 2x
                    else:
                        strength = min(expected_value / metric_value, 2.0)
                    total_confidence += min(strength, 1.0)
                    trigger_count += 1
            elif operator == '==':
                total_confidence += 1.0 if metric_value == expected_value else 0.0
                trigger_count += 1
            elif operator == 'exists':
                total_confidence += 1.0 if bool(metric_value) == expected_value else 0.0
                trigger_count += 1
        
        return total_confidence / max(trigger_count, 1)
    
    def _get_triggering_factors(self, metrics: Dict[str, Any], triggers: List[tuple]) -> List[str]:
        """Retorna fatores que dispararam a detecção"""
        
        factors = []
        
        for trigger in triggers:
            metric_name, operator, expected_value = trigger
            
            if metric_name in metrics:
                metric_value = metrics[metric_name]
                
                if self._single_trigger_satisfied(metric_value, operator, expected_value):
                    factor_desc = f"{metric_name} {operator} {expected_value} (atual: {metric_value})"
                    factors.append(factor_desc)
        
        return factors
    
    def _single_trigger_satisfied(self, metric_value: Any, operator: str, expected_value: Any) -> bool:
        """Verifica se um único trigger foi satisfeito"""
        if operator == '>':
            return metric_value > expected_value
        elif operator == '>=':
            return metric_value >= expected_value
        elif operator == '<':
            return metric_value < expected_value
        elif operator == '<=':
            return metric_value <= expected_value
        elif operator == '==':
            return metric_value == expected_value
        elif operator == '!=':
            return metric_value != expected_value
        elif operator == 'exists':
            return bool(metric_value) == expected_value
        else:
            return False
    
    def _get_task_description(self, task_type: str) -> str:
        """Retorna descrição amigável da tarefa"""
        descriptions = {
            'clinical_documentation': 'Geração automática de documentação clínica da sessão',
            'administrative_scheduling': 'Agendamento automático de consultas de seguimento',
            'billing_coding': 'Codificação automática para faturamento médico',
            'fhir_integration': 'Sincronização automática com sistemas FHIR/EHR',
            'follow_up_automation': 'Criação automática de tarefas de acompanhamento'
        }
        return descriptions.get(task_type, f'Automação de {task_type}')
    
    def _check_monitoring_needed(self, metrics: Dict[str, Any]) -> bool:
        """Verifica se há necessidade de monitoramento"""
        return metrics.get('monitoring_required', False)
    
    def _analyze_historical_patterns(self, historical_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analisa padrões históricos para identificar tarefas recorrentes"""
        
        task_patterns = {}
        
        for session in historical_data:
            # Identificar tarefas que foram executadas
            executed_tasks = session.get('executed_tasks', [])
            
            for task in executed_tasks:
                task_type = task.get('type', 'unknown')
                time_spent = task.get('time_spent_minutes', 5)
                
                if task_type not in task_patterns:
                    task_patterns[task_type] = {
                        'task_type': task_type,
                        'frequency': 0,
                        'total_time': 0,
                        'avg_time_spent': 0
                    }
                
                task_patterns[task_type]['frequency'] += 1
                task_patterns[task_type]['total_time'] += time_spent
        
        # Calcular médias
        for pattern in task_patterns.values():
            pattern['avg_time_spent'] = pattern['total_time'] / pattern['frequency']
        
        return list(task_patterns.values())
    
    def _estimate_implementation_effort(self, task_type: str) -> str:
        """Estima esforço de implementação"""
        effort_map = {
            'clinical_documentation': 'low',
            'administrative_scheduling': 'medium',
            'billing_coding': 'medium',
            'fhir_integration': 'high',
            'follow_up_automation': 'low'
        }
        return effort_map.get(task_type, 'medium')
    
    def _calculate_automation_roi(self, time_saved_monthly: float, implementation_effort: str) -> float:
        """Calcula ROI da automação"""
        effort_cost = {
            'immediate': 0,
            'low': 10,      # 10 horas de implementação
            'medium': 40,   # 40 horas
            'high': 100     # 100 horas
        }
        
        implementation_hours = effort_cost.get(implementation_effort, 40)
        
        if implementation_hours == 0:
            return time_saved_monthly  # ROI infinito para implementação imediata
        
        # ROI = (tempo economizado por mês * 12 meses) / horas de implementação
        annual_savings = time_saved_monthly * 12
        roi = annual_savings / implementation_hours
        
        return roi
```

## DEPLOYMENT

### Deployment Script

```bash
#!/bin/bash
# deploy_autoagency.sh

set -e

echo "🚀 Deploying VOITHER AUTOAGENCY"

# Validate Sprint 6 dependencies
echo "🔍 Validating dependencies..."
./validate_sprint_6.sh

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
pip install celery==5.3.1 redis==4.6.0

# Setup Redis for task queue
echo "🔴 Setting up Redis task queue..."
kubectl apply -f k8s/redis-task-queue.yaml

# Setup Celery workers
echo "👷 Setting up Celery workers..."
kubectl apply -f k8s/celery-workers.yaml

# Initialize workflow templates
echo "📋 Setting up workflow templates..."
python scripts/initialize_templates.py

# Start AUTOAGENCY engine
echo "🤖 Starting AUTOAGENCY engine..."
python -c "
import asyncio
from src.autoagency.agency_engine import VoitherAutoAgency

async def test_autoagency():
    config = {
        'redis': {'host': 'redis-task-queue', 'port': 6379},
        'dsl_runtime': {'host': 'dsl-runtime-service'},
        'fhir': {'endpoint': '${FHIR_ENDPOINT}', 'enabled': True},
        'max_concurrent_automations': 5
    }
    
    autoagency = VoitherAutoAgency(config)
    
    assert await autoagency.start_automation_engine(), 'AUTOAGENCY failed to start'
    
    # Test automation detection
    test_session = {
        'med_analysis': {'global_confidence': 0.85, 'success': True, 'dimensions': {}},
        'apothecary_recommendations': {'global_confidence': 0.78, 'treatment_recommendations': [{}]},
        'patient_profile': {'patient_metadata': {'age': 35, 'sex': 'M'}}
    }
    
    result = await autoagency.process_clinical_session(test_session)
    assert result['success'], 'Session processing failed'
    
    await autoagency.stop_automation_engine()
    print(f'✅ AUTOAGENCY operational: {result[\"tasks_detected\"]} tasks detected')

asyncio.run(test_autoagency())
"

# Run integration tests
echo "🧪 Running AUTOAGENCY tests..."
pytest tests/integration/test_autoagency_integration.py -v

# Build Docker image
echo "🐳 Building Docker image..."
docker build -t voither-autoagency:latest .

# Deploy to production
echo "☸️ Deploying to production..."
kubectl apply -f k8s/autoagency-deployment.yaml
kubectl rollout status deployment/voither-autoagency

echo "✅ VOITHER AUTOAGENCY deployment completed!"
```

## VALIDATION

### Success Criteria (Binary Validation)

1. **Task Detection Intelligence**
   - [ ] Detects automation needs with >85% accuracy compared to manual review
   - [ ] Correctly prioritizes tasks based on clinical importance
   - [ ] Confidence scores correlate with actual automation success (r >0.75)
   - [ ] False positive rate <15% for task detection

2. **Workflow Execution**
   - [ ] All detected tasks execute successfully >90% of the time
   - [ ] DSL workflow integration functions correctly with .e/.Re runtime
   - [ ] Concurrent task execution supports 5+ parallel automations
   - [ ] Task timeout and error handling work correctly

3. **Administrative Automation**
   - [ ] Clinical documentation generation achieves >95% completeness
   - [ ] Scheduling automation creates valid appointments with correct timing
   - [ ] Billing code generation accuracy >90% compared to manual coding
   - [ ] FHIR integration successfully stores 100% of generated documents

4. **Time Savings and Efficiency**
   - [ ] Achieves >70% time savings compared to manual processes
   - [ ] Average automation processing time <3 seconds per session
   - [ ] System handles 100+ concurrent session automations
   - [ ] Error recovery and retry mechanisms function correctly

### Integration Tests

```python
# tests/integration/test_autoagency_integration.py
import pytest
import asyncio
from src.autoagency.agency_engine import VoitherAutoAgency
from src.apothecary.apothecary_engine import VoitherApothecary
from src.med.dimensional_extractor import DimensionalExtractor

@pytest.mark.asyncio
async def test_full_autoagency_pipeline():
    """Test complete MED → Apothecary → AUTOAGENCY pipeline"""
    
    # Setup complete pipeline
    med_config = {'spacy_model': 'pt_core_news_lg'}
    apothecary_config = {'models_dir': 'models/apothecary'}
    autoagency_config = {
        'redis': {'host': 'redis-test', 'port': 6379},
        'dsl_runtime': {'host': 'test'},
        'max_concurrent_automations': 3
    }
    
    med = DimensionalExtractor(med_config)
    apothecary = VoitherApothecary(apothecary_config)
    autoagency = VoitherAutoAgency(autoagency_config)
    
    # Start AUTOAGENCY
    assert await autoagency.start_automation_engine()
    
    try:
        # Simulate complete clinical session
        clinical_text = """
        Paciente relata sentir-se muito deprimido nas últimas 3 semanas.
        Dificuldade para dormir, perda de apetite, falta de energia.
        Pensamentos negativos recorrentes sobre o futuro.
        Dificuldade de concentração no trabalho.
        Nunca teve episódios assim antes.
        Nega uso de substâncias ou problemas médicos significativos.
        """
        
        # 1. Extract dimensions
        med_result = await med.extract_all_dimensions(clinical_text)
        assert med_result['success']
        
        # 2. Generate treatment recommendations
        patient_profile = {
            'patient_id': 'integration_test_001',
            'raw_dimensions': med_result['dimensions'],
            'calibrated_frameworks': {
                'rdoc': {'scores': {'negative_valence': 8.2}},
                'hitop': {'scores': {'internalizing': 7.8}},
                'perma': {'scores': {'positive_emotions': 2.1}},
                'bigfive': {'scores': {'neuroticism': 8.5}}
            },
            'patient_metadata': {
                'age': 42,
                'sex': 'M',
                'weight': 78,
                'medical_history': []
            }
        }
        
        apothecary_result = await apothecary.generate_treatment_recommendations(patient_profile)
        assert apothecary_result['success']
        
        # 3. Process through AUTOAGENCY
        session_data = {
            'med_analysis': med_result,
            'apothecary_recommendations': apothecary_result,
            'patient_profile': patient_profile,
            'session_metadata': {
                'session_id': 'integration_session_001',
                'duration_minutes': 45,
                'completeness_score': 0.92
            }
        }
        
        automation_result = await autoagency.process_clinical_session(session_data)
        
        # Validate automation results
        assert automation_result['success']
        assert automation_result['tasks_detected'] > 0
        assert automation_result['tasks_completed'] > 0
        assert automation_result['time_saved_minutes'] > 0
        
        # Check specific automations
        automation_outputs = automation_result['automated_outputs']
        
        # Should have clinical documentation
        assert len(automation_outputs['clinical_documentation']) > 0
        clinical_doc = automation_outputs['clinical_documentation'][0]
        assert 'document' in clinical_doc
        assert 'success' in clinical_doc
        
        # Should have administrative tasks
        assert 'administrative_tasks' in automation_outputs
        
        # Check FHIR integration if enabled
        if automation_outputs.get('system_integrations'):
            fhir_integration = automation_outputs['system_integrations'][0]
            assert 'success' in fhir_integration
        
    finally:
        await autoagency.stop_automation_engine()

@pytest.mark.asyncio
async def test_autoagency_task_detection_accuracy():
    """Test accuracy of intelligent task detection"""
    
    autoagency = VoitherAutoAgency({
        'redis': {'host': 'redis-test', 'port': 6379}
    })
    
    # Test cases with expected automations
    test_cases = [
        {
            'name': 'High confidence session with treatment',
            'session_data': {
                'med_analysis': {
                    'global_confidence': 0.88,
                    'success': True,
                    'dimensions': {f'v{i}_test': 5.0 for i in range(1, 16)}
                },
                'apothecary_recommendations': {
                    'global_confidence': 0.82,
                    'treatment_recommendations': [
                        {'medication_name': 'sertraline', 'follow_up_recommended': True}
                    ]
                },
                'patient_profile': {
                    'patient_metadata': {'age': 35, 'sex': 'F'},
                    'raw_dimensions': {f'v{i}_test': 5.0 for i in range(1, 16)}
                },
                'session_metadata': {
                    'duration_minutes': 50,
                    'completeness_score': 0.95
                }
            },
            'expected_tasks': ['clinical_documentation', 'administrative_scheduling', 'billing_coding']
        },
        {
            'name': 'Low confidence session',
            'session_data': {
                'med_analysis': {
                    'global_confidence': 0.45,
                    'success': True
                },
                'apothecary_recommendations': {
                    'global_confidence': 0.35,
                    'treatment_recommendations': []
                },
                'patient_profile': {'patient_metadata': {'age': 25, 'sex': 'M'}},
                'session_metadata': {
                    'duration_minutes': 15,
                    'completeness_score': 0.60
                }
            },
            'expected_tasks': []  # Should detect few or no tasks
        }
    ]
    
    for test_case in test_cases:
        detected_tasks = await autoagency.task_detector.detect_automation_needs(
            test_case['session_data']
        )
        
        detected_types = [task['type'] for task in detected_tasks]
        
        # Check if detected tasks align with expectations
        for expected_task in test_case['expected_tasks']:
            assert expected_task in detected_types, f"Expected {expected_task} not detected in {test_case['name']}"
        
        # High confidence should detect more tasks
        if test_case['name'].startswith('High confidence'):
            assert len(detected_tasks) >= 3, f"High confidence session should detect 3+ tasks, got {len(detected_tasks)}"
        elif test_case['name'].startswith('Low confidence'):
            assert len(detected_tasks) <= 1, f"Low confidence session should detect ≤1 tasks, got {len(detected_tasks)}"

@pytest.mark.asyncio
async def test_autoagency_time_savings():
    """Test that AUTOAGENCY actually saves time"""
    
    autoagency_config = {'redis': {'host': 'redis-test', 'port': 6379}}
    autoagency = VoitherAutoAgency(autoagency_config)
    
    await autoagency.start_automation_engine()
    
    try:
        # Process multiple sessions to test time savings
        test_sessions = []
        for i in range(5):
            session_data = {
                'med_analysis': {
                    'global_confidence': 0.85,
                    'success': True,
                    'dimensions': {f'v{j}_test': 5.0 for j in range(1, 16)}
                },
                'apothecary_recommendations': {
                    'global_confidence': 0.80,
                    'treatment_recommendations': [{'medication_name': f'med_{i}'}]
                },
                'patient_profile': {
                    'patient_id': f'time_test_{i}',
                    'patient_metadata': {'age': 30 + i, 'sex': 'M' if i % 2 else 'F'}
                },
                'session_metadata': {
                    'duration_minutes': 40,
                    'completeness_score': 0.90
                }
            }
            test_sessions.append(session_data)
        
        total_time_saved = 0
        for session_data in test_sessions:
            result = await autoagency.process_clinical_session(session_data)
            if result['success']:
                total_time_saved += result.get('time_saved_minutes', 0)
        
        # Should save significant time across multiple sessions
        assert total_time_saved > 30, f"Expected >30 minutes saved across 5 sessions, got {total_time_saved}"
        
        # Check automation statistics
        stats = autoagency.get_automation_statistics()
        assert stats['operational_stats']['successful_automations'] >= 5
        assert stats['operational_stats']['time_saved_hours'] > 0.5
        
    finally:
        await autoagency.stop_automation_engine()
```

## OUTPUTS GENERATED

Upon successful completion, this sprint generates:

1. **Production AUTOAGENCY System**
   - Complete automation engine with intelligent task detection
   - DSL workflow orchestration using .e/.Re runtime
   - Administrative task automation (documentation, scheduling, billing)
   - FHIR/EHR system integration capabilities

2. **Clinical Workflow Automation**
   - Automatic clinical documentation generation from MED/Apothecary data
   - Intelligent scheduling of follow-up appointments
   - Automated billing code generation and submission
   - Treatment monitoring and reminder creation

3. **Task Intelligence Engine**
   - ML-powered detection of automation opportunities
   - Confidence scoring and task prioritization
   - Historical pattern analysis for continuous improvement
   - Real-time adaptation to clinical workflows

4. **Administrative Efficiency Tools**
   - Time tracking and savings measurement
   - Automation ROI analysis and reporting
   - Integration with existing clinical systems
   - Error handling and task retry mechanisms

**This sprint completes the administrative automation layer of VOITHER, creating a comprehensive system that reduces manual overhead and allows clinicians to focus on direct patient care while maintaining full compliance and documentation standards.**