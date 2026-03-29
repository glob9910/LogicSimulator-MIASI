import collections

def get_coordinates(components, connections):
    # 1: Obliczanie poziomów (Ranks)
    ranks = {c['id']: (0 if c['type'] == 'INPUT' else -1) for c in components}
    
    changed = True
    while changed:
        changed = False
        for c in components:
            if ranks[c['id']] != -1: continue
            
            inputs = [ranks[src.split('.')[0]]
                      for src, dst in connections
                      if dst.split('.')[0] == c['id']
                      and src.split('.')[0] in ranks]
            if inputs and all(r != -1 for r in inputs):
                ranks[c['id']] = max(inputs) + 1
                changed = True

    # 2: Grupowanie w warstwy
    layers = collections.defaultdict(list)
    for c_id, rank in ranks.items():
        layers[rank].append(c_id)

    # 3: Przeliczanie na piksele i tworzenie Portów (Pinów)
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
            elif c_type == 'SIGNAL':
                gate_data['in_1'] = {'x': x - 30, 'y': y, 'occupied': False}
                gate_data['out']  = {'x': x + 30, 'y': y}
            elif c_type in ('AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR'):
                gate_data['in_1'] = {'x': x - 30, 'y': y - 10, 'occupied': False}
                gate_data['in_2'] = {'x': x - 30, 'y': y + 10, 'occupied': False}
                gate_data['out']  = {'x': x + 30, 'y': y}
            else:
                # Instancja komponentu (np. kaczka) — liczymy piny z connections
                in_pins = set()
                out_pins = set()
                for s, d in connections:
                    if '.' in d and d.split('.')[0] == c_id:
                        in_pins.add(d.split('.')[1])
                    if '.' in s and s.split('.')[0] == c_id:
                        out_pins.add(s.split('.')[1])

                num_in = len(in_pins) if in_pins else 2
                num_out = len(out_pins) if out_pins else 1

                spacing = 20
                total_in = (num_in - 1) * spacing
                for j in range(num_in):
                    pin_y = y - total_in / 2 + j * spacing
                    gate_data[f'in_{j+1}'] = {'x': x - 30, 'y': pin_y, 'occupied': False}

                if num_out == 1:
                    gate_data['out'] = {'x': x + 30, 'y': y}
                else:
                    total_out = (num_out - 1) * spacing
                    for j in range(num_out):
                        pin_y = y - total_out / 2 + j * spacing
                        gate_data[f'out_{j+1}'] = {'x': x + 30, 'y': pin_y}

            coords[c_id] = gate_data
            
    return coords
