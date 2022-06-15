import random
import sqlite3
import tkinter as tk
from tkinter import ttk


class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = None
        self.switchframe(StartPage)

    def switchframe(self, frame_class):
        newframe = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = newframe
        self.frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        lbl_text = f'Привет, готов к новой порции английских слов? \n \t Сколько слов ты хочешь изучить?'
        ttk.Label(self, text=lbl_text).pack(side="top", fill="x", pady=5)

        number_chosen = ttk.Combobox(self, textvariable=tk.StringVar(), width=10)
        number_chosen['values'] = ('5', '10', '15', '30', '50', '100')
        # number_chosen.grid(column=0, row=2)
        number_chosen.pack()
        number_chosen.current(1)
        number_of_words = int(number_chosen.get())

        ttk.Button(self, text='Погнали тренировать', command=lambda: master.switchframe(PageOne)).pack()


class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.all_lines = []
        self.word_set = []
        self.line_number = 0
        self.index = -1
        self.rand_line = ''
        self.english_word = ''
        self.transcription = ''
        self.translation = ''
        """three_options stores CORRECT TRANSLATION so that we could randomly assign to the buttons 1 correct option and 2
        other wrong options from one list"""
        self.three_options = []
        self.number_of_words = 10
        self.option1, self.option2, self.option3 = '', '', ''
        self.create_word_set()

        head_label = ttk.Label(self, text='Выбери правильный перевод\n')
        head_label.grid(column=0, row=0)

        a_label = ttk.Label(self, text=f'{self.english_word.upper()}\n{self.transcription}',
                            font=('Algerian', 12, ''), anchor='center')
        a_label.grid(column=0, row=1)

        label_word_nmbr = ttk.Label(self, text=f'{self.line_number} / {len(self.word_set)}')
        label_word_nmbr.grid(column=1, row=1)

        # below we have all buttons
        action_button1 = ttk.Button(self, text=self.option1, command=self.click_button1)
        action_button1.grid(column=0, row=2)

        action_button2 = ttk.Button(self, text=self.option2, command=self.click_button2)
        action_button2.grid(column=0, row=3)

        action_button3 = ttk.Button(self, text=self.option3, command=self.click_button3)
        action_button3.grid(column=0, row=4)

        action_button4 = ttk.Button(self, text='NEXT', command=self.click_next)
        action_button4.grid(column=0, row=5)
        button_i_know_this_word = ttk.Button(self, text='Убрать в изученные', command=self.click_move_to_learned)
        button_i_know_this_word.grid(column=1, row=3)

        button_new_word_set = ttk.Button(self, text='Переключить набор слов', command=self.click_create_new_set)
        button_new_word_set.grid(column=1, row=5)

    def create_word_set(self):

        with sqlite3.connect('LINGUALEO.db') as db:
            database = db.execute
            for row in database("SELECT * FROM lingualeo_words"):
                self.all_lines.append(row)
        self.word_set = []
        while len(self.word_set) != self.number_of_words:
            self.word_set.append(random.choice(self.all_lines))
        for i in enumerate(self.word_set, 1):  # temporary part
            print(i)

    def choose_from_three_options(self):
        option = random.choice(self.three_options)
        self.three_options.remove(option)
        return option

    def update_vars(self):  # created this function to generate new values after pressing NEXT button

        if self.index < len(self.word_set) - 1:
            self.index += 1
        else:
            self.index = 0

        self.rand_line = self.word_set[self.index]
        self.english_word = self.rand_line[0]  # A word in English from random line

        self.transcription = self.rand_line[1]
        if self.transcription == '[]':
            self.transcription = ''
        else:
            self.transcription = self.rand_line[1]
        self.translation = self.rand_line[2].lower()
        self.three_options = \
            [
                self.translation,
                random.choice(self.all_lines)[2].lower(),
                random.choice(self.all_lines)[2].lower(),
            ]
        self.line_number = self.word_set.index(self.rand_line) + 1

        self.option1 = choose_from_three_options()
        self.option2 = choose_from_three_options()
        self.option3 = choose_from_three_options()

    def change_label_color(self, option):
        if option == self.translation:
            a_label.configure(foreground='green')
        else:
            a_label.configure(foreground='red')

    def click_button1(self):
        change_label_color(self.option1)
        action_button1.configure(self, state='disabled')

    def click_button2(self):
        change_label_color(self.option2)
        action_button2.configure(self, state='disabled')

    def click_button3(self):
        change_label_color(self.option3)
        action_button3.configure(self, state='disabled')

    def click_next(self):
        update_vars(self)

        a_label.configure(self, text=f'{self.english_word.upper()}\n{self.transcription}', foreground='black')
        label_word_nmbr.configure(self, text=f'{self.line_number} / {len(word_set)}')

        action_button1.configure(self, text=self.option1, state='enabled')

        action_button2.configure(self, text=self.option2, state='enabled')

        action_button3.configure(self, text=self.option3, state='enabled')

    def click_move_to_learned(self):
        with sqlite3.connect('LINGUALEO.db') as learned_words:
            learned_words.execute(
                "INSERT INTO learned_words ('english_word', 'transcription', 'translation') "
                "VALUES (?, ?, ?)", (english_word, transcription, translation))

            learned_words.execute("DELETE FROM lingualeo_words WHERE english_word = ?", (english_word,))
        self.word_set.remove(self.rand_line)

        self.index -= 1
        self.click_next()

    def click_create_new_set(self):
        self.index = -1
        create_word_set()
        click_next()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
