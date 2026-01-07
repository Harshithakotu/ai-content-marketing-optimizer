

def calculate_metrics(row) -> float:
    likes = int(row.get("likes", 0))
    shares = int(row.get("shares", 0))
    comments = int(row.get("comments", 0))

    return likes + shares + comments

