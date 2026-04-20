import tkinter as tk
import re

class CustomCodeEditor(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # 1. Pasek boczny (Canvas)
        self.line_numbers = tk.Canvas(self, width=30, bg="#2b2b2b", highlightthickness=0)
        self.line_numbers.pack(side="left", fill="y")

        # 2. Pasek przewijania (Scrollbar)
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side="right", fill="y")

        # 3. Pole tekstowe (Text)
        self.text_area = tk.Text(self, bg="#2b2b2b", fg="#a9b7c6", 
                                 insertbackground="white", font=("Consolas", 12),
                                 undo=True, wrap="none",
                                 yscrollcommand=self.set_scroll) # Łączymy z funkcją scrollowania
        self.text_area.pack(side="left", fill="both", expand=True)

        # Konfiguracja paska przewijania
        self.scrollbar.config(command=self.sync_scroll)

        # --- KONFIGURACJA TWOICH KOLORÓW ---
        # Tutaj definiujesz tagi (nazwa, kolor)
        self.text_area.tag_configure("component", foreground="#cc7832", font=("Consolas", 12, "bold"))
        self.text_area.tag_configure("signal", foreground="#29B29D", font=("Consolas", 12, "bold"))
        self.text_area.tag_configure("input", foreground="#2BC654", font=("Consolas", 12, "bold"))
        self.text_area.tag_configure("output", foreground="#D43C2B", font=("Consolas", 12, "bold"))
        self.text_area.tag_configure("logic", foreground="#1f38c8")
        self.text_area.tag_configure("strings", foreground="#6a8759")
        self.text_area.tag_configure("comments", foreground="#808080")

        # Twoja mapa: { "reguła_regex": "nazwa_tagu" }
        self.highlight_rules = {
            r'\b(component)\b': "component",
            r'\b(main)\b': "component",
            r'\b(signal)\b': "signal",
            r'\b(input)\b': "input",
            r'\b(output)\b': "output",
            r'\b(not|and|or|xor|nand|nor|xnor)\b': "logic",
            r'(\".*?\"|\'.*?\')': "strings",
            r'#.*': "comments",
        }

        # Synchronizacja zdarzeń
        self.text_area.bind("<Return>", self.auto_indent)
        self.text_area.bind(")", self.handle_closing_bracket)
        self.text_area.bind("}", self.handle_closing_bracket)
        self.text_area.bind("<KeyRelease>", self.on_key_release)
        self.text_area.bind("<MouseWheel>", self.update_line_numbers)
        self.text_area.bind("<Configure>", self.update_line_numbers)

        self.update_line_numbers()

    def auto_indent(self, event):
        # 1. Pobierz tekst z aktualnej linii (przed naciśnięciem Enter)
        line_index = self.text_area.index("insert linestart")
        line_text = self.text_area.get(line_index, "insert")

        # 2. Znajdź białe znaki na początku tej linii
        match = re.match(r'^(\s*)', line_text)
        current_indent = match.group(1) if match else ""

        # 3. Opcjonalnie: zwiększ wcięcie, jeśli linia kończy się na '('
        if line_text.strip().endswith("(") or line_text.strip().endswith("{"):
            current_indent += "    "  # Dodaj 4 spacje (lub "\t")

        # 4. Wstaw nową linię i zachowane wcięcie
        self.text_area.insert("insert", "\n" + current_indent)

        # 5. Odśwież numery linii i podświetlanie
        self.update_line_numbers()
        self.apply_highlighting()

        # 6. Zwróć "break", aby tkinter nie wstawił drugiego (standardowego) Entera
        return "break"
    
    def handle_closing_bracket(self, event):
        # 1. Pobierz tekst linii przed kursorem
        line_start = self.text_area.index("insert linestart")
        line_text = self.text_area.get(line_start, "insert")

        # 2. Jeśli linia składa się tylko z białych znaków (spacji/tabów)
        if line_text.strip() == "" and line_text != "":
            # Usuń ostatnie 4 spacje (standardowe wcięcie)
            indent_size = 4
            if line_text.endswith(" " * indent_size):
                self.text_area.delete(f"insert-{indent_size}c", "insert")
            elif line_text.endswith("\t"):
                self.text_area.delete("insert-1c", "insert")

        # Pozwól tkinterowi wstawić znak ")" normalnie (brak return "break")
        # Ale odświeżymy podświetlanie po chwili
        self.after(10, self.apply_highlighting)

    def on_key_release(self, event=None):
        self.update_line_numbers()
        self.apply_highlighting()

    def apply_highlighting(self):
        # Usuwamy stare podświetlanie przed nałożeniem nowego
        for tag in self.highlight_rules.values():
            self.text_area.tag_remove(tag, "1.0", tk.END)

        content = self.text_area.get("1.0", tk.END)
        
        for pattern, tag in self.highlight_rules.items():
            for match in re.finditer(pattern, content):
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"
                self.text_area.tag_add(tag, start, end)

    def set_scroll(self, *args):
        """Aktualizuje pozycję paska przewijania i odświeża numery linii."""
        self.scrollbar.set(*args)
        self.update_line_numbers()

    def sync_scroll(self, *args):
        """Przewija tekst i odświeża numery linii."""
        self.text_area.yview(*args)
        self.update_line_numbers()

    def update_line_numbers(self, event=None):
        self.line_numbers.delete("all")
        
        i = self.text_area.index("@0,0")
        while True:
            dline = self.text_area.dlineinfo(i)
            if dline is None:
                break
            
            y = dline[1]
            line_num = str(i).split(".")[0]
            
            self.line_numbers.create_text(
                25, y, anchor="ne", text=line_num, 
                fill="#606366", font=("Consolas", 11)
            )
            i = self.text_area.index(f"{i}+1line")