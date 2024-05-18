# -*- coding: utf-8 -*-
import random
import seaborn
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
# Since there was an issue with the execution environment, let's try again to generate the probability graph for the sum of two six-sided dice (2D6).

# Calculate the probabilities
roll_counts = {total: 0 for total in range(2, 13)}
for die1 in range(1, 7):
    for die2 in range(1, 7):
        roll_counts[die1 + die2] += 1

# Convert counts to probabilities
roll_probabilities = {roll: count / 36 for roll, count in roll_counts.items()}

# Sort rolls and probabilities for plotting
sorted_rolls = sorted(roll_probabilities.keys())
sorted_probs = [roll_probabilities[roll] for roll in sorted_rolls]

# Plotting the probabilities
plt.figure(figsize=(10, 6))
plt.bar(sorted_rolls, sorted_probs, color='skyblue', edgecolor='black')
plt.xlabel('Sum of Dice Roll')
plt.ylabel('Probability')
plt.title('Probability Distribution of 2D6 Dice Rolls')
plt.xticks(sorted_rolls)
plt.yticks([i / 36 for i in range(0, 9)])
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig("2d6")
