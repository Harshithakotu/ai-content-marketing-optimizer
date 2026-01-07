from generators.content_generator import generate_content
from generators.trend_optimizer import load_data, merge_data

import pandas as pd

def generate_initial_marketing_content(merged_df):
    prompt = f"""
Use this dataset to:
1. Identify trending topics  
2. Generate 5 content ideas  
3. Write 2 short social media posts  
4. Suggest 3 SEO keywords  

DATA SAMPLE:
{merged_df.head(10).to_string()}
"""
    return generate_content(prompt)

def generate_optimized_content(merged_df):
    prompt = f"""
Based on these platform trends, produce:
1. Top 5 emerging trends  
2. Optimized content strategy  
3. Best posting times  
4. CTA suggestions  

DATA SAMPLE:
{merged_df.sample(10).to_string()}
"""
    return generate_content(prompt)

def main():
    youtube_df, reddit_df, pinterest_df = load_data()
    merged_df = merge_data(youtube_df, reddit_df, pinterest_df)

    initial = generate_initial_marketing_content(merged_df)
    optimized = generate_optimized_content(merged_df)

    with open("../data/milestone2_output.txt", "w", encoding="utf-8") as f:
        f.write("===== Initial Marketing Content =====\n\n")
        f.write(initial + "\n\n")
        f.write("===== Optimized Trend-Based Content =====\n\n")
        f.write(optimized)

    print("Milestone 2 completed! Output saved to /data/milestone2_output.txt")

if __name__ == "__main__":
    main()
