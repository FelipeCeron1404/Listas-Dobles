"""
Train Yard Manager - Doubly Linked List case study.

In a railway yard, an operator builds a freight train by coupling wagons.
Each wagon is coupled to the wagon in front of it and to the wagon behind it,
so the train behaves like a doubly linked list: wagons can be coupled or
uncoupled at any position, and the train can be inspected in both directions.
"""

import tkinter as tk
from tkinter import messagebox


class Wagon:

    def __init__(self, code, cargo, weight_tons):
        self.code = code
        self.cargo = cargo
        self.weight_tons = weight_tons
        self.next_wagon = None
        self.previous_wagon = None


class Train:

    def __init__(self):
        self.first_wagon = None
        self.last_wagon = None
        self.wagon_count = 0

    def is_empty(self):
        return self.first_wagon is None

    def couple_at_rear(self, code, cargo, weight_tons):
        new_wagon = Wagon(code, cargo, weight_tons)
        if self.is_empty():
            self.first_wagon = new_wagon
            self.last_wagon = new_wagon
        else:
            new_wagon.previous_wagon = self.last_wagon
            self.last_wagon.next_wagon = new_wagon
            self.last_wagon = new_wagon
        self.wagon_count += 1
        return new_wagon

    def couple_at_front(self, code, cargo, weight_tons):
        new_wagon = Wagon(code, cargo, weight_tons)
        if self.is_empty():
            self.first_wagon = new_wagon
            self.last_wagon = new_wagon
        else:
            new_wagon.next_wagon = self.first_wagon
            self.first_wagon.previous_wagon = new_wagon
            self.first_wagon = new_wagon
        self.wagon_count += 1
        return new_wagon

    def go_to_position(self, position):
        if position < 0 or position >= self.wagon_count:
            return None

        if position < self.wagon_count // 2:
            current_wagon = self.first_wagon
            step = 0
            while step != position:
                current_wagon = current_wagon.next_wagon
                step += 1
        else:
            current_wagon = self.last_wagon
            step = self.wagon_count - 1
            while step != position:
                current_wagon = current_wagon.previous_wagon
                step -= 1
        return current_wagon

    def couple_at_position(self, position, code, cargo, weight_tons):
        if position <= 0:
            return self.couple_at_front(code, cargo, weight_tons)
        if position >= self.wagon_count:
            return self.couple_at_rear(code, cargo, weight_tons)

        new_wagon = Wagon(code, cargo, weight_tons)
        wagon_ahead = self.go_to_position(position - 1)
        wagon_behind = wagon_ahead.next_wagon

        wagon_ahead.next_wagon = new_wagon
        new_wagon.previous_wagon = wagon_ahead
        new_wagon.next_wagon = wagon_behind
        wagon_behind.previous_wagon = new_wagon

        self.wagon_count += 1
        return new_wagon

    def uncouple_wagon(self, wagon):
        if wagon is None:
            return None

        if wagon.previous_wagon is None:
            self.first_wagon = wagon.next_wagon
        else:
            wagon.previous_wagon.next_wagon = wagon.next_wagon

        if wagon.next_wagon is None:
            self.last_wagon = wagon.previous_wagon
        else:
            wagon.next_wagon.previous_wagon = wagon.previous_wagon

        wagon.next_wagon = None
        wagon.previous_wagon = None
        self.wagon_count -= 1
        return wagon

    def uncouple_at_position(self, position):
        return self.uncouple_wagon(self.go_to_position(position))

    def find_position_by_code(self, code):
        current_wagon = self.first_wagon
        position = 0
        while current_wagon is not None:
            if current_wagon.code == code:
                return position
            current_wagon = current_wagon.next_wagon
            position += 1
        return -1

    def has_code(self, code):
        return self.find_position_by_code(code) != -1

    def position_of(self, wagon):
        current_wagon = self.first_wagon
        position = 0
        while current_wagon is not None:
            if current_wagon is wagon:
                return position
            current_wagon = current_wagon.next_wagon
            position += 1
        return -1

    def total_weight(self):
        total = 0.0
        current_wagon = self.first_wagon
        while current_wagon is not None:
            total += current_wagon.weight_tons
            current_wagon = current_wagon.next_wagon
        return total

    def describe_forward(self):
        text = ""
        current_wagon = self.first_wagon
        while current_wagon is not None:
            text += current_wagon.code
            if current_wagon.next_wagon is not None:
                text += " -> "
            current_wagon = current_wagon.next_wagon
        return text

    def describe_backward(self):
        text = ""
        current_wagon = self.last_wagon
        while current_wagon is not None:
            text += current_wagon.code
            if current_wagon.previous_wagon is not None:
                text += " -> "
            current_wagon = current_wagon.previous_wagon
        return text


