def load_schedules(file_name):
    with open(file_name, "r") as file:
        table = "".join(file.readlines()).replace("\n", ",").split(",")
        table.pop(-1)
    return table


def save_schedule(file_name, table):
    with open(file_name, "w") as file:
        for i in range(len(table)):
            if i % 3 == 2:
                file.write(f"{table[i]}\n")
            else:
                file.write(f"{table[i]},")
