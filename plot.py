import matplotlib.pyplot as plt
import numpy as np

# Plots a grouped bar plot: sociability vs. win Percentage for each strategy
def plot_sociability_box(results):
    sociability_bins = np.arange(0.5, 1.0, 0.1)
    bin_labels = [f"{bin_start:.1f}-{bin_start+0.1:.1f}" for bin_start in sociability_bins]

    width = 0.2  # Width of each bar

    strategy = "Logic"  # Specify the strategy to plot
    sociability_values_town = results[strategy]["Townfolk"]
    sociability_values_mafia = results[strategy]["Mafia"]

    win_percentages_town = []
    win_percentages_mafia = []
    num_entries = []

    for bin_start in sociability_bins:
        bin_end = bin_start + 0.1
        bin_wins_town = [s for s in sociability_values_town if bin_start <= s < bin_end]
        bin_wins_mafia = [s for s in sociability_values_mafia if bin_start <= s < bin_end]

        bin_wins = len(bin_wins_town) + len(bin_wins_mafia)
        num_entries.append(bin_wins)

        # Prevent division by 0
        win_percentage_town = 0 if bin_wins == 0 else len(bin_wins_town) / bin_wins * 100
        win_percentage_mafia = 0 if bin_wins == 0 else len(bin_wins_mafia) / bin_wins * 100

        win_percentages_town.append(win_percentage_town)
        win_percentages_mafia.append(win_percentage_mafia)

    x = np.arange(len(sociability_bins))

    plt.bar(x, win_percentages_town, width=width, align='center', label=strategy)

    # Calculate standard deviation based on win percentages
    std_dev_town = np.std(win_percentages_town)

    # Plot error bars
    plt.errorbar(x, win_percentages_town, yerr=std_dev_town, fmt='none', color='k', capsize=5)

    plt.xlabel("Sociability")
    plt.ylabel("Win Percentage (%)")
    plt.xticks(x + width / 2, bin_labels)  # Adjust the x-ticks position
    plt.title("Townfolk Win Percentage over differing Sociability (Logic Strategy)")

    plt.savefig("img/sociability.png")
    plt.show()
# Plots the win percentages of townfolk/mafia per strategy
def plot_win_percentages(results):
    random_townfolk_wins = len(results["Random"]["Townfolk"])
    random_mafia_wins = len(results["Random"]["Mafia"])
    logic_townfolk_wins = len(results["Logic"]["Townfolk"])
    logic_mafia_wins = len(results["Logic"]["Mafia"])
    total_rounds = random_townfolk_wins + random_mafia_wins

    random_townfolk_percentage = random_townfolk_wins / total_rounds * 100
    random_mafia_percentage = random_mafia_wins / total_rounds * 100
    logic_townfolk_percentage = logic_townfolk_wins / total_rounds * 100
    logic_mafia_percentage = logic_mafia_wins / total_rounds * 100

    fig, ax = plt.subplots()
    width = 0.4

    random_box = ax.barh(0, random_townfolk_percentage, width, color="green")
    ax.barh(0, random_mafia_percentage, width,
            color="red", left=random_townfolk_percentage)

    logic_box = ax.barh(1, logic_townfolk_percentage, width, color="green")
    ax.barh(1, logic_mafia_percentage, width,
            color="red", left=logic_townfolk_percentage)

    # Add labels to the boxes
    ax.annotate(f"{random_townfolk_percentage:.2f}%", xy=(random_townfolk_percentage / 2, 0), xytext=(0, 5),
                textcoords="offset points", ha="center", va="bottom")
    ax.annotate(f"{random_mafia_percentage:.2f}%", xy=(random_townfolk_percentage + random_mafia_percentage / 2, 0),
                xytext=(0, 5), textcoords="offset points", ha="center", va="bottom")

    ax.annotate(f"{logic_townfolk_percentage:.2f}%", xy=(logic_townfolk_percentage / 2, 1), xytext=(0, 5),
                textcoords="offset points", ha="center", va="bottom")
    ax.annotate(f"{logic_mafia_percentage:.2f}%", xy=(logic_townfolk_percentage + logic_mafia_percentage / 2, 1),
                xytext=(0, 5), textcoords="offset points", ha="center", va="bottom")
    # Add legend
    legend_townfolk = plt.Line2D([], [], color="green", label="Townfolk")
    legend_mafia = plt.Line2D([], [], color="red", label="Mafia")
    plt.legend(handles=[legend_townfolk, legend_mafia], loc="lower right")

    # Set plot properties
    ax.set_xlim(0, 100)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Random", "Logic"])
    plt.xlabel("Win Percentage (%)")
    plt.title("Win Percentage of both factions across the different strategies")

    plt.savefig("img/wins.png")
    plt.show()
