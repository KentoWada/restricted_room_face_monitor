import numpy as np

THRESHOLD = 0.47


def best_match(embedding, enrolled):
    best_name = None
    best_score = -1.0
    for name, embeddings in enrolled.items():
        for e in embeddings:
            score = float(np.dot(embedding, e))
            if score > best_score:
                best_name = name
                best_score = score
    if best_score < THRESHOLD:
        return "Unknown", best_score
    return best_name, best_score
