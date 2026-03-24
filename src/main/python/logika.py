import collections

# --- 1. DANE WEJŚCIOWE ---
components = [
    {'id': 'I1', 'type': 'INPUT', 'label': 'A'},
    {'id': 'I2', 'type': 'INPUT', 'label': 'B'},
    {'id': 'I3', 'type': 'INPUT', 'label': 'C'},
    {'id': 'G1', 'type': 'AND', 'label': 'AND_1'},
    {'id': 'G2', 'type': 'OR', 'label': 'OR_1'},
    {'id': 'G3', 'type': 'NOT', 'label': 'NOT_1'},
    {'id': 'O1', 'type': 'OUTPUT', 'label': 'OUT_1'}
]

connections = [
    ('I1', 'G1'),
    ('I2', 'G1'),
    ('G1', 'G2'),
    ('I3', 'G3'),
    ('G3', 'G2'),
    ('G2', 'O1')
]

def get_coordinates(components, connections):
    # Faza 1: Obliczanie poziomów (Ranks)
    ranks = {c['id']: (0 if c['type'] == 'INPUT' else -1) for c in components}
    
    changed = True
    while changed:
        changed = False
        for c in components:
            if ranks[c['id']] != -1: continue
            
            inputs = [ranks[src] for src, dst in connections if dst == c['id']]
            if inputs and all(r != -1 for r in inputs):
                ranks[c['id']] = max(inputs) + 1
                changed = True

    # Faza 2: Grupowanie w warstwy
    layers = collections.defaultdict(list)
    for c_id, rank in ranks.items():
        layers[rank].append(c_id)

    # Faza 3: Przeliczanie na piksele i tworzenie Portów (Pinów)
    coords = {}
    x_spacing, y_spacing = 150, 80
    comp_types = {c['id']: c['type'] for c in components}

    for rank, ids in layers.items():
        start_y = 100
        for i, c_id in enumerate(ids):
            x = 100 + rank * x_spacing
            y = start_y + i * y_spacing
            c_type = comp_types[c_id]
            
            gate_data = {'x': x, 'y': y, 'type': c_type}
            
            if c_type == 'INPUT':
                gate_data['out'] = {'x': x + 30, 'y': y}
            elif c_type == 'OUTPUT':
                gate_data['in_1'] = {'x': x - 30, 'y': y, 'occupied': False}
            elif c_type == 'NOT':
                gate_data['in_1'] = {'x': x - 30, 'y': y, 'occupied': False}
                gate_data['out']  = {'x': x + 30, 'y': y}
            else: # AND, OR, XOR...
                gate_data['in_1'] = {'x': x - 30, 'y': y - 10, 'occupied': False}
                gate_data['in_2'] = {'x': x - 30, 'y': y + 10, 'occupied': False}
                gate_data['out']  = {'x': x + 30, 'y': y}

            coords[c_id] = gate_data
            
    return coords
