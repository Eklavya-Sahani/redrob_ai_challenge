# Senior AI Engineer Candidate Ranking Pipeline

This repository contains a high-throughput, memory-efficient production-grade semantic pipeline to filter and rank candidates for the Redrob AI Challenge.

## 🚀 Key Features
- **OOM Protection:** Line-by-line JSONL data streaming optimized for low-resource CPU environments (under 15 seconds execution time).
- **Fraud Detection:** Anti-trap filtering to catch timeline paradoxes and strip out malicious keyword-stuffing.
- **Semantic Core:** Utilizes `all-MiniLM-L6-v2` Sentence-Transformers for dense vector spatial matching against the target Job Description.

## 📁 Repository Structure
- `src/`: Main pipeline scripts (stream parsing, preprocessing, ranking logic).
- `data/`: Local verification samples.
- `Eklavya_Sahani.csv`: Final optimized output of top-100 ranked candidates.
- `Eklavya_Sahani_Presentation.pdf`: Detailed project blueprint and approach deck.

## 🛠️ Tech Stack
- Python (Native I/O Data Streams)
- Hugging Face / Sentence-Transformers (`all-MiniLM-L6-v2`)
- Pandas & NumPy