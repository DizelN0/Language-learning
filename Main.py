import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar, Combobox
from ttkthemes import ThemedTk
from ttkbootstrap import Style
import random

# Создаем подключение к базе данных
connection = sqlite3.connect('flashcards.db')

# Создаем таблицу для хранения карточек
connection.execute('''
    CREATE TABLE IF NOT EXISTS flashcards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        term TEXT NOT NULL,
        translation TEXT NOT NULL,
        level INTEGER DEFAULT 1,
        date_added TEXT DEFAULT CURRENT_TIMESTAMP
    )
''')

# Функция для добавления карточки
def add_flashcard():
    term = term_entry.get().strip()
    translation = translation_entry.get().strip()

    if term and translation:
        connection.execute('INSERT INTO flashcards (term, translation) VALUES (?, ?)', (term, translation))
        connection.commit()
        messagebox.showinfo("Успех", "Карточка успешно добавлена!")
        term_entry.delete(0, END)
        translation_entry.delete(0, END)
    else:
        messagebox.showwarning("Ошибка", "Введите термин и перевод")

# Функция для отображения карточек
def display_flashcards():
    flashcards_window = Toplevel(root)
    flashcards_window.title("Карточки")

    flashcards_frame = Frame(flashcards_window)
    flashcards_frame.pack()

    scrollbar = Scrollbar(flashcards_frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    flashcards_listbox = Listbox(flashcards_frame, width=50, yscrollcommand=scrollbar.set)
    flashcards_listbox.pack(side=LEFT, fill=Y)

    scrollbar.config(command=flashcards_listbox.yview)

    cursor = connection.execute('SELECT term, translation FROM flashcards')
    flashcards = cursor.fetchall()

    for term, translation in flashcards:
        flashcards_listbox.insert(END, f"{term} - {translation}")

# Функция для тестирования знаний
def test_flashcards():
    test_window = Toplevel(root)
    test_window.title("Тестирование")

    period_label = Label(test_window, text="Период:")
    period_label.pack(pady=10)

    period_combo = Combobox(test_window, values=["За последний день", "За последнюю неделю", "За последний месяц"])
    period_combo.pack()

    cursor = connection.execute('SELECT term, translation FROM flashcards')
    flashcards = cursor.fetchall()

    if len(flashcards) == 0:
        messagebox.showwarning("Ошибка", "Нет доступных карточек для тестирования.")
        test_window.destroy()
        return

    random.shuffle(flashcards)

    score = 0
    total_flashcards = len(flashcards)
    index = 0

    def check_translation():
        nonlocal score, index
        term, translation = flashcards[index]
        user_translation = user_translation_entry.get().strip()

        if user_translation.lower() == translation.lower():
            score += 1

        user_translation_entry.delete(0, END)
        progress_bar['value'] = (score / total_flashcards) * 100

        index += 1
        if index < total_flashcards:
            term, _ = flashcards[index]
            flashcard_label.config(text=term)
        else:
            messagebox.showinfo("РHere's the updated code with the implemented changes")
# Функция для тестирования знаний
def test_flashcards():
    test_window = Toplevel(root)
    test_window.title("Тестирование")

    period_label = Label(test_window, text="Период:")
    period_label.pack(pady=10)

    period_combo = Combobox(test_window, values=["За последний день", "За последнюю неделю", "За последний месяц"])
    period_combo.pack()

    cursor = connection.execute('SELECT term, translation FROM flashcards')
    flashcards = cursor.fetchall()

    if len(flashcards) == 0:
        messagebox.showwarning("Ошибка", "Нет доступных карточек для тестирования.")
        test_window.destroy()
        return

    random.shuffle(flashcards)

    score = 0
    total_flashcards = len(flashcards)
    index = 0

    def check_translation():
        nonlocal score, index
        term, translation = flashcards[index]
        user_translation = user_translation_entry.get().strip()

        if user_translation.lower() == translation.lower():
            score += 1

        user_translation_entry.delete(0, END)
        progress_bar['value'] = (score / total_flashcards) * 100

        index += 1
        if index < total_flashcards:
            term, _ = flashcards[index]
            flashcard_label.config(text=term)
        else:
            messagebox.showinfo("Результат", f"Тестирование завершено. Ваш счет: {score}/{total_flashcards}")
            test_window.destroy()

    flashcard_label = Label(test_window, text="")
    flashcard_label.pack(pady=10)

    user_translation_entry = Entry(test_window, width=30)
    user_translation_entry.pack(pady=10)

    def check_and_next(event=None):
        check_translation()
        if index < total_flashcards:
            term, _ = flashcards[index]
            flashcard_label.config(text=term)
        else:
            messagebox.showinfo("Результат", f"Тестирование завершено. Ваш счет: {score}/{total_flashcards}")
            test_window.destroy()

    user_translation_entry.bind('<Return>', check_and_next)

    submit_button = Button(test_window, text="Ответить", command=check_and_next)
    submit_button.pack(pady=5)

    progress_bar = Progressbar(test_window, orient=HORIZONTAL, length=200, mode='determinate')
    progress_bar.pack(pady=10)

    term, _ = flashcards[index]
    flashcard_label.config(text=term)

# Функция для редактирования карточек
def edit_flashcards():
    edit_window = Toplevel(root)
    edit_window.title("Редактирование карточек")

    flashcards_frame = Frame(edit_window)
    flashcards_frame.pack()

    scrollbar = Scrollbar(flashcards_frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    flashcards_listbox = Listbox(flashcards_frame, width=50, yscrollcommand=scrollbar.set)
    flashcards_listbox.pack(side=LEFT, fill=Y)

    scrollbar.config(command=flashcards_listbox.yview)

    cursor = connection.execute('SELECT id, term, translation FROM flashcards')
    flashcards = cursor.fetchall()

    for card in flashcards:
        flashcards_listbox.insert(END, f"{card[1]} - {card[2]}")

    def edit_selected():
        selected_index = flashcards_listbox.curselection()
        if selected_index:
            card_id = flashcards[selected_index[0]][0]
            edit_card(card_id)
        else:
            messagebox.showwarning("Ошибка", "Выберите карточку для редактирования.")

    def edit_card(card_id):
        card = connection.execute('SELECT term, translation FROM flashcards WHERE id = ?', (card_id,)).fetchone()
        if card:
            edit_card_window = Toplevel(edit_window)
            edit_card_window.title("Редактирование карточки")

            term_label = Label(edit_card_window, text="Термин:")
            term_label.pack(pady=10)

            term_entry = Entry(edit_card_window, width=30)
            term_entry.pack()
            term_entry.insert(END, card[0])

            translation_label = Label(edit_card_window, text="Перевод:")
            translation_label.pack(pady=10)

            translation_entry = Entry(edit_card_window, width=30)
            translation_entry.pack()
            translation_entry.insert(END, card[1])

            def save_changes():
                new_term = term_entry.get().strip()
                new_translation = translation_entry.get().strip()

                if new_term and new_translation:
                    connection.execute('UPDATE flashcards SET term = ?, translation = ? WHERE id = ?', (new_term, new_translation, card_id))
                    connection.commit()
                    messagebox.showinfo("Успех", "Изменения сохранены!")
                    edit_card_window.destroy()
                else:
                    messagebox.showwarning("Ошибка", "Введите термин и перевод")

            save_button = Button(edit_card_window, text="Сохранить", command=save_changes)
            save_button.pack(pady=5)

        else:
            messagebox.showwarning("Ошибка", "Не удалось найти карточку для редактирования.")

    edit_button = Button(edit_window, text="Редактировать выбранную карточку", command=edit_selected)
    edit_button.pack(pady=5)

# Главное окно приложения
root = ThemedTk(theme="radiance")
root.title("Помощник по изучению иностранных языков")

# Создаем метки и поля ввода для добавления карточек
term_label = Label(root, text="Термин:")
term_label.pack(pady=10)

term_entry = Entry(root, width=30)
term_entry.pack()

translation_label = Label(root, text="Перевод:")
translation_label.pack(pady=10)

translation_entry = Entry(root, width=30)
translation_entry.pack()

add_button = Button(root, text="Добавить карточку", command=add_flashcard)
add_button.pack(pady=5)

# Создаем кнопки для отображения карточек, тестирования знаний и редактирования карточек
display_button = Button(root, text="Отобразить карточки", command=display_flashcards)
display_button.pack(pady=5)

test_button = Button(root, text="Тестирование", command=test_flashcards)
test_button.pack(pady=5)

edit_button = Button(root, text="Редактировать карточки", command=edit_flashcards)
edit_button.pack(pady=5)

# Настройка стилей кнопок
style = Style(theme='darkly')
style.configure('TButton', background='#007bff', foreground='white')

# Запускаем главное окно приложения
root.mainloop()
