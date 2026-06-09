import json
from datetime import datetime

def is_trap_candidate(candidate):
    profile = candidate['profile']
    skills = candidate['skills']
    career = candidate['career_history']
    
    current_title = profile.get('current_title', '').lower()
    
    # 1. Catch Keyword Stuffers (Non-technical roles listing heavy AI keywords)
    non_tech_titles = ['hr manager', 'content writer', 'graphic designer', 'sales executive', 'marketing manager', 'customer support']
    ai_keywords = {'rag', 'llm', 'embeddings', 'vector', 'fine-tuning', 'pinecone', 'langchain'}
    
    has_ai_skills = any(any(kw in skill['name'].lower() for kw in ai_keywords) for skill in skills)
    is_non_tech = any(title in current_title for title in non_tech_titles)
    
    if is_non_tech and has_ai_skills:
        return True  # Trap found
        
    # 2. Catch Honeypots (Temporal Contradictions)
    reported_yoe = profile.get('years_of_experience', 0)
    calculated_months = sum(exp.get('duration_months', 0) for exp in career if exp.get('duration_months') is not None)
    calculated_yoe = calculated_months / 12.0
    
    if calculated_yoe > (reported_yoe + 3.0):
        return True  # Paradoxical temporal trap
        
    return False

def check_eligibility(candidate):
    profile = candidate['profile']
    signals = candidate['redrob_signals']
    
    yoe = profile.get('years_of_experience', 0)
    if not (4.5 <= yoe <= 11.0):
        return False
        
    loc = profile.get('location', '').lower()
    willing_to_relocate = signals.get('willing_to_relocate', False)
    
    is_target_city = ('pune' in loc or 'noida' in loc)
    if not is_target_city and not willing_to_relocate:
        return False
        
    return True

def stream_and_filter(input_path):
    """Streams candidates from the plain JSONL file line-by-line."""
    clean_pool = []
    
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            candidate = json.loads(line)
            
            if is_trap_candidate(candidate):
                continue
            if not check_eligibility(candidate):
                continue
                
            clean_pool.append(candidate)
            
    return clean_pool
