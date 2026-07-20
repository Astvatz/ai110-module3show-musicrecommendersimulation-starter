"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def format_recommendations(
    recommendations: list[tuple[dict, float, list[str]]],
    user_prefs: dict,
) -> str:
    """Build a clean, readable terminal layout for recommendation results."""
    genre = user_prefs.get("genre") or user_prefs.get("favorite_genre", "any")
    mood = user_prefs.get("mood") or user_prefs.get("favorite_mood", "any")
    energy = user_prefs.get("energy", user_prefs.get("target_energy", 0.5))

    lines = [
        "",
        "=" * 60,
        "  MUSIC RECOMMENDATIONS",
        "=" * 60,
        f"  Profile: genre={genre}, mood={mood}, energy={energy:.1f}",
        "-" * 60,
        "",
    ]

    if not recommendations:
        lines.append("  No recommendations found.")
        lines.append("")
        return "\n".join(lines)

    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        lines.append(f"  #{rank}  {song['title']}")
        lines.append(f"       Final score: {score:.2f}")
        lines.append("       Reasons:")
        if reasons:
            for reason in reasons:
                lines.append(f"         - {reason}")
        else:
            lines.append("         - No strong matches")
        lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(format_recommendations(recommendations, user_prefs))


if __name__ == "__main__":
    main()
