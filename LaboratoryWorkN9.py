import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import CoolProp.CoolProp as CP
import math

def calculate_results():
    try:
        h0_values_str = h0_entry.get()
        mreal_values_str = mreal_entry.get()
        p2_values_str = p2_entry.get()
        f2_values_str = f2_entry.get() # Changed variable name to plural to reflect potentially multiple f2 values
        start_i_str = start_i_entry.get()
        end_i_str = end_i_entry.get()
        step_i_str = step_i_entry.get()

        h0_values = [float(x.strip()) for x in h0_values_str.split(',')]
        mreal_values = [float(x.strip()) for x in mreal_values_str.split(',')]
        p2_values = [float(x.strip()) for x in p2_values_str.split(',')]
        start_i = float(start_i_str)
        end_i = float(end_i_str)
        step_i = float(step_i_str)
        R = 287.002507

        f2_values_input = [x.strip() for x in f2_values_str.split(',')] # Split f2 input into a list of strings
        f2_values = [] # List to store the processed float values for f2

        if f2_values_str: # Check if f2 input is not empty
            if len(f2_values_input) == 1 and f2_values_input[0] != '': # Single f2 value provided
                f2_single_value = float(f2_values_input[0])
                f2_values = [f2_single_value] * len(h0_values) # Apply to all pairs
            elif len(f2_values_input) == len(h0_values): # Multiple f2 values provided, matching number of pairs
                try:
                    f2_values = [float(f) for f in f2_values_input] # Convert each to float
                except ValueError:
                    messagebox.showerror("Ошибка ввода", "Некорректное значение f2 в списке.")
                    return
            else: # Number of f2 values doesn't match number of pairs and not a single value
                messagebox.showerror("Ошибка ввода", "Количество значений f2 должно быть равно 1 или количеству значений h0, mreal, p2.")
                return
        else: # f2 input is empty, handle as needed - for now, error message, could also set a default if appropriate
            messagebox.showerror("Ошибка ввода", "Необходимо ввести значение f2.")
            return

        if not (len(h0_values) == len(mreal_values) == len(p2_values) == len(f2_values)): # Include f2_values in length check
            messagebox.showerror("Ошибка", "Списки h0, mreal, p2 и f2 должны иметь одинаковую длину или f2 должно быть единичным значением.")
            return

        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)

        for param_set_index in range(len(h0_values)):
            h0 = h0_values[param_set_index]
            mreal = mreal_values[param_set_index]
            p2 = p2_values[param_set_index]
            f2 = f2_values[param_set_index] # Get f2 for the current pair

            min_diff = float('inf')
            best_i = None

            i = start_i
            while i < end_i:
                try:
                    first = 44.72 * (math.sqrt(abs(h0 - CP.PropsSI('H', 'P', p2, 'T', i, 'Air')) / 1000))
                    second = mreal * R * i / (p2 * f2)
                    current_diff = abs(first - second)

                    if current_diff < min_diff:
                        min_diff = current_diff
                        best_i = i
                except ValueError as e_coolprop:
                    messagebox.showerror("Ошибка CoolProp", f"Ошибка CoolProp при i={i}: {e_coolprop}")
                    output_text.config(state=tk.DISABLED)
                    return

                i += step_i

            result_str = f"\nРезультаты для набора параметров №{param_set_index + 1}:\n"
            result_str += f"  h0 = {h0}, mreal = {mreal}, p2 = {p2}, f2 = {f2}\n" # Include f2 in output
            if best_i is not None:
                result_str += f"  Наименьшая абсолютная разница: {min_diff:.6f}\n"
                result_str += f"  Значение T, К, при котором достигается наименьшая разница: {best_i}\n" # Changed "i" to "T, К"
            else:
                result_str += "  Не удалось найти значение i в заданном диапазоне.\n"
            output_text.insert(tk.END, result_str)

        output_text.config(state=tk.DISABLED)

    except ValueError:
        messagebox.showerror("Ошибка ввода", "Пожалуйста, введите корректные числовые значения.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
        output_text.config(state=tk.DISABLED)

# --- GUI ---
root = tk.Tk()
root.title("Лабораторная работа №9")

# --- Ввод параметров ---
input_frame = ttk.Frame(root, padding="10")
input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# h0
h0_label = ttk.Label(input_frame, text="h0 (Дж/(кг*К)), через запятую:")
h0_label.grid(row=0, column=0, sticky=tk.W, pady=5)
h0_entry = ttk.Entry(input_frame, width=30)
h0_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

# mreal
mreal_label = ttk.Label(input_frame, text="mreal (кг/с), через запятую:")
mreal_label.grid(row=1, column=0, sticky=tk.W, pady=5)
mreal_entry = ttk.Entry(input_frame, width=30)
mreal_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

# p2
p2_label = ttk.Label(input_frame, text="p2 (Па), через запятую:")
p2_label.grid(row=2, column=0, sticky=tk.W, pady=5)
p2_entry = ttk.Entry(input_frame, width=30)
p2_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

# f2
f2_label = ttk.Label(input_frame, text="f2 (м^2), через запятую (или одно значение):") # Updated label to reflect new input options
f2_label.grid(row=3, column=0, sticky=tk.W, pady=5)
f2_entry = ttk.Entry(input_frame, width=30)
f2_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
# f2_entry.insert(0, "1.347822e-6") # Removed default value

# start_i
start_i_label = ttk.Label(input_frame, text="Начальное i (К):")
start_i_label.grid(row=4, column=0, sticky=tk.W, pady=5)
start_i_entry = ttk.Entry(input_frame, width=10)
start_i_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
start_i_entry.insert(0, "140")

# end_i
end_i_label = ttk.Label(input_frame, text="Конечное i (К):")
end_i_label.grid(row=5, column=0, sticky=tk.W, pady=5)
end_i_entry = ttk.Entry(input_frame, width=10)
end_i_entry.grid(row=5, column=1, sticky=tk.W, pady=5)
end_i_entry.insert(0, "300")

# step_i
step_i_label = ttk.Label(input_frame, text="Шаг для i (К):")
step_i_label.grid(row=6, column=0, sticky=tk.W, pady=5)
step_i_entry = ttk.Entry(input_frame, width=10)
step_i_entry.grid(row=6, column=1, sticky=tk.W, pady=5)
step_i_entry.insert(0, "1")

# --- Кнопка расчета ---
calculate_button = ttk.Button(input_frame, text="Рассчитать", command=calculate_results)
calculate_button.grid(row=7, column=0, columnspan=2, pady=10)

# --- Вывод результатов ---
output_frame = ttk.Frame(root, padding="10")
output_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

output_label = ttk.Label(output_frame, text="Результаты:")
output_label.grid(row=0, column=0, sticky=tk.W)

output_text = scrolledtext.ScrolledText(output_frame, height=15, width=60)
output_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
output_text.config(state=tk.DISABLED)

# --- Справка ---
help_label = ttk.Label(output_frame, text="Справка:\nЧтобы умножить на 10 в степени X, используйте формат eX, где X - степень десяти.\nВставка чисел осуществляется только при включённой английской раскладке.\nАвтор программы - Маркин Михаил Ашотович, данное ПО распространяется под лицензией GNU GPL V3", justify=tk.LEFT)
help_label.grid(row=2, column=0, sticky=tk.W)

root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
input_frame.columnconfigure(1, weight=1)
output_frame.columnconfigure(0, weight=1)

root.mainloop()