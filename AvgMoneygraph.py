import random
import numpy as np
import matplotlib.pyplot as plt

# Define positions for Chance and Community Chest cards
chance_positions = [7, 22, 36]
community_chest_positions = [2, 17, 33]

# Define the costs for each property on the Monopoly board
property_costs = [
    60,    # Mediterranean Avenue
    0,     # Community Chest
    60,    # Baltic Avenue
    200,     # Income Tax
    200,   # Reading Railroad
    100,   # Oriental Avenue
    0,     # Chance
    100,   # Vermont Avenue
    120,   # Connecticut Avenue
    0,     # Jail
    140,   # St. Charles Place
    150,   # Electric Company
    140,   # States Avenue
    160,   # Virginia Avenue
    200,   # Pennsylvania Railroad
    180,   # St. James Place
    0,     # Community Chest
    180,   # Tennessee Avenue
    200,   # New York Avenue
    0,     # Free Parking
    220,   # Kentucky Avenue
    0,     # Chance
    220,   # Indiana Avenue
    240,   # Illinois Avenue
    200,   # B. & O. Railroad
    260,   # Atlantic Avenue
    260,   # Ventnor Avenue
    150,   # Water Works
    280,   # Marvin Gardens
    0,     # Go to Jail
    300,   # Pacific Avenue
    300,   # North Carolina Avenue
    0,     # Chance
    320,   # vert 3
    200,   # gare 4
    0,     # Community Chest
    350,   # Park Place
    100,    # Luxury Tax
    400    # Boardwalk
]

# List of financial outcomes for Chance cards (positive for gains, negative for costs)
chance_values = [
    200,  # Advance to "Go"
    # Skipping movement cards as they do not have a direct monetary value
    50,   # Bank pays you dividend of $50
    # Skipping Get Out of Jail Free and movement cards
    #-25*9, -100*3,  # House/hotel repair costs would depend on the current property status
    -15,  # Pay poor tax of $15
    # Skipping movement cards
    150,  # Your building loan matures
    100   # You have won a crossword competition
    # Add more Chance card effects as needed
]

# List of financial outcomes for Community Chest cards
community_chest_values = [
    200,  # Bank error in your favor
    -50,  # Doctor's fees
    50,   # From sale of stock
    # Skipping Get Out of Jail Free
    100,  # Holiday Fund matures
    20,   # Income tax refund
    -50, -50,  # Hospital and School fees
    25,   # Receive consultancy fee
    #-40*9, -115*3,  # Street repairs would depend on current property status
    10,   # You have won second prize in a beauty contest
    100   # You inherit $100
    # Add more Community Chest card effects as needed
]

# Define the sizes of each property set
set_sizes = [2, 2, 3, 3, 3, 3, 3, 2]

def draw_chance_card():
    """
    Simulates drawing a Chance card and returns the monetary effect of the drawn card.
    """
    return random.choice(chance_values)

def draw_community_chest_card():
    """
    Simulates drawing a Community Chest card and returns the monetary effect of the drawn card.
    """
    return random.choice(community_chest_values)

def roll_dice():
    return random.randint(1, 6) + random.randint(1, 6)

def move_position_with_chance(position, player_money):
    # Implement Chance card effects here
    card_effect = draw_chance_card()
    player_money += card_effect
    # Add more Chance card effects as needed
    return position, player_money

def move_position_with_community_chest(position, player_money):
    # Implement Community Chest card effects here
    card_effect = draw_community_chest_card()
    player_money += card_effect
    # Add more Community Chest card effects as needed
    return position, player_money

def simulate_monopoly_game(num_turns, starting_money):
    """
    Simulates a game of Monopoly for a given number of turns and starting money,
    and returns the final remaining money after the simulation.
    """
    # Track ownership of properties
    properties_owned = [False] * 40
    # Initialize player's money
    player_money = starting_money
    # Start at 'GO'
    current_position = 0

    # Main game loop
    for _ in range(num_turns):
        # Roll the dice
        dice_roll = roll_dice()
        # Calculate new position after dice roll
        new_position = (current_position + dice_roll) % len(property_costs)
        

        # Check for passing "Go"
        if new_position < current_position:
            player_money += 200

        # Handle landing on Chance or Community Chest
        if new_position in chance_positions:
            # Draw a Chance card and apply its effect
            chance_card_effect = draw_chance_card()
            player_money += chance_card_effect
        elif new_position in community_chest_positions:
            # Draw a Community Chest card and apply its effect
            community_chest_card_effect = draw_community_chest_card()
            player_money += community_chest_card_effect

        # Property purchase logic (excluding "GO" position)
        if new_position != 0:
            if not properties_owned[new_position] and player_money >= property_costs[new_position]:
                player_money -= property_costs[new_position]
                properties_owned[new_position] = True

        # Update current position
        current_position = new_position

    return player_money




# Simulation parameters
num_simulations = 1000
num_turns = 15  # Adjust the number of turns as needed
starting_money = 1500

# List to store average remaining money for each number of turns
average_money_list = []

# Number of turns for each simulation
turns_list = [1, 5, 10, 15, 20,30,40]

for num_turns in turns_list:
    # Run simulations
    results = [simulate_monopoly_game(num_turns, starting_money) for _ in range(num_simulations)]
    # Calculate statistics
    average_remaining_money = np.mean(results)
    average_money_list.append(average_remaining_money)
    lower_quartile = np.percentile(results, 25)
    upper_quartile = np.percentile(results, 75)
    # Print results
    print(f"Average remaining money after {num_turns} turns: ${average_remaining_money:.2f}")
    print(f"Typical range for remaining money: ${lower_quartile:.2f} to ${upper_quartile:.2f}")

# Plotting the bar graph
plt.bar(turns_list, average_money_list, color='skyblue')
plt.xlabel('Number of Turns')
plt.ylabel('Average Remaining Money')
plt.title('Average Remaining Money vs. Number of Turns')
plt.xticks(turns_list)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

