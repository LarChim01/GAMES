from tkinter import *
import random
import time

root = Tk()
root.title('Крестики Нолики')
root.geometry('350x350')

games = Canvas(root, width=300, height=300, bg='#CCCCCC')
games.place(x=25, y=25)

combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
you_win, bot_win, draw_game = 0, 0, 0


def new_game():
    global run_game, win, condition
    run_game = True
    condition = [None] * 9
    win = None
    games.delete("all")
    for i in range(0, 9):
        x = i // 3 * 100
        y = i % 3 * 100
        games.create_rectangle(x, y, x + 100, y + 100,
                               width=3,
                               outline='#A5A5A5',
                               fill='#CCCCCC',
                               activefill='#FFFAFA')


def add_x(column, row):
    x = 10 + 100 * column
    y = 10 + 100 * row
    games.create_line(x, y, x + 80, y + 80, width=7, fill='#0000FF')
    games.create_line(x, y + 80, x + 80, y, width=7, fill='#0000FF')


def add_o(column, row):
    x = 10 + 100 * column
    y = 10 + 100 * row
    games.create_oval(x, y, x + 80, y + 80, width=7, outline='#FF0000')


def click(event):
    if run_game:
        colum = event.x // 100
        row = event.y // 100
        index = colum + row * 3
        if condition[index] is None:
            condition[index] = 'x'
            add_x(colum, row)
            if winner():
                end_game()
            else:
                bot_move()
                if winner():
                    end_game()
    else:
        new_game()


def bot_move():
    empty_indexes = []
    for index, el in enumerate(condition):
        if el is None:
            empty_indexes.append(index)
    if empty_indexes:
        index = random.choice(empty_indexes)
        condition[index] = 'o'
        colum = index % 3
        row = index // 3
        add_o(colum, row)


def winner():
    global win, you_win, bot_win, draw_game
    variants = []
    for i in combinations:
        variants.append([condition[i[0]], condition[i[1]], condition[i[2]]])
    if ['x'] * 3 in variants:
        you_win += 1
        creat_win_line()
        win = 'Ты ПОБЕДИЛ!'
    elif ['o'] * 3 in variants:
        bot_win += 1
        creat_win_line()
        win = 'Бот Выиграл'
    elif None not in condition:
        draw_game += 1
        win = 'Ничья'
    return win


def creat_win_line():
    for i in combinations:
        win_line = (condition[i[0]], condition[i[1]], condition[i[2]])
        if win_line.count('x') == 3 or win_line.count('o') == 3:
            index_start = i[0]
            index_end = i[2]
            games.create_line((index_start % 3) * 100 + 50, (index_start // 3) * 100 + 50,
                              (index_end % 3) * 100 + 50, (index_end // 3) * 100 + 50, width=12, fill='#FF00FF')
            games.update()
            break


def end_game():
    global run_game
    run_game = False
    time.sleep(0.5)
    games.delete("all")
    games.create_text(150, 150, text=win, font=("Arial", 28))
    games.update()
    time.sleep(0.5)
    games.delete("all")
    games.create_text(120, 110, text=f"Ты выиграл - {you_win}\nБот выиграл - {bot_win}\nНичья  - {draw_game} ",
                      font=("Hack", 20))
    games.create_text(150, 260, text=f"Нажми для продолжения", font=("Arial", 15))


games.bind('<Button-1>', click)
new_game()
root.mainloop()