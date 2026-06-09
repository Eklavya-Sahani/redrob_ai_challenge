import pandas as pd
from preprocess import stream_and_filter
from ranker import rank_candidates

def main():
    print("Executing Stage 1: Continuous Data Streaming & Trap Neutralization...")
    input_path = "data/candidates.jsonl" 
    clean_candidates = stream_and_filter(input_path)
    print(f"Sanitization complete. Verified {len(clean_candidates)} valid profiles.")
    
    target_job_description = (
        "Senior AI Engineer focused on full-stack ML development. Experience with embeddings, "
        "retrieval models, ranking algorithms, semantic search pipelines, and Vector Databases. "
        "Product-oriented mindset capable of standing up initial systems quickly and scaling infrastructure. "
        "Background in engineering robust systems architectures or data pipelines."
    )
    
    print("\nExecuting Stage 2 & 3: Dense Encoding & Behavioral Signals Multiplier Cascade...")
    ranked_results = rank_candidates(clean_candidates, target_job_description)
    
    top_100 = ranked_results[:100]
    
    df_out = pd.DataFrame(top_100)
    df_out['rank'] = range(1, 101)
    df_out = df_out[['candidate_id', 'rank', 'score', 'reasoning']]
    
    output_filename = "team_submission.csv"
    df_out.to_csv(output_filename, index=False, encoding='utf-8')
    print(f"\nSuccess! Top 100 output file compiled and saved to {output_filename}")

if __name__ == "__main__":
    main()
