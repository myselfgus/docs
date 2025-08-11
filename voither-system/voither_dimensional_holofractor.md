# Manual de Operações do Motor de Extração Dimensional (MED)
## Compêndio das 15 Dimensões Fundamentais do Espaço Mental ℳ

---

## Introdução

Este documento detalha a função de cada vetor-campo que constitui o Espaço Mental ℳ. Juntas, elas formam a base para a Geometria Computacional da Mente, permitindo a criação de um "gêmeo digital" da psique, extraído da linguagem e renderizado visualmente.

Cada dimensão será detalhada em **seis facetas críticas**:

1. **Definição Funcional:** O que a dimensão representa em termos psicológicos.
2. **Justificativa Clínica:** Por que esta dimensão é crucial para a avaliação psiquiátrica.
3. **Método de Extração:** Como a extraímos da linguagem (áudio e texto).
4. **Formalização Matemática:** A equação ou algoritmo que a calcula.
5. **Renderização no Holofractor Mental:** O seu papel específico na visualização 3D.
6. **Relação com Frameworks (RDoC/HiTOP):** Como ela se conecta aos modelos de pesquisa atuais.

---

## Meta-Dimensão Afetiva: O Terreno Emocional

Esta meta-dimensão descreve a qualidade e a dinâmica da experiência emocional.

### 1. Valência Emocional (v₁)

#### Definição Funcional
A polaridade hedônica da experiência; o grau de prazer ou desprazer, variando de um estado negativo (tristeza, raiva) a um positivo (alegria, serenidade).

#### Justificativa Clínica
É o indicador mais direto do humor. Essencial para diagnosticar e monitorar transtornos de humor (depressão, mania), ansiedade e o bem-estar geral.

#### Método de Extração
Análise de sentimento do texto, utilizando modelos de linguagem (como BERT ou serviços do Azure Language) que são sensíveis ao contexto, negações e intensificadores.

#### Formalização Matemática
$$v₁(t) = \int K(t-τ) \left[ \sum_i s(\text{palavra}_i(τ)) \cdot w_i \right] dτ$$

Uma integral de convolução que calcula a soma ponderada do sentimento (`s`) das palavras recentes, com um kernel de decaimento exponencial (`K`) que modela a inércia e a memória do humor.

#### Renderização no Holofractor
Controla a **Cor Base (Matiz)**. O espectro de cores é mapeado de vermelho (valência -5) a verde/azul (valência +5), passando por tons neutros de amarelo.

#### Relação com Frameworks
Corresponde diretamente aos construtos de "Sistemas de Valência Negativa" e "Sistemas de Valência Positiva" do **RDoC**.

### 2. Arousal / Ativação (v₂)

#### Definição Funcional
O nível de ativação neurofisiológica e energia, variando de um estado de baixa energia (sonolência, letargia) a um de alta energia (agitação, excitação).

#### Justificativa Clínica
Crucial para diferenciar estados emocionais (ex: ansiedade [alto arousal] vs. depressão [baixo arousal]) e para avaliar o nível de energia psicomotora do paciente.

#### Método de Extração
Primariamente da análise prosódica do áudio (velocidade da fala, volume, variância do pitch) e secundariamente de marcadores lexicais no texto ("agitado", "cansado").

#### Formalização Matemática
$$v₂(t) = α \cdot σ(F₀(t)) + β \cdot E(\text{sinal}(t))$$

Uma combinação ponderada da variância da frequência fundamental (`σ(F₀)`) e da energia do sinal de voz (`E(sinal)`).

#### Renderização no Holofractor
Controla a **Saturação da Cor** e a **Frequência de Pulsão** da forma. Alto arousal torna a cor mais vibrante e a animação de pulsão mais rápida.

#### Relação com Frameworks
Alinha-se com o construto "Sistemas de Arousal e Regulatórios" do **RDoC**.

### 3. Dominância / Agência (v₉)

#### Definição Funcional
O senso de controle, poder e autoria sobre as próprias ações e o ambiente. Varia de um sentimento de impotência a um de empoderamento.

#### Justificativa Clínica
Central para avaliar a autoestima, autoeficácia e o locus de controle. Baixa agência é comum na depressão e em traumas; alta agência é um indicador de resiliência.

#### Método de Extração
Análise sintática da proporção de verbos na voz ativa vs. passiva e análise lexical da densidade de palavras de agência ("eu decidi", "eu consigo", "eu fiz").

#### Formalização Matemática
$$v₉(t) = \frac{\text{contagem\_voz\_ativa}}{\text{contagem\_total\_vozes}} \cdot \text{Densidade}(\text{palavras de agência})$$

