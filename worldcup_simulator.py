#=========================================
#دانشجو : مبین شاطری
# شماره دانشجویی : 404130803
# عنوان پروژه : شبیه سازی جام جهانی
# تاریخ تحویل : 1405/05/03
#=========================================

import matplotlib.pyplot as plt
from WorldCupSimulator_class import WorldCupSimulator


DEFAULT_CSV = "worldcup_2026_teams.csv"


def show_menu():
    """
    تابعی برای نمایش دادن منو
    """
    print("\n===== World Cup Simulator =====")
    print("1. Load teams from CSV")
    print("2. Seed and draw groups")
    print("3. Run group stage")
    print("4. Run full simulation")
    print("5. Run multiple simulations")
    print("6. Display bracket")
    print("7. Exit")


def plot_champion_percentages(percentages):
    """
    تابعی برای نمایش نمودار میله ای در درصد قهرمانی هر تیم با گرفتن اسم تیم ها و درصد هر کدام از دیکشمری
    پارامتر:percentages(درصد قهرمانی هر تیم)
    """
    teams = list(percentages.keys())
    values = list(percentages.values())

    plt.style.use("dark_background")
    plt.figure(figsize=(16, 8))

    bars = plt.bar(teams, values, color="yellow")

    plt.title("Championship Percentage")
    plt.xlabel("Teams")
    plt.ylabel("Percentage (%)")
    plt.xticks(rotation=45)

    plt.bar_label(bars, fmt="%.1f%%")

    plt.tight_layout()
    plt.show()


simulator = WorldCupSimulator()
groups_drawn = False
simulation_done = False

while True:
    show_menu()
    choice = input("Choose an option: ").strip()

    if choice == "1":
        filename = input(f"CSV filename [{DEFAULT_CSV}]: ").strip()
        if not filename:
            filename = DEFAULT_CSV

        if simulator.load_teams_from_csv(filename):
            groups_drawn = False
            simulation_done = False

    elif choice == "2":
        if not simulator.teams:
            print("Please load teams first.")
            continue

        if simulator.seed_and_draw_groups():
            groups_drawn = True
            simulation_done = False
            print("Groups drawn successfully.")

    elif choice == "3":
        if not groups_drawn:
            print("Please draw the groups first.")
            continue

        simulator.run_group_stage()

    elif choice == "4":
        if not simulator.teams:
            print("Please load teams first.")
            continue

        champion = simulator.run_full_simulation()
        if champion:
            simulation_done = True
            print(f"Champion: {champion.name}")

    elif choice == "5":
        if not simulator.teams:
            print("Please load teams first.")
            continue

        raw_count = input("Number of simulations [1000]: ").strip()
        if not raw_count:
            count = 1000
        else:
            try:
                count = int(raw_count)
                if count <= 0:
                    print("Please enter a positive number.")
                    continue
            except ValueError:
                print("Invalid number.")
                continue

        percentages = simulator.most_likely_champion(count)
        if percentages:
            simulation_done = True
            plot_champion_percentages(percentages)

    elif choice == "6":
        if not simulation_done:
            print("Please run a full simulation first.")
            continue

        simulator.display_bracket()

    elif choice == "7":
        print("Goodbye.")
        break

    else:
        print("Invalid option.")
