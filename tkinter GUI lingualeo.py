import random
import sqlite3
import tkinter as tk
from tkinter import ttk
# declaring all variables
all_lines = []
word_set = []
line_number = 0
index = -1
rand_line = ''
english_word = ''
transcription = ''
translation = ''
"""three_options stores CORRECT TRANSLATION so that we could randomly assign to the buttons 1 correct option and 2
 other wrong options from one list"""
three_options = []
number_of_words = 0
option1, option2, option3 = '', '', ''


def create_first_frame():
    global number_of_words

    start_window = tk.Tk()

    start_label = ttk.Label(start_window, text='Привет, готов к новой порции английских слов?')
    start_label.grid(column=0, row=0)

    ttk.Label(start_window, text='Сколько слов ты хочешь изучить?').grid(column=0, row=2)

    number_chosen = ttk.Combobox(start_window, textvariable=tk.StringVar(), width=10)
    number_chosen['values'] = ('5', '10', '15', '30', '50', '100')
    number_chosen.grid(column=0, row=3)
    number_chosen.current(1)

    def click_start():
        global number_of_words
        number_of_words = int(number_chosen.get())
        start_window.destroy()

    start_button = ttk.Button(start_window, text='Погнали тренировать', command=click_start)
    start_button.grid(column=0, row=1)

    start_window.mainloop()


def create_word_set():
    global word_set, all_lines

    with sqlite3.connect('LINGUALEO.db') as db:
        database = db.execute
        for row in database("SELECT * FROM lingualeo_words"):
            all_lines.append(row)
    word_set = []
    while len(word_set) != number_of_words:
        word_set.append(random.choice(all_lines))
    for i in enumerate(word_set, 1):  # temporary part
        print(i)


def choose_from_three_options():
    global three_options
    option = random.choice(three_options)
    three_options.remove(option)
    return option


def update_vars():  # created this function to generate new values after pressing NEXT button
    global \
        english_word, transcription, translation, line_number, \
        three_options, rand_line, index, option1, option2, option3

    if index < len(word_set) - 1:
        index += 1
    else:
        index = 0

    rand_line = word_set[index]
    english_word = rand_line[0]  # A word in English from random line

    transcription = rand_line[1]
    if transcription == '[]':
        transcription = ''
    else:
        transcription = rand_line[1]
    translation = rand_line[2].lower()
    three_options = \
        [
            translation,
            random.choice(all_lines)[2].lower(),
            random.choice(all_lines)[2].lower(),
        ]
    line_number = word_set.index(rand_line) + 1

    option1 = choose_from_three_options()
    option2 = choose_from_three_options()
    option3 = choose_from_three_options()


create_first_frame()
create_word_set()
update_vars()
win = tk.Tk()
win.title("***Word practice*** kuzantiv")
# win.geometry('400x200')
win.resizable(False, False)
win.iconbitmap('icon.ico')

first_frame = ttk.LabelFrame(win, text='this frame')
first_frame.grid(column=0, row=0, padx=15, pady=15)

head_label = ttk.Label(first_frame, text='Выбери правильный перевод\n')
head_label.grid(column=0, row=0)

a_label = ttk.Label(first_frame, text=f'{english_word.upper()}\n{transcription}', font=('Calibri', 12, 'bold'))
a_label.grid(column=0, row=1)

label_word_nmbr = ttk.Label(first_frame, text=f'{line_number} / {len(word_set)}')
label_word_nmbr.grid(column=1, row=1)


def change_label_color(option):
    if option == translation:
        a_label.configure(foreground='green')
    else:
        a_label.configure(foreground='red')


def click_button1():
    change_label_color(option1)
    action_button1.configure(state='disabled')


def click_button2():
    change_label_color(option2)
    action_button2.configure(state='disabled')


def click_button3():
    change_label_color(option3)
    action_button3.configure(state='disabled')


def click_next():
    global option1, option2, option3
    update_vars()

    a_label.configure(text=f'{english_word.upper()}\n{transcription}', foreground='black')
    label_word_nmbr.configure(text=f'{line_number} / {len(word_set)}')

    action_button1.configure(text=option1, state='enabled')

    action_button2.configure(text=option2, state='enabled')

    action_button3.configure(text=option3, state='enabled')


def click_move_to_learned():
    global index
    with sqlite3.connect('LINGUALEO.db') as db:
        db.execute(
            "INSERT INTO learned_words ('english_word', 'transcription', 'translation') "
            "VALUES (?, ?, ?)", (english_word, transcription, translation))

        # db.execute(
        #     f"INSERT INTO learned_words VALUES  (?, ?, ?)",
        #     (english_word, transcription, translation))

        db.execute("DELETE FROM lingualeo_words WHERE english_word = ?", (english_word,))
        # обязательная запятая после english_word (почему?)
        # без запятой, такая ошибка => sqlite3.ProgrammingError: Incorrect number of bindings supplied.
        # The current statement uses 1, and there are 4 supplied.
    word_set.remove(rand_line)
    index -= 1
    click_next()


def click_create_new_set():
    global index
    index = -1
    create_word_set()
    click_next()


# below we have all the buttons
action_button1 = ttk.Button(first_frame, text=option1, command=click_button1)
action_button1.grid(column=0, row=2)

action_button2 = ttk.Button(first_frame, text=option2, command=click_button2)
action_button2.grid(column=0, row=3)

action_button3 = ttk.Button(first_frame, text=option3, command=click_button3)
action_button3.grid(column=0, row=4)

action_button4 = ttk.Button(first_frame, text='NEXT', command=click_next)
action_button4.grid(column=0, row=5)
button_i_know_this_word = ttk.Button(first_frame, text='Убрать в изученные', command=click_move_to_learned)
button_i_know_this_word.grid(column=1, row=3)

button_new_word_set = ttk.Button(first_frame, text='Переключить набор слов', command=click_create_new_set)
button_new_word_set.grid(column=1, row=5)

win.mainloop()

""" 
ДОБАВИТЬ ФУНКЦИОНАЛ

1. голосовое озвучивание англ слов 
2. редактирование слова (в случае если оно содержит ошибку)
3. проверить версию tkinter
4. отбрасывать легкие слова в отдельную базу ***СДЕЛАНО***
5. выровнять заглавные буквы ***СДЕЛАНО***
6. где отсутсвует транскрипция спарсить из интернета 
7. статистику сколько слов изучил за сегодня/неделю/месяц
8. отдельную статистику на каждого игрока
9. добавить картинки к слову
10. добавить примеры использования слова в предложении
11. идея на будущее, при чтении книги парсить все слова 
из нее проверять со списком изученных слов
и добавлять оставшиеся в неизученные

"""
