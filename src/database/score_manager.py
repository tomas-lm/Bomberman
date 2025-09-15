import json
import os
from typing import List, Tuple, Optional
from datetime import datetime


class ScoreManager:
    def __init__(self, database_path: str = "data/scores.json"):
        self.database_path = database_path
        self.max_scores = 10
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        os.makedirs(os.path.dirname(self.database_path), exist_ok=True)
        
        if not os.path.exists(self.database_path):
            self._create_empty_database()
    
    def _create_empty_database(self):
        empty_data = {
            "scores": [],
            "last_updated": datetime.now().isoformat()
        }
        self._save_data(empty_data)
    
    def _load_data(self) -> dict:
        try:
            with open(self.database_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self._create_empty_database()
            return self._load_data()
    
    def _save_data(self, data: dict):
        data["last_updated"] = datetime.now().isoformat()
        with open(self.database_path, 'w') as file:
            json.dump(data, file, indent=2)
    
    def add_score(self, player_name: str, score: int) -> bool:
        if not player_name.strip():
            return False
        
        data = self._load_data()
        scores = data.get("scores", [])
        
        new_score_entry = {
            "player_name": player_name.strip(),
            "score": score,
            "date": datetime.now().isoformat()
        }
        
        scores.append(new_score_entry)
        scores.sort(key=lambda x: x["score"], reverse=True)
        
        if len(scores) > self.max_scores:
            scores = scores[:self.max_scores]
        
        data["scores"] = scores
        self._save_data(data)
        
        return True
    
    def get_high_scores(self) -> List[Tuple[str, int]]:
        data = self._load_data()
        scores = data.get("scores", [])
        
        return [(entry["player_name"], entry["score"]) for entry in scores]
    
    def is_high_score(self, score: int) -> bool:
        high_scores = self.get_high_scores()
        
        if len(high_scores) < self.max_scores:
            return True
        
        return score > high_scores[-1][1]
    
    def get_player_stats(self, player_name: str) -> dict:
        data = self._load_data()
        scores = data.get("scores", [])
        
        player_scores = [entry for entry in scores if entry["player_name"].lower() == player_name.lower()]
        
        if not player_scores:
            return {
                "games_played": 0,
                "highest_score": 0,
                "average_score": 0,
                "total_score": 0
            }
        
        total_score = sum(entry["score"] for entry in player_scores)
        highest_score = max(entry["score"] for entry in player_scores)
        average_score = total_score / len(player_scores)
        
        return {
            "games_played": len(player_scores),
            "highest_score": highest_score,
            "average_score": round(average_score, 2),
            "total_score": total_score
        }
    
    def clear_all_scores(self):
        self._create_empty_database()
    
    def get_database_stats(self) -> dict:
        data = self._load_data()
        scores = data.get("scores", [])
        
        if not scores:
            return {
                "total_games": 0,
                "unique_players": 0,
                "highest_score": 0,
                "last_updated": data.get("last_updated", "Never")
            }
        
        unique_players = len(set(entry["player_name"] for entry in scores))
        highest_score = max(entry["score"] for entry in scores)
        
        return {
            "total_games": len(scores),
            "unique_players": unique_players,
            "highest_score": highest_score,
            "last_updated": data.get("last_updated", "Unknown")
        }
