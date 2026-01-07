
def extract_features(row):
    return [
        row.get("views", 0),
        row.get("likes", 0),
        row.get("comments", 0),
        row.get("saves", 0),
        row.get("clicks", 0)
    ]
