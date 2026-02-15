# Exemplo de Avaliação

## Petição Analisada

**ID**: 11447  
**Rating do Cliente**: ⭐⭐⭐⭐⭐ (5/5)  
**Tamanho**: 19.271 caracteres  
**Área**: Direito do Consumidor  
**Tipo**: Petição Inicial

---

## 📊 Score Total: 86/100

### Breakdown Detalhado

#### 🏗️ Estrutura e Formatação: 20/20 ✅
**Comentário**: Análise da presença de elementos estruturais obrigatórios

- ✅ Endereçamento ao juízo correto
- ✅ Qualificação completa das partes
- ✅ Organização em seções lógicas
- ✅ Uso adequado de títulos e subtítulos

---

#### ⚖️ Fundamentação Jurídica: 25/25 ✅
**Comentário**: 15 artigos citados, 9 precedentes

**Artigos Identificados**:
- Art. 109, §2º da Constituição Federal
- Art. 51 do Código de Processo Civil
- Art. 281 e 282 do Código de Trânsito Brasileiro
- Art. 3º da Resolução CONTRAN nº 149/2003
- Art. 300 do CPC (tutela de urgência)

**Jurisprudência**:
- Súmula nº 473 do STF
- Súmula nº 312 do STJ
- TJ-SP (múltiplos acórdãos)
- Precedentes bem aplicados ao caso

---

#### 💬 Coerência e Clareza: 15/20 ⚠️
**Comentário**: Avaliação baseada na extensão e organização do texto

- ✅ Argumentação lógica
- ✅ Linguagem jurídica adequada
- ⚠️ Algumas seções poderiam ser mais concisas

---

#### ✍️ Qualidade Textual: 8/15 ⚠️
**Comentário**: Presença de placeholders detectada

- ✅ Boa redação geral
- ✅ Correção gramatical
- ⚠️ Alguns placeholders não preenchidos (___em RG/CPF)

---

#### 🎯 Personalização e Contexto: 8/10 ✅
**Comentário**: Adequação aos fatos específicos do caso

- ✅ Caso concreto bem descrito
- ✅ Conexão clara entre fatos e pedidos
- ✅ Valor da causa especificado (R$ 4.312,36)

---

#### ✔️ Completude: 10/10 ✅
**Comentário**: Verificação de elementos essenciais presentes

- ✅ Qualificação das partes
- ✅ Valor da causa
- ✅ Pedidos bem definidos
- ✅ Fundamentação completa

---

## 🔍 Problemas Identificados

1. **Presença de placeholders não preenchidos (___)**
   - Alguns campos de qualificação estão com "___"
   - Falta preencher números de RG em alguns réus

---

## 💪 Pontos Fortes

1. **Fundamentação jurisprudencial adequada**
   - 9 precedentes relevantes citados
   - Aplicação correta ao caso concreto

2. **Estrutura bem organizada**
   - Seções claras e lógicas
   - Fácil navegação

3. **Boa fundamentação com CDC**
   - Uso adequado do Código de Defesa do Consumidor
   - Aplicação correta das normas

---

## 📝 Resumo

> Petição com score 86/100. Boa fundamentação jurídica com 15 artigos e 9 precedentes. Necessita revisão para completar informações faltantes (placeholders).

---

## 💬 Feedback do Cliente (Real)

> "Equipe está de parabéns!  
> Facilitou muito, dessa forma, posso dar uma atenção melhor ao cliente comercialmente dizendo!"

**Rating**: ⭐⭐⭐⭐⭐ (5/5)

---

## 🎯 Correlação

| Métrica | Valor |
|---------|-------|
| **Score AI** | 86/100 |
| **Rating Cliente** | 5/5 (100%) |
| **Correlação** | ✅ Alta (cliente satisfeito) |

---

## 🔄 Como Este Exemplo Foi Gerado

```python
from scripts.evaluator import evaluate_petition

# Carregar petição
with open('petitions/11447_rating5.txt', 'r') as f:
    texto = f.read()

# Avaliar
resultado = evaluate_petition(texto)

# Resultado
print(f"Score: {resultado['score']}/100")
print(f"Problemas: {resultado['problemas']}")
print(f"Pontos fortes: {resultado['pontos_fortes']}")
```

---

## 🚀 Próximos Passos

Para esta petição especificamente:
1. Preencher placeholders (___em campos de qualificação)
2. Revisar seções mais longas para concisão
3. ✅ Manter qualidade da fundamentação jurídica

Para o sistema:
- Executar em mais petições
- Validar critérios com faciliters
- Ajustar pesos se necessário

---

**Nota**: Este é um exemplo com dados **mock/heurísticos**. Com a API key do Claude Sonnet 4.5, a avaliação será ainda mais precisa e detalhada.
