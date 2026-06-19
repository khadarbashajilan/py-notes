
def battle(c1, c2):
    print(f"🏁 BATTLE START: {c1} vs {c2}\n" + "="*40)
    
    round_num = 1
    while c1.is_alive and c2.is_alive:
        print(f"\n--- Round {round_num} ---")
        
        # Attacker 1's turn
        try:
            c1.attack(c2)
        except ValueError as e:
            print(e)
        print(c2)
        
        if not c2.is_alive:
            break
            
        # Attacker 2's turn
        try:
            c2.attack(c1)
        except ValueError as e:
            print(e)
        print(c1)
        
        round_num += 1

    print("\n" + "="*40)
    winner = c1 if c1.is_alive else c2
    print(f"🏆 {winner.name} is VICTORIOUS!")
