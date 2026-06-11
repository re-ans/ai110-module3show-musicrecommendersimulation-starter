"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, Recommender, UserProfile


def run_and_print_recommendations(profile: UserProfile, recommender: Recommender, title: str):
    """Runs the recommender for a given profile and prints the results."""
    print(f"\n--- {title} ---")
    print(f"Genre: {profile.favorite_genre}, Mood: {profile.favorite_mood}")
    print(f"Target Vibe: Energy={profile.target_energy}, Valence={profile.target_valence}, Danceability={profile.target_danceability}")
    
    recommendations = recommender.recommend(profile, num_recommendations=5)
    
    print("\n--- Top 5 Recommendations ---\n")
    if not recommendations:
        print("No recommendations found.")
        return

    for song, score in recommendations:
        print(f"'{song.title}' by {song.artist} (Score: {score:.2f})")
        print(f"   - Genre: {song.genre}, Mood: {song.mood}, Energy: {song.energy}, Valence: {song.valence}, Danceability: {song.danceability}\n")


def main() -> None:
    # Define the weights for each feature
    weights = {
        'genre': 40,
        'mood': 30,
        'energy': 10,
        'valence': 10,
        'danceability': 10,
    }

    # Load the song catalog
    songs = load_songs("data/songs.csv")

    # Create a recommender instance
    recommender = Recommender(songs, weights)

    # --- Profile 1: The "Conflicting Vibe" ---
    # A user who wants a 'chill' mood but with very high energy.
    profile1 = UserProfile(
        favorite_genre="lofi",
        favorite_mood="chill",
        target_energy=0.9,
        target_valence=0.8,
        target_danceability=0.8
    )
    run_and_print_recommendations(profile1, recommender, "Test Case 1: Conflicting Vibe (Chill + High Energy)")

    # --- Profile 2: The "Niche Genre" ---
    # A user who wants an 'intense' 'jazz' song, which doesn't exist in the catalog.
    profile2 = UserProfile(
        favorite_genre="jazz",
        favorite_mood="intense",
        target_energy=0.95,
        target_valence=0.4,
        target_danceability=0.7
    )
    run_and_print_recommendations(profile2, recommender, "Test Case 2: Niche Genre (Intense Jazz)")

    # --- Profile 3: The "Ambiguous Pop" ---
    # A user who likes 'pop' with a 'moody' vibe but neutral numerical preferences.
    profile3 = UserProfile(
        favorite_genre="pop",
        favorite_mood="moody",
        target_energy=0.5,
        target_valence=0.5,
        target_danceability=0.5
    )
    run_and_print_recommendations(profile3, recommender, "Test Case 3: Ambiguous Pop (Neutral Vibe)")


if __name__ == "__main__":
    main()
