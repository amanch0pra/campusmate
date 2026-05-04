import pandas as pd
import json
import os

def export_to_jsonl(csv_path, output_path):
    print(f"📂 Reading dataset from {csv_path}...")
    if not os.path.exists(csv_path):
        print(f"❌ Error: {csv_path} not found.")
        return

    df = pd.read_csv(csv_path)
    print(f"📊 Found {len(df)} Q&A pairs.")

    print(f"🔄 Converting to JSONL format...")
    jsonl_data = []
    
    system_prompt = "You are Campus Mate, a highly intelligent and specialized assistant for students of Lovely Professional University (LPU). Provide accurate, professional, and helpful information about academics, admissions, campus life, and more."

    for _, row in df.iterrows():
        entry = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": row['Question']},
                {"role": "assistant", "content": row['Answer']}
            ]
        }
        jsonl_data.append(entry)

    print(f"💾 Saving to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in jsonl_data:
            f.write(json.dumps(entry) + '\n')

    print(f"✅ Export completed! Total entries: {len(jsonl_data)}")
    print(f"📍 File location: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    export_to_jsonl('data/dataset_v2.csv', 'data/training_data.jsonl')
