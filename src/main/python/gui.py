import tkinter as tk
from tkinter import messagebox
from logika import get_coordinates
import json



class App:
    def __init__(self, root: tk.Tk, javaFunc) -> None:
        self.root = root
        self.root.title("Symulator Logiczny - Porty i Łamane Linie")
        self.root.geometry("800x600")
        # self.root.state('zoomed') -- na linuxie nie dziala zoomed


        # Kod Aleksandra
        self.passToJava = javaFunc


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

        # Przesuwanie canvasu myszką (przeciąganie lewym przyciskiem)
        self.canvas.bind("<ButtonPress-1>", self._pan_start)
        self.canvas.bind("<B1-Motion>", self._pan_move)
        # Zoom scrollem
        self.canvas.bind("<MouseWheel>", self._zoom)

        self.jsonString = ""

        # Kod Maćka — canvas startuje pusty, rysowanie po Convert()
        self.coords = {}



    def draw_wires(self, connections):
        for src, dst in connections:
            # Obsługa notacji kropkowej: 'kaczka.x' → 'kaczka'
            src_id = src.split('.')[0]
            dst_id = dst.split('.')[0]

            # Punkt startowy — szukamy wyjścia (NIE oznaczamy jako occupied,
            # bo jedno wyjście może zasilać wiele wejść)
            src_gate = self.coords[src_id]
            start_pin = None
            for key in sorted(src_gate.keys()):
                if (key == 'out' or key.startswith('out_')) and isinstance(src_gate[key], dict):
                    start_pin = src_gate[key]
                    break
            if start_pin is None:
                print(f"BŁĄD: Nie znaleziono wyjścia dla '{src}'!")
                continue
            start_x = start_pin['x']
            start_y = start_pin['y']

            # Punkt docelowy — szukamy wolnego wejścia
            dst_gate = self.coords[dst_id]
            end_pin = None
            for key in sorted(dst_gate.keys()):
                if key.startswith('in_') and isinstance(dst_gate[key], dict):
                    if not dst_gate[key].get('occupied', False):
                        end_pin = dst_gate[key]
                        end_pin['occupied'] = True
                        break
            if end_pin is None:
                print(f"BŁĄD: Za dużo połączeń do bramki {dst}!")
                continue
            end_x = end_pin['x']
            end_y = end_pin['y']

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
            for key in gate_data:
                if (key.startswith('in_') or key == 'out' or key.startswith('out_')):
                    if isinstance(gate_data[key], dict) and 'x' in gate_data[key]:
                        px, py = gate_data[key]['x'], gate_data[key]['y']
                        self.canvas.create_oval(px-r, py-r, px+r, py+r, outline="black")



    def parse_json(self, json_string):
        data = json.loads(json_string)
        main = data['main']

        components = []
        for elem in main['elements']:
            components.append({
                'id': elem['name'],
                'type': elem['type'],
                'label': elem['name']
            })

        connections = []
        const_counter = 0
        for conn in main['connections']:
            src, dst = str(conn[0]), str(conn[1])
            # Stała logiczna ("1" lub "0") → tworzymy wirtualny INPUT
            if src in ('0', '1'):
                const_id = f'const_{src}_{const_counter}'
                const_counter += 1
                components.append({'id': const_id, 'type': 'INPUT', 'label': src})
                src = const_id
            connections.append((src, dst))

        return components, connections

    def Convert(self):
        self.inputText = self.textbox.get("1.0", tk.END)
        self.jsonString = str(self.passToJava(self.inputText))
        print(self.jsonString)  # print for testing

        components, connections = self.parse_json(self.jsonString)
        self.coords = get_coordinates(components, connections)
        self.canvas.delete("all")
        self.draw_wires(connections)
        self.draw_components(components)
        # Ustawiamy scrollregion na cały narysowany obszar
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def _pan_start(self, event):
        # Zapamiętujemy punkt startu przeciągania
        self.canvas.scan_mark(event.x, event.y)

    def _pan_move(self, event):
        # Przesuwamy canvas o różnicę od punktu startu
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def _zoom(self, event):
        # Scroll w górę = powiększenie, w dół = pomniejszenie
        if event.delta > 0:
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        else:
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_close(self):
        close_app = messagebox.askyesno(title="Exit app?", message="Do you really want to exit?")
        if close_app:
            self.root.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    tempFunc = lambda str: str
    app = App(root, tempFunc)
    root.mainloop()