#### Renderização no Holofractor
Controla o **Raio Base / Tamanho Geral**. Alta agência expande a forma, representando uma maior "presença" e ocupação do espaço pelo self.

#### Relação com Frameworks
Relaciona-se com o espectro de "Internalização" do **HiTOP**, onde baixa agência é um fator de vulnerabilidade.

### 4. Prosódia Emocional (v₁₅)

#### Definição Funcional
A "melodia" ou contorno musical da fala que transmite emoções sutis, independentemente das palavras usadas (ex: sarcasmo, ternura, hesitação).

#### Justificativa Clínica
Captura o afeto "real" que pode ser incongruente com o conteúdo verbal (afeto embotado, incongruente), crucial para o diagnóstico de esquizofrenia, depressão e autismo.

#### Método de Extração
Análise do sinal de áudio para extrair características acústicas avançadas como jitter (variação da frequência), shimmer (variação da amplitude) e contornos de entonação.

#### Formalização Matemática
$$v₁₅(t) = [\text{jitter}(t), \text{shimmer}(t), \text{slope}(F₀(t))]$$

Representado como um vetor de características acústicas, não um único número.

#### Renderização no Holofractor
Controla a **Micro-vibração da Textura** da superfície. Uma voz trêmula (alto jitter/shimmer) cria uma textura visualmente vibratória e instável.

#### Relação com Frameworks
Contribui para os "Sistemas de Percepção Social" do **RDoC**, especificamente na comunicação não-verbal.

---

## Meta-Dimensão Cognitiva: A Estrutura do Pensamento

### 5. Coerência Narrativa (v₃)

#### Definição Funcional
A organização lógica, causal e temporal do discurso. A capacidade de contar uma história de forma que as partes se conectem significativamente.

#### Justificativa Clínica
Um dos indicadores mais importantes de transtornos do pensamento, como os encontrados na esquizofrenia. Baixa coerência pode indicar confusão ou desorganização cognitiva.

#### Método de Extração
Análise da similaridade semântica entre sentenças ou cláusulas consecutivas usando embeddings vetoriais (ex: BERT, spaCy).

#### Formalização Matemática
$$v₃(t) = E[\cos(θ(\text{emb}(s_i), \text{emb}(s_{i+1})))]$$

A média da similaridade cosseno entre os vetores de sentenças adjacentes.

#### Renderização no Holofractor
Controla a **Suavidade vs. Rugosidade** da geometria. Alta coerência produz uma superfície lisa e orgânica; baixa coerência cria uma textura caótica e ruidosa.

#### Relação com Frameworks
Central para o construto "Sistemas Cognitivos" do **RDoC**, especialmente funções executivas e controle cognitivo.

### 6. Complexidade Sintática (v₄)

#### Definição Funcional
A sofisticação e elaboração das estruturas gramaticais utilizadas.

#### Justificativa Clínica
Reflete a capacidade de pensamento abstrato e função executiva. Uma redução na complexidade pode ser um sinal precoce de deterioração cognitiva ou de embotamento afetivo.

#### Método de Extração
Análise sintática (parsing) para medir a profundidade das árvores de dependência, o uso de orações subordinadas e a variedade de estruturas gramaticais.

#### Formalização Matemática
$$v₄(t) = - \sum_i p(\text{regra}_i) \cdot \log₂(p(\text{regra}_i))$$

A entropia de Shannon sobre a distribuição de regras de produção sintática usadas.

#### Renderização no Holofractor
Adiciona **Camadas de Detalhe Fractal** à superfície. Maior complexidade gera um relevo geométrico mais intrincado e detalhado.

#### Relação com Frameworks
Alinha-se com os "Sistemas Cognitivos" do **RDoC**.

### 7. Orientação Temporal (v₅)

#### Definição Funcional
O foco predominante do discurso no contínuo passado, presente ou futuro.

#### Justificativa Clínica
Altamente diagnóstico. Foco excessivo no passado está ligado à ruminação e depressão. Foco no futuro à ansiedade e planejamento. Foco no presente ao mindfulness e bem-estar.

#### Método de Extração
Análise de tempos verbais, advérbios de tempo e outras palavras-chave temporais.

#### Formalização Matemática
$$v₅(t) = (p_{\text{passado}}, p_{\text{presente}}, p_{\text{futuro}})$$

Coordenadas baricêntricas em um simplexo (triângulo), garantindo que a soma das proporções seja 1.

#### Renderização no Holofractor
Controla a **Cor da Aura** de partículas. Ex: Vermelho para o passado, Branco para o presente, Azul para o futuro. A mistura das cores na aura representa a distribuição do foco.

#### Relação com Frameworks
Relaciona-se com múltiplos domínios, incluindo "Sistemas de Valência Negativa" (ruminação) e "Sistemas Cognitivos" (planejamento futuro) do **RDoC**.

### 8. Flexibilidade Discursiva (v₈)

#### Definição Funcional
A capacidade de mudar de perspectiva, adaptar o pensamento e transitar suavemente entre diferentes tópicos.

#### Justificativa Clínica
A rigidez cognitiva é uma característica central de transtornos como o TOC e certos transtornos de personalidade. A flexibilidade é um marcador de saúde mental adaptativa.

#### Método de Extração
Análise da trajetória do discurso em um espaço vetorial semântico. Mudanças de tópico são detectadas como mudanças de direção na trajetória.

#### Formalização Matemática
$$v₈(t) = \left\| \frac{d}{dt} \left[ \frac{T(t)}{||T(t)||} \right] \right\|$$

A curvatura da trajetória no espaço semântico, onde `T(t)` é o vetor do tópico dominante.

#### Renderização no Holofractor
Modula a **Elasticidade da Física** do objeto. Alta flexibilidade torna a forma maleável e responsiva; baixa flexibilidade a torna rígida e quebradiça.

#### Relação com Frameworks
Um componente chave do "Controle Cognitivo" dentro dos "Sistemas Cognitivos" do **RDoC**.

### 9. Fragmentação do Discurso (v₁₀)

#### Definição Funcional
A quebra do fluxo lógico e gramatical da fala, manifestada em frases incompletas, pausas inadequadas, e associações frouxas.

#### Justificativa Clínica
Um sintoma clássico de transtornos do pensamento, especialmente na esquizofrenia. Também pode indicar estados de ansiedade extrema ou sobrecarga cognitiva.

#### Método de Extração
Análise da sintaxe local, frequência de pausas preenchidas ("uhm", "ah"), e a distância semântica entre palavras consecutivas.

#### Formalização Matemática
$$v₁₀(t) = H_{\text{local}}(t) + γ \cdot (\text{contagem de disfluências})$$

A entropia local da distribuição de palavras (imprevisibilidade) mais uma penalidade por disfluências.

#### Renderização no Holofractor
Causa a **Fragmentação Geométrica**. A forma principal se quebra em múltiplos fragmentos que se afastam do centro, com a distância sendo proporcional a `v₁₀`.

#### Relação com Frameworks
Alinha-se com o espectro de "Psicoticismo" do **HiTOP**.

### 10. Densidade Semântica (v₁₁)

#### Definição Funcional
A riqueza de informação e significado por unidade de linguagem. Discursos de baixa densidade são vagos, repetitivos ou cheios de palavras de função.

#### Justificativa Clínica
Pode indicar pobreza de pensamento (alogia) em transtornos psicóticos, ou evasividade em transtornos de personalidade.

#### Método de Extração
Cálculo da proporção de palavras de conteúdo (substantivos, verbos, adjetivos) versus palavras de função (artigos, preposições).

#### Formalização Matemática
$$v₁₁(t) = \frac{\text{contagem\_palavras\_conteúdo}}{\text{contagem\_total\_palavras}}$$

#### Renderização no Holofractor
Controla a **Densidade de Partículas Internas**. Se o Holofractor for transparente, um "enxame" de partículas luminosas em seu interior se torna mais denso com o aumento de `v₁₁`.

#### Relação com Frameworks
Relaciona-se com a "Fluência" dentro dos "Sistemas Cognitivos" do **RDoC**.

### 11. Padrões de Conectividade (v₁₃)

#### Definição Funcional
O uso de raciocínio lógico e causal, explicitado através de conectivos linguísticos.

#### Justificativa Clínica
Reflete a capacidade de pensamento abstrato e de construir argumentos lógicos. Sua ausência pode indicar pensamento concreto ou desorganizado.

#### Método de Extração
Contagem da frequência de conjunções lógicas e causais ("porque", "então", "portanto", "se...então").

#### Formalização Matemática
$$v₁₃(t) = \frac{\text{contagem}(\text{conectivos\_lógicos})}{\text{total de sentenças}}$$

#### Renderização no Holofractor
Controla a **Estrutura de Rede Interna**. Uma teia de "andaimes" luminosos visível dentro do objeto, cuja densidade e complexidade aumentam com `v₁₃`.

#### Relação com Frameworks
Central para as "Funções Executivas" dentro dos "Sistemas Cognitivos" do **RDoC**.

### 12. Comunicação Pragmática (v₁₄)

#### Definição Funcional
A habilidade de usar a linguagem de forma socialmente apropriada, considerando o contexto, as regras implícitas da conversação e a perspectiva do ouvinte.

#### Justificativa Clínica
Déficits pragmáticos são uma característica marcante do Transtorno do Espectro Autista e de transtornos de comunicação social.

#### Método de Extração
Requer um modelo de ML treinado para classificar atos de fala (ex: pedir, afirmar, perguntar) e avaliar sua adequação ao contexto da díade terapêutica.

#### Formalização Matemática
$$v₁₄(t) = P(\text{ato\_de\_fala}_i | \text{contexto})$$

A probabilidade de um ato de fala ser apropriado, dado o estado atual da conversa.

#### Renderização no Holofractor
Regula a **Dinâmica do Campo de Partículas da Aura**. Alta pragmática gera um fluxo orbital, suave e harmônico; baixa pragmática gera um fluxo caótico, com partículas colidindo.

#### Relação com Frameworks
Mapeia diretamente para os "Sistemas de Percepção Social" do **RDoC**.

---

## Meta-Dimensão de Agência: A Expressão do Self no Mundo

### 13. Densidade de Autoreferência (v₆)

#### Definição Funcional
O grau em que o discurso é focado no "eu" em oposição ao mundo externo, outras pessoas ou ideias abstratas.

#### Justificativa Clínica
Alta autoreferência é um marcador robusto para ruminação, preocupação e depressão. Baixa autoreferência pode indicar distanciamento ou foco em relacionamentos.

#### Método de Extração
Cálculo da proporção de pronomes de primeira pessoa singular ("eu", "meu", "mim") em relação ao total de pronomes.

#### Formalização Matemática
$$v₆(t) = \frac{\text{contagem}(\text{"eu", "meu", ...})}{\text{contagem\_total\_pronomes}}$$

#### Renderização no Holofractor
Controla a **Opacidade vs. Transparência**. Alta autoreferência torna o objeto opaco e com alta refletividade (voltado para si); baixa o torna translúcido e etéreo.

#### Relação com Frameworks
Relaciona-se com o espectro de "Internalização" do **HiTOP**.

### 14. Linguagem Social (v₇)

#### Definição Funcional
A quantidade e qualidade das referências a outras pessoas e interações sociais.

#### Justificativa Clínica
Um indicador direto do engajamento e da qualidade do mundo social do indivíduo. Baixa pontuação pode indicar isolamento, ansiedade social ou anedonia social.

#### Método de Extração
Contagem ponderada de pronomes de outras pessoas ("ele", "ela", "eles"), nomes próprios e verbos de interação social ("conversar", "encontrar").

#### Formalização Matemática
$$v₇(t) = \sum w_i \cdot \text{freq}(\text{palavra\_social}_i)$$

#### Renderização no Holofractor
Gera **Filamentos de Conexão** que emergem da superfície. O número, comprimento e brilho desses "tentáculos" de luz são proporcionais a `v₇`.

#### Relação com Frameworks
Alinha-se com os "Sistemas de Percepção Social" do **RDoC** e o espectro de "Desapego" do **HiTOP**.

### 15. Marcadores de Certeza/Incerteza (v₁₂)

#### Definição Funcional
O grau de convicção, confiança ou dúvida que o falante expressa em suas declarações.

#### Justificativa Clínica
A incerteza crônica é um pilar da ansiedade generalizada. O pensamento excessivamente certo e rígido ("preto no branco") é característico de certos transtornos de personalidade.

#### Método de Extração
Análise lexical para contar a frequência de palavras e frases que indicam certeza ("sempre", "definitivamente") versus incerteza ("talvez", "acho que").

#### Formalização Matemática
$$v₁₂(t) = \frac{\text{Freq}(\text{certeza}) - \text{Freq}(\text{incerteza})}{\text{Freq}(\text{certeza}) + \text{Freq}(\text{incerteza})}$$

Uma razão normalizada variando de -1 (total incerteza) a +1 (total certeza).

#### Renderização no Holofractor
Controla a **Nitidez das Bordas**. Alta certeza cria bordas nítidas e cristalinas; alta incerteza cria um efeito de "desfoque" ou "névoa" nos contornos da forma.

#### Relação com Frameworks
Relaciona-se com o espectro de "Internalização" do **HiTOP** (preocupação, ansiedade) e "Antagonismo" (rigidez).

---

## Conclusão

Este manual fornece a especificação técnica completa de cada dimensão do Espaço Mental ℳ. Cada dimensão foi rigorosamente definida em termos de sua relevância clínica, método de extração, formalização matemática e papel na visualização.

Juntas, essas 15 dimensões formam um sistema coeso e abrangente para capturar, quantificar e visualizar a complexidade da experiência mental humana, representando uma evolução fundamental na interface entre tecnologia e cuidados de saúde mental.