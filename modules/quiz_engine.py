import random

def evaluate_quiz_submission(questions: list, user_answers: dict) -> dict:
    """Evaluate multiple choice quiz answers and calculate performance breakdown."""
    total = len(questions)
    if total == 0:
        return {"score": 0, "total": 0, "percentage": 0.0, "details": []}
        
    correct_count = 0
    details = []
    
    for idx, q in enumerate(questions):
        qid = q.get("id", str(idx))
        selected = user_answers.get(qid)
        correct_idx = q.get("correct_option_index")
        correct_text = q.get("options", [])[correct_idx] if (correct_idx is not None and correct_idx < len(q.get("options", []))) else None
        
        is_correct = (selected == correct_idx)
        if is_correct:
            correct_count += 1
            
        details.append({
            "question_id": qid,
            "question": q.get("question"),
            "selected_index": selected,
            "correct_index": correct_idx,
            "is_correct": is_correct,
            "explanation": q.get("explanation", "")
        })
        
    percentage = round((correct_count / total) * 100.0, 2)
    return {
        "score": correct_count,
        "total": total,
        "percentage": percentage,
        "passed": percentage >= 60.0,
        "details": details
    }

def get_sample_flashcards(flashcard_pool: list, count: int = 5, subject: str = None) -> list:
    """Select a randomized batch of revision flashcards filtered by subject."""
    if subject:
        cards = [c for c in flashcard_pool if c.get("subject", "").lower() == subject.lower()]
    else:
        cards = list(flashcard_pool)
        
    random.shuffle(cards)
    return cards[:count]
