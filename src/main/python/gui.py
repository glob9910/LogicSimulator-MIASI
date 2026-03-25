import tkinter as tk
from tkinter import messagebox
from logika import components, connections, get_coordinates



class App:
    def __init__(self, root: tk.Tk, javaFunc) -> None:
        self.root = root
        self.root.title("Symulator Logiczny - Porty i Łamane Linie")
        self.root.geometry("800x600")
        self.root.state('zoomed')


        self.passToJava = javaFunc


        # Kod Aleksandra
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)


        self.menubar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Close", command=self.on_close)

        self.menubar.add_cascade(menu=self.filemenu, label="File")

        self.root.config(menu=self.menubar)


        self.mainWindow = tk.Frame(self.root, bg="#2b2b2b")
        self.mainWindow.columnconfigure(0, weight=1, uniform='one')
        self.mainWindow.columnconfigure(1, weight=0)
        self.mainWindow.columnconfigure(2, weight=1, uniform='one')
        self.mainWindow.rowconfigure(0, weight=0)
        self.mainWindow.rowconfigure(1, weight=1)
        self.mainWindow.grid(row=0, column=0, sticky=tk.NSEW)


        self.label = tk.Label(self.mainWindow, text="Logic text", font=('Arial', 18))
        self.label.grid(row=0, column=0, pady=20)

        self.textbox = tk.Text(self.mainWindow, font=('Arial', 12), bg="#2b2b2b", fg="#FFFFFF")
        self.textbox.grid(row=1, column=0, padx=20, sticky=tk.NSEW)

        self.button = tk.Button(self.mainWindow, text="Convert", font=('Arial', 16), command=self.Convert)
        self.button.grid(row=1, column=1, padx=10, pady=10, sticky=tk.N)

        self.inputText = ""
        

        # self.canvas = tk.Canvas(root, width=800, height=500, bg="#2b2b2b")
        # self.canvas.pack(fill="both", expand=True)

        # Zmieniony kod Maćka aby działał z kodem Aleksandra
        self.canvas = tk.Canvas(self.mainWindow, bg="#2b2b2b", highlightthickness=1)
        self.canvas.grid(row=1, column=2, padx=20, sticky=tk.NSEW)


        # Kod Maćka
        self.coords = get_coordinates(components, connections)
        self.draw_wires(connections)
        self.draw_components(components)



    def draw_wires(self, connections):
        for src, dst in connections:
            # Punkt startowy z wyjścia bramki źródłowej
            start_x = self.coords[src]['out']['x']
            start_y = self.coords[src]['out']['y']
            
            # Punkt docelowy szukamy w wolnych wejściach
            dst_gate = self.coords[dst]
            
            if 'in_1' in dst_gate and not dst_gate['in_1']['occupied']:
                end_x, end_y = dst_gate['in_1']['x'], dst_gate['in_1']['y']
                dst_gate['in_1']['occupied'] = True
            elif 'in_2' in dst_gate and not dst_gate['in_2']['occupied']:
                end_x, end_y = dst_gate['in_2']['x'], dst_gate['in_2']['y']
                dst_gate['in_2']['occupied'] = True
            else:
                print(f"BŁĄD: Za dużo połączeń do bramki {dst}!")
                continue

            # Manhattan Routing
            mid_x = (start_x + end_x) / 2
            
            self.canvas.create_line(
                start_x, start_y,  # Start
                mid_x, start_y,    # Poziomo do połowy
                mid_x, end_y,      # Pionowo do poziomu celu
                end_x, end_y,      # Poziomo do celu
                fill="#00ffcc", 
                width=2
            )

    def draw_components(self, components):
        for comp in components:
            c_id = comp['id']
            gate_data = self.coords[c_id]
            x, y = gate_data['x'], gate_data['y']
            
            # Prostokąt reprezentujący bramkę
            self.canvas.create_rectangle(x - 30, y - 20, x + 30, y + 20, 
                                         fill="#3c3f41", outline="#5e6266", width=2)
            
            # Etykiety i teksty
            self.canvas.create_text(x, y-5, text=comp['type'], font=("Arial", 9, "bold"), fill="white")
            self.canvas.create_text(x, y+10, text=comp['label'], font=("Arial", 7), fill="#aaaaaa")
            
            # Rysowanie małych kropek (pinów) dla wizualizacji portów
            r = 3 # promień pinu
            if 'in_1' in gate_data:
                px, py = gate_data['in_1']['x'], gate_data['in_1']['y']
                self.canvas.create_oval(px-r, py-r, px+r, py+r, outline="black")
            if 'in_2' in gate_data:
                px, py = gate_data['in_2']['x'], gate_data['in_2']['y']
                self.canvas.create_oval(px-r, py-r, px+r, py+r, outline="black")
            if 'out' in gate_data:
                px, py = gate_data['out']['x'], gate_data['out']['y']
                self.canvas.create_oval(px-r, py-r, px+r, py+r, outline="black")



    def Convert(self):
        self.inputText = self.textbox.get("1.0", tk.END)
        self.passToJava(self.inputText)

    def on_close(self):
        close_app = messagebox.askyesno(title="Exit app?", message="Do you really want to exit?")
        if close_app:
            self.root.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()