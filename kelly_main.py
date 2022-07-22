import random
import matplotlib as mpl
import matplotlib.pyplot as plt
import xlsxwriter

# ========================= Set Variables =========================#
run = 100
tries = 50  # tries >= 12
rounds = 1000
start_bal = 100
main_graph_show_amt = 20

limit = 1  # 0 ~ 1 || Only bet on fkelly <= limit

# ========================= List Variables =========================#
simulation_logs = list()  # tuple ([bal_list],[count_list])
simulation_results = list()  # [1]/[0]

fkelly_logs = list()
bc_logs = list()  # Balance Change Log

colors = [
    "tomato",
    "sandybrown",
    "gold",
    "yellowgreen",
    "mediumseagreen",
    "mediumaquamarine",
    "teal",
    "steelblue",
    "cornflowerblue",
    "mediumslateblue",
    "blueviolet",
    "violet",
]
for i in range(main_graph_show_amt - 12):
    r = random.random()
    b = random.random()
    g = random.random()
    colors.append((r, g, b))

# ========================= Simulations =========================#
def simulateGamble():
    comp_val = random.randint(0, 1)
    play_val = random.randint(0, 1)

    if comp_val == play_val:
        simulation_results.append(1)
        return 1
    else:
        simulation_results.append(0)
        return 0


def preSimulation():
    simulation_results.clear()

    for i in range(100):
        simulateGamble()
    win_prob = simulation_results.count(1) / len(simulation_results)
    return win_prob


def mainSimulation():
    fkelly_results = list()
    bc_results = list()
    bal_list = list()
    round_list = list()

    curr_bal = start_bal
    p = preSimulation()
    q = 1 - p
    b = 1
    f = float(str(round(p - (q / b), 2)))

    fkelly_results.append(f)
    bc_results.append(start_bal)
    bal_list.append(curr_bal)
    round_list.append(0)

    for i in range(rounds):
        win_state = simulateGamble()
        p = simulation_results.count(1) / len(simulation_results)
        q = 1 - p
        b = 1
        f = float(str(round(p - (q / b), 2)))
        curr_bal = float(str(round(curr_bal, 2)))
        fkelly_results.append(f)

        if f > 0:
            if f <= limit:
                bet_bal = float(str(round(curr_bal * f, 2)))
                if win_state == 1:
                    curr_bal += bet_bal
                    bc_results.append(f"+{bet_bal}")
                else:
                    curr_bal -= bet_bal
                    bc_results.append(f"-{bet_bal}")

                if curr_bal <= 0:
                    curr_bal = 0
        else:
            bc_results.append("+0.00")
        bal_list.append(curr_bal)
        round_list.append(i + 1)

    fkelly_logs.append(fkelly_results)
    bc_logs.append(bc_results)
    simulation_logs.append((bal_list, round_list))


# ========================= Matplot Main-Plot =========================#
fig1 = plt.figure()
ax = fig1.subplots()
ax.set_xlabel("Round")
ax.set_ylabel("Balance")

for i in range(tries):
    mainSimulation()
    if i < main_graph_show_amt:
        plt.plot(
            simulation_logs[i][1],
            simulation_logs[i][0],
            ".",
            ls="-",
            markevery=int(rounds / 10),
            markersize=5,
            c=colors[i],
        )
plt.grid()

# ========================= Matplot Sub-Plots =========================#
fig2 = plt.figure()
axs = fig2.subplots(3, 4)
t = 0
for i in range(3):
    for j in range(4):
        axs[i][j].plot(simulation_logs[t][1], simulation_logs[t][0], c=colors[t])
        t += 1
plt.tight_layout()

# ========================= Matplot Result =========================#
wb = xlsxwriter.Workbook("./results/kelly_main.xlsx")
ws = wb.add_worksheet()
for row in range(tries * 5):  # (+2) Last line for Calculation of Average
    if (row % 5) == 0:
        ws.write(row, 0, f"Sim {int(row/5)+1}")
        ws.write(row, 1, "[ROUND]")
    if (row % 5) == 1:
        ws.write(row, 1, "[F_KELLY]")
    if (row % 5) == 2:
        ws.write(row, 1, "[BAL_CHG]")
    if (row % 5) == 3:
        ws.write(row, 1, "[BAL_TOT]")
    for column in range(rounds + 1):  #  oooo | oooo | rounds+1
        if (row % 5) == 0:
            ws.write(row, column + 2, f"Round {column}")
        if (row % 5) == 1:
            ws.write(row, column + 2, fkelly_logs[int(row / 5)][column])
        if (row % 5) == 2:
            ws.write(row, column + 2, bc_logs[int(row / 5)][column])
        if (row % 5) == 3:
            ws.write(row, column + 2, simulation_logs[int(row / 5)][0][column])

wb.close()

# ========================= Matplot Show =========================#
plt.show()
