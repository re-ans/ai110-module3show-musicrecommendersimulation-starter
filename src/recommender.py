import csv
from dataclasses import dataclass

@dataclass
class Song:
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

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=int(d['id']),
            title=d['title'],
            artist=d['artist'],
            genre=d['genre'],
            mood=d['mood'],
            energy=float(d['energy']),
            tempo_bpm=float(d['tempo_bpm']),
            valence=float(d['valence']),
            danceability=float(d['danceability']),
            acousticness=float(d['acousticness']),
        )

@dataclass
class UserProfile:
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_valence: float
    target_danceability: float

class Recommender:
    def __init__(self, songs, weights):
        self.songs = songs
        self.weights = weights

    def calculate_score(self, song, profile):
        score = 0

        # Categorical feature scoring
        if song.genre == profile.favorite_genre:
            score += self.weights['genre']
        if song.mood == profile.favorite_mood:
            score += self.weights['mood']

        # Numerical feature scoring (inverse absolute difference)
        score += self.calculate_numerical_score(
            profile.target_energy, song.energy, self.weights['energy']
        )
        score += self.calculate_numerical_score(
            profile.target_valence, song.valence, self.weights['valence']
        )
        score += self.calculate_numerical_score(
            profile.target_danceability, song.danceability, self.weights['danceability']
        )
        
        return score

    def calculate_numerical_score(self, target, value, weight):
        """Calculates score based on closeness to a target value."""
        # The +1 in the denominator prevents division by zero and normalizes the score
        similarity = 1 / (1 + abs(target - value))
        return similarity * weight

    def recommend(self, profile, num_recommendations=5):
        scored_songs = []
        for song in self.songs:
            score = self._calculate_score(song, profile)
            scored_songs.append((song, score))
        
        # Sort songs by score in descending order
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        
        # Return the top N recommendations
        return scored_songs[:num_recommendations]

def load_songs(filename="data/songs.csv"):
    songs = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append(Song.from_dict(row))
    return songs
