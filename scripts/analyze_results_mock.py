#!/usr/bin/env python3
"""
Analyze evaluation results and generate calibration report
"""
import json
from pathlib import Path
import statistics

def calculate_correlation(x, y):
    """Calculate Pearson correlation coefficient"""
    if len(x) != len(y) or len(x) < 2:
        return 0
    
    mean_x = statistics.mean(x)
    mean_y = statistics.mean(y)
    
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator_x = sum((xi - mean_x) ** 2 for xi in x)
    denominator_y = sum((yi - mean_y) ** 2 for yi in y)
    
    if denominator_x == 0 or denominator_y == 0:
        return 0
    
    return numerator / (denominator_x * denominator_y) ** 0.5

def main():
    project_dir = Path(__file__).parent.parent
    results_dir = project_dir / 'results'
    
    # Load all evaluations
    all_evals_file = results_dir / 'all_evaluations_mock.json'
    if not all_evals_file.exists():
        print("No evaluations found!")
        return
    
    with open(all_evals_file, 'r', encoding='utf-8') as f:
        evaluations = json.load(f)
    
    print("="*80)
    print("PETITION EVALUATOR - CALIBRATION REPORT")
    print("="*80)
    
    # Group by customer rating
    by_rating = {}
    for eval_data in evaluations:
        rating = eval_data['customer_rating']
        if rating not in by_rating:
            by_rating[rating] = []
        by_rating[rating].append(eval_data)
    
    print(f"\nTotal petitions evaluated: {len(evaluations)}")
    print("\n" + "-"*80)
    print("RESULTS BY CUSTOMER RATING")
    print("-"*80)
    
    for rating in sorted(by_rating.keys(), reverse=True):
        petitions = by_rating[rating]
        ai_scores = [p['ai_score'] for p in petitions]
        
        print(f"\nCustomer Rating {rating} ({len(petitions)} petitions)")
        print(f"  AI Score Range: {min(ai_scores)} - {max(ai_scores)}")
        print(f"  AI Score Average: {statistics.mean(ai_scores):.1f}")
        print(f"  AI Score Median: {statistics.median(ai_scores):.1f}")
        if len(ai_scores) > 1:
            print(f"  AI Score Std Dev: {statistics.stdev(ai_scores):.1f}")
        
        # Show individual scores
        print(f"  Individual scores:")
        for p in petitions:
            print(f"    - Request {p['request_id']}: {p['ai_score']}/100")
    
    print("\n" + "-"*80)
    print("CORRELATION ANALYSIS")
    print("-"*80)
    
    customer_ratings = [e['customer_rating'] for e in evaluations]
    ai_scores = [e['ai_score'] for e in evaluations]
    
    correlation = calculate_correlation(customer_ratings, ai_scores)
    print(f"\nPearson Correlation (Customer Rating vs AI Score): {correlation:.3f}")
    
    # Calculate accuracy for rating 5 (should be >= 85)
    rating_5 = [e for e in evaluations if e['customer_rating'] == 5]
    if rating_5:
        rating_5_scores = [e['ai_score'] for e in rating_5]
        rating_5_avg = statistics.mean(rating_5_scores)
        rating_5_above_85 = len([s for s in rating_5_scores if s >= 85])
        
        print(f"\nRating 5 petitions (Gold Standard):")
        print(f"  Count: {len(rating_5)}")
        print(f"  Average AI Score: {rating_5_avg:.1f}")
        print(f"  Scores >= 85: {rating_5_above_85}/{len(rating_5)} ({rating_5_above_85/len(rating_5)*100:.1f}%)")
        print(f"  Target: ≥85 average score ✓" if rating_5_avg >= 85 else f"  Target: ≥85 average score ✗ (adjust needed)")
    
    # Calculate for low ratings (should be < 85)
    low_ratings = [e for e in evaluations if e['customer_rating'] <= 3]
    if low_ratings:
        low_scores = [e['ai_score'] for e in low_ratings]
        low_avg = statistics.mean(low_scores)
        
        print(f"\nRating 1-3 petitions (Low Quality):")
        print(f"  Count: {len(low_ratings)}")
        print(f"  Average AI Score: {low_avg:.1f}")
        print(f"  Target: <85 average score ✓" if low_avg < 85 else f"  Target: <85 average score ✗ (adjust needed)")
    
    print("\n" + "-"*80)
    print("COMMON ISSUES BY RATING")
    print("-"*80)
    
    for rating in sorted(by_rating.keys(), reverse=True):
        petitions = by_rating[rating]
        all_problems = []
        
        for p in petitions:
            if 'evaluation' in p and 'problemas' in p['evaluation']:
                all_problems.extend(p['evaluation']['problemas'])
        
        if all_problems:
            print(f"\nCustomer Rating {rating}:")
            # Count problem frequency
            from collections import Counter
            problem_counts = Counter(all_problems)
            for problem, count in problem_counts.most_common(5):
                print(f"  - {problem} ({count}x)")
    
    print("\n" + "="*80)
    print("END OF REPORT")
    print("="*80)
    
    # Save summary to file
    summary = {
        'total_evaluations': len(evaluations),
        'correlation': correlation,
        'by_rating': {}
    }
    
    for rating in sorted(by_rating.keys(), reverse=True):
        petitions = by_rating[rating]
        ai_scores = [p['ai_score'] for p in petitions]
        
        summary['by_rating'][rating] = {
            'count': len(petitions),
            'ai_score_avg': statistics.mean(ai_scores),
            'ai_score_median': statistics.median(ai_scores),
            'ai_score_min': min(ai_scores),
            'ai_score_max': max(ai_scores),
            'ai_score_stdev': statistics.stdev(ai_scores) if len(ai_scores) > 1 else 0
        }
    
    summary_file = results_dir / 'calibration_summary.json'
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\nSummary saved to: {summary_file}")

if __name__ == '__main__':
    main()
