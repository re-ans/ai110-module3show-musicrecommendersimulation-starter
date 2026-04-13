# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**SonicMatch 1.0**

---

## 2. Intended Use  

SonicMatch is a content-based music recommendation engine designed for **classroom exploration and learning only**—not for real production use. It suggests 5 personalized songs from a small catalog (10 tracks) based on a user's stated favorite genre, mood preference, target energy level, and acoustic preference. The system is built to help students understand how music streaming platforms like Spotify, Apple Music, and YouTube Music decide what to recommend next, and to practice identifying where algorithmic bias naturally emerges in even simple systems. 

**Key assumptions**: Users can clearly articulate their taste preferences (genre, mood, energy), and the system assumes that songs with matching genres/moods and similar energy levels are "good" recommendations. The system does not learn from user behavior, adapt to context, or consider cultural trends.

---

## 3. How the Model Works  

Imagine you tell your friend: "I want to hear energetic happy pop music, and I don't care if it's acoustic or produced." SonicMatch takes that statement and checks every song in its catalog against those criteria.

For each song, it awards points:
- **Genre match**: If the song is in your favorite genre, it gets 2 points out of 5. This is the biggest factor.
- **Mood match**: If the song has your preferred mood (happy, chill, intense, etc.), it gets 1.5 points.
- **Energy match**: The system checks if the song's energy is close to what you want. A song with your exact target energy gets the full 1.5 points; songs further away get less.
- **Acoustic preference**: If you like acoustic music and the song is acoustic (acousticness > 0.5), it gets a 0.5-point bonus. If you like produced music and the song is electronic/produced, same bonus.

All points are added up. Songs with the highest total score are recommended first, and the system explains why each song scored well (e.g., "Genre match (pop) + mood match (happy) + matches your energy level").

The system is **deterministic**—same user profile always produces the same ranking. No randomness. Very predictable.

---

## 4. Data  

**Dataset size**: 10 songs with 10 features each (id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness).

**Genres represented**: Pop, Rock, Lofi, Ambient, Synthwave, Indie Pop, Jazz (7 genres total, but imbalanced—pop appears 3 times, lofi 2 times).

**Moods represented**: Happy, Chill, Intense, Relaxed, Moody (focused is also represented).

**Data modifications**: No songs were added or removed. Used the provided starter dataset as-is.

**Missing music**: The catalog severely underrepresents or excludes:
- Classical, orchestral, or acoustic instrumental music
- Hip-hop, rap, R&B, soul
- Country, folk, bluegrass
- Regional/non-English language music
- Electronic dance music (EDM) beyond synthwave
- Metal, punk, experimental genres

This creates an inherent bias toward young, Western, tech-savvy listeners with a taste for modern electronic/indie styles. A 50-year-old who loves classic rock or a Bollywood fan would get poor recommendations.

---

## 5. Strengths  

- **Genre-mood alignment works well**: The system excels at matching users who know exactly what they want. A "pop + happy" user can reliably find upbeat pop songs.

- **Energy matching is intuitive**: Users who want energetic music see high-energy songs ranked first; users wanting chill music get low-energy picks. This matches how people think about music.

- **Transparent explanations**: Every recommendation comes with a reason: "You got this because it matches your pop + happy preference and has energy level 0.82." Users understand *why* a song was suggested, which builds trust.

- **Simple and fast**: With 10 songs, the algorithm runs instantly. Real datasets would scale linearly, which is efficient compared to collaborative filtering.

- **Consistent and deterministic**: Same profile always yields identical results, making it easy to test, debug, and understand the system's behavior.

- **Captures genre enthusiasm**: For users strongly committed to a genre, the system delivers focused recommendations without wasting time on adjacent genres.

---

## 6. Limitations and Bias 

- **Genre weight is overwhelming (2.0 out of 5 max)**: Genre matches are so heavily rewarded that other factors barely matter. A user asking for "pop recommendations" will get pop first regardless of whether other songs better match their mood/energy. This narrows discovery.

- **Extreme dataset bias toward pop/lofi/indie**: The starter data reflects a narrow slice of music. Jazz lovers get 1 song, rock fans get 1 song, pop fans get 3. This inequality means recommendations aren't equally good for all users.

- **No contextual awareness**: The system doesn't know if it's Monday morning (study mode), Friday night (party mode), or Sunday evening (relaxation mode). Same profile always yields same recommendations regardless of context.

- **Binary acoustic preference misses nuance**: Real music exists on a spectrum. A user might love "acoustic guitar with electronic drums"—neither purely acoustic nor produced. But the system only offers on/off.

- **No user history or learning**: The system doesn't improve with feedback. If you hate every recommendation despite stating your preferences, the system keeps recommending the same way.

