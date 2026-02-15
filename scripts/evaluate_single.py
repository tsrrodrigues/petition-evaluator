#!/usr/bin/env python3
"""
Single petition evaluator - can be called with API key as argument
"""
import sys
import json
import os

# Try to get API key from argument, environment, or stdin
if len(sys.argv) > 2:
    api_key = sys.argv[2]
    os.environ['ANTHROPIC_API_KEY'] = api_key
elif 'ANTHROPIC_API_KEY' not in os.environ:
    print("ERROR: ANTHROPIC_API_KEY not provided", file=sys.stderr)
    print("Usage: python evaluate_single.py <petition_file> [api_key]", file=sys.stderr)
    sys.exit(1)

from anthropic import Anthropic

def evaluate_petition(text):
    """Evaluate a single petition"""
    client = Anthropic()
    
    prompt = f"""Você é um avaliador de petições jurídicas de Direito do Consumidor.

Avalie a petição abaixo usando estes critérios (0-100 total):
- Estrutura (0-20): elementos obrigatórios, organização
- Fundamentação (0-25): citações legais, CDC, precedentes
- Coerência (0-20): argumentação lógica
- Qualidade textual (0-15): gramática, linguagem jurídica
- Personalização (0-10): adequação ao caso específico
- Completude (0-10): todos elementos presentes

Retorne JSON:
{{
  "score": 85,
  "breakdown": {{
    "estrutura_formatacao": {{"score": 18, "max": 20, "comentario": "..."}},
    "fundamentacao_juridica": {{"score": 22, "max": 25, "comentario": "..."}},
    "coerencia_clareza": {{"score": 17, "max": 20, "comentario": "..."}},
    "qualidade_textual": {{"score": 13, "max": 15, "comentario": "..."}},
    "personalizacao_contexto": {{"score": 8, "max": 10, "comentario": "..."}},
    "completude": {{"score": 7, "max": 10, "comentario": "..."}}
  }},
  "problemas": ["problema 1", "problema 2"],
  "pontos_fortes": ["ponto 1", "ponto 2"],
  "summary": "Resumo em 2-3 frases"
}}

PETIÇÃO:
{text[:15000]}
"""
    
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    
    result_text = response.content[0].text.strip()
    
    # Extract JSON
    if result_text.startswith('```'):
        result_text = result_text.split('```')[1]
        if result_text.startswith('json'):
            result_text = result_text[4:]
        result_text = result_text.strip()
    
    return json.loads(result_text)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python evaluate_single.py <petition_file> [api_key]")
        sys.exit(1)
    
    petition_file = sys.argv[1]
    
    with open(petition_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    try:
        result = evaluate_petition(text)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
