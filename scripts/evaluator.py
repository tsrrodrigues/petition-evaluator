#!/usr/bin/env python3
"""
Petition Quality Evaluator using Claude Sonnet 4.5
"""
import json
import os
from pathlib import Path
from anthropic import Anthropic
import time

# Initialize Anthropic client (will use ANTHROPIC_API_KEY from environment or SDK defaults)
client = Anthropic()

EVALUATION_PROMPT = """Você é um avaliador especializado em petições iniciais de Direito do Consumidor.

Sua tarefa é avaliar a qualidade da petição fornecida usando os seguintes critérios:

**CRITÉRIOS DE AVALIAÇÃO:**

1. **ESTRUTURA E FORMATAÇÃO (0-20 pontos)**
   - Presença de todos os elementos obrigatórios (endereçamento, qualificação das partes, dos fatos, do direito, dos pedidos)
   - Organização lógica e clara
   - Formatação profissional
   - Uso adequado de títulos e subtítulos

2. **FUNDAMENTAÇÃO JURÍDICA (0-25 pontos)**
   - Citação adequada de leis, códigos e precedentes
   - Aplicação correta das normas ao caso concreto
   - Uso do CDC (Código de Defesa do Consumidor) de forma apropriada
   - Fundamentação sólida e coerente

3. **COERÊNCIA E CLAREZA (0-20 pontos)**
   - Argumentação lógica e bem estruturada
   - Linguagem clara e objetiva
   - Ausência de contradições
   - Fluidez na leitura

4. **QUALIDADE TEXTUAL (0-15 pontos)**
   - Correção gramatical e ortográfica
   - Uso adequado de linguagem jurídica
   - Redação profissional
   - Concisão sem perda de informação relevante

5. **PERSONALIZAÇÃO E CONTEXTO (0-10 pontos)**
   - Adequação aos fatos específicos do caso
   - Evidências de análise individual (não texto genérico)
   - Conexão entre fatos narrados e pedidos

6. **COMPLETUDE (0-10 pontos)**
   - Todos os elementos necessários estão presentes
   - Valor da causa (quando aplicável)
   - Documentos mencionados
   - Qualificação completa das partes

**FORMATO DE RESPOSTA:**

Retorne APENAS um JSON válido no seguinte formato:

```json
{{
  "score": 85,
  "breakdown": {{
    "estrutura_formatacao": {{
      "score": 18,
      "max": 20,
      "comentario": "Breve comentário sobre este critério"
    }},
    "fundamentacao_juridica": {{
      "score": 22,
      "max": 25,
      "comentario": "Breve comentário sobre este critério"
    }},
    "coerencia_clareza": {{
      "score": 17,
      "max": 20,
      "comentario": "Breve comentário sobre este critério"
    }},
    "qualidade_textual": {{
      "score": 13,
      "max": 15,
      "comentario": "Breve comentário sobre este critério"
    }},
    "personalizacao_contexto": {{
      "score": 8,
      "max": 10,
      "comentario": "Breve comentário sobre este critério"
    }},
    "completude": {{
      "score": 7,
      "max": 10,
      "comentario": "Breve comentário sobre este critério"
    }}
  }},
  "problemas": [
    "Lista de problemas específicos encontrados",
    "Cada item deve ser claro e objetivo",
    "Máximo 10 problemas mais relevantes"
  ],
  "pontos_fortes": [
    "Lista de pontos positivos da petição",
    "Aspectos bem executados",
    "Máximo 5 pontos fortes"
  ],
  "summary": "Resumo geral da avaliação em 2-3 frases"
}}
```

**PETIÇÃO A AVALIAR:**

{petition_text}

**IMPORTANTE:** Retorne APENAS o JSON, sem texto adicional antes ou depois."""

def evaluate_petition(petition_text, model="claude-sonnet-4-5"):
    """Evaluate a petition using Claude"""
    
    prompt = EVALUATION_PROMPT.format(petition_text=petition_text)
    
    try:
        response = client.messages.create(
            model=model,
            max_tokens=4000,
            temperature=0.3,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Extract JSON from response
        response_text = response.content[0].text.strip()
        
        # Try to extract JSON if wrapped in code blocks
        if response_text.startswith('```'):
            # Remove code block markers
            response_text = response_text.split('```')[1]
            if response_text.startswith('json'):
                response_text = response_text[4:]
            response_text = response_text.strip()
        
        evaluation = json.loads(response_text)
        
        return evaluation
        
    except Exception as e:
        print(f"Error evaluating petition: {e}")
        print(f"Response: {response_text if 'response_text' in locals() else 'N/A'}")
        return None

def main():
    project_dir = Path(__file__).parent.parent
    data_dir = project_dir / 'data'
    petitions_dir = project_dir / 'petitions'
    results_dir = project_dir / 'results'
    results_dir.mkdir(exist_ok=True)
    
    # Load processed petitions
    processed_file = data_dir / 'processed_petitions.json'
    with open(processed_file, 'r', encoding='utf-8') as f:
        petitions = json.load(f)
    
    print(f"Evaluating {len(petitions)} petitions using Claude Sonnet 4.5...")
    print("="*60)
    
    evaluations = []
    
    for i, petition in enumerate(petitions, 1):
        request_id = petition['request_id']
        rating = petition['rating']
        txt_file = petitions_dir / petition['txt_file']
        
        print(f"\n[{i}/{len(petitions)}] Evaluating request_id={request_id}, rating={rating}")
        
        # Read petition text
        with open(txt_file, 'r', encoding='utf-8') as f:
            petition_text = f.read()
        
        # Evaluate
        print(f"  Sending to Claude...")
        evaluation = evaluate_petition(petition_text)
        
        if evaluation:
            score = evaluation.get('score', 0)
            print(f"  ✓ Score: {score}/100")
            
            evaluations.append({
                'request_id': request_id,
                'customer_rating': rating,
                'ai_score': score,
                'evaluation': evaluation,
                'text_length': len(petition_text)
            })
            
            # Save individual evaluation
            eval_file = results_dir / f'eval_{request_id}_rating{rating}.json'
            with open(eval_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'request_id': request_id,
                    'customer_rating': rating,
                    'evaluation': evaluation,
                    'metadata': petition
                }, f, indent=2, ensure_ascii=False)
        else:
            print(f"  ✗ Failed to evaluate")
        
        # Rate limiting
        time.sleep(2)
    
    # Save all evaluations
    all_evals_file = results_dir / 'all_evaluations.json'
    with open(all_evals_file, 'w', encoding='utf-8') as f:
        json.dump(evaluations, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"Completed {len(evaluations)} evaluations")
    print(f"Results saved to: {results_dir}")
    
    # Calculate statistics
    if evaluations:
        rating_5_scores = [e['ai_score'] for e in evaluations if e['customer_rating'] == 5]
        low_rating_scores = [e['ai_score'] for e in evaluations if e['customer_rating'] <= 3]
        
        print("\n📊 CALIBRATION RESULTS:")
        print(f"\nRating 5 petitions (n={len(rating_5_scores)}):")
        if rating_5_scores:
            print(f"  Average AI score: {sum(rating_5_scores)/len(rating_5_scores):.1f}")
            print(f"  Min: {min(rating_5_scores)}, Max: {max(rating_5_scores)}")
        
        print(f"\nRating 1-3 petitions (n={len(low_rating_scores)}):")
        if low_rating_scores:
            print(f"  Average AI score: {sum(low_rating_scores)/len(low_rating_scores):.1f}")
            print(f"  Min: {min(low_rating_scores)}, Max: {max(low_rating_scores)}")

if __name__ == '__main__':
    main()
