import random
import random
from itertools import product 
def create_deck():
    suits = ["Diamonds", "Clubs", "Hearts", "Spades"]
    ranks = ["Ace"] + list(range(2, 11)) + ["Jack", "Queen", "King"]
    deck = list(product(suits, ranks))
    random.shuffle(deck)
    return deck

def shuffle_discard_into_deck(deck, discard_pile):
    print("Deck is getting small. Shuffling the deck now!")
    if not discard_pile:
        print("Warning: Discard pile is empty. Continuing with small deck.")
        return
    deck.extend(discard_pile)
    discard_pile.clear()
    random.shuffle(deck)
    print(f"New Deck Size: {len(deck)}")
    return 

def deal_cards(num_cards, deck):
    if len(deck) < num_cards:
        raise ValueError("Not enough cards in the deck to deal the required amount.")

    hand = [deck.pop(0) for _ in range(num_cards)]
    return hand

def cleanup_hands(discard_pile, dealer_hand, player_hand):
    discard_pile.extend(dealer_hand)
    discard_pile.extend(player_hand)
    
    dealer_hand.clear()
    player_hand.clear()
    
    print(f"Round finished. Discard pile now has {len(discard_pile)} cards.")

def initial_dealing(deck):
    player_hand = deal_cards(2, deck)
    dealer_hand = deal_cards(2, deck)
    
    # Now we print what the player sees
    dealer_up_card = dealer_hand[0] 
    
    print(f"\nDealer gets two cards: Face down and Face up: {dealer_up_card}")
    print(f"Player gets two cards both face up: {player_hand}")
    
    return player_hand, dealer_hand, deck

class Player:
    def __init__(self, playerMoney):
        self.money = playerMoney

    def mon(self):
        print(f"Player starts with ${self.money}")


def players_turn(player_hand, dealer_hand, deck):
    print("--- Player's Turn ---")
    print(f"Player Hand: {player_hand}")
    print(f"Dealer Up Card: {dealer_hand[0]}")

    players_sum = card_sum_convert(player_hand)
    print(f"Player sum: {players_sum}")
    
    # Call the refactored function and return its results
    final_sum, is_busted = hit_stay(players_sum, player_hand, deck)
    
    return final_sum, is_busted

def dealers_turn(dealer_hand, deck, is_player_busted):
    print("\n--- Dealer's Turn ---")
    
    # If player busted, dealer doesn't need to play (unless for show)
    if is_player_busted:
        print("Player busted. Dealer wins by default.")
        dealer_sum = card_sum_convert(dealer_hand)
        # We need the final sum, so we calculate it but don't play the turn
        return dealer_sum, False # Return sum, NOT busted (since they didn't hit)

    # 1. Reveal the hand
    print(f"Dealer reveals hole card. Dealer Hand: {dealer_hand}")
    dealer_sum = card_sum_convert(dealer_hand)
    print(f"Dealer's initial sum: {dealer_sum}")

    # 2. Dealer hits on 16 or less
    while dealer_sum < 17:
        print("Dealer hits (must hit on 16 or less)...")
        new_card = deck.pop(0)
        dealer_hand.append(new_card)
        dealer_sum = card_sum_convert(dealer_hand)
        print(f"Dealer draws: {new_card}. \n New Hand: {dealer_hand}")
        print(f"Dealer's new sum: {dealer_sum}")

    # 3. Check final status
    if dealer_sum > 21:
        print(f"Dealer busts with {dealer_sum}!")
        return dealer_sum, True # Dealer busted
    
    print(f"Dealer stands with a total of {dealer_sum}.")
    return dealer_sum, False # Dealer stood, not busted


def card_sum_convert(card_hand):
    card_sum = 0
    ace_count = 0
    for card in card_hand:
        rank = card[1] 
        
        if rank in ['King', 'Queen', 'Jack']:
            card_sum += 10
            
        elif rank == 'Ace':
            ace_count += 1
            
        else: 
            card_sum += rank
            
    if ace_count > 0:
        card_sum += 11  
        card_sum += (ace_count - 1) 
        while card_sum > 21 and ace_count > 0:
            card_sum -= 10
            ace_count -= 1       
    return card_sum

def ace_case(value):
    if value < 10:
        print("Ace value changes to 11")
        return 11
    else:
        print("Ace value changes to 1")
        return 1

def checksum2(dealer_sum):
    if dealer_sum > 21:
        print(f"Dealer busted with value = {dealer_sum}")
        return False
    elif dealer_sum == 21:
        print("Dealer got 21. You Lose")
        return False
    elif dealer_sum == 16:
        print("Dealer hit soft 16. Cant hit anymore")
        return False
    elif dealer_sum < 16:
        return True

def checksum(current_sum):
    if current_sum > 21:
        print(f"Busted with value = {current_sum}")
        return False
    elif current_sum == 21:
        print("You got 21. You win")
        return False
    
    else:
        return True
    

def hit_stay(current_sum, current_hand, deck):
    # Returns: (final_sum, is_busted)
    
    while True:
        # Check for immediate bust or 21 (Blackjack/21)
        if current_sum > 21:
            print(f"Busted with value = {current_sum}")
            return current_sum, True # Busted
        if current_sum == 21:
            print("You got 21!")
            return current_sum, False # Stood on 21

        print(f"Current sum: {current_sum}")
        x = input("Press 1 to hit and 2 to stay: ")

        if x == "1":
            # HIT
            current_hand.append(deck.pop(0))
            print(f"Current hand: {current_hand}")
            current_sum = card_sum_convert(current_hand)
            print(f"Current sum: {current_sum}")
            # Loop continues to check the sum again
            
        elif x == "2":
            # STAY
            print(f"Player decided to stay, player sum = : {current_sum}")
            return current_sum, False # Not busted, Stood

        else:
            print("Invalid input. Please try again.")
            # Continue the loop for valid input

def determine_winner(player_sum, dealer_sum, is_player_busted, is_dealer_busted, bet_amount, player_object):
    
    print("\n--- FINAL RESULTS ---")
    
    winnings = 0
    message = ""
    
    # A. Determine win/loss based on busts
    if is_player_busted:
        message = "Player busted. Dealer wins."
        
    elif is_dealer_busted:
        winnings = bet_amount * 2
        message = "Dealer busts! Player wins."
    
    # B. If no busts, compare totals
    elif player_sum > dealer_sum:
        winnings = bet_amount * 2
        message = "Player's hand is higher. Player wins."
        
    elif player_sum < dealer_sum:
        message = "Dealer's hand is higher. Dealer wins."
        
    else: # player_sum == dealer_sum
        winnings = bet_amount # Player gets their bet back
        message = "It's a Push! Bet is returned."
        
    player_object.money += winnings
    print(f"{message}. Player's money is now: ${player_object.money}")

#betting -> dealing -> players turn -> dealers turn
def game():
    print("--- 🃏 GAME STARTS 🃏 ---")
    
    # Initialize Game State Variables
    p1 = Player(100)
    p1.mon()
    
    # Initialize the core game resources
    shuffled_deck = create_deck()
    discard_pile = [] 
    
    print(f"Initial Deck Size: {len(shuffled_deck)}")

    while True:
        print("\n--- NEW ROUND ---")
        
        # A. Deck Check/Refill
        if len(shuffled_deck) < 10: # Check before dealing 4 cards
            shuffle_discard_into_deck(shuffled_deck, discard_pile)
            
        # B. Betting (Your existing logic)
        try:
            bet_amount = int(input(f"Current Money: ${p1.money}. Enter bet amount: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        
        if bet_amount > p1.money or bet_amount <= 0:
            print("Amount invalid or insufficient funds.")
            continue
        
        if p1.money <= 0:
            print("Game over! Out of money.")
            break
            
        # Apply bet
        p1.money -= bet_amount
        print(f"Bet of ${bet_amount} placed. Remaining money: ${p1.money}")
        
        # C. Dealing
        try:
            current_player_hand, current_dealer_hand, deck = initial_dealing(shuffled_deck)
        except ValueError as e:
            print(f"Error dealing cards: {e}. Cannot continue.")
            break
            
        # D. Player's Turn: Capture final state
        final_player_sum, is_player_busted = players_turn(current_player_hand, current_dealer_hand, deck)
        
        # E. Dealer's Turn: Capture final state
        dealer_sum, is_dealer_busted = dealers_turn(current_dealer_hand, deck, is_player_busted)
        
        # F. WIN/LOSS/PUSH LOGIC
        determine_winner(final_player_sum, dealer_sum, is_player_busted, is_dealer_busted, bet_amount, p1)
        
        # G. Cleanup
        cleanup_hands(discard_pile, current_dealer_hand, current_player_hand)
        
        if input("Continue to next round? (y/n): ").lower() != 'y':
            break

# You must add the determine_winner function and replace your existing
# players_turn, hit_stay, and dealers_turn functions with the ones provided above.

def main():
    game()
    
if __name__ == "__main__":
    main()