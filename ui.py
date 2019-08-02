import getch
import time

def get_menu_input():
    print("\nChoose an option...")
    return getch.getch()


def get_input(quest_list):
    return [input(f"{quest}: ") for quest in quest_list]


def display_menu(options, marks, menu_name):
    for i in range(len(options)):
        if i == 0:
            print(f"{menu_name}:")
        print(f"({marks[i]}) {options[i]}")


def display_meetings(table, display_title):
    if len(table) == 0:
        print(f"{display_title}:\n(empty)\n\n")
    else:
        for i in range(2, len(table), 3):
            title = table[i - 2]
            from_hour = table[i]
            to_hour = table[i - 1]
            if i == 2:
                print(f"{display_title}: ")
            print(f"{title} {from_hour}-{to_hour}")
        print("\n")

def display_error_messages(message):
    print(f"{message}")
    time.sleep(2)


def display_tot_time(total_time):
    print(f"Total time of meetings: {total_time} hour(s)\n")