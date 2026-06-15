import random

countries = ["Brazil", "France", "Argentina", "England", "Germany",
             "Spain", "Portugal", "Senegal", "USA", "Morocco"]

print( )
print("WORLD CUP 2026 SIMULATOR")
print( )
print("Countries in the tournament:")
for i, country in enumerate(countries, 1):
    print(f"  {i}. {country}")

# Ask the user to pick a country to support
print()
chosen = input("Enter the name of the country you think will win: ").strip().title()

if chosen not in countries:
    print(f"{chosen} is not in the tournament. Adding them as a wildcard!")
    countries.append(chosen)

print()
print(f"You are supporting: {chosen}")
print("Simulating matches... press Enter after each result.\n")

round_number = 1
remaining = countries.copy()

# ── Main simulation loop ───────────────────────────────────
while len(remaining) > 1:

    print(f"--- ROUND {round_number} ---")
    next_round = []

    i = 0
    while i < len(remaining):

        # If odd number of teams, last one gets a bye (pass example)
        if i + 1 == len(remaining):
            print(f"  {remaining[i]} gets a bye (no opponent this round).")
            next_round.append(remaining[i])
            pass  # nothing extra to do, move on

        else:
            team1 = remaining[i]
            team2 = remaining[i + 1]

            input(f"  Match: {team1}  vs  {team2}  -- press Enter to see result...")

            # Simulate match result randomly
            winner = random.choice([team1, team2])
            loser  = team2 if winner == team1 else team1

            print(f"  Result: {winner} wins! {loser} is eliminated.")

            # If the chosen country lost, react but continue watching
            if loser == chosen:
                print(f"\n  Oh no! {chosen} has been eliminated.")
                print("  You'll keep watching as a neutral fan.\n")
                chosen = None   # they're out; stop tracking
                next_round.append(winner)
                i += 2
                continue        # skip to next match

            next_round.append(winner)

        i += 2

    remaining = next_round
    round_number += 1
    print()

    # If only one team left, the loop will end naturally
    if len(remaining) == 1:
        break   # exit the while loop — we have a winner

# ── Announce the winner ────────────────────────────────────
print( )
winner = remaining[0]
print(f"  WORLD CUP 2026 WINNER:  {winner}!")
print( )

if winner == chosen:
    print(f"  Congratulations! Your country {winner} won the World Cup!")
elif chosen is None:
    print(f"  Your country was eliminated, but {winner} took the trophy!")
else:
    print(f"  {winner} is the champion! Better luck next time for {chosen}.")

print()