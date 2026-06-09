import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

# Use a highly-efficient, lightweight pre-trained model for sentence embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_candidate_string(candidate):
    """Compiles the core historical profile text of a candidate to parse meaning."""
    profile = candidate['profile']
    career = candidate['career_history']
    
    history_snippets = []
    for job in career[:2]: # Look deeply at their most recent two roles
        title = job.get('title', '')
        desc = job.get('description', '')
        history_snippets.append(f"Worked as a {title}. Responsibility: {desc}")
        
    history_text = " ".join(history_snippets)
    
    full_summary = f"Headline: {profile.get('headline', '')}. Summary: {profile.get('summary', '')}. History: {history_text}"
    return full_summary

def get_behavioral_multiplier(signals):
    """Applies a scaling factor based on the platform availability matrix."""
    response_rate = signals.get('recruiter_response_rate', 0.5)
    interview_rate = signals.get('interview_completion_rate', 0.5)
    
    # Calculate continuous penalty for dead/dormant accounts
    last_active_str = signals.get('last_active_date', '2026-01-01')
    try:
        last_active = datetime.strptime(last_active_str, '%Y-%m-%d')
    except ValueError:
        last_active = datetime(2026, 1, 1)
        
    # Evaluate age relative to June 2026
    days_inactive = (datetime(2026, 6, 9) - last_active).days
    activity_penalty = 1.0 if days_inactive <= 60 else (0.5 if days_inactive <= 180 else 0.1)
    
    # Weighted calculation balancing responsiveness and real activity
    base_signal = (response_rate * 0.6) + (interview_rate * 0.4)
    return max(base_signal * activity_penalty, 0.01)

def rank_candidates(candidates, jd_text):
    """Embeds the pool, checks similarity, maps modifiers, and returns sorted outputs."""
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)
    
    scored_list = []
    
    # Extract structural summaries for fast batch embedding execution
    corpus_strings = [create_candidate_string(c) for c in candidates]
    corpus_embeddings = model.encode(corpus_strings, convert_to_tensor=True, show_progress_bar=True)
    
    # Compute Cosine Similarities between JD and candidates
    cosine_scores = util.cos_sim(jd_embedding, corpus_embeddings)[0].cpu().numpy()
    
    for idx, candidate in enumerate(candidates):
        semantic_score = float(cosine_scores[idx])
        multiplier = get_behavioral_multiplier(candidate['redrob_signals'])
        
        # Determine the blended overall execution rank metric
        final_score = semantic_score * multiplier
        
        # Build contextual justification for Stage 4 manual reviews
        reasoning = (f"AI/Backend hybrid tracking {candidate['profile']['years_of_experience']} YOE; "
                     f"Active with {int(candidate['redrob_signals'].get('recruiter_response_rate', 0)*100)}% response rate.")
        
        scored_list.append({
            'candidate_id': candidate['candidate_id'],
            'score': final_score,
            'reasoning': reasoning
        })
        
    # Order candidates: Descending by score, ascending by ID as a fallback tiebreaker
    scored_list.sort(key=lambda x: (-x['score'], x['candidate_id']))
    return scored_list
