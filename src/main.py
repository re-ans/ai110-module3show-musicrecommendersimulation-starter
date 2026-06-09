"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, Recommender, UserProfile


def main() -> None:
    # Define the weights for each feature
    weights = {
        'genre': 40,
        'mood': 30,
        'energy': 10,
        'valence': 10,
        'danceability': 10,
    }

    # Define the user's taste profile
    user_profile = UserProfile(
        favorite_genre="rock",
        favorite_mood="intense",
        target_energy=0.9,
        target_valence=0.5,
        target_danceability=0.7
    )

    # Load the song catalog
    songs = load_songs("data/songs.csv")

    # Create a recommender instance
    recommender = Recommender(songs, weights)

    # Get recommendations
    recommendations = recommender.recommend(user_profile, num_recommendations=5)

    print("\n--- User Profile ---")
    print(f"Genre: {user_profile.favorite_genre}, Mood: {user_profile.favorite_mood}")
    print(f"Target Vibe: Energy={user_profile.target_energy}, Valence={user_profile.target_valence}, Danceability={user_profile.target_danceability}")
    print("\n--- Top 5 Recommendations ---\n")

    for song, score in recommendations:
        print(f"'{song.title}' by {song.artist} (Score: {score:.2f})")
        print(f"   - Genre: {song.genre}, Mood: {song.mood}, Energy: {song.energy}, Valence: {song.valence}, Danceability: {song.danceability}\n")


if __name__ == "__main__":
    main()
