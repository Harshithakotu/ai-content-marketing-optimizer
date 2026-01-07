import pandas as pd
import os

def load_data():
    """
    Load raw data from YouTube, Reddit, and Pinterest Excel files.
    Assumes files are in 'data' folder at project root.
    """
    # Absolute path to data folder (relative to this file)
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))

    youtube_file = os.path.join(base_path, "youtube_data.xlsx")
    reddit_file = os.path.join(base_path, "reddit_data.xlsx")
    pinterest_file = os.path.join(base_path, "pinterest_data.xlsx")

    # Load Excel files
    for file in [youtube_file, reddit_file, pinterest_file]:
        if not os.path.exists(file):
            raise FileNotFoundError(f"File not found: {file}")

    youtube_df = pd.read_excel(youtube_file)
    reddit_df = pd.read_excel(reddit_file)
    pinterest_df = pd.read_excel(pinterest_file)

    return youtube_df, reddit_df, pinterest_df

def merge_data(youtube_df, reddit_df, pinterest_df):
    youtube_df["source"] = "YouTube"
    reddit_df["source"] = "Reddit"
    pinterest_df["source"] = "Pinterest"

    if "pin_url" in pinterest_df.columns:
        pinterest_df.rename(columns={"pin_url": "url"}, inplace=True)

    merged_df = pd.concat([youtube_df, reddit_df, pinterest_df], ignore_index=True)
    return merged_df

if __name__ == "__main__":
    try:
        youtube_df, reddit_df, pinterest_df = load_data()
        merged_df = merge_data(youtube_df, reddit_df, pinterest_df)

        # Save merged Excel file
        output_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../merged_data.xlsx"))
        merged_df.to_excel(output_file, index=False)
        print(f"\n✅ Merged data successfully saved at: {output_file}")
    except Exception as e:
        print(f"❌ Error: {e}")