- **Tiny catalog makes diversity impossible**: With 10 songs, if you like indie pop, you'll get the same 2 indie pop songs in every top-5 list. No opportunity for serendipitous discovery.

- **No popularity or freshness signal**: A forgotten deep cut that matches your taste scores identically to a trending hit. The system can't surface rising artists or capitalize on cultural moments.

- **No handling of nuanced mood preferences**: The system treats "intense" and "chill" as binary categories, but mood exists on a spectrum. Someone might want "intense but not aggressive" or "chill but with some energy."

---

## 7. Evaluation  

**User profiles tested:**

| Profile | Tested Preferences | Expected Result | Actual Result | Grade |
|---------|-------------------|-----------------|---------------|-------|
| **Pop + Happy** | pop, happy, energy=0.8, likes_acoustic=False | Upbeat pop songs first | "Sunrise City", "Gym Hero", "Rooftop Lights" | ✓ |
| **Lofi + Chill** | lofi, chill, energy=0.4, likes_acoustic=True | Relaxed acoustic lofi tracks | "Library Rain", "Midnight Coding" | ✓ |
| **Rock + Intense** | rock, intense, energy=0.9, likes_acoustic=False | High-energy rock songs | "Storm Runner" (only rock song available) | ⚠️ Limited |
| **Jazz + Relaxed** | jazz, relaxed, energy=0.35, likes_acoustic=True | Smooth acoustic jazz | "Coffee Shop Stories" | ✓ |
| **Ambient + Chill** | ambient, chill, energy=0.28, likes_acoustic=True | Ambient atmospheric tracks | "Spacewalk Thoughts" | ✓ |

**Surprises discovered:**
- Songs ranked #2 were often very close in score to #1, suggesting ties at different weights would swap rankings frequently. The system is sensitive to weight changes.
- A user with "intense" mood + high energy (0.9) who likes acoustic music ended up with no good recommendations (most intense songs are non-acoustic), revealing the acoustic preference conflict.
- Genre weight of 2.0 was so dominant that mood didn't matter much—if no songs matched your exact genre, even perfect mood/energy matches ranked poorly.

**Conclusion**: System works well for mainstream preferences (pop, lofi, indie) but fails gracefully for minority genres (rock, jazz get only 1 song each) and doesn't handle contradictory preferences well.

---

## 8. Future Work  

- **Expand dataset significantly**: Add 100+ songs across all genres, explicitly balancing representation. Include classical, hip-hop, country, regional music.
- **Add context awareness**: Support multiple profiles—"GymRecommender," "StudyRecommender," "PartyRecommender"—that suggest different songs based on user's activity.
- **Implement diversity penalty**: After recommending a song, temporarily lower the score of similar songs (same artist, same subgenre) so users get varied results.
- **Spectrum instead of binary**: Replace "likes_acoustic" with a continuous preference from 0 (pure electronic) to 1 (pure acoustic).
- **Add collaborative filtering**: Learn from similar users' behavior; if users with taste profile X also liked song Y, recommend Y even if it doesn't match all of X's stated preferences.
- **Incorporate popularity and freshness**: Add signals for songs trending, newly released, or historically significant.
- **Allow complex preferences**: Let users say "I like both intense rock AND chill jazz" instead of forcing a single mood/genre choice.
- **User feedback loop**: If a user rejects a recommendation, reduce future scores for similar songs rather than ignoring the feedback.

---

## 9. Personal Reflection  

This project fundamentally changed how I think about algorithms. Before building this, "personalization" sounded magical—the system *just knows* what you'll love. But once I assigned the weights and saw the results, I realized personalization is just encoding someone's *opinion* about what good taste looks like, then scaling it to millions of users. The +2.0 weight on genre wasn't neutral; it was me saying genre matters more than mood. Spotify engineers made the same choice, just at a larger scale.

The most powerful moment was discovering that smallest design choices have outsized impact. Changing one weight from 2.0 to 0.5 completely reshuffled rankings. In production systems with millions of users, such a change could reshape what music gets heard across the entire platform—deciding the fate of genres and artists. I realized that data scientists and engineers hold more cultural power than they often acknowledge.

What surprised me most was how the system's failures revealed truth. When rock fans got bad recommendations because there was only one rock song, or when a user's contradictory preferences broke the system, these failures weren't bugs—they were the algorithm faithfully executing its design. Real recommenders fail in the same ways, just hidden at scale. The "poor recommendations you see on Spotify for your taste" might not be bugs; they might be intentional design choices prioritizing other goals (engagement, profitability) over pure accuracy.

If I extended this, I'd want to interview users with different backgrounds—someone who loves classical, someone who loves regional Indian music, someone over 60—and redesign the system to serve *them* well, not just teenage pop fans. because right now, my recommender is biased toward people like me. Real recommendation systems have that same bias, usually invisible, affecting billions of choices about what culture gets promoted.  
