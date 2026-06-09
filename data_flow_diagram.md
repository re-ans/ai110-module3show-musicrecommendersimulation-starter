```mermaid
graph TD
    subgraph 1. Input
        A[UserProfile <br> {genre, mood, energy...}]
        B[Song Catalog <br> (from songs.csv)]
    end

    subgraph 2. Process
        C{Loop Through <br> Every Song}
        D[Calculate Score <br> - Genre Match? <br> - Mood Match? <br> - Energy Closeness? <br> - etc.]
        E[(Song, Score) <br> Unsorted List]
    end

    subgraph 3. Output
        F[Sort List by <br> Score Descending]
        G[Select Top 5 <br> Recommendations]
        H{{Final Playlist}}
    end

    A --> C
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
```
