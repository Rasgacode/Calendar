import ui
import storage
import sys
import os


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def sort_meetings(table):
    for i in range(2, len(table), 3):
        for j in range(i + 3, len(table), 3):
            if int(table[i]) > int(table[j]):
                temp = table[i - 2]
                table[i - 2] = table[j - 2]
                table[j - 2] = temp
                temp = table[i - 1]
                table[i - 1] = table[j - 1]
                table[j - 1] = temp
                temp = table[i]
                table[i] = table[j]
                table[j] = temp


def compact_meetings(table):
    for i in range(2, len(table), 3):
        start_time = int(table[i])
        end_time = int(table[i - 1])
        last_end_time = int(table[i - 4])
        if i == 2:
            table[i - 1] = 8 + end_time - start_time
            table[i] = 8
        else:
            table[i - 1] = last_end_time + end_time - start_time
            table[i] = last_end_time


def total_time(table):
    return sum([int(table[i-1]) - int(table[i]) for i in range(2, len(table), 3)])


def check_work_time(start_time, end_time):
    work_time = [i for i in range(8, 19)]
    if end_time not in work_time or start_time not in work_time:
        return True
    return False


def check_exist_meeting_time(start_time, end_time, table):
    for i in range(2, len(table), 3):
        check_list_to_start_time = [j for j in range(int(table[i]), int(table[i-1]))]
        check_list_to_end_time = [j for j in range(int(table[i]) + 1, int(table[i-1]) + 1)]
        if start_time in check_list_to_start_time or end_time in check_list_to_end_time:
            return True
    return False


def add_schedule(table, input_list, file_name):
    start_time = int(input_list[2])
    end_time = int(input_list[2]) + int(input_list[1])
    if check_work_time(start_time, end_time):
        ui.display_error_messages("ERROR: Meeting is outside of your working hours (8 to 18)!")
    elif check_exist_meeting_time(start_time, end_time, table):
        ui.display_error_messages("ERROR: Meeting is inside of your another meeting hours!")
    else:
        table += [int(input_list[i + 1]) + int(input_list[i]) if i == 1 else input_list[i] for i in range(len(input_list))]
        sort_meetings(table)
        storage.save_schedule(file_name, table)


def remove_schedule(table, input_, file_name):
    if not any(table[i] == input_ for i in range(len(table)) if i % 3 == 2):
        ui.display_error_messages("ERROR: This start time is not exist!")
    else:
        for i in range(2, len(table), 3):
            start_time = table[i]
            index_of_start_time = i
            index_of_end_time = i - 1
            index_of_title_of_meeting = i - 2
            if start_time == input_:
                table.pop(index_of_start_time)
                table.pop(index_of_end_time)
                table.pop(index_of_title_of_meeting)
                break
        storage.save_schedule(file_name, table)


def edit_schedule(table, input_, file_name):
    if not any(table[i] == input_ for i in range(len(table)) if i % 3 == 2):
        ui.display_error_messages("ERROR: This start time is not exist!")
    else:
        for i in range(2, len(table), 3):
            start_time = table[i]
            if start_time == input_:
                edited_datas = ui.get_input(["Enter a new meeting title", "Enter a new duration in hours(1 or 2)", "Enter a new start time"])
                start_time = int(edited_datas[2])
                end_time = int(edited_datas[2]) + int(edited_datas[1])
                meeting_title = edited_datas[0]
                if check_work_time(start_time, end_time):
                    ui.display_error_messages("ERROR: Meeting is outside of your working hours (8 to 18)!")
                elif check_exist_meeting_time(start_time, end_time, table):
                    ui.display_error_messages("ERROR: Meeting is inside of your another meeting hours!")
                else:
                    table[i] = start_time
                    table[i - 1] = end_time
                    table[i - 2] = meeting_title
    sort_meetings(table)
    storage.save_schedule(file_name, table)


def choose(table, file_name):
    input_ = ui.get_menu_input()
    if input_ == "s":
        add_schedule(table, ui.get_input(["Enter meeting title", "Enter duration in hours(1 or 2)", "Enter start time"]), file_name)
    elif input_ == "c":
        remove_schedule(table, ui.get_input(["Enter a start time to remove a meeting"])[0], file_name)
    elif input_ == "e":
        edit_schedule(table, ui.get_input(["Enter a start time to edit a meeting"])[0], file_name)
    elif input_ == "m":
        compact_meetings(table)
    elif input_ == "q":
        sys.exit()
    else:
        ui.display_error_messages("ERROR: Wrong input!")


def main():
    file_name = "meeting.txt"
    table = storage.load_schedules(file_name)
    title = "Your schedule for the day"
    options = ["schedule a new meeting", "cancel an existing meeting", "edit a meeting", "meeting compression", "quit"]
    marks = ["s", "c", "e", "m", "q"]
    menu_name = "Menu"
    while(True):
        cls()
        ui.display_meetings(table, title)
        ui.display_tot_time(total_time(table))
        ui.display_menu(options , marks, menu_name)
        choose(table, file_name)


if __name__ == '__main__':
    main() 