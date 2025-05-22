import pandas as pd
import time
import csv
import os
from openai import OpenAI

# ✅ Set API key securely
client = OpenAI()

# ✅ File paths
INPUT_FILE = "sample_queries.xlsx"
OUTPUT_FILE = "augmented_queries.csv"
PARAPHRASE_COUNT = 5

def paraphrase_query(prompt: str, count: int = 5):
    system_msg = (
        "You are a helpful assistant that generates professional, business-context "
        "paraphrases of user queries in supply chain, finance, or enterprise settings. "
        "Keep the original intent intact but rephrase each one naturally."
    )

    user_msg = f"Generate {count} paraphrased versions of the following user query:\n\n\"{prompt}\""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.7,
        )

        text = response.choices[0].message.content
        variants = [line.strip("-• ").strip() for line in text.split("\n") if line.strip()]
        return variants[:count]
    except Exception as e:
        print(f"❌ Error paraphrasing \"{prompt}\": {e}")
        return []

def main():
    df = pd.read_excel(INPUT_FILE)
    results = []

    for _, row in df.iterrows():
        query, label = row["Query"], row["Type"]
        print(f"🔄 Paraphrasing: \"{query}\" ({label})")

        results.append((query, label))  # Include original
        variants = paraphrase_query(query, PARAPHRASE_COUNT)
        for var in variants:
            results.append((var, label))
        time.sleep(1)

    # ✅ Write to output CSV
    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["query", "label"])
        for query, label in results:
            writer.writerow([query, label])

    print(f"\n✅ Augmented queries saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