BACKGROUND = "#eef2f7"
PANEL = "#ffffff"
DARK = "#1f2a44"
ACCENT = "#e07a1f"
HIGHLIGHT = "#ffd400"

WAGON_WIDTH = 130
WAGON_HEIGHT = 80
WAGON_GAP = 55
TRACK_Y = 170


def cargo_color(cargo):
    if cargo == "Café":
        return "#8b5a2b"
    if cargo == "Carbón":
        return "#4a4a4a"
    if cargo == "Combustible":
        return "#c0392b"
    if cargo == "Granos":
        return "#d4a017"
    if cargo == "Contenedores":
        return "#2e86c1"
    return "#7f8c8d"


class TrainYardApp:

    def __init__(self, window):
        self.window = window
        self.train = Train()
        self.inspected_wagon = None

        self.window.title("Patio de Maniobras - Lista Doblemente Enlazada")
        self.window.geometry("1150x700")
        self.window.configure(bg=BACKGROUND)

        self.code_value = tk.StringVar()
        self.cargo_value = tk.StringVar(value="Café")
        self.weight_value = tk.StringVar()
        self.position_value = tk.StringVar()

        self.build_header()
        self.build_controls()
        self.build_canvas()
        self.build_status_panel()

        self.load_sample_train()
        self.refresh_view()

    def build_header(self):
        header = tk.Frame(self.window, bg=DARK)
        header.pack(fill="x")
        tk.Label(header, text="PATIO DE MANIOBRAS", bg=DARK, fg="white",
                 font="Helvetica 18 bold").pack(side="left", padx=20, pady=12)
        tk.Label(header, text="Armado de trenes de carga con una lista doblemente enlazada",
                 bg=DARK, fg="#c9d3e6", font="Helvetica 11").pack(side="left", pady=12)

    def build_controls(self):
        controls = tk.Frame(self.window, bg=BACKGROUND)
        controls.pack(fill="x", padx=15, pady=10)

        data_panel = tk.LabelFrame(controls, text=" Datos del vagón ", bg=PANEL,
                                   fg=DARK, font="Helvetica 11 bold", padx=10, pady=8)
        data_panel.pack(side="left", fill="y", padx=5)

        tk.Label(data_panel, text="Código:", bg=PANEL).grid(row=0, column=0, sticky="w")
        tk.Entry(data_panel, textvariable=self.code_value, width=14).grid(row=0, column=1, sticky="w")

        tk.Label(data_panel, text="Peso (t):", bg=PANEL).grid(row=1, column=0, sticky="w")
        tk.Entry(data_panel, textvariable=self.weight_value, width=14).grid(row=1, column=1, sticky="w")

        tk.Label(data_panel, text="Posición:", bg=PANEL).grid(row=2, column=0, sticky="w")
        tk.Entry(data_panel, textvariable=self.position_value, width=14).grid(row=2, column=1, sticky="w")

        cargo_box = tk.Frame(data_panel, bg=PANEL)
        cargo_box.grid(row=0, column=2, rowspan=3, padx=12, sticky="n")
        tk.Label(cargo_box, text="Carga:", bg=PANEL).pack(anchor="w")
        self.add_cargo_option(cargo_box, "Café")
        self.add_cargo_option(cargo_box, "Carbón")
        self.add_cargo_option(cargo_box, "Combustible")
        self.add_cargo_option(cargo_box, "Granos")
        self.add_cargo_option(cargo_box, "Contenedores")

        couple_panel = tk.LabelFrame(controls, text=" Enganche ", bg=PANEL,
                                     fg=DARK, font="Helvetica 11 bold", padx=10, pady=8)
        couple_panel.pack(side="left", fill="y", padx=5)
        self.add_button(couple_panel, "Enganchar al inicio", self.on_couple_front, "#27ae60")
        self.add_button(couple_panel, "Enganchar al final", self.on_couple_rear, "#27ae60")
        self.add_button(couple_panel, "Enganchar en posición", self.on_couple_position, "#27ae60")
        self.add_button(couple_panel, "Desenganchar en posición", self.on_uncouple_position, "#c0392b")
        self.add_button(couple_panel, "Desenganchar inspeccionado", self.on_uncouple_inspected, "#c0392b")

        inspector_panel = tk.LabelFrame(controls, text=" Inspector (recorrer el tren) ",
                                        bg=PANEL, fg=DARK, font="Helvetica 11 bold",
                                        padx=10, pady=8)
        inspector_panel.pack(side="left", fill="both", expand=True, padx=5)

        nav = tk.Frame(inspector_panel, bg=PANEL)
        nav.pack(fill="x")
        self.add_small_button(nav, "|< Primero", self.on_inspect_first)
        self.add_small_button(nav, "< Anterior", self.on_inspect_previous)
        self.add_small_button(nav, "Siguiente >", self.on_inspect_next)
        self.add_small_button(nav, "Último >|", self.on_inspect_last)

        search = tk.Frame(inspector_panel, bg=PANEL)
        search.pack(fill="x", pady=6)
        self.add_small_button(search, "Buscar por código", self.on_find_by_code)
        self.add_small_button(search, "Vaciar patio", self.on_clear_train)

        self.inspector_label = tk.Label(inspector_panel, text="", bg="#fff8d6", fg=DARK,
                                        justify="left", anchor="w", font="Consolas 10",
                                        padx=8, pady=6)
        self.inspector_label.pack(fill="both", expand=True)

    def build_canvas(self):
        canvas_frame = tk.Frame(self.window, bg=BACKGROUND)
        canvas_frame.pack(fill="both", expand=True, padx=15)

        self.canvas = tk.Canvas(canvas_frame, bg="#f9fbfd", height=300,
                                highlightthickness=1, highlightbackground="#c9d3e6")
        scroll = tk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=scroll.set)
        self.canvas.pack(fill="both", expand=True)
        scroll.pack(fill="x")

    def build_status_panel(self):
        status = tk.Frame(self.window, bg=DARK)
        status.pack(fill="x", side="bottom")
        self.summary_label = tk.Label(status, text="", bg=DARK, fg="white",
                                      font="Helvetica 11 bold", anchor="w")
        self.summary_label.pack(fill="x", padx=15, pady=4)
        self.forward_label = tk.Label(status, text="", bg=DARK, fg="#9be7a5",
                                      font="Consolas 10", anchor="w")
        self.forward_label.pack(fill="x", padx=15)
        self.backward_label = tk.Label(status, text="", bg=DARK, fg="#f5b77a",
                                       font="Consolas 10", anchor="w")
        self.backward_label.pack(fill="x", padx=15, pady=4)

    def add_cargo_option(self, parent, cargo):
        tk.Radiobutton(parent, text=cargo, value=cargo, variable=self.cargo_value,
                       bg=PANEL, activebackground=PANEL,
                       fg=cargo_color(cargo), font="Helvetica 10 bold").pack(anchor="w")

    def add_button(self, parent, text, action, color):
        tk.Button(parent, text=text, command=action, bg=color, fg="white",
                  activebackground=DARK, activeforeground="white",
                  font="Helvetica 10 bold", width=24, relief="flat",
                  cursor="hand2").pack(pady=2)

    def add_small_button(self, parent, text, action):
        tk.Button(parent, text=text, command=action, bg=DARK, fg="white",
                  activebackground=ACCENT, activeforeground="white",
                  font="Helvetica 10 bold", relief="flat", padx=8,
                  cursor="hand2").pack(side="left", padx=3)

    def read_new_wagon_data(self):
        code = self.code_value.get().strip().upper()
        cargo = self.cargo_value.get()
        weight_text = self.weight_value.get().strip().replace(",", ".")

        if code == "":
            messagebox.showwarning("Faltan datos", "Escribe un código para el vagón.")
            return None
        if self.train.has_code(code):
            messagebox.showwarning("Código repetido", "El vagón " + code + " ya está en el tren.")
            return None
        try:
            weight_tons = float(weight_text)
        except ValueError:
            messagebox.showwarning("Peso inválido", "El peso debe ser un número.")
            return None
        if weight_tons <= 0:
            messagebox.showwarning("Peso inválido", "El peso debe ser mayor que cero.")
            return None
        return code, cargo, weight_tons

    def read_position(self):
        try:
            return int(self.position_value.get().strip())
        except ValueError:
            messagebox.showwarning("Posición inválida", "Escribe un número entero en la posición.")
            return None

    def clear_form(self):
        self.code_value.set("")
        self.weight_value.set("")
        self.position_value.set("")

    def on_couple_front(self):
        data = self.read_new_wagon_data()
        if data is None:
            return
        code, cargo, weight_tons = data
        self.inspected_wagon = self.train.couple_at_front(code, cargo, weight_tons)
        self.clear_form()
        self.refresh_view()

    def on_couple_rear(self):
        data = self.read_new_wagon_data()
        if data is None:
            return
        code, cargo, weight_tons = data
        self.inspected_wagon = self.train.couple_at_rear(code, cargo, weight_tons)
        self.clear_form()
        self.refresh_view()

    def on_couple_position(self):
        position = self.read_position()
        if position is None:
            return
        if position < 0 or position > self.train.wagon_count:
            messagebox.showwarning("Posición inválida",
                                   "Posiciones válidas: de 0 a " + str(self.train.wagon_count) + ".")
            return
        data = self.read_new_wagon_data()
        if data is None:
            return
        code, cargo, weight_tons = data
        self.inspected_wagon = self.train.couple_at_position(position, code, cargo, weight_tons)
        self.clear_form()
        self.refresh_view()

    def on_uncouple_position(self):
        if self.train.is_empty():
            messagebox.showinfo("Tren vacío", "No hay vagones para desenganchar.")
            return
        position = self.read_position()
        if position is None:
            return
        target = self.train.go_to_position(position)
        if target is None:
            messagebox.showwarning("Posición inválida",
                                   "Posiciones válidas: de 0 a " + str(self.train.wagon_count - 1) + ".")
            return
        self.remove_wagon(target)

    def on_uncouple_inspected(self):
        if self.inspected_wagon is None:
            messagebox.showinfo("Sin selección", "Primero selecciona un vagón con el inspector.")
            return
        self.remove_wagon(self.inspected_wagon)

    def remove_wagon(self, target):
        if not messagebox.askyesno("Confirmar", "¿Desenganchar el vagón " + target.code + "?"):
            return
        if target is self.inspected_wagon:
            if target.next_wagon is not None:
                self.inspected_wagon = target.next_wagon
            else:
                self.inspected_wagon = target.previous_wagon
        self.train.uncouple_wagon(target)
        self.position_value.set("")
        self.refresh_view()

    def on_inspect_first(self):
        self.inspected_wagon = self.train.first_wagon
        self.refresh_view()

    def on_inspect_last(self):
        self.inspected_wagon = self.train.last_wagon
        self.refresh_view()

    def on_inspect_next(self):
        if self.inspected_wagon is None:
            self.inspected_wagon = self.train.first_wagon
        elif self.inspected_wagon.next_wagon is not None:
            self.inspected_wagon = self.inspected_wagon.next_wagon
        else:
            messagebox.showinfo("Fin del tren", "Este es el último vagón (siguiente = NULL).")
        self.refresh_view()

    def on_inspect_previous(self):
        if self.inspected_wagon is None:
            self.inspected_wagon = self.train.last_wagon
        elif self.inspected_wagon.previous_wagon is not None:
            self.inspected_wagon = self.inspected_wagon.previous_wagon
        else:
            messagebox.showinfo("Inicio del tren", "Este es el primer vagón (anterior = NULL).")
        self.refresh_view()

    def on_find_by_code(self):
        code = self.code_value.get().strip().upper()
        if code == "":
            messagebox.showwarning("Faltan datos", "Escribe el código a buscar en el campo Código.")
            return
        position = self.train.find_position_by_code(code)
        if position == -1:
            messagebox.showinfo("No encontrado", "El vagón " + code + " no está en el tren.")
            return
        self.inspected_wagon = self.train.go_to_position(position)
        self.refresh_view()

    def on_clear_train(self):
        if self.train.is_empty():
            return
        if messagebox.askyesno("Confirmar", "¿Desenganchar TODOS los vagones?"):
            while not self.train.is_empty():
                self.train.uncouple_wagon(self.train.first_wagon)
            self.inspected_wagon = None
            self.refresh_view()

    def refresh_view(self):
        self.draw_train()
        self.update_inspector()
        self.summary_label.config(
            text="Vagones: " + str(self.train.wagon_count)
                 + "     Carga total: " + format(self.train.total_weight(), ".1f") + " t")

        forward_text = self.train.describe_forward()
        backward_text = self.train.describe_backward()
        if self.train.is_empty():
            forward_text = "(tren vacío)"
            backward_text = "(tren vacío)"
        self.forward_label.config(text="Recorrido hacia adelante (primero -> último):  " + forward_text)
        self.backward_label.config(text="Recorrido hacia atrás    (último -> primero):  " + backward_text)

    def update_inspector(self):
        wagon = self.inspected_wagon
        if wagon is None:
            self.inspector_label.config(text="Ningún vagón seleccionado.")
            return
        previous_code = "NULL" if wagon.previous_wagon is None else wagon.previous_wagon.code
        next_code = "NULL" if wagon.next_wagon is None else wagon.next_wagon.code
        self.inspector_label.config(
            text="Posición:       " + str(self.train.position_of(wagon))
                 + "\nCódigo:         " + wagon.code
                 + "\nCarga:          " + wagon.cargo + "  (" + format(wagon.weight_tons, ".1f") + " t)"
                 + "\nVagón anterior: " + previous_code
                 + "\nVagón siguiente: " + next_code)

    def draw_train(self):
        canvas = self.canvas
        canvas.delete("all")

        right_end = 230 + self.train.wagon_count * (WAGON_WIDTH + WAGON_GAP) + 150
        canvas.create_line(0, TRACK_Y + 22, right_end, TRACK_Y + 22, fill="#8d6e63", width=3)
        canvas.create_line(0, TRACK_Y + 30, right_end, TRACK_Y + 30, fill="#8d6e63", width=3)

        self.draw_locomotive(20)

        x = 230
        if self.train.is_empty():
            canvas.create_text(x + 90, TRACK_Y - 40, text="Cabeza = NULL\nCola = NULL",
                               fill="#7f8c8d", font="Consolas 11")
        else:
            canvas.create_text(x - 28, TRACK_Y - 18, text="NULL", fill="#95a5a6", font="Consolas 9")

        current_wagon = self.train.first_wagon
        position = 0
        while current_wagon is not None:
            self.draw_wagon(current_wagon, x, position)
            if current_wagon.next_wagon is not None:
                self.draw_links(x + WAGON_WIDTH, x + WAGON_WIDTH + WAGON_GAP)
            else:
                canvas.create_text(x + WAGON_WIDTH + 28, TRACK_Y - 62, text="NULL",
                                   fill="#95a5a6", font="Consolas 9")
            current_wagon = current_wagon.next_wagon
            x += WAGON_WIDTH + WAGON_GAP
            position += 1

        canvas.configure(scrollregion=canvas.bbox("all"))

    def draw_locomotive(self, x):
        canvas = self.canvas
        top = TRACK_Y - WAGON_HEIGHT
        canvas.create_rectangle(x + 40, top - 10, x + 180, TRACK_Y + 8, fill=DARK, outline=DARK)
        canvas.create_rectangle(x + 120, top - 45, x + 180, top - 10, fill=DARK, outline=DARK)
        canvas.create_rectangle(x + 130, top - 38, x + 170, top - 18, fill="#aed6f1", outline="")
        canvas.create_polygon(x + 40, top - 10, x, TRACK_Y + 8, x + 40, TRACK_Y + 8,
                              fill=ACCENT, outline=ACCENT)
        canvas.create_text(x + 85, top + 35, text="LOCOMOTORA", fill="white", font="Helvetica 10 bold")
        self.draw_wheels(x + 55, x + 155)
        if not self.train.is_empty():
            canvas.create_line(x + 180, TRACK_Y - 5, x + 210, TRACK_Y - 5, fill=DARK, width=4)

    def draw_wagon(self, wagon, x, position):
        canvas = self.canvas
        top = TRACK_Y - WAGON_HEIGHT

        if wagon is self.inspected_wagon:
            canvas.create_rectangle(x - 6, top - 32, x + WAGON_WIDTH + 6, TRACK_Y + 38,
                                    fill="", outline=HIGHLIGHT, width=4)

        canvas.create_text(x + WAGON_WIDTH / 2, top - 18, text="[" + str(position) + "]",
                           fill=DARK, font="Helvetica 11 bold")
        canvas.create_rectangle(x, top, x + WAGON_WIDTH, TRACK_Y + 8,
                                fill=cargo_color(wagon.cargo), outline=DARK, width=2)
        canvas.create_text(x + WAGON_WIDTH / 2, top + 20, text=wagon.code,
                           fill="white", font="Helvetica 12 bold")
        canvas.create_text(x + WAGON_WIDTH / 2, top + 42, text=wagon.cargo,
                           fill="white", font="Helvetica 10")
        canvas.create_text(x + WAGON_WIDTH / 2, top + 62,
                           text=format(wagon.weight_tons, ".1f") + " t",
                           fill="white", font="Helvetica 10 bold")
        self.draw_wheels(x + 15, x + WAGON_WIDTH - 35)

        label_y = TRACK_Y + 55
        if wagon is self.train.first_wagon:
            canvas.create_text(x + WAGON_WIDTH / 2, label_y, text="CABEZA",
                               fill="#27ae60", font="Consolas 10 bold")
            label_y += 16
        if wagon is self.train.last_wagon:
            canvas.create_text(x + WAGON_WIDTH / 2, label_y, text="COLA",
                               fill="#c0392b", font="Consolas 10 bold")

    def draw_wheels(self, first_x, second_x):
        self.canvas.create_oval(first_x, TRACK_Y + 2, first_x + 20, TRACK_Y + 22,
                                fill="#2c3e50", outline="")
        self.canvas.create_oval(second_x, TRACK_Y + 2, second_x + 20, TRACK_Y + 22,
                                fill="#2c3e50", outline="")

    def draw_links(self, from_x, to_x):
        canvas = self.canvas
        next_y = TRACK_Y - 55
        previous_y = TRACK_Y - 25
        canvas.create_line(from_x + 2, next_y, to_x - 2, next_y,
                           arrow="last", fill="#27ae60", width=2)
        canvas.create_text((from_x + to_x) / 2, next_y - 9, text="sig",
                           fill="#27ae60", font="Consolas 8")
        canvas.create_line(to_x - 2, previous_y, from_x + 2, previous_y,
                           arrow="last", fill="#c0392b", width=2)
        canvas.create_text((from_x + to_x) / 2, previous_y + 9, text="ant",
                           fill="#c0392b", font="Consolas 8")

    def load_sample_train(self):
        self.train.couple_at_rear("CF-101", "Café", 32.5)
        self.train.couple_at_rear("GR-205", "Granos", 40.0)
        self.train.couple_at_rear("CT-310", "Contenedores", 28.0)
        self.train.couple_at_rear("FU-412", "Combustible", 55.0)
        self.inspected_wagon = self.train.first_wagon


if __name__ == "__main__":
    main_window = tk.Tk()
    TrainYardApp(main_window)
    main_window.mainloop()
