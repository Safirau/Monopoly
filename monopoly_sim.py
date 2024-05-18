import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Initialize the board and properties
board_visits = [0] * 40  # 40 squares on the board
indirect_landings = [0] * 40  # Track landings due to cards
current_position = 0  # Start at 'GO'
consecutive_doubles = 0  # Track consecutive doubles for going to jail

def MonopolyMap(probabilities):
    # Create a layout of the board with zeros
    board_layout = np.zeros((11, 11))
    
    # Fill the edges with probabilities
    board_layout[0, :] = probabilities[20:31]  # Top row
    board_layout[-1, :] = probabilities[10::-1]  # Bottom row
    board_layout[1:-1, 0] = probabilities[19:10:-1]  # Left column
    board_layout[1:-1, -1] = probabilities[31:40]  # Right column
    board_layout[1:-1, 1:-1] = np.nan  # Center cells set to NaN

    # Create the heatmap with a black background
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
    min_probability = np.nanmin(board_layout[np.isfinite(board_layout)])  # Minimum non-NaN value
    max_probability = np.nanmax(board_layout[np.isfinite(board_layout)])  # Maximum non-NaN value

    heatmap = ax.imshow(board_layout, cmap='viridis', interpolation='nearest',
                        vmin=min_probability, vmax=max_probability)

    # Set the central patch to a chroma-key-friendly green color
    ax.patch.set_facecolor('lime')
    cbar = plt.colorbar(heatmap)
    cbar.set_label('Probability of landing (%)')

    # Add percentage labels to each cell
    for i in range(11):
        for j in range(11):
            cell_value = board_layout[i, j]
            if not np.isnan(cell_value):
                # Determine brightness of the cell by converting RGB to lightness (HSP model)
                rgb = heatmap.cmap((cell_value - min_probability) / (max_probability - min_probability))
                lightness = np.sqrt(0.299 * (rgb[0]**2) + 0.587 * (rgb[1]**2) + 0.114 * (rgb[2]**2))

                # Set text color based on lightness
                text_color = 'black' if lightness > 0.5 else 'white'
                ax.text(j, i, f"{cell_value:.2f}%", ha='center', va='center', color=text_color, fontsize=9, weight='bold')

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title('Monopoly Board Landing Probabilities Heatmap', color='white')

    # Save the figure
    plt.savefig("monopolyfinal_chromakey_center_fonts2.png", facecolor=fig.get_facecolor())
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
    """Roll two six-sided dice and check for doubles."""
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    return die1 + die2, die1 == die2

def move_position_with_cards(current_position, roll_result):
    """Calculate new position with special card effects and doubles rule."""
    global consecutive_doubles
    roll_total, is_double = roll_result  # Unpack the tuple to get the roll total and whether it was a double

    # Check for consecutive doubles
   #if is_double:
    #    consecutive_doubles += 1
    #    if consecutive_doubles == 3:
    #        consecutive_doubles = 0
    #        return 10  # Jail position for three consecutive doubles
    #else:
    #    consecutive_doubles = 0

    new_position = (current_position + roll_total) % 40  # Correct use of roll_total

    #if new_position == 30:  # Go to Jail space
     #   return 10  # Move directly to Jail

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
            if new_position == 7 or (new_position == 36 and roll_total == 12):  # Adjusted to check roll_total
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


# Simulation loop
for _ in range(1000000):  # Number of games
    current_position = 0
    for _ in range(30):  # Turns per game
        roll_result = roll_dice()
        previous_position = current_position
        current_position = move_position_with_cards(current_position, roll_result)
        board_visits[current_position] += 1

# Calculate probabilities for landing on each space
total_rolls = sum(board_visits)
heatmap = [(visits / total_rolls) * 100 for visits in board_visits]
MonopolyMap(heatmap)
