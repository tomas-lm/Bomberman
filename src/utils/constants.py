GAME_CONFIG = {
    'SCREEN_WIDTH': 800,
    'SCREEN_HEIGHT': 600,
    'TILE_SIZE': 40,
    'MAP_WIDTH': 20,
    'MAP_HEIGHT': 15,
    'FPS': 60,

    # Player movement & lives
    'PLAYER_SPEED': 3.0,
    'PLAYER_LIVES': 3,
    'PLAYER_INVINCIBILITY_TIME': 1.25,

    # Enemies
    'ENEMY_SPEED': 1.5,

    # Bombs & explosions
    'BOMB_TIMER': 3.0,
    'BOMB_COOLDOWN': 0.5,
    'PLAYER_BOMB_CAPACITY': 1,
    'EXPLOSION_RADIUS': 2,
    'EXPLOSION_DURATION_MS': 500,  # duração da chama

    # Scores
    'ENEMY_SCORE': 100,
    'WALL_SCORE': 50,
    'LEVEL_COMPLETE_BONUS': 500,

    # Power-ups
    'POWERUP_DROP_CHANCE': 0.25,   # 25%
    'SPEED_UP_DELTA': 0.5,
    'MAX_SPEED': 5.0,
    'MAX_BOMB_CAPACITY': 6,
    'MAX_FLAME_RADIUS': 8,
}

COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'GRAY': (128, 128, 128),
    'DARK_GRAY': (64, 64, 64),
    'BROWN': (139, 69, 19),
    'YELLOW': (255, 221, 0),
    'ORANGE': (255, 140, 0),
    'CYAN': (0, 200, 255),
    'PINK': (255, 105, 180),
}
