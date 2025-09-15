import unittest
import tempfile
import os
from src.database.score_manager import ScoreManager


class TestScoreManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_scores.json")
        self.score_manager = ScoreManager(self.db_path)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_add_score(self):
        self.assertTrue(self.score_manager.add_score("Player1", 1000))
        self.assertTrue(self.score_manager.add_score("Player2", 500))
        
        high_scores = self.score_manager.get_high_scores()
        self.assertEqual(len(high_scores), 2)
        self.assertEqual(high_scores[0], ("Player1", 1000))
        self.assertEqual(high_scores[1], ("Player2", 500))
    
    def test_high_score_detection(self):
        self.score_manager.add_score("Player1", 1000)
        self.score_manager.add_score("Player2", 500)
        
        self.assertTrue(self.score_manager.is_high_score(1500))
        self.assertTrue(self.score_manager.is_high_score(600))
        self.assertTrue(self.score_manager.is_high_score(400))  # Still high score since we have < 10 scores
        
        # Fill up to max scores with scores that will be lower than 400
        for i in range(8):
            self.score_manager.add_score(f"Player{i+3}", 100 + i * 10)  # Scores: 100, 110, 120, ..., 170
        
        high_scores = self.score_manager.get_high_scores()
        lowest_score = high_scores[-1][1]  # Should be 100
        
        self.assertTrue(self.score_manager.is_high_score(1500))
        self.assertTrue(self.score_manager.is_high_score(600))
        self.assertTrue(self.score_manager.is_high_score(400))  # 400 > 100, so still high score
        self.assertFalse(self.score_manager.is_high_score(50))  # 50 < 100, so not high score
    
    def test_empty_player_name(self):
        self.assertFalse(self.score_manager.add_score("", 1000))
        self.assertFalse(self.score_manager.add_score("   ", 1000))
    
    def test_max_scores_limit(self):
        for i in range(15):
            self.score_manager.add_score(f"Player{i}", i * 100)
        
        high_scores = self.score_manager.get_high_scores()
        self.assertEqual(len(high_scores), 10)
        self.assertEqual(high_scores[0][1], 1400)
    
    def test_player_stats(self):
        self.score_manager.add_score("Player1", 1000)
        self.score_manager.add_score("Player1", 800)
        self.score_manager.add_score("Player1", 1200)
        
        stats = self.score_manager.get_player_stats("Player1")
        self.assertEqual(stats["games_played"], 3)
        self.assertEqual(stats["highest_score"], 1200)
        self.assertEqual(stats["average_score"], 1000.0)
        self.assertEqual(stats["total_score"], 3000)


if __name__ == "__main__":
    unittest.main()
