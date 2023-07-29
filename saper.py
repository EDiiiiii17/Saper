import random
import sys
import os


def display_menu(options, selected_option):
    print("=== Сапер ===")
    print("W- вверх| S- вниз")
    for i, option in enumerate(options):
        if i == selected_option:
            print("\033[31m->", option + "\033[0m")
        else:
            print("  ", option)


def countAdjacentMines(field, row, column):
    count = 0
    for i in range(max(0, row - 1), min(row + 2, len(field))):
        for j in range(max(0, column - 1), min(column + 2, len(field[0]))):
            if field[i][j] == '\033[32m@\033[0m':
                count += 1
    return count


def startGame():
    playing = True
    options = ["5x5 с 5 минами", "10x10 с 8 минами", "15x15 с 10 минами"]
    selected_option = 0

    rows, cols, num_mines = 5, 5, 5

    while playing:
        os.system('cls' if os.name == 'nt' else 'clear')

        display_menu(options, selected_option)

        key = input()

        if key == 'w':
            selected_option = (selected_option - 1) % len(options)
        elif key == 's':
            selected_option = (selected_option + 1) % len(options)
        elif key == '':
            if selected_option == 0:
                rows, cols, num_mines = 5, 5, 5
            elif selected_option == 1:
                rows, cols, num_mines = 10, 10, 8
            elif selected_option == 2:
                rows, cols, num_mines = 15, 15, 10

            print("\033[31mДобро пожаловать в игру Сапер! Давайте взорвем всех СВИНОСОБАК\033[0m")
            player_field = [['\033[32m*\033[0m' for _ in range(cols)] for _ in range(rows)]
            mines_field = [['\033[32m \033[0m' for _ in range(cols)] for _ in range(rows)]
            flags_field = [[False for _ in range(cols)] for _ in range(rows)]

            mines = 0
            while mines < num_mines:
                x = random.randint(0, rows - 1)
                y = random.randint(0, cols - 1)
                if mines_field[x][y] != '\033[32m@\033[0m':
                    mines_field[x][y] = '\033[32m@\033[0m'
                    mines += 1

            print('\033[32m   ' + '   '.join([str(i + 1) for i in range(cols)]) + '           ' + ' ' + '   '.join([str(i + 1) for i in range(cols)]) + '\033[0m')
            print('\033[32m  ' + '─' * (4 * cols - 1) + '      ' + '     ' + '─' * (4 * cols - 1) + '\033[0m')
            for i in range(rows):
                row_player = chr(65 + i) + ' \033[32m│\033[0m ' + ' \033[32m│\033[0m '.join(['\033[32m' + cell + '\033[0m' for cell in player_field[i]]) + ' \033[32m│\033[0m      '
                row_mines = chr(65 + i) + ' \033[32m│\033[0m ' + ' \033[32m│\033[0m '.join(['\033[32m' + cell + '\033[0m' for cell in mines_field[i]]) + ' \033[32m│\033[0m'
                print('\033[32m' + row_player + row_mines + '\033[0m')
                print('\033[32m' + '  ' + '─' * (4 * cols - 1) + '      ' + '     ' + '─' * (4 * cols - 1) + '\033[0m')

            while True:
                user_input = input("\033[31mВведите координаты (например, A1) или F для флага/снятия флага: \033[0m")

                if len(user_input) > 2 and user_input[0].lower() == 'f':
                    flag_input = user_input[1:]
                    if len(flag_input) < 2 or len(flag_input) > 3:
                        print("Ошибка: Введите корректные координаты (например, A1).")
                        continue

                    flag_column_char, flag_row_char = flag_input[1:], flag_input[0].upper()

                    if not ('A' <= flag_row_char <= 'O'):
                        print("Ошибка: Некорректная буква строки. Используйте буквы A-O.")
                        continue

                    if not ('1' <= flag_column_char <= '9' or flag_column_char == '10'):
                        print("Ошибка: Некорректное число столбца. Используйте числа 1-10.")
                        continue

                    flag_column = int(flag_column_char)
                    flag_row = ord(flag_row_char) - ord('A')

                    if flag_column < 1 or flag_column > cols or flag_row < 0 or flag_row >= rows:
                        print("Ошибка: Некорректные координаты.")
                        continue

                    flags_field[flag_row][flag_column - 1] = not flags_field[flag_row][flag_column - 1]
                    player_field[flag_row][flag_column - 1] = '\033[31m!\033[0m' if flags_field[flag_row][flag_column - 1] else '\033[32m*\033[0m'

                else:
                    column_char, row_char = user_input[1:], user_input[0].upper()

                    if not ('A' <= row_char <= 'O'):
                        print("Ошибка: Некорректная буква строки. Используйте буквы A-O.")
                        continue

                    if not ('1' <= column_char <= '9' or column_char == '10'):
                        print("Ошибка: Некорректное число столбца. Используйте числа 1-10.")
                        continue

                    column = int(column_char)
                    row = ord(row_char) - ord('A')

                    if column < 1 or column > cols or row < 0 or row >= rows:
                        print("Ошибка: Некорректные координаты.")
                        continue

                    if flags_field[row][column - 1]:
                        print("Эта ячейка уже помечена флагом!")
                        continue

                    if player_field[row][column - 1] != '\033[32m*\033[0m':
                        print("Эта ячейка уже открыта!")
                        continue

                    if mines_field[row][column - 1] == '\033[32m@\033[0m':
                        player_field[row][column - 1] = '\033[31m!\033[0m'
                        print('\033[31mАллах Бабах! Игра окончена.\033[0m')
                        sys.exit()
                    else:
                        count = countAdjacentMines(mines_field, row, column - 1)
                        player_field[row][column - 1] = str(count) if count > 0 else ' '

                    closed_cells = sum(row.count('\033[32m*\033[0m') for row in player_field)
                    if closed_cells == num_mines:
                        print("Поздравляю! Вы открыли все ячейки без мин. Вы победили!")
                        sys.exit()

                print('\033[32m   ' + '   '.join([str(i + 1) for i in range(cols)]) + '           ' + ' ' + '   '.join(
                    [str(i + 1) for i in range(cols)]) + '\033[0m')
                print('\033[32m  ' + '─' * (4 * cols - 1) + '      ' + '     ' + '─' * (
                            4 * cols - 1) + '\033[0m')
                for i in range(rows):
                    row_player = chr(65 + i) + ' \033[32m│\033[0m ' + ' \033[32m│\033[0m '.join(
                        ['\033[31m!\033[0m' if flags_field[i][j] else '\033[32m' + cell + '\033[0m' for j, cell in
                         enumerate(player_field[i])]) + ' \033[32m│\033[0m      '
                    row_mines = chr(65 + i) + ' \033[32m│\033[0m ' + ' \033[32m│\033[0m '.join(
                        ['\033[32m' + cell + '\033[0m' for cell in mines_field[i]]) + ' \033[32m│\033[0m'
                    print('\033[32m' + row_player + row_mines + '\033[0m')
                    print('\033[32m' + '  ' + '─' * (4 * cols - 1) + '      ' + '     ' + '─' * (
                                4 * cols - 1) + '\033[0m')

        elif selected_option == 1:
            print("\033[31mДо свидания! Выход из игры.\033[0m")
            sys.exit()


startGame()