import sqlite3
from tkinter import *
from tkinter import messagebox

# Создаем подключение к базе данных
connection = sqlite3.connect('flashcards.db')

# Создаем таблицу для хранения карточек
connection.execute('''
    CREATE TABLE IF NOT EXISTS flashcards (
        term TEXT NOT NULL,
        translation TEXT NOT NULL
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

    scrollbar = Scrollbar(flashcards_window)
    scrollbar.pack(side=RIGHT, fill=Y)

    flashcards_listbox = Listbox(flashcards_window, width=50, yscrollcommand=scrollbar.set)
    flashcards_listbox.pack()

    scrollbar.config(command=flashcards_listbox.yview)

    cursor = connection.execute('SELECT term, translation FROM flashcards')
    flashcards = cursor.fetchall()

    for term, translation in flashcards:
        flashcards_listbox.insert(END, f"{term} - {translation}")

# Функция для тестирования знаний
def test_flashcards():
    test_window = Toplevel(root)
    test_window.title("Тестирование")

    cursor = connection.execute('SELECT term, translation FROM flashcards')
    flashcards = cursor.fetchall()

    if len(flashcards) == 0:
        messagebox.showwarning("Ошибка", "Нет доступных карточек для тестирования.")
        test_window.destroy()
        return

    score = 0

    def check_translation():
        nonlocal score
        term, translation = flashcards[index]
        user_translation = user_translation_entry.get().strip()

        if user_translation.lower() == translation.lower():
            messagebox.showinfo("Правильно!", "Ответ верный")
            score += 1
        else:
            messagebox.showwarning("Неправильно", f"Неправильный ответ. Правильный ответ: {translation}")

        user_translation_entry.delete(0, END)
        test_flashcard()

    def test_flashcard():
        nonlocal index

        if index < len(flashcards):
            term, _ = flashcards[index]
            flashcard_label.config(text=term)
            index += 1
        else:
            messagebox.showinfo("Результат", f"Тестирование завершено. Ваш счет: {score}/{len(flashcards)}")
            test_window.destroy()

    flashcard_label = Label(test_window, text="")
    flashcard_label.pack(pady=10)

    user_translation_entry = Entry(test_window)
    user_translation_entry.pack(pady=10)

    submit_button = Button(test_window, text="Ответить", command=check_translation)
    submit_button.pack(pady=5)

    index = 0
    test_flashcard()

# Главное окно приложения
root = Tk()
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

# Создаем кнопки для отображения карточек и тестирования знаний
display_button = Button(root, text="Отобразить карточки", command=display_flashcards)
display_button.pack(pady=5)

test_button = Button(root, text="Тестирование", command=test_flashcards)
test_button.pack(pady=5)

# Запускаем главное окно приложения
root.mainloop()

# Закрываем подключение к базе данных
connection.close()
