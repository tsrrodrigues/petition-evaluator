#!/usr/bin/env python3
"""
Script to collect petitions from the database for evaluation
"""
import psycopg2
import json
import os
from pathlib import Path

DB_CONFIG = {
    'host': '34.95.205.110',
    'user': 'aegis-tiago',
    'password': '2?uUbBGA]oH@[]a',
    'database': 'facilitajuridico'
}

# Area ID for Consumidor
AREA_ID = 10
# Modality ID for Inicial
MODALITY_ID = 4

def get_petitions_by_rating(rating_values, limit=15):
    """Get petitions with specific ratings"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    query = """
    SELECT DISTINCT ON (r.id)
      r.id as request_id,
      rcr.value as rating,
      rd.id as doc_id,
      rd.url,
      rd.name,
      rd.source,
      rd.was_developed_with_ia,
      rcr.remark,
      rcr.rating_text
    FROM operations.request r
    JOIN operations.request_customer_rating rcr ON r.id = rcr.request_id
    JOIN operations.request_documents rd ON r.id = rd.request_id
    WHERE r.area_id = %s
      AND r.modality_id = %s
      AND rcr.value = ANY(%s)
      AND rd.source = 'faciliter'
      AND rd.deleted IS NULL
      AND (rd.file_type LIKE '%%wordprocessingml%%' OR rd.name LIKE '%%.docx' OR rd.name LIKE '%%.doc')
    ORDER BY r.id, rd.id DESC
    LIMIT %s;
    """
    
    cur.execute(query, (AREA_ID, MODALITY_ID, rating_values, limit))
    results = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return results

def main():
    # Create data directory
    data_dir = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(exist_ok=True)
    
    # Collect rating 5 petitions (gold standard)
    print("Collecting rating 5 petitions...")
    rating_5 = get_petitions_by_rating([5], limit=15)
    
    # Collect low rating petitions (1-3)
    print("Collecting low rating petitions (1-3)...")
    low_ratings = get_petitions_by_rating([1, 2, 3], limit=12)
    
    # Combine and save metadata
    all_petitions = []
    
    for row in rating_5:
        petition = {
            'request_id': row[0],
            'rating': row[1],
            'doc_id': row[2],
            'url': row[3],
            'name': row[4],
            'source': row[5],
            'was_developed_with_ia': row[6],
            'remark': row[7],
            'rating_text': row[8]
        }
        all_petitions.append(petition)
    
    for row in low_ratings:
        petition = {
            'request_id': row[0],
            'rating': row[1],
            'doc_id': row[2],
            'url': row[3],
            'name': row[4],
            'source': row[5],
            'was_developed_with_ia': row[6],
            'remark': row[7],
            'rating_text': row[8]
        }
        all_petitions.append(petition)
    
    # Save metadata
    metadata_file = data_dir / 'petitions_metadata.json'
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(all_petitions, f, indent=2, ensure_ascii=False)
    
    print(f"\nCollected {len(all_petitions)} petitions:")
    print(f"  - Rating 5: {len(rating_5)}")
    print(f"  - Rating 1-3: {len(low_ratings)}")
    print(f"\nMetadata saved to: {metadata_file}")
    
    # Print summary by rating
    from collections import Counter
    rating_counts = Counter([p['rating'] for p in all_petitions])
    print("\nRating distribution:")
    for rating in sorted(rating_counts.keys(), reverse=True):
        print(f"  Rating {rating}: {rating_counts[rating]} petitions")

if __name__ == '__main__':
    main()
