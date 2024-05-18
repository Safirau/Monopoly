import numpy as np

def simulate_monopoly(num_players=4, board_probabilities=[], sets_to_acquire=3):
    # Define the sizes of each set (2 sets of 2 properties and 6 sets of 3 properties)
    set_sizes = [2, 3, 3, 3, 3, 3, 3, 2]  # Adjusted based on your description
    rounds = 0
    # Create a list of lists to track acquired properties, adjusting for the size of each set
    properties_acquired = [([False] * size) for size in set_sizes]
    complete_sets_count = 0

    # Map to the indices of the buyable properties (the example may need adjustment to match exact board indices)
    buyable_property_indices = [
        1, 3,  # First set of 2
        6, 8, 9, 11, 13, 14, 16,  # Middle sets of 3
        18, 19, 21, 23, 24, 26,  # More sets of 3
        27, 29, 31, 32, 34,  # Another set of 3
        37, 39  # Last set of 2
    ]

    while complete_sets_count < sets_to_acquire:
        rounds += 1
        for _ in range(num_players):
            for i, prob in enumerate(board_probabilities):
                if np.random.random() < (prob / 100):  # Convert percentages to probabilities
                    if i in buyable_property_indices:
                        property_global_index = buyable_property_indices.index(i)
                        # Determine which set and which property within the set this index corresponds to
                        set_index = 0
                        property_index = property_global_index
                        for size in set_sizes:
                            if property_index < size:
                                break
                            property_index -= size
                            set_index += 1
                        
                        # Check and update property acquisition status
                        if not properties_acquired[set_index][property_index]:
                            properties_acquired[set_index][property_index] = True
                            # Check if all properties in this set are acquired
                            if all(properties_acquired[set_index]):
                                complete_sets_count += 1
                                if complete_sets_count >= sets_to_acquire:
                                    return rounds
    return rounds

# Probabilities for each space on the board
board_probabilities = [2.96, 2,1.83,2.17,2.41,2.96,2.47,1.13,2.55,2.48,6.3,2.84,2.57,2.44,2.54,2.87,2.86,2.64,2.96,3.09,2.87,2.81,1.2,2.69,3.15,2.85,2.65,2.62,2.88,2.51,0,2.57,2.51,2.28,2.39,2.32,0.96,2.08,2.06,2.51]  # Fill in the correct probabilities

num_simulations = 10000
total_rounds = sum(simulate_monopoly(board_probabilities=board_probabilities) for _ in range(num_simulations))
average_rounds = total_rounds / num_simulations
print(average_rounds)