
# -*- coding: utf-8 -*-
import random
import seaborn
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Initialize the board and properties
board_visits = [0] * 40  # 40 squares on the board
indirect_landings = [0] * 40  # Track landings due to cards
current_position = 0  # Start at 'GO'






def generate_difference_heatmap(prob1, prob2):
    differences = [p2 - p1 for p1, p2 in zip(prob1, prob2)]  # Calculate differences

    board_layout = np.zeros((11, 11))
    # Fill the board edges with differences
    board_layout[0, :] = differences[20:31]
    board_layout[-1, :] = differences[0:11][::-1]
    board_layout[1:-1, 0] = differences[11:20][::-1]
    board_layout[1:-1, -1] = differences[31:40]

    # Create the heatmap
    fig, ax = plt.subplots(figsize=(10, 10))
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["blue", "white", "red"])
    heatmap = ax.imshow(board_layout, cmap=cmap, interpolation='nearest')
    cbar = plt.colorbar(heatmap)
    cbar.set_label('Percentage Point Difference')

    # Add difference labels to each cell
    for i in range(11):
        for j in range(11):
            if board_layout[i, j] != 0:
                ax.text(j, i, f"{board_layout[i, j]:.2f}%", ha='center', va='center', color='black')

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title('Monopoly Board Landing Probability Differences Heatmap')
    plt.savefig("Delta")
    plt.close()



def MonopolyMap(probabilities):
    
    board_layout = np.zeros((11, 11))
    
    # Fill the board edges with probabilities
    board_layout[0, :] = probabilities[20:31]
    board_layout[-1, :] = probabilities[0:11][::-1]
    board_layout[1:-1, 0] = probabilities[11:20][::-1]
    board_layout[1:-1, -1] = probabilities[31:40]
    
    # Create the heatmap
    fig, ax = plt.subplots(figsize=(10, 10))
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["blue", "red"])
    heatmap = ax.imshow(board_layout, cmap=cmap, interpolation='nearest')
    cbar = plt.colorbar(heatmap)
    cbar.set_label('Probability of landing (%)')
    
    # Add percentage labels to each cell
    for i in range(11):
        for j in range(11):
            if board_layout[i, j] != 0:
                ax.text(j, i, f"{board_layout[i, j]:.2f}%", ha='center', va='center', color='black')
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title('Monopoly Board Landing Probabilities Heatmap with Percentages')
    
    # Save the figure
    plt.savefig("Heatmap30Tours")
    plt.close()



# Define the French Monopoly property names
property_names = [
    "Départ (Go)",
    "Boulevard de Belleville (Mediterranean Avenue)",
    "Caisse de communauté (Community Chest)",
    "Rue Lecourbe (Baltic Avenue)",
    "Impôts sur le revenu (Income Tax)",
    "Gare Montparnasse (Reading Railroad)",
    "Rue de Vaugirard (Oriental Avenue)",
    "Chance",
    "Rue de Courcelles (Vermont Avenue)",
    "Avenue de la République (Connecticut Avenue)",
    "En prison / Juste de passage (Jail)",
    "Boulevard de la Villette (St. Charles Place)",
    "Compagnie de distribution d'électricité (Electric Company)",
    "Avenue de Neuilly (States Avenue)",
    "Rue de Paradis (Virginia Avenue)",
    "Gare de Lyon (Pennsylvania Railroad)",
    "Avenue Mozart (St. James Place)",
    "Caisse de communauté (Community Chest)",
    "Boulevard Saint-Michel (Tennessee Avenue)",
    "Place Pigalle (New York Avenue)",
    "Parc Gratuit (Free Parking)",
    "Avenue Matignon (Kentucky Avenue)",
    "Chance",
    "Boulevard Malesherbes (Indiana Avenue)",
    "Avenue Henri-Martin (Illinois Avenue)",
    "Gare du Nord (B. & O. Railroad)",
    "Faubourg Saint-Honoré (Atlantic Avenue)",
    "Place de la Bourse (Ventnor Avenue)",
    "Compagnie des eaux (Water Works)",
    "Rue La Fayette (Marvin Gardens)",
    "Allez en prison (Go to Jail)",
    "Avenue de Breteuil (Pacific Avenue)",
    "Avenue Foch (North Carolina Avenue)",
    "Caisse de communauté (Community Chest)",
    "Boulevard des Capucines (Pennsylvania Avenue)",
    "Gare Saint-Lazare (Short Line)",
    "Chance",
    "Avenue des Champs-Élysées (Park Place)",
    "Taxe de luxe (Luxury Tax)",
    "Rue de la Paix (Boardwalk)"
]

