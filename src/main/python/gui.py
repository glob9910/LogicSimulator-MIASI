import tkinter as tk
from logika import components, connections, get_coordinates

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Symulator Logiczny - Porty i Łamane Linie")
        
        self.canvas = tk.Canvas(root, width=800, height=500, bg="#2b2b2b")
        self.canvas.pack(fill="both", expand=True)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
