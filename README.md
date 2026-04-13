# 🎵 Music Recommender Simulation

## Project Summary

This is a content-based music recommendation system that represents songs and user taste profiles as data, then uses a weighted-score algorithm to predict which songs a user will love. The system loads a catalog of songs with audio features (genre, mood, energy, acousticness, etc.), captures a user's preferences, and scores each song based on how well it matches the user's taste. The top-k recommendations are returned with human-readable explanations for why each song was suggested. This simulation demonstrates how companies like Spotify and Apple Music make personalization decisions, and reveals how simple algorithms naturally encode bias—overprioritizing certain genres, ignoring minority preferences, and creating "filter bubbles." By building and testing this system, we learn that recommendation engines are not neutral; they reflect the design choices and data we give them.

---

## How The System Works

### Song Features

Each song is represented by the following attributes:

- **Categorical**: `genre` (pop, rock, lofi, ambient, etc.), `mood` (happy, chill, intense, relaxed, etc.)
- **Numeric**: `energy` (0.0–1.0 scale), `tempo_bpm` (beats per minute), `valence` (musical positivity), `danceability`, `acousticness`

These features are loaded from `data/songs.csv` and stored as dictionaries with numeric values converted to floats for scoring calculations.

### User Profile

A user's taste preferences are captured as a dictionary:

```python
{
    "genre": "pop",          # Favorite genre
    "mood": "happy",         # Desired mood
    "energy": 0.8,           # Target energy level (0-1)
    "likes_acoustic": False  # Acoustic preference (True/False)
}
```

### Scoring Algorithm (Algorithm Recipe)

The system scores each song using a **weighted sum** of four factors:

1. **Genre Match** (weight: +2.0) — If the song's genre matches user's favorite genre, add 2.0 points.
2. **Mood Match** (weight: +1.5) — If the song's mood matches user's desired mood, add 1.5 points.
3. **Energy Proximity** (weight: +1.5) — Songs close to the user's target energy score higher. Score = 1.5 × (1.0 − |song_energy − target_energy|)
4. **Acoustic Preference** (weight: +0.5) — If user likes acoustic music AND song acousticness > 0.5, add 0.5 points. If user dislikes acoustic AND acousticness ≤ 0.5, add 0.5 points.

**Example**: For a pop + happy + high-energy user:
- "Sunrise City" (pop, happy, 0.82 energy) scores: 2.0 + 1.5 + 1.41 + 0.5 = **5.41 points**
- "Night Drive Loop" (synthwave, moody, 0.75 energy) scores: 0 + 0 + 1.33 + 0.5 = **1.83 points**

### Recommendation Process

1. Load all songs from CSV
2. For each song, calculate its score using the algorithm above
3. Sort songs by score (highest first)
4. Return top `k` recommendations (default: 5) with explanations

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

### Experiment 1: Weight Sensitivity
Tested how changing genre weight affected recommendations:
- **Default (Genre: 2.0)**: Pop fan always gets pop songs first; very consistent but homogeneous.
- **Reduced (Genre: 0.5)**: Results became more diverse—moody synthwave ranked high for a happy user if it matched energy.
- **Key finding**: Genre weight at 2.0 is strong; users get what they ask for but lose discovery opportunities.

### Experiment 2: User Profiles
Tested three distinct user profiles:
- **"High-Energy Pop" user** (pop, happy, energy=0.8, likes_acoustic=False):
  - Top results: "Sunrise City", "Gym Hero", "Rooftop Lights" ✓ Correct! All high-energy pop.
- **"Chill Lofi" user** (lofi, chill, energy=0.4, likes_acoustic=True):
  - Top results: "Library Rain", "Midnight Coding" ✓ Correct! Acoustic, lo-fi, under 0.5 energy.
- **"Intense Rock" user** (rock, intense, energy=0.9, likes_acoustic=False):
  - Top result: "Storm Runner" (only rock song in catalog) ⚠️ Limited choice; system works but dataset is too small.