def roll_dice():
    return random.randint(1, 6) + random.randint(1, 6)



# Enhanced movement function that now includes Chance and Community Chest cards
def move_position_with_cards(current_position, roll):
    new_position = (current_position + roll) % 40  # Regular movement
    # Simulate Chance (position 7, 22, 36) and Community Chest (position 2, 17, 33) cards
    if new_position in [7, 22, 36]:  # Landed on a Chance square
        # Simulate drawing a Chance card
        card = random.randint(1, 16)
        # Implement the effects of certain Chance cards
        if card == 1:  # Advance to "Go" 
            new_position = 0
        elif card == 2:  # Go directly to jail
            new_position = 10
        elif card == 3:  # Advance to Illinois Ave
            new_position = 24
        elif card == 4:  # Advance to St. Charles Place
            new_position = 11
        elif card == 5:  # Advance to nearest Utility
            if new_position == 7 or (new_position == 36 and roll == 12):  # Specific case where a roll of 12 from square 36 would overshoot the Water Works
                new_position = 12  # Electric Company
            else:
                new_position = 28  # Water Works
        elif card == 6:  # Advance to nearest Railroad
            if new_position == 7:
                new_position = 15  # Nearest from Chance 1 is Pennsylvania Railroad
            elif new_position == 22:
                new_position = 25  # Nearest from Chance 2 is B. & O. Railroad
            else:  # new_position == 36
                new_position = 5   # Nearest from Chance 3 is Reading Railroad
        elif card == 7:  # Take a trip to Reading Railroad
            new_position = 5
        elif card == 8:  # Take a walk on the Boardwalk
            new_position = 39
        elif card == 9:  # Go back three spaces
            new_position = (new_position - 3) % 40

    elif new_position in [2, 17, 33]:  # Landed on a Community Chest square
        # Simulate drawing a Community Chest card
        card = random.randint(1, 16)
        # Implement the effects of certain Community Chest cards
        if card == 1:
            new_position = 0  # Go to "Go"
        elif card == 2:
            new_position = 10  # Go directly to jail
        # ... (Include other specific Community Chest card actions here)
    return new_position

# Simulation loop - this replaces your previous loop
for k in range(1000000):    # Simulate 1,000,000 games
    current_position = 0

    for i in range(30):  #Simulate 30 turns
        
        roll = roll_dice()
        previous_position = current_position  # Track the previous position to detect indirect moves
        current_position = move_position_with_cards(current_position, roll)
        if i>=0:

            board_visits[current_position] += 1
        # Check if the new position is due to a card effect and not a direct roll
        if current_position != (previous_position + roll) % 40:
            indirect_landings[current_position] += 1

# Calculate total rolls for percentages
total_rolls = sum(board_visits)

# Print results with property names and percentages

heatmap = []

def simulate_monopoly_games(num_games, turns_per_game):
    board_visits = [0] * 40  # 40 squares on the board
    for _ in range(num_games):  # Simulate a large number of games
        current_position = 0  # Start at 'GO'
        for __ in range(turns_per_game):  # Simulate a set number of turns per game
            roll = roll_dice()
            current_position = move_position_with_cards(current_position, roll)
            board_visits[current_position] += 1
    
    total_visits = sum(board_visits)
    probabilities = [visits / total_visits * 100 for visits in board_visits]  # Convert counts to percentages
    return probabilities

probabilities_20_turns = simulate_monopoly_games(1000000, 20)
probabilities_40_turns = simulate_monopoly_games(1000000, 40)

# Generate the heatmap for the differences
generate_difference_heatmap(probabilities_20_turns, probabilities_40_turns)

for position in range(40):
    
    percentage = (board_visits[position] / total_rolls) * 100
    heatmap.append(percentage)
    if indirect_landings[position] > 0:
    
        indirect_percentage = (indirect_landings[position] / board_visits[position]) * 100  # Changed to calculate percentage of indirect landings out of total landings for the position
        print(f"{property_names[position]} was landed on {percentage:.2f}% of the time. ({indirect_percentage:.2f}% of landings were from Chance/Community Chest)")
    else:
        
        print(f"{property_names[position]} was landed on {percentage:.2f}% of the time.")


MonopolyMap(heatmap)