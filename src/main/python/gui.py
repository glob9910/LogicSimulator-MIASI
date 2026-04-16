import tkinter as tk
from tkinter import messagebox
from logika import get_coordinates
from simulator import CustomComponent
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


        self.labelTxt = tk.Label(self.mainWindow, text="Logic text", font=('Arial', 18))
        self.labelTxt.grid(row=0, column=0, pady=20)

        self.labelSim = tk.Label(self.mainWindow, text="Logic Sim:\nmain", font=('Arial', 18))
        self.labelSim.grid(row=0, column=2, pady=20)

        self.textbox = tk.Text(self.mainWindow, font=('Arial', 12), bg="#2b2b2b", fg="#FFFFFF")
        self.textbox.grid(row=1, column=0, padx=20, sticky=tk.NSEW)

        self.button = tk.Button(self.mainWindow, text="Convert", font=('Arial', 16), command=self.Convert)
        self.button.grid(row=0, column=1, padx=10, pady=10)

        self.backButton = tk.Button(self.mainWindow, text="Back", font=('Arial', 16), command=self.BackToMain)

        self.inputText = ""
        

        # self.canvas = tk.Canvas(root, width=800, height=500, bg="#2b2b2b")
        # self.canvas.pack(fill="both", expand=True)

        # Zmieniony kod Maćka aby działał z kodem Aleksandra
        self.inpColor = "#3c3f41"
        self.actColor = "#ffff00"
        self.wire0Col = "#00ffcc"
        self.wire1Col = "#ffff00"
        self.canvas = tk.Canvas(self.mainWindow, bg="#2b2b2b", highlightthickness=1)
        self.canvas.grid(row=1, column=2, padx=20, sticky=tk.NSEW)

        # Przesuwanie canvasu myszką (przeciąganie lewym przyciskiem)
        self.canvas.bind("<ButtonPress-1>", self._pan_start)
        self.canvas.bind("<B1-Motion>", self._pan_move)
        # Zoom scrollem
        self.canvas.bind("<MouseWheel>", self._zoom)

        self.jsonString = ""

        # Kod Maćka — canvas startuje pusty, rysowanie po Convert()
        self.strCurrentComp = "main"
        self.COM_AND_CON_COORDS = {}

        # Symulator
        self.ID_TO_CANVID = {}
        self.CANVID_TO_ID = {}
        self.currentComponent : CustomComponent = None
        self.outputRects = []



    def draw_wires(self, connections, coords):
        for src, dst in connections:
            src_id = src.split('.')[0]
            dst_id = dst.split('.')[0]

            # Punkt startowy 
            src_gate = coords[src_id]
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

            # Punkt docelowy 
            dst_gate = coords[dst_id]
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
                fill=self.wire0Col, 
                width=2
            )

    def draw_components(self, components, coords):
        self.outputRects = []
        for comp in components:
            c_id = comp['id']
            gate_data = coords[c_id]
            x, y = gate_data['x'], gate_data['y']
            
            # Prostokąt reprezentujący bramkę
            rectId = self.canvas.create_rectangle(x - 30, y - 20, x + 30, y + 20, 
                                         fill=self.inpColor, outline="#5e6266", width=2, tags=(comp['type'], "__component__"))
            
            self.ID_TO_CANVID[c_id] = rectId
            self.CANVID_TO_ID[rectId] = c_id

            if comp['type'] == "OUTPUT":
                self.outputRects.append(rectId)
            
            # Etykiety i teksty
            self.canvas.create_text(x, y-5, text=comp['type'], font=("Arial", 9, "bold"), fill="white", tags=comp['type'])
            self.canvas.create_text(x, y+10, text=comp['label'], font=("Arial", 7), fill="#aaaaaa", tags=comp['type'])
            
            # Rysowanie małych kropek (pinów) dla wizualizacji portów
            r = 3 # promień pinu
            for key in gate_data:
                if (key.startswith('in_') or key == 'out' or key.startswith('out_')):
                    if isinstance(gate_data[key], dict) and 'x' in gate_data[key]:
                        px, py = gate_data[key]['x'], gate_data[key]['y']
                        self.canvas.create_oval(px-r, py-r, px+r, py+r, outline="black")
    


    def setup_inner_component(self, name):
        components, connections, coords = self.COM_AND_CON_COORDS[name]

        gateComp = CustomComponent(self.strCurrentComp, lambda a: None)

        gates = {}
        special = {}
        for comp in components:
            c_id = comp['id']
            if comp['type'] in gateComp.GATE_MAPPING.keys():
                gates[c_id] = gateComp.create_component(comp['type'], c_id, lambda a: None)
            else:
                gates[c_id] = self.setup_inner_component(comp['type'])
                special[c_id] = gates[c_id]

        inputCounter = {}
        for src, dst in connections:
            src_id = src.split('.')[0]
            dst_id = dst.split('.')[0]

            if dst_id in special:
                if dst_id not in inputCounter:
                    inputCounter[dst_id] = 0

                special[dst_id].inputs[inputCounter[dst_id]].inputs.append(gates[src_id])
                inputCounter[dst_id] += 1
            else:
                gates[dst_id].inputs.append(gates[src_id])


            src_gate = coords[src_id]
            for key in sorted(src_gate.keys()):
                if key == 'out' and isinstance(src_gate[key], dict):
                    gates[dst_id].prevOutputs.append(0)
                    break
                elif key.startswith('out_') and isinstance(src_gate[key], dict):
                    gates[dst_id].prevOutputs.append(int(key.split('_')[1]))
                    break

        return gateComp

    def setup_simulation(self):
        self.currentComponent = None
        components, connections, coords = self.COM_AND_CON_COORDS[self.strCurrentComp]

        gateComp = CustomComponent(self.strCurrentComp, lambda a: None)

        gates = {}
        special = {}
        for comp in components:
            c_id = comp['id']
            if comp['type'] in gateComp.GATE_MAPPING.keys():
                gates[c_id] = gateComp.create_component(comp['type'], c_id, lambda a: None)
            else:
                gates[c_id] = self.setup_inner_component(comp['type'])
                special[c_id] = gates[c_id]

        inputCounter = {}
        for src, dst in connections:
            src_id = src.split('.')[0]
            dst_id = dst.split('.')[0]

            if dst_id in special:
                if dst_id not in inputCounter:
                    inputCounter[dst_id] = 0

                special[dst_id].inputs[inputCounter[dst_id]].inputs.append(gates[src_id])
                inputCounter[dst_id] += 1
            else:
                gates[dst_id].inputs.append(gates[src_id])


            src_gate = coords[src_id]
            for key in sorted(src_gate.keys()):
                if key == 'out' and isinstance(src_gate[key], dict):
                    gates[dst_id].prevOutputs.append(0)
                    break
                elif key.startswith('out_') and isinstance(src_gate[key], dict):
                    gates[dst_id].prevOutputs.append(int(key.split('_')[1]))
                    break
                

        self.currentComponent = gateComp

        outputs = self.currentComponent.evaluate()
        print(outputs)

        for i, out in enumerate(outputs):
            if out:
                self.canvas.itemconfig(self.outputRects[i], fill=self.actColor)
            else:
                self.canvas.itemconfig(self.outputRects[i], fill=self.inpColor)




    def parse_json(self, json_string):
        data = json.loads(json_string)

        # Other components
        otherComponents = data['components']
        for compName in otherComponents:
            element = otherComponents[compName]

            components = []
            for elem in element['elements']:
                components.append({
                    'id': elem['name'],
                    'type': elem['type'],
                    'label': elem['name']
                })

            connections = []
            const_counter = 0
            for conn in element['connections']:
                src, dst = str(conn[0]), str(conn[1])
                # Stała logiczna
                if src in ('0', '1'):
                    const_id = f'const_{src}_{const_counter}'
                    const_counter += 1
                    components.append({'id': const_id, 'type': 'INPUT', 'label': src})
                    src = const_id
                connections.append((src, dst))

            coords = get_coordinates(components, connections)
            self.COM_AND_CON_COORDS[compName] = (components, connections, coords)

        # Main component
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
            # Stała logiczna
            if src in ('0', '1'):
                const_id = f'const_{src}_{const_counter}'
                const_counter += 1
                components.append({'id': const_id, 'type': 'INPUT', 'label': src})
                src = const_id
            connections.append((src, dst))

        coords = get_coordinates(components, connections)
        self.COM_AND_CON_COORDS['main'] = (components, connections, coords)

            

    def Convert(self):
        self.inputText = self.textbox.get("1.0", tk.END)
        self.jsonString = str(self.passToJava(self.inputText))
        #print(self.jsonString)  # print for testing

        self.parse_json(self.jsonString)

        self.backButton.grid_forget()

        self.canvas.delete("all")
        self.draw_wires(self.COM_AND_CON_COORDS['main'][1], self.COM_AND_CON_COORDS['main'][2])
        self.draw_components(self.COM_AND_CON_COORDS['main'][0], self.COM_AND_CON_COORDS['main'][2])
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.canvas.tag_bind("INPUT", "<Button-1>", self._click_input)
        for compName in self.COM_AND_CON_COORDS:
            if compName != "main":
                self.canvas.tag_bind(compName, "<Button-1>", lambda e, n=compName: self._click_component(e, n))

        self.strCurrentComp = "main"
        self.setup_simulation()

    def BackToMain(self):
        self.Convert()
        self.labelSim['text'] = "Logic Sim:\nmain"



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



    def _click_input(self, event):
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        items = self.canvas.find_overlapping(x, y, x, y)

        item = next((i for i in items if "__component__" in self.canvas.gettags(i)), None)

        if item:
            color = self.canvas.itemcget(item, "fill")
            val = 1 if color != self.actColor else 0
            self.canvas.itemconfig(item, fill=self.actColor if color != self.actColor else self.inpColor)

            for inp in self.currentComponent.inputs:
                if inp.name == self.CANVID_TO_ID[item]:
                    inp.set_value(val)

            outputs = self.currentComponent.evaluate()
            print(outputs)

            for i, out in enumerate(outputs):
                if out:
                    self.canvas.itemconfig(self.outputRects[i], fill=self.actColor)
                else:
                    self.canvas.itemconfig(self.outputRects[i], fill=self.inpColor)
                    
            

    def _click_component(self, event, compName):
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        items = self.canvas.find_overlapping(x, y, x, y)

        item = next((i for i in items if "__component__" in self.canvas.gettags(i)), None)

        if item:
            self.canvas.delete("all")
            self.draw_wires(self.COM_AND_CON_COORDS[compName][1], self.COM_AND_CON_COORDS[compName][2])
            self.draw_components(self.COM_AND_CON_COORDS[compName][0], self.COM_AND_CON_COORDS[compName][2])
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

            self.backButton.grid(row=1, column=1, padx=10, pady=10, sticky=tk.N)

            self.canvas.tag_bind("INPUT", "<Button-1>", self._click_input)
            for _compName in self.COM_AND_CON_COORDS:
                if _compName != "main":
                    self.canvas.tag_bind(_compName, "<Button-1>", lambda e, n=_compName: self._click_component(e, n))
            
            self.labelSim['text'] = f"Logic Sim:\n{compName}"

            self.strCurrentComp = compName
            self.setup_simulation()



    def on_close(self):
        close_app = messagebox.askyesno(title="Exit app?", message="Do you really want to exit?")
        if close_app:
            self.root.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    tempFunc = lambda str: str
    app = App(root, tempFunc)
    root.mainloop()
