# List of financial outcomes for Chance cards (positive for gains, negative for costs)
chance_values = [
    200, # Advance to "Go"
    # Skipping movement cards as they do not have a direct monetary value
    50, # Bank pays you dividend of $50
    # Skipping Get Out of Jail Free and movement cards
    #-25*9, -100*3, # House/hotel repair costs would depend on the current property status
    -15, # Pay poor tax of $15
    # Skipping movement cards
    150, # Your building loan matures
    100  # You have won a crossword competition
    # Assume all other cards are movement cards or do not affect finances directly
]

# Calculate average expectancy for Chance
average_chance_value = sum(chance_values) / len(chance_values)

# List of financial outcomes for Community Chest cards
community_chest_values = [
    200, # Bank error in your favor
    -50, # Doctor's fees
    50, # From sale of stock
    # Skipping Get Out of Jail Free
    100, # Holiday Fund matures
    20,  # Income tax refund
    -50, -50, # Hospital and School fees
    25,  # Receive consultancy fee
   #-40*9, -115*3, # Street repairs would depend on current property status
    10,  # You have won second prize in a beauty contest
    100  # You inherit $100
    # Assume all other cards are movement cards or do not affect finances directly
]

# Calculate average expectancy for Community Chest
average_community_chest_value = sum(community_chest_values) / len(community_chest_values)

# Print the results
print(f"Average Chance card value: ${average_chance_value}")
print(f"Average Community Chest card value: ${average_community_chest_value}")
