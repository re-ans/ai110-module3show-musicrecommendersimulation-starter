# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Shabeat Shabang

---

## 2. Intended Use  

This model generates personalized song recommendations based on a user's taste profile. It assumes the user has specific preferences for genre, mood, and musical attributes. The system is designed for classroom exploration, not for real users.  

---

## 3. How the Model Works  

The model scores songs by comparing their features to a user's preferences. It uses genre, mood, energy, valence, and danceability. The final score is a weighted sum, where genre and mood matches are most important. This is a custom implementation moving beyond the starter logic.

---

## 4. Data  

The model uses a catalog of 20 songs. The data represents a mix of genres like pop, lofi, rock, and jazz, with various moods. I expanded the dataset from the original 10 songs. The catalog is missing many genres and does not consider lyrical content.  

---

## 5. Strengths  

The system works well for users with clear genre and mood preferences. It correctly captures the idea that categorical matches are more important than numerical vibes. The recommendations for the "Conflicting Vibe" profile matched my intuition perfectly.  

---

## 6. Limitations and Bias 

The system does not consider lyrics, artist, or song popularity. Genres like jazz and rock are underrepresented in the data. The recommender heavily overfits to genre, making it hard for users to discover new styles. The scoring might unintentionally favor mainstream genres with more songs in the catalog.  

---

## 7. Evaluation  

I tested the system with three adversarial profiles: a conflicting vibe, a niche genre, and an ambiguous profile. I looked for logical and predictable outcomes in the recommendations. I was surprised by how the "Niche Genre" test produced two distinct types of compromise recommendations. I also ran simple comparisons by changing the feature weights.

---

## 8. Future Work  

I would add artist and popularity as new features. I would also create a better explanation for why each song is recommended. To improve diversity, I would add a rule to prevent showing too many songs from the same artist. The system could also be improved to handle multiple genre or mood preferences.  

---

## 9. Personal Reflection  

I learned that recommendation is a game of trade-offs and compromises. I was surprised that changing weights didn't always change the top results. This project made me realize that real-world recommenders are less about finding a "perfect" song and more about creating a balanced and diverse list of "good enough" options.  
