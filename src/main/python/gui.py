import tkinter as tk
from tkinter import messagebox
from logika import get_coordinates
import json
from simulator import CustomComponent


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

        self.label = tk.Label(
            self.mainWindow, text="Logic text", font=('Arial', 18))
        self.label.grid(row=0, column=0, pady=20)

        self.textbox = tk.Text(self.mainWindow, font=(
            'Arial', 12), bg="#2b2b2b", fg="#FFFFFF")
        self.textbox.grid(row=1, column=0, padx=20, sticky=tk.NSEW)

        self.button = tk.Button(self.mainWindow, text="Convert", font=(
            'Arial', 16), command=self.Convert)
        self.button.grid(row=1, column=1, padx=10, pady=10, sticky=tk.N)

        self.inputText = ""

        # self.canvas = tk.Canvas(root, width=800, height=500, bg="#2b2b2b")
        # self.canvas.pack(fill="both", expand=True)

        # Zmieniony kod Maćka aby działał z kodem Aleksandra
        self.canvas = tk.Canvas(
            self.mainWindow, bg="#2b2b2b", highlightthickness=1)
        self.canvas.grid(row=1, column=2, padx=20, sticky=tk.NSEW)

        # Przesuwanie canvasu myszką (przeciąganie lewym przyciskiem)
        self.canvas.bind("<ButtonPress-1>", self._pan_start)
        self.canvas.bind("<B1-Motion>", self._pan_move)
        # Zoom scrollem
        self.canvas.bind("<MouseWheel>", self._zoom)

        self.jsonString = ""

        # Kod Maćka — canvas startuje pusty, rysowanie po Convert()
        self.coords = {}

        # Kod Aleksandra - Symulator
        self.COMPONENT_TO_CANVAS = {'main': self.canvas}
        self.COMPONENT_TO_SIMULATOR = {'main': None}
        self.COMPONENT_TO_RECTID = {'main': []}
        self.act_comp = "#dddd00"
        self.inact_comp = "#3c3f41"



    def draw_wires(self, connections, target_canvas=None, target_coords=None):
        canvas = target_canvas if target_canvas else self.canvas
        coords = target_coords if target_coords else self.coords
        for offset_i, conn_data in enumerate(connections):
            src, dst = conn_data[0], conn_data[1]
            # Używamy ujednoliconego net_id z logika.py jeśli istnieje (cały przewód = 1 tag)
            net_id = conn_data[2] if len(conn_data) > 2 else src

            # Obsługa notacji kropkowej: 'kaczka.x' → 'kaczka', 'or1' -> 'or1'
            src_id = src.split('.')[0]
            dst_id = dst.split('.')[0]

            # Obsługa notacji kropkowej: 'kaczka.x' → 'x', 'or1' -> ''
            src_g_name = src.split('.')[1] if '.' in src else ''
            dst_g_name = dst.split('.')[1] if '.' in dst else ''

            # Punkt startowy — szukamy nazwy wyjścia
            src_gate = coords[src_id]
            start_pin = None
            for key in sorted(src_gate.keys()):
                if (key == 'out' or key.startswith('out_')) and isinstance(src_gate[key], dict):
                    if src_gate[key].get('name', '') == src_g_name:
                        start_pin = src_gate[key]
                        break
            if start_pin is None:
                print(f"BŁĄD: Nie znaleziono wyjścia dla '{src}'!")
                continue
            start_x = start_pin['x']
            start_y = start_pin['y']

            # Punkt docelowy — szukamy nazwy wejścia
            dst_gate = coords[dst_id]
            end_pin = None
            for key in sorted(dst_gate.keys()):
                if key.startswith('in_') and isinstance(dst_gate[key], dict):
                    if dst_gate[key].get('name', '') == dst_g_name and not dst_gate[key].get('occupied', False):
                        end_pin = dst_gate[key]
                        end_pin['occupied'] = True
                        break

            if end_pin is None:
                print(f"BŁĄD: Za dużo połączeń do bramki {dst}!")
                continue
            end_x = end_pin['x']
            end_y = end_pin['y']

            # Manhattan Routing
            fraction = 0.2 + (offset_i % 7) * 0.1
            mid_x = start_x + (end_x - start_x) * fraction

            w_tag = f"wire_group_{str(net_id).replace('.', '_')}"
            #print(
            #    f"[DEBUG] Wires: src={src}, dst={dst}, net_id={net_id}, w_tag={w_tag}")

            canvas.create_line(
                start_x, start_y, mid_x, start_y, mid_x, end_y, end_x, end_y,
                fill="#00ffcc", width=2, tags=(w_tag,)
            )

            def make_on_enter(tag):
                def _enter(e):
                    canvas.itemconfig(tag, fill="#ffffff", width=4)
                    canvas.tag_raise(tag)
                return _enter

            def make_on_leave(tag):
                def _leave(e):
                    canvas.itemconfig(tag, fill="#00ffcc", width=2)
                    canvas.tag_lower(tag)
                return _leave

            canvas.tag_bind(w_tag, "<Enter>", make_on_enter(w_tag))
            canvas.tag_bind(w_tag, "<Leave>", make_on_leave(w_tag))

    def draw_components(self, components, target_comp, target_canvas=None, target_coords=None):
        canvas = target_canvas if target_canvas else self.canvas
        coords = target_coords if target_coords else self.coords
        for comp in components:
            if comp['type'] == 'VIRTUAL':
                continue

            c_id = comp['id']
            gate_data = coords[c_id]
            x, y = gate_data['x'], gate_data['y']

            # Prostokąt reprezentujący bramkę
            is_custom = comp['type'] not in (
                'INPUT', 'OUTPUT', 'AND', 'OR', 'NOT', 'XOR', 'NAND', 'NOR', 'XNOR', 'SIGNAL', 'VIRTUAL')
            outline_color = "#e6a822" if is_custom else "#5e6266"
            rect_tags = (f"comp_{c_id}",) if is_custom else ()

            rect_id = canvas.create_rectangle(x - 30, y - 20, x + 30, y + 20,
                                    fill=self.inact_comp, outline=outline_color, width=2, tags=rect_tags)
            
            if c_id.startswith('const_1'):
                canvas.itemconfig(rect_id, fill=self.act_comp, outline='#ffff00')

            if comp['type'] == 'OUTPUT':
                self.COMPONENT_TO_RECTID[target_comp].append(rect_id)

            if comp['type'] == 'INPUT' and not c_id.startswith('const_'):
                canvas.itemconfig(rect_id, tags=(f"in_{c_id}",))
                canvas.tag_bind(f"in_{c_id}", "<Button-1>", lambda e,
                                tc=target_comp, rId=rect_id, cId=c_id: self.click_input(tc, rId, cId))

            if is_custom:
                canvas.tag_bind(f"comp_{c_id}", "<Button-1>", lambda e,
                                ct=comp['type']: self.open_subcomponent(ct))
                canvas.tag_bind(f"comp_{c_id}", "<Enter>", lambda e,
                                tag=f"comp_{c_id}": canvas.config(cursor="hand2"))
                canvas.tag_bind(f"comp_{c_id}", "<Leave>", lambda e,
                                tag=f"comp_{c_id}": canvas.config(cursor=""))

            # Etykiety i teksty
            canvas.create_text(
                x, y-5, text=comp['type'], font=("Arial", 9, "bold"), fill="white", tags=rect_tags)
            canvas.create_text(
                x, y+10, text=comp['label'], font=("Arial", 7), fill="#aaaaaa", tags=rect_tags)

            # Rysowanie małych kropek (pinów) dla wizualizacji portów
            r = 3  # promień pinu
            for key in gate_data:
                if (key.startswith('in_') or key == 'out' or key.startswith('out_')):
                    if isinstance(gate_data[key], dict) and 'x' in gate_data[key]:
                        px, py = gate_data[key]['x'], gate_data[key]['y']
                        canvas.create_oval(
                            px-r, py-r, px+r, py+r, outline="black")
                        
                        if key.startswith('in_'):
                            canvas.create_text(
                                px+r+2, py, text=gate_data[key].get('name', ''), font=("Arial", 7), fill="white")
                        else:
                            canvas.create_text(
                                px-r-2, py, text=gate_data[key].get('name', ''), font=("Arial", 7), fill="white")

    def parse_json(self, json_string, target='main'):
        self.full_data = json.loads(json_string)
        if target == 'main':
            main = self.full_data['main']
        else:
            main = self.full_data['components'][target]

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
            # Stała logiczna ("1" lub "0")
            if src in ('0', '1'):
                const_id = f'const_{src}_{const_counter}'
                const_counter += 1
                components.append(
                    {'id': const_id, 'type': 'INPUT', 'label': src})
                src = const_id
            connections.append((src, dst))
        
        orders = {}
        for key, comp in self.full_data.get('components', {}).items():
            orders[key] = {'INPUT': [], 'OUTPUT': []}
            for elem in comp['elements']:
                if elem['type'] == 'INPUT':
                    orders[key]['INPUT'].append(elem['name'])
                if elem['type'] == 'OUTPUT':
                    orders[key]['OUTPUT'].append(elem['name'])

        return components, connections, orders

    def open_subcomponent(self, comp_type):
        if not hasattr(self, 'full_data') or 'components' not in self.full_data or comp_type not in self.full_data['components']:
            return

        import tkinter as tk
        from logika import get_coordinates

        top = tk.Toplevel(self.root)
        top.title(f"Wnętrze układu: {comp_type}")
        top.geometry("800x600")

        canvas = tk.Canvas(top, bg="#2b2b2b", highlightthickness=1)
        canvas.pack(fill=tk.BOTH, expand=True)

        # Przesuwanie scrollem na nowym oknie
        canvas.bind("<ButtonPress-1>", lambda e: canvas.scan_mark(e.x, e.y))
        canvas.bind("<B1-Motion>",
                    lambda e: canvas.scan_dragto(e.x, e.y, gain=1))

        def _sub_zoom(e):
            delta = e.delta if hasattr(e, 'delta') else (
                1 if getattr(e, 'num', 0) == 4 else -1)
            scale = 1.1 if delta > 0 else 0.9
            canvas.scale("all", e.x, e.y, scale, scale)
            canvas.config(scrollregion=canvas.bbox("all"))
        canvas.bind("<MouseWheel>", _sub_zoom)

        self.COMPONENT_TO_CANVAS[comp_type] = canvas
        self.COMPONENT_TO_RECTID[comp_type] = []

        components, connections, orders = self.parse_json(
            self.jsonString, target=comp_type)
        coords, components, connections = get_coordinates(
            components, connections, orders)

        self.draw_wires(connections, target_canvas=canvas,
                        target_coords=coords)
        self.draw_components(
            components, comp_type, target_canvas=canvas, target_coords=coords)

        canvas.config(scrollregion=canvas.bbox("all"))

        self.start_simulator(comp_type)



    def createCustomComponent(self, target, name):
        if target == 'main':
            component = self.full_data['main']
        else:
            component = self.full_data['components'][target]

        orders = {}
        in_num = {}
        out_num = {}
        for key, comp in self.full_data.get('components', {}).items():
            orders[key] = {'INPUT': {}, 'OUTPUT': {}}
            in_num[key] = 0
            out_num[key] = 0
            for elem in comp['elements']:
                if elem['type'] == 'INPUT':
                    orders[key]['INPUT'][elem['name']] = in_num[key]
                    in_num[key] += 1
                if elem['type'] == 'OUTPUT':
                    orders[key]['OUTPUT'][elem['name']] = out_num[key]
                    out_num[key] += 1
        
        custom = CustomComponent(name)

        gates = {}
        special = {}
        for elem in component['elements']:
            e_type, e_name = elem['type'], elem['name']
            if e_type not in custom.GATE_MAPPING:
                special[e_name] = self.createCustomComponent(e_type, e_name)
                custom.components.append(special[e_name])
            else:
                gates[e_name] = custom.create_component(elem['type'], elem['name'])
        
        dst_counter = {}

        for conn in component['connections']:
            src, dst = str(conn[0]), str(conn[1])

            const_counter = 0
            if src in ('0', '1'):
                const_id = f'const_{src}_{const_counter}'
                const_counter += 1
                gates[const_id] = custom.create_component('INPUT', const_id)
                gates[const_id].set_value(1 if src == '1' else 0)
                src = const_id

            src_id, separator, src_g_name = src.partition('.')
            dst_id, separator, dst_g_name = dst.partition('.')

            if dst_id in special:
                dst_gate = special[dst_id]
                dst_g_type = next((item['type'] for item in component['elements'] if item['name'] == dst_id), None)
                dst_g_num = orders[dst_g_type]['INPUT'][dst_g_name]

                if src_id in special:
                    src_gate = special[src_id]
                    src_g_type = next((item['type'] for item in component['elements'] if item['name'] == src_id), None)
                    src_g_num = orders[src_g_type]['OUTPUT'][src_g_name]

                    dst_gate.inputs[dst_g_num].inputs[0] = src_gate
                    dst_gate.inputs[dst_g_num].prevOutputs[0] = src_g_num
                else:
                    src_gate = gates[src_id]

                    dst_gate.inputs[dst_g_num].inputs[0] = src_gate
            else:
                dst_gate = gates[dst_id]

                if dst_id not in dst_counter:
                    dst_counter[dst_id] = 0

                if src_id in special:
                    src_gate = special[src_id]
                    src_g_type = next((item['type'] for item in component['elements'] if item['name'] == src_id), None)
                    src_g_num = orders[src_g_type]['OUTPUT'][src_g_name]

                    dst_gate.inputs[dst_counter[dst_id]] = src_gate
                    dst_gate.prevOutputs[dst_counter[dst_id]] = src_g_num
                else:
                    src_gate = gates[src_id]

                    dst_gate.inputs[dst_counter[dst_id]] = src_gate
                
                dst_counter[dst_id] += 1

        return custom



    def setupSimulator(self, target='main'):
        self.COMPONENT_TO_SIMULATOR[target] = self.createCustomComponent(target, target)

    def start_simulator(self, comp_type):
        self.setupSimulator(comp_type)
        self.COMPONENT_TO_SIMULATOR[comp_type].evaluate(0)
        for i, val in enumerate(self.COMPONENT_TO_SIMULATOR[comp_type].outputs):
            out_id = self.COMPONENT_TO_RECTID[comp_type][i]
            self.COMPONENT_TO_CANVAS[comp_type].itemconfig(out_id, fill=self.act_comp if val else self.inact_comp)



    def Convert(self):
        self.inputText = self.textbox.get("1.0", tk.END)
        self.jsonString = str(self.passToJava(self.inputText))
        print(self.jsonString)  # print for testing

        components, connections, orders = self.parse_json(self.jsonString)
        self.coords, components, connections = get_coordinates(
            components, connections, orders)
        
        self.COMPONENT_TO_CANVAS = {'main': self.canvas}
        self.COMPONENT_TO_RECTID = {'main': []}
        self.COMPONENT_TO_SIMULATOR = {'main': None}

        self.canvas.delete("all")
        self.draw_wires(connections)
        self.draw_components(components, 'main')
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.start_simulator('main')



    def _pan_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def _pan_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def _zoom(self, event):
        if event.delta > 0:
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        else:
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))



    def click_input(self, comp_type, rect_id, comp_id):
        for input in self.COMPONENT_TO_SIMULATOR[comp_type].inputs:
            if input.name == comp_id:
                input.set_value(0 if input.outputs[0] else 1)
                self.COMPONENT_TO_CANVAS[comp_type].itemconfig(rect_id, fill=self.act_comp if input.outputs[0] else self.inact_comp)

                self.COMPONENT_TO_SIMULATOR[comp_type].evaluate(0)
                print(f"{comp_type} : {self.COMPONENT_TO_SIMULATOR[comp_type].outputs}")

                for i, val in enumerate(self.COMPONENT_TO_SIMULATOR[comp_type].outputs):
                    out_id = self.COMPONENT_TO_RECTID[comp_type][i]
                    self.COMPONENT_TO_CANVAS[comp_type].itemconfig(out_id, fill=self.act_comp if val else self.inact_comp)
                break



    def on_close(self):
        close_app = messagebox.askyesno(
            title="Exit app?", message="Do you really want to exit?")
        if close_app:
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    def tempFunc(str): return str
    app = App(root, tempFunc)
    root.mainloop()
