---
title: "Main Automation Pipeline Flow"
description: "Complete visual flow of the main auto-documentation update pipeline"
version: "1.0"
last_updated: "2025-01-19"
audience: ["developers", "maintainers"]
priority: "essential"
reading_time: "8 minutes"
tags: ["automation", "pipeline", "workflow", "mermaid", "github-actions"]
---

# 🔄 Main Automation Pipeline Flow

## Fluxo Principal de Automação de Documentação

Este diagrama mostra **exatamente** o que acontece quando você faz upload ou commit de arquivos no repositório.

```mermaid
flowchart TD
    A[👤 User faz Upload/Commit] --> B{📁 Arquivos Relevantes?}
    B -->|✅ .md/.py/.js/.ts/.json/.yml| C[🔍 Detectar Mudanças]
    B -->|❌ Outros arquivos| Z[🚫 Nenhuma Ação]
    
    C --> D{📝 Tipos de Mudança}
    D -->|📄 Novos Arquivos| E[📊 Análise de Novos Conteúdos]
    D -->|✏️ Arquivos Editados| F[🔍 Análise de Modificações]
    D -->|🗑️ Arquivos Removidos| G[🧹 Limpeza de Referências]
    
    E --> H[🐍 Setup Python Environment]
    F --> H
    G --> H
    
    H --> I[📦 Instalar Dependências]
    I -->|✅ requirements.txt existe| J[pip install -r requirements.txt]
    I -->|❌ Fallback| K[pip install requests pyyaml python-frontmatter markdownify beautifulsoup4]
    
    J --> L[🔧 Executar Validação]
    K --> L
    
    L --> M{🚨 Erros Críticos?}
    M -->|✅ Sucesso| N[📊 Gerar Estatísticas]
    M -->|❌ Erros| ERROR1[⚠️ Log de Erros]
    
    N --> O[🤖 Preparar Prompt para Copilot]
    O --> P[🏷️ Adicionar Frontmatter Faltante]
    
    P --> Q{📝 Novos Arquivos .md?}
    Q -->|✅ Sim| R[📚 Atualizar DOCUMENTATION_INDEX.md]
    Q -->|❌ Não| S[🔄 Atualizar Knowledge Graph]
    
    R --> S
    S --> T[🔗 Validar Links Internos]
    
    T --> U{🔍 Links Quebrados?}
    U -->|✅ Todos válidos| V[📋 Criar Resumo de Atualização]
    U -->|❌ Links quebrados| ERROR2[⚠️ Log de Links Quebrados]
    
    ERROR2 --> V
    V --> W{💾 Há Mudanças para Commit?}
    
    W -->|✅ Sim| X[📝 Commit Automático]
    W -->|❌ Não| Y[📝 Log: Nenhuma Mudança]
    
    X --> BRANCH{🌿 Branch Principal?}
    BRANCH -->|✅ main| PUSH[🚀 Push para Repositório]
    BRANCH -->|❌ outras| COMMIT_ONLY[📝 Apenas Commit Local]
    
    PUSH --> SUCCESS[✅ Atualização Completa]
    COMMIT_ONLY --> SUCCESS
    Y --> SUCCESS
    
    ERROR1 --> NOTIFY[🔔 Notificar Erros]
    NOTIFY --> END[🏁 Fim do Processo]
    SUCCESS --> END
    
    %% Styling
    classDef user fill:#e1f5fe
    classDef process fill:#f3e5f5
    classDef decision fill:#fff3e0
    classDef success fill:#e8f5e8
    classDef error fill:#ffebee
    classDef action fill:#e3f2fd
    
    class A user
    class C,H,I,L,N,O,P,R,S,T,V,X process
    class B,D,M,Q,U,W,BRANCH decision
    class SUCCESS,PUSH success
    class ERROR1,ERROR2,NOTIFY error
    class J,K,COMMIT_ONLY,Y action
```

## 🎯 Detalhamento das Etapas

### **🔍 1. Detecção de Mudanças**
```bash
# Arquivos monitorados
MONITORED_EXTENSIONS = ['.md', '.py', '.js', '.ts', '.json', '.yml', '.yaml']

# Comando de detecção
git diff --name-only HEAD~1 HEAD | grep -E '\.(md|py|js|ts|json|yml|yaml)$'
```

### **🏷️ 2. Adição de Frontmatter Automático**
```yaml
# Template automático aplicado
---
title: "Título Gerado Automaticamente"
description: "Descrição baseada no conteúdo"
version: "1.0"
last_updated: "2025-01-19"
audience: ["general"]
priority: "important"
reading_time: "X minutes"  # Calculado automaticamente
tags: ["documentation"]
---
```

### **📊 3. Atualização de Estatísticas**
```python
# Estatísticas calculadas automaticamente
total_md_files = count_markdown_files()
total_lines = count_total_lines()
files_with_frontmatter = count_frontmatter_compliance()
broken_links = validate_internal_links()
```

### **🔄 4. Atualização do Knowledge Graph**
```python
# Entrada automática adicionada
automation_entry = f'''
### **AUTOMATED DOCUMENTATION UPDATE** 🤖
*Atualização automática executada em {timestamp}*

#### **Arquivos Processados**
- Changed files: {changed_files_list}
- Validation: ✅ Executada
- Frontmatter: ✅ Atualizado
- Index: ✅ Regenerado
- Links: ✅ Validados
'''
```

## 🚨 Tratamento de Erros e Fallbacks

### **Erro: requirements.txt não encontrado**
```bash
# Fallback automático
if [ ! -f requirements.txt ]; then
    echo "Installing fallback dependencies..."
    pip install requests pyyaml python-frontmatter markdownify beautifulsoup4
fi
```

### **Erro: Validação de links falhando**
```bash
# Continua mesmo com warnings
make validate || echo "Validation completed with warnings"
python scripts/validate-docs.py || echo "Link validation completed with warnings"
```

### **Erro: Sem permissões de push**
```bash
# Commit local apenas
if [[ "${{ github.ref_name }}" != "main" ]]; then
    echo "Documentation updates committed (push skipped for non-main branch)"
fi
```

## ⚡ Frequência de Execução

| Trigger | Frequência | Ação |
|---------|------------|------|
| **Push para main** | Imediato | Execução completa + Push |
| **Push para outras branches** | Imediato | Execução completa + Commit local |
| **Pull Request** | Imediato | Execução + Comentário no PR |
| **Manual Dispatch** | On-demand | Execução personalizada |

## 📝 Logs e Monitoramento

### **Exemplo de Log de Sucesso**
```
✅ Documentation automation workflow completed
📊 Total Documents: 42
📏 Total Lines: 27,118
🔗 Links Validated: 253 (0 broken)
⏱️ Execution Time: 2m 34s
🎯 Files Updated: 5
```

### **Exemplo de Log com Warnings**
```
⚠️ Documentation automation completed with warnings
🔍 Validation: 3 warnings found
🔗 Links: 2 broken links detected
📝 Frontmatter: 1 file missing metadata
🔧 Action: Issues logged for manual review
```

---

**Resultado**: Toda vez que você faz upload/commit, este fluxo **executa automaticamente** e mantém a documentação sempre atualizada e validada! ✨