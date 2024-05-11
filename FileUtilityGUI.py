import tkinter as tk
from tkinter import filedialog
import chardet

def detect_encoding(filename, chunk_size=1024):
    with open(filename, 'rb') as file:
        rawdata = file.read(chunk_size)
        result = chardet.detect(rawdata)
    return result['encoding']

def process_file(input_filename, output_filename, processing_function, log_text):
    encoding = detect_encoding(input_filename)
    log_text.insert(tk.END, f"{'='*30}\nВыполняется операция над файлом: {input_filename}\n")
    try:
        with open(input_filename, 'r', encoding=encoding) as file:
            lines = file.readlines()
        processed_lines = processing_function(lines)
        with open(output_filename, 'w', encoding=encoding) as file:
            file.writelines(processed_lines)
        log_text.insert(tk.END, f"Операция успешно завершена.\nРезультат сохранен в файл: {output_filename}\n")
        log_text.insert(tk.END, f"Количество обработанных строк: {len(processed_lines)}\n")
        if processing_function == remove_duplicates:
            removed_duplicates = len(lines) - len(processed_lines)
            log_text.insert(tk.END, f"Количество удаленных дубликатов: {removed_duplicates}\n")
        log_text.insert(tk.END, '='*30 + '\n\n')
        # Оптимизация размера окна
        # update_window_size(root)
    except Exception as e:
        log_text.insert(tk.END, f"Ошибка при выполнении операции: {e}\n{'='*30}\n\n")
        # Оптимизация размера окна
        # update_window_size(root)

def sort_lines(lines):
    return sorted(lines)

def remove_duplicates(lines):
    return list(dict.fromkeys(lines))

def sort_and_remove_duplicates(input_filename, log_text):
    sorted_filename = input_filename.split('.')[0] + '_sorted.txt'
    removed_duplicates_filename = input_filename.split('.')[0] + '_removed_duplicates.txt'
    process_file(input_filename, sorted_filename, sort_lines, log_text)
    process_file(sorted_filename, removed_duplicates_filename, remove_duplicates, log_text)

def display_operation(operation_name, processing_function, log_text):
    input_filename = filedialog.askopenfilename(title=f"Выберите файл для {operation_name}")
    if input_filename:
        output_filename = input_filename.split('.')[0] + f'_{operation_name.lower().replace(" ", "_")}.txt'
        process_file(input_filename, output_filename, processing_function, log_text)

# Создание интерфейса
root = tk.Tk()
root.title("Утилита для работы с файлами")
root.geometry("600x400")
root.resizable(False, False)  # Запрет изменения размеров окна

# Область лога
log_text = tk.Text(root, height=10)
log_text.pack(fill=tk.BOTH, expand=True)

# Кнопки в ряд
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

sort_button = tk.Button(button_frame, text="Сортировка", command=lambda: display_operation("Сортировка", sort_lines, log_text))
sort_button.pack(side=tk.LEFT, padx=5)

remove_duplicates_button = tk.Button(button_frame, text="Удаление дубликатов", command=lambda: display_operation("Удаление дубликатов", remove_duplicates, log_text))
remove_duplicates_button.pack(side=tk.LEFT, padx=5)

sort_and_remove_duplicates_button = tk.Button(button_frame, text="Сортировка и удаление дубликатов", command=lambda: sort_and_remove_duplicates(log_text))
sort_and_remove_duplicates_button.pack(side=tk.LEFT, padx=5)

exit_button = tk.Button(root, text="Выход", command=root.destroy)
exit_button.pack(pady=5)

root.mainloop()
