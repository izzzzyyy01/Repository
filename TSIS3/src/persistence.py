import json
import os

def load_data(filename, default):
    if not os.path.exists(filename):
        return default
    with open(filename, "r") as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def update_leaderboard(name, score, distance):
    leaderboard = load_data("leaderboard.json", [])
    leaderboard.append({"name": name, "score": score, "distance": distance})

    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
    save_data("leaderboard.json", leaderboard)