### Experiment 3: Edge Case - Conflicting Preferences
Tested user with contradictory preferences (e.g., "intense" mood but "acoustic" songs):
- **Result**: System prioritized genre and mood, then adjusted energy. Acoustic preference became a tie-breaker.
- **Issue identified**: Binary "likes_acoustic" can't represent nuanced preferences like "intense acoustic guitar." Real users have more complex relationships with production style.

### Experiment 4: Acoustic Preference Impact
Toggled `likes_acoustic` to see its influence:
- **With acoustic=True**: Songs with acousticness > 0.5 got a +0.5 bonus (e.g., "Library Rain" rose in rankings).
- **With acoustic=False**: Same songs were penalized; produced tracks like "Gym Hero" dominated.
- **Finding**: The 0.5 weight is subtle. Most results didn't change much, suggesting acoustic preference is a minor factor compared to genre/mood.

---

## Limitations and Risks

1. **Tiny Catalog**: With only 10 songs, the system can't provide meaningful variety. Real recommenders need millions of songs; ours exhausts all options in one or two searches.

2. **Genre Dominance**: The +2.0 weight on genre is so strong that non-genre matches are effectively ignored. A user who "feels like rock" gets rock songs even if they'd prefer mood/energy matches in other genres.

3. **No Semantic Understanding**: Features are pure numbers. The system can't understand that "intense" might pair well with "aggressive guitar" or understand the emotional arc of a song. A song's cultural meaning, lyrics, or artist identity are invisible.

4. **Binary Acoustic Preference**: Acousticness is treated as on/off, but real music exists on a spectrum of acoustic/electronic blends. A user might love "acoustic drums on an electronic beat" but there's no way to express this.

5. **No Diversity Penalty**: If a user loves indie pop, they'll get the same 5 indie pop songs ranked by energy. There's no incentive to explore adjacent genres—just repetition of "best matches."

6. **Dataset Bias**: The song catalog skews toward modern electronic/indie styles (lofi, synthwave, indie pop). Rock, classical, hip-hop, country, and regional music are absent. This ensures minority genre fans get poor recommendations while pop/lofi fans get great ones.

7. **Cold-Start Problem**: New users with no profile can't be matched. The system assumes users can articulate their taste precisely; many can't or don't want to.

8. **Static Profiles**: Real music taste is context-dependent. Someone listens to different music at the gym, studying, working, or sleeping. Our fixed profile can't adapt.

9. **Popularity Bias Ignored**: A forgotten deep cut scores the same as a chart-topper. The system has no sense of cultural moment, trends, or discovery potential.

---

## Reflection

Building this music recommender revealed something surprising: algorithms don't just describe preferences—they actively shape them. The moment I chose to weight genre at 2.0 instead of 1.0, I wasn't neutrally "predicting" taste; I was deciding that genre mattered more than mood or energy. Every design choice bakes in assumptions about what users care about. I realized that "personalization" is really a mathematical encoding of someone else's beliefs about what "good" recommendations look like.

The most striking moment was testing the rock fan profile and seeing only one rock song come up. I could have blamed the tiny dataset, but that's exactly the point—the system amplifies whatever pattern exists in the data. If 70% of songs are pop, the algorithm naturally gravitates toward pop dominance. Real platforms face this at massive scale: if Spotify's training data reflects what already-popular users stream, the recommendations reinforce existing popularity, creating a feedback loop that locks out niche genres and emerging artists. What I built as a classroom simulation is actually a template for how algorithmic bias gets baked into real products. The tools (Python, CSV, weighted scores) are simple, but the impact—on whose music gets heard, whose culture gets represented, how much discovery someone gets—is massive. This project taught me that responsible AI starts not with a clever algorithm, but with asking hard questions about who benefits and who gets left behind.

**Key takeaway**: There's no such thing as a neutral recommender. Every system we build is a reflection of choices about what matters, who we serve, and what kind of world we're building. Using AI didn't change this; it just made the effects faster and bigger.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

