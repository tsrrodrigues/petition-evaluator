#!/usr/bin/env python3
"""
Mock petition evaluator for demonstration purposes
Generates realistic evaluations based on heuristics until API key is available
"""
import json
import re
from pathlib import Path
import time

def analyze_petition_heuristics(text):
    """Analyze petition using heuristics to generate realistic scores"""
    
    # Basic metrics
    length = len(text)
    has_articles = len(re.findall(r'Art\.|Artigo|art\.', text))
    has_jurisprudence = len(re.findall(r'STJ|STF|TJ[A-Z]{2}|Súmula', text, re.IGNORECASE))
    has_cdc = len(re.findall(r'CDC|Código de Defesa do Consumidor', text, re.IGNORECASE))
    paragraphs = len([p for p in text.split('\n') if p.strip()])
    has_parties = 'em desfavor de' in text or 'em face de' in text
    has_requests = 'pedidos' in text.lower() or 'requer' in text.lower()
    has_value = re.search(r'R\$\s*[\d.,]+', text) is not None
    has_placeholders = '___' in text or '  ' in text  # Generic placeholders
    
    # Base scores
    estrutura_score = min(20, (15 if has_parties else 10) + (3 if has_requests else 0) + (2 if paragraphs > 20 else 0))
    fundamentacao_score = min(25, has_articles * 2 + has_jurisprudence * 3 + has_cdc * 4)
    coerencia_score = min(20, 15 if length > 10000 else 10)
    qualidade_score = min(15, 12 if not has_placeholders else 8)
    personalizacao_score = min(10, 8 if has_value and length > 15000 else 4)
    completude_score = min(10, (3 if has_parties else 0) + (2 if has_value else 0) + (3 if has_requests else 0) + 2)
    
    total_score = estrutura_score + fundamentacao_score + coerencia_score + qualidade_score + personalizacao_score + completude_score
    
    # Generate problems and strengths
    problemas = []
    if has_placeholders:
        problemas.append("Presença de placeholders não preenchidos (___)")
    if not has_value:
        problemas.append("Valor da causa não especificado")
    if has_articles < 5:
        problemas.append("Poucas citações de artigos legais")
    if has_jurisprudence < 2:
        problemas.append("Fundamentação jurisprudencial insuficiente")
    if length < 10000:
        problemas.append("Petição muito curta, pode estar incompleta")
    
    pontos_fortes = []
    if has_cdc >= 3:
        pontos_fortes.append("Bom uso do Código de Defesa do Consumidor")
    if has_jurisprudence >= 3:
        pontos_fortes.append("Fundamentação jurisprudencial adequada")
    if length > 20000:
        pontos_fortes.append("Petição bem desenvolvida e detalhada")
    if estrutura_score >= 18:
        pontos_fortes.append("Estrutura bem organizada")
    
    return {
        "score": total_score,
        "breakdown": {
            "estrutura_formatacao": {
                "score": estrutura_score,
                "max": 20,
                "comentario": "Análise da presença de elementos estruturais obrigatórios"
            },
            "fundamentacao_juridica": {
                "score": fundamentacao_score,
                "max": 25,
                "comentario": f"{has_articles} artigos citados, {has_jurisprudence} precedentes"
            },
            "coerencia_clareza": {
                "score": coerencia_score,
                "max": 20,
                "comentario": "Avaliação baseada na extensão e organização do texto"
            },
            "qualidade_textual": {
                "score": qualidade_score,
                "max": 15,
                "comentario": "Sem placeholders" if not has_placeholders else "Presença de placeholders detectada"
            },
            "personalizacao_contexto": {
                "score": personalizacao_score,
                "max": 10,
                "comentario": "Adequação aos fatos específicos do caso"
            },
            "completude": {
                "score": completude_score,
                "max": 10,
                "comentario": "Verificação de elementos essenciais presentes"
            }
        },
        "problemas": problemas if problemas else ["Nenhum problema crítico detectado"],
        "pontos_fortes": pontos_fortes if pontos_fortes else ["Petição atende requisitos mínimos"],
        "summary": f"Petição com score {total_score}/100. " + 
                  (f"Boa fundamentação jurídica com {has_articles} artigos e {has_jurisprudence} precedentes." if fundamentacao_score >= 15 else "Fundamentação jurídica pode ser aprimorada.") +
                  (" Necessita revisão para completar informações faltantes." if has_placeholders or not has_value else "")
    }

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
    
    print(f"Evaluating {len(petitions)} petitions using MOCK evaluator (heuristic-based)...")
    print("="*60)
    print("NOTE: This is a DEMO evaluator using heuristics.")
    print("For real AI evaluation, provide ANTHROPIC_API_KEY and use evaluator.py")
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
        
        # Evaluate using heuristics
        print(f"  Analyzing with heuristics...")
        evaluation = analyze_petition_heuristics(petition_text)
        score = evaluation['score']
        
        print(f"  ✓ Score: {score}/100")
        
        evaluations.append({
            'request_id': request_id,
            'customer_rating': rating,
            'ai_score': score,
            'evaluation': evaluation,
            'text_length': len(petition_text),
            'method': 'heuristic'
        })
        
        # Save individual evaluation
        eval_file = results_dir / f'eval_{request_id}_rating{rating}_mock.json'
        with open(eval_file, 'w', encoding='utf-8') as f:
            json.dump({
                'request_id': request_id,
                'customer_rating': rating,
                'evaluation': evaluation,
                'metadata': petition,
                'method': 'heuristic'
            }, f, indent=2, ensure_ascii=False)
        
        time.sleep(0.1)  # Simulate processing time
    
    # Save all evaluations
    all_evals_file = results_dir / 'all_evaluations_mock.json'
    with open(all_evals_file, 'w', encoding='utf-8') as f:
        json.dump(evaluations, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"Completed {len(evaluations)} evaluations (MOCK/Heuristic)")
    print(f"Results saved to: {results_dir}")
    
    # Calculate statistics
    if evaluations:
        rating_5_scores = [e['ai_score'] for e in evaluations if e['customer_rating'] == 5]
        low_rating_scores = [e['ai_score'] for e in evaluations if e['customer_rating'] <= 3]
        
        print("\n📊 MOCK CALIBRATION RESULTS:")
        print(f"\nRating 5 petitions (n={len(rating_5_scores)}):")
        if rating_5_scores:
            print(f"  Average AI score: {sum(rating_5_scores)/len(rating_5_scores):.1f}")
            print(f"  Min: {min(rating_5_scores)}, Max: {max(rating_5_scores)}")
        
        print(f"\nRating 1-3 petitions (n={len(low_rating_scores)}):")
        if low_rating_scores:
            print(f"  Average AI score: {sum(low_rating_scores)/len(low_rating_scores):.1f}")
            print(f"  Min: {min(low_rating_scores)}, Max: {max(low_rating_scores)}")
        
        print(f"\n⚠️  These are HEURISTIC-BASED scores, not real AI evaluations")
        print(f"Set ANTHROPIC_API_KEY to use real Claude Sonnet 4.5 evaluation")

if __name__ == '__main__':
    main()
