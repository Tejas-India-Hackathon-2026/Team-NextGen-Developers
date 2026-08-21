import re
from collections import Counter

def compute_word_vector(text: str) -> Counter:
    """Compute word frequency vector for a text string."""
    words = re.findall(r'\w+', text.lower())
    return Counter(words)

def calculate_cosine_similarity(text1: str, text2: str) -> float:
    """Calculate cosine similarity percentage between two texts."""
    vec1 = compute_word_vector(text1)
    vec2 = compute_word_vector(text2)
    
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    
    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = (sum1 ** 0.5) * (sum2 ** 0.5)
    
    if not denominator:
        return 0.0
    return round((numerator / denominator) * 100.0, 2)

def check_duplicate_notes(new_text: str, existing_notes: list, threshold: float = 85.0) -> dict:
    """Check if new uploaded notes have high similarity with existing repository notes."""
    highest_similarity = 0.0
    matched_title = None
    
    for note in existing_notes:
        note_text = note.get("content_sample", "") or note.get("description", "")
        sim = calculate_cosine_similarity(new_text, note_text)
        if sim > highest_similarity:
            highest_similarity = sim
            matched_title = note.get("title")
            
    is_duplicate = highest_similarity >= threshold
    return {
        "is_duplicate": is_duplicate,
        "similarity_score": highest_similarity,
        "matched_with": matched_title,
        "flagged": is_duplicate
    }
