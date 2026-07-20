import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load song records from a CSV file and return them as dictionaries."""
    print(f"Loading songs from {csv_path}...")

    numeric_fields = {
        "id": int,
        "energy": float,
        "tempo_bpm": float,
        "valence": float,
        "danceability": float,
        "acousticness": float,
    }

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            song = dict(row)
            for field, converter in numeric_fields.items():
                song[field] = converter(song[field])
            songs.append(song)

    print(f"Loaded songs: {len(songs)}")
    return songs

# Algorithm Recipe (Phase 2): point weights for scoring
GENRE_MATCH_POINTS = 2.0
MOOD_MATCH_POINTS = 2.0
ENERGY_MAX_POINTS = 2.0
ACOUSTIC_MATCH_POINTS = 1.0
ACOUSTIC_MISMATCH_PENALTY = -0.5
ACOUSTIC_THRESHOLD = 0.5


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return the score with reason strings."""
    score = 0.0
    reasons: List[str] = []

    user_genre = user_prefs.get("genre") or user_prefs.get("favorite_genre", "")
    user_mood = user_prefs.get("mood") or user_prefs.get("favorite_mood", "")
    target_energy = user_prefs.get("energy", user_prefs.get("target_energy", 0.5))
    likes_acoustic = user_prefs.get("likes_acoustic")

    if song["genre"].lower() == user_genre.lower():
        score += GENRE_MATCH_POINTS
        reasons.append(f"genre match (+{GENRE_MATCH_POINTS:.1f})")

    if song["mood"].lower() == user_mood.lower():
        score += MOOD_MATCH_POINTS
        reasons.append(f"mood match (+{MOOD_MATCH_POINTS:.1f})")

    energy_diff = abs(song["energy"] - target_energy)
    energy_points = ENERGY_MAX_POINTS * (1.0 - energy_diff)
    if energy_points > 0:
        score += energy_points
        reasons.append(f"energy close to target (+{energy_points:.1f})")

    if likes_acoustic is not None:
        if likes_acoustic and song["acousticness"] >= ACOUSTIC_THRESHOLD:
            score += ACOUSTIC_MATCH_POINTS
            reasons.append(f"acoustic style match (+{ACOUSTIC_MATCH_POINTS:.1f})")
        elif not likes_acoustic and song["acousticness"] >= ACOUSTIC_THRESHOLD:
            score += ACOUSTIC_MISMATCH_PENALTY
            reasons.append(f"acoustic style mismatch ({ACOUSTIC_MISMATCH_PENALTY:+.1f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Return the top k songs ranked by score against the given user preferences."""
    scored: List[Tuple[Dict, float, List[str]]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))

    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
