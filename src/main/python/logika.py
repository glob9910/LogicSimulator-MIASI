import collections


def get_coordinates(components, connections, orders):
    # 1: Obliczanie poziomów (Ranks)
    ranks = {c['id']: (0 if c['type'] == 'INPUT' else -1) for c in components}

    changed = True
    while changed:
        changed = False
        for c in components:
            if ranks[c['id']] != -1:
                continue

            inputs = [ranks[src.split('.')[0]]
                      for src, dst in connections
                      if dst.split('.')[0] == c['id']
                      and src.split('.')[0] in ranks]
            if inputs and all(r != -1 for r in inputs):
                ranks[c['id']] = max(inputs) + 1
                changed = True

    # Wirtualne bramki dla długich połączeń (Shared Virtual Nodes)
    new_components = components.copy()
    new_connections = []
    virtual_nodes = {} # Key: (source_pin, rank), Value: virtual_id
    added_links = set() # To avoid duplicate segments: (src, dst)

    virtual_counter = 0
    for src, dst in connections:
        src_id = src.split('.')[0]
        dst_id = dst.split('.')[0]

        r_src = ranks.get(src_id, -1)
        r_dst = ranks.get(dst_id, -1)

        if r_src != -1 and r_dst != -1 and r_dst - r_src > 1:
            prev_out = src
            for r in range(r_src + 1, r_dst):
                # Unique key for this trunk: the source pin and the target rank
                v_key = (src, r)
                
                if v_key not in virtual_nodes:
                    v_id = f"v_node_{virtual_counter}"
                    virtual_counter += 1
                    new_components.append({'id': v_id, 'type': 'VIRTUAL', 'label': ''})
                    ranks[v_id] = r
                    virtual_nodes[v_key] = v_id
                
                v_id = virtual_nodes[v_key]
                
                # Add connection segment if not already drawn for this net
                if (prev_out, v_id) not in added_links:
                    new_connections.append((prev_out, v_id, src))
                    added_links.add((prev_out, v_id))
                
                prev_out = v_id

            # Connect the last virtual node to the final destination
            if (prev_out, dst) not in added_links:
                new_connections.append((prev_out, dst, src))
                added_links.add((prev_out, dst))
        else:
            # Short connection or already handled
            if (src, dst) not in added_links:
                new_connections.append((src, dst, src))
                added_links.add((src, dst))

    components = new_components
    connections = new_connections

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

            if c_type == 'VIRTUAL':
                y += 40

            gate_data = {'x': x, 'y': y, 'type': c_type}

            if c_type == 'INPUT':
                gate_data['out'] = {'x': x + 30, 'y': y}
            elif c_type == 'OUTPUT':
                gate_data['in_1'] = {'x': x - 30, 'y': y, 'occupied': False}
            elif c_type == 'NOT':
                gate_data['in_1'] = {'x': x - 30, 'y': y, 'occupied': False}
                gate_data['out'] = {'x': x + 30, 'y': y}
            elif c_type == 'VIRTUAL':
                gate_data['in_1'] = {'x': x, 'y': y, 'occupied': False}
                gate_data['out'] = {'x': x, 'y': y}
            elif c_type == 'SIGNAL':
                gate_data['in_1'] = {'x': x - 30, 'y': y, 'occupied': False}
                gate_data['out'] = {'x': x + 30, 'y': y}
            elif c_type in ('AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR'):
                gate_data['in_1'] = {'x': x - 30,
                                     'y': y - 10, 'occupied': False}
                gate_data['in_2'] = {'x': x - 30,
                                     'y': y + 10, 'occupied': False}
                gate_data['out'] = {'x': x + 30, 'y': y}
            else:
                # Instancja komponentu (np. kaczka) — liczymy piny z connections
                in_pins = []
                out_pins = []
                for conn_data in connections:
                    s, d = conn_data[0], conn_data[1]
                    if '.' in d and d.split('.')[0] == c_id:
                        in_pins.append(d.split('.')[1])
                    if '.' in s and s.split('.')[0] == c_id:
                        out_pins.append(s.split('.')[1])

                num_in = len(in_pins) if in_pins else 2
                num_out = len(out_pins) if out_pins else 1

                c_id_type = next((item['type'] for item in components if item['id'] == c_id), None)

                rect_size = 40
                spacing_in = rect_size / (num_in + 1)
                for j in range(num_in):
                    pin_y = y - rect_size / 2 + (j + 1) * spacing_in
                    in_name = orders[c_id_type]['INPUT'][j] if in_pins else ''
                    gate_data[f'in_{j+1}'] = {'x': x -
                                              30, 'y': pin_y, 'occupied': False, 'name': in_name}

                if num_out == 1:
                    out_name = orders[c_id_type]['OUTPUT'][0] if out_pins else ''
                    gate_data['out'] = {'x': x + 30, 'y': y, 'name': out_name}
                else:
                    spacing_out = rect_size / (num_out + 1)
                    for j in range(num_out):
                        pin_y = y - rect_size / 2 + (j + 1) * spacing_out
                        out_name = orders[c_id_type]['OUTPUT'][j] if out_pins else ''
                        gate_data[f'out_{j+1}'] = {'x': x + 30, 'y': pin_y, 'name': out_name}

            coords[c_id] = gate_data
    return coords, components, connections
