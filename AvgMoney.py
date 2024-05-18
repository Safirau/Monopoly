import random
import numpy as np

# Define positions for special cards and actions
chance_positions = [7, 22, 36]
community_chest_positions = [2, 17, 33]
go_position = 0
go_to_jail_position = 30
jail_position = 10
free_parking_position = 20
income_tax_position = 4
luxury_tax_position = 38

# Define property costs including utilities and railroads
property_costs = [60, 0, 60, 200, 200, 100, 0, 100, 120, 0, 140, 150, 140, 160, 200, 180, 0, 180, 200, 0, 220, 0, 220, 240, 200, 260, 260, 150, 280, 0, 300, 300, 0, 320, 200, 0, 350, 100, 400]

# Define financial outcomes for Chance and Community Chest cards
chance_values = [200, 50, -15, 150, 100]
community_chest_values = [200, -50, 50, 100, 20, -50, -50, 25, 10, 100]

def roll_dice():
    return random.randint(1, 6) + random.randint(1, 6)

def draw_chance_card(player_position, player_money):
    card_effect = random.choice(chance_values)
    player_money += card_effect
    return player_position, player_money

def draw_community_chest_card(player_position, player_money):
    card_effect = random.choice(community_chest_values)
    player_money += card_effect
    return player_position, player_money

def simulate_monopoly_game(num_turns, num_players, starting_money):
    properties_owned = [None] * 40
    players_money = [starting_money] * num_players
    players_positions = [0] * num_players
    for turn in range(num_turns):
        for player in range(num_players):
            dice_roll = roll_dice()
            players_positions[player] = (players_positions[player] + dice_roll) % len(property_costs)
            if players_positions[player] == go_to_jail_position:
                players_positions[player] = jail_position
            if players_positions[player] < dice_roll:
                players_money[player] += 200  # Passed 'GO'
            if players_positions[player] in chance_positions:
                players_positions[player], players_money[player] = draw_chance_card(players_positions[player], players_money[player])
            elif players_positions[player] in community_chest_positions:
                players_positions[player], players_money[player] = draw_community_chest_card(players_positions[player], players_money[player])
            if players_positions[player] in [income_tax_position, luxury_tax_position]:
                tax = 200 if players_positions[player] == income_tax_position else 100
                players_money[player] -= tax
            elif property_costs[players_positions[player]] > 0 and properties_owned[players_positions[player]] is None and players_money[player] >= property_costs[players_positions[player]]:
                players_money[player] -= property_costs[players_positions[player]]
                properties_owned[players_positions[player]] = player  # Mark the property as owned by the current player

    # Calculate statistics for each player
    properties_per_player = [0] * num_players
    for property_owner in properties_owned:
        if property_owner is not None:
            properties_per_player[property_owner] += 1

    return players_money, properties_per_player

# Simulation parameters
num_simulations = 10000
num_turns = 11
num_players = 4
starting_money = 1500

# Run simulations
all_results = [simulate_monopoly_game(num_turns, num_players, starting_money) for _ in range(num_simulations)]
all_money = [result[0] for result in all_results]
all_properties = [result[1] for result in all_results]

# Flatten lists to calculate overall statistics
flat_money = [money for sublist in all_money for money in sublist]
flat_properties = [prop for sublist in all_properties for prop in sublist]

# Calculate average and quartiles
average_money = np.mean(flat_money)
lower_money_quartile = np.percentile(flat_money, 25)
upper_money_quartile = np.percentile(flat_money, 75)
average_properties = np.mean(flat_properties)
lower_properties_quartile = np.percentile(flat_properties, 25)
upper_properties_quartile = np.percentile(flat_properties, 75)

print(f"Average remaining money: ${average_money:.2f}")
print(f"Money quartile range: ${lower_money_quartile:.2f} to ${upper_money_quartile:.2f}")
print(f"Average number of properties: {average_properties:.2f}")
print(f"Properties quartile range: {lower_properties_quartile:.2f} to {upper_properties_quartile:.2f}")
