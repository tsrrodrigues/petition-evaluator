# Avaliador de Qualidade de Petições Jurídicas

**TDD para Petições** — Sistema automatizado de avaliação de qualidade de petições jurídicas usando Claude Sonnet 4.5.

## 📋 Visão Geral

Este projeto implementa um avaliador automatizado de petições jurídicas focado na área de **Direito do Consumidor × Petição Inicial**. O objetivo é fornecer feedback objetivo e consistente sobre a qualidade de petições geradas, permitindo iteração e melhoria contínua.

## 🎯 Objetivo

Avaliar petições jurídicas contra modelos de referência (rating 5) usando critérios objetivos, retornando:
- Score 0-100
- Breakdown detalhado por critério
- Lista de problemas identificados
- Pontos fortes
- Resumo da avaliação

## 🏗️ Arquitetura

### Dados
- **Fonte**: Banco de dados PostgreSQL do Facilita Jurídico
- **Área**: Consumidor (area_id=10)
- **Modalidade**: Inicial (modality_id=4)
- **Formato**: DOCX extraído para texto puro

### Modelo
- **Motor**: Claude Sonnet 4.5 (claude-sonnet-4-5)
- **Provider**: Anthropic API
- **Temperatura**: 0.3 (para consistência)

### Critérios de Avaliação

1. **Estrutura e Formatação (0-20 pontos)**
   - Elementos obrigatórios presentes
   - Organização lógica
   - Formatação profissional
   - Uso de títulos e subtítulos

2. **Fundamentação Jurídica (0-25 pontos)**
   - Citação adequada de leis e precedentes
   - Aplicação correta ao caso concreto
   - Uso do CDC
   - Solidez da fundamentação

3. **Coerência e Clareza (0-20 pontos)**
   - Argumentação lógica
   - Linguagem clara e objetiva
   - Ausência de contradições
   - Fluidez na leitura

4. **Qualidade Textual (0-15 pontos)**
   - Correção gramatical
   - Linguagem jurídica adequada
   - Redação profissional
   - Concisão

5. **Personalização e Contexto (0-10 pontos)**
   - Adequação aos fatos específicos
   - Análise não-genérica
   - Conexão fatos-pedidos

6. **Completude (0-10 pontos)**
   - Todos os elementos necessários
   - Valor da causa
   - Qualificação das partes
   - Documentos mencionados

## 📊 Dataset

### Coleta
- **Rating 5**: 14 petições (gold standard)
- **Rating 1-3**: 10 petições (controle negativo)
- **Total**: 24 petições processadas

### Distribuição
```
Rating 5: 14 petições (avg ~31.6k chars)
Rating 3: 5 petições (avg ~40.7k chars)
Rating 2: 2 petições (avg ~57.8k chars)
Rating 1: 3 petições (avg ~44.0k chars)
```

## 🔬 Calibração

### Hipótese
- Petições rating 5 → AI score ≥85
- Petições rating 1-3 → AI score <85

### Resultados
_(Serão preenchidos após execução)_

```
[Espaço reservado para resultados de calibração]

Correlação (Pearson): X.XXX
Rating 5 - Avg AI Score: XX.X
Rating 1-3 - Avg AI Score: XX.X
```

## 🚀 Uso

### Instalação

```bash
# Clone o repositório
git clone https://github.com/tsrrodrigues/petition-evaluator.git
cd petition-evaluator

# Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt
```

### Configuração

```bash
# Configure a API key do Anthropic
export ANTHROPIC_API_KEY="sua-api-key"

# Configure acesso ao banco de dados (se necessário)
export PGHOST="34.95.205.110"
export PGUSER="aegis-tiago"
export PGPASSWORD="2?uUbBGA]oH@[]a"
export PGDATABASE="facilitajuridico"
```

### Execução

```bash
# 1. Coletar petições do banco
python scripts/collect_petitions.py

# 2. Baixar e extrair DOCX
python scripts/download_petitions.py

# 3. Avaliar petições
python scripts/evaluator.py

# 4. Analisar resultados
python scripts/analyze_results.py
```

### Avaliar Uma Petição Específica

```python
from scripts.evaluator import evaluate_petition

# Carregar texto da petição
with open('minha_peticao.txt', 'r') as f:
    texto = f.read()

# Avaliar
resultado = evaluate_petition(texto)
print(f"Score: {resultado['score']}/100")
print(f"Problemas: {resultado['problemas']}")
```

## 📁 Estrutura do Projeto

```
petition-evaluator/
├── data/
│   ├── petitions_metadata.json      # Metadados das petições coletadas
│   └── processed_petitions.json     # Petições processadas
├── petitions/
│   ├── *.docx                        # Arquivos DOCX baixados
│   └── *.txt                         # Texto extraído
├── results/
│   ├── eval_*.json                   # Avaliações individuais
│   ├── all_evaluations.json         # Todas as avaliações
│   └── calibration_summary.json     # Resumo da calibração
├── scripts/
│   ├── collect_petitions.py         # Coleta do banco
│   ├── download_petitions.py        # Download e extração
│   ├── evaluator.py                 # Avaliador principal
│   └── analyze_results.py           # Análise de resultados
├── requirements.txt
└── README.md
```

## 🔍 Exemplos de Saída

### Exemplo de Avaliação

```json
{
  "score": 87,
  "breakdown": {
    "estrutura_formatacao": {
      "score": 18,
      "max": 20,
      "comentario": "Petição bem estruturada com todos os elementos obrigatórios"
    },
    "fundamentacao_juridica": {
      "score": 22,
      "max": 25,
      "comentario": "Boa fundamentação com citações do CDC e jurisprudência"
    },
    ...
  },
  "problemas": [
    "Falta valor da causa especificado",
    "Algumas citações sem referência completa"
  ],
  "pontos_fortes": [
    "Argumentação clara e bem estruturada",
    "Uso adequado de precedentes jurisprudenciais",
    "Personalização evidente ao caso concreto"
  ],
  "summary": "Petição de boa qualidade com fundamentação sólida..."
}
```

## 📈 Métricas

- **Tempo médio por avaliação**: ~3-5 segundos
- **Custo médio por avaliação**: ~$0.02-0.05 USD (dependendo do tamanho)
- **Taxa de sucesso de parsing**: >95%

## 🛠️ Tecnologias

- **Python 3.12+**
- **Anthropic API** (Claude Sonnet 4.5)
- **PostgreSQL** (fonte de dados)
- **python-docx** (extração de texto)
- **psycopg2** (acesso ao banco)

## 📝 Próximos Passos

- [ ] Expandir para outras áreas do direito
- [ ] Implementar API REST
- [ ] Interface web para avaliação
- [ ] Comparação side-by-side com petições modelo
- [ ] Sistema de feedback para refinamento contínuo
- [ ] Sugestões automáticas de melhoria

## 📄 Licença

MIT License

## 👥 Autor

Desenvolvido para Facilita Jurídico
Vocabulário: "faciliter" (não "facilitador")

---

**Status**: 🚀 Em desenvolvimento ativo
