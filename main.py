# Imports
import random
import tkinter as tk

FONT = ("Helvetica", 16)


class App(tk.Frame):
    # Tkinter initialization
    def __init__(self, parent):
        # Creates the list of words from txt file
        word_list = []
        with open('1-1000.txt') as file:
            for line in file:
                word_list.append(line.strip('\n'))

        # Creates the words used for testing by selecting words at random for the word list.
        self.test_sample = []
        for n in range(120):
            self.test_sample.append(random.choice(word_list))

        self.current_index = 0

        # Creates dictionary containing 3 lines which will be used throughout the program
        self.lines_dict = {}
        for n in range(3):
            self.lines_dict[f'line{n}'] = self.create_line(self.current_index)
            self.current_index += 7

        # Initialize variables
        self.current_line_num = -1
        self.current_line = self.get_next_line()
        self.current_word = ''
        self.current_word = self.get_next_word()
        self.word_count = 0
        self.char_count = 0
        self.time_left = 60
        self.timer = None

        # Tkinter initialization
        tk.Frame.__init__(self, parent)
        self.text = tk.Text(width=50, height=4, spacing1=20, spacing2=1,
                            font=FONT, bd=2, relief='solid')
        self.text.tag_configure("center", justify='center')
        self.text.insert(1.0, self.convert_text())
        self.text.tag_add("center", 1.0, "end")
        self.text.config(state=tk.DISABLED)
        self.text.grid(row=1, column=0, )
        self.entry = tk.Entry(width=50, justify='center', font=FONT)
        self.entry.grid(row=2, column=0, pady=(0, 10))
        self.entry.focus_set()
        self.scoreboard = tk.Label(width=75, height=1, font=("Helvetica", 10))
        self.scoreboard.config(text=f'CPM: {self.char_count} \tWPM: {self.word_count} \tTime left: {self.time_left}')
        self.scoreboard.grid(row=0, column=0, pady=(20, 0))

    # Creates a new line of text (6 words separated by a space)
    def create_line(self, index):
        new_line = ''
        for i in range(index, index + 6):
            new_line += f'{self.test_sample[i]} '
        return new_line

    # Converts dictionary into text to be displayed on the Tkinter label
    def convert_text(self):
        lines = list(self.lines_dict.values())
        display_text = ''
        for line in lines:
            display_text += f'{line}\n'
        return display_text

    # This function runs when user hits the spacebar
    # Takes entered word and updates scores if correct
    # Also starts timer if not already started
    def take_word(self, e):
        if len(self.entry.get()) != 0:
            if self.time_left == 60:
                self.count_down()
            print(self.entry.get())
            print(self.current_word)
            if self.entry.get() == f'{self.current_word} ':
                self.word_count += 1
                self.char_count += len(self.entry.get())
            self.current_word = self.get_next_word()
            self.entry.delete(0, 'end')
            print(self.word_count, self.char_count)

    # Returns next line as list of words
    def get_next_line(self):
        if self.current_line_num < 1:
            next_line = self.lines_dict[f'line{self.current_line_num + 1}'].split()
            self.current_line_num += 1
        else:
            self.lines_dict['line0'] = self.lines_dict['line1']
            self.lines_dict['line1'] = self.lines_dict['line2']
            self.lines_dict['line2'] = self.create_line(self.current_index)
            self.current_index += 7
            next_line = self.lines_dict[f'line1'].split()

            self.text.config(state=tk.NORMAL)
            self.text.delete('1.0', tk.END)
            self.text.insert(1.0, self.convert_text())
            self.text.tag_add("center", 1.0, "end")
            self.text.config(state=tk.DISABLED)
        return next_line

    # Returns next word as string
    def get_next_word(self):
        try:
            next_word = self.current_line[self.current_line.index(self.current_word) + 1]
        except ValueError:
            next_word = self.current_line[0]
        except IndexError:
            self.current_line = self.get_next_line()
            next_word = self.current_line[0]
        return next_word

    # Timer Utility
    def count_down(self):
        if self.time_left > 0:
            self.timer = tk.Frame.after(self, 1000, self.count_down)
            self.time_left -= 1
        else:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, 'TIME!')
            self.entry.config(state=tk.DISABLED)
            tk.Frame.after_cancel(self, self.timer)

        self.scoreboard.config(text=f'CPM: {self.char_count} \tWPM: {self.word_count}'
                                    f' \tTime left: {self.time_left}')


def main():
    root = tk.Tk()
    root.title("Type Speed Tester")
    root.minsize(width=500, height=300)
    root.config(padx=20, pady=20, background='grey')
    app = App(root)
    root.bind('<space>', app.take_word)
    root.mainloop()


if __name__ == "__main__":
    main()
