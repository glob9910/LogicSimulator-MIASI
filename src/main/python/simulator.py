class LogicComponent:
    def __init__(self, name, canvFunc):
        self.name = name
        self.canvFunc = canvFunc
        self.inputs = []  # Tu będą podłączone inne komponenty
        self.prevOutputs = []
        self.outputs = []   # Cache wyniku

    def evaluate(self):
        # Ta metoda zostanie nadpisana w konkretnych klasach
        raise NotImplementedError



class Input(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.outputs = [0,]
    def set_value(self, val):
        self.outputs[0] = True if val else False
        self.canvFunc(self.outputs[0])
    def evaluate(self):
        if len(self.inputs) != 0 and len(self.prevOutputs) != 0:
            self.outputs[0] = self.inputs[0].evaluate()[self.prevOutputs[0]]
        return self.outputs
    
class Output(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.outputs = [0,]
    def evaluate(self):
        self.outputs[0] = self.inputs[0].evaluate()[self.prevOutputs[0]]
        self.canvFunc(self.outputs[0])
        return self.outputs
    
class Wire(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.outputs = [0,]
    def evaluate(self):
        self.outputs[0] = self.inputs[0].evaluate()[self.prevOutputs[0]]
        self.canvFunc(self.outputs[0])
        return self.outputs
    
class Signal(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.outputs = [0,]
    def evaluate(self):
        self.outputs[0] = self.inputs[0].evaluate()[self.prevOutputs[0]]
        self.canvFunc(self.outputs[0])
        return self.outputs

class NotGate(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.outputs = [0,]
    def evaluate(self):
        val = self.inputs[0].evaluate()[self.prevOutputs[0]]
        self.outputs[0] = not val
        self.canvFunc(self.outputs[0])
        return self.outputs

class AndGate(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.outputs = [0,]
    def evaluate(self):
        val1 = self.inputs[0].evaluate()[self.prevOutputs[0]]
        val2 = self.inputs[1].evaluate()[self.prevOutputs[1]]
        self.outputs[0] = val1 and val2
        self.canvFunc(self.outputs[0])
        return self.outputs

class OrGate(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.outputs = [0,]
    def evaluate(self):
        val1 = self.inputs[0].evaluate()[self.prevOutputs[0]]
        val2 = self.inputs[1].evaluate()[self.prevOutputs[1]]
        self.outputs[0] = val1 or val2
        self.canvFunc(self.outputs[0])
        return self.outputs
    
class XorGate(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.outputs = [0,]
    def evaluate(self):
        val1 = self.inputs[0].evaluate()[self.prevOutputs[0]]
        val2 = self.inputs[1].evaluate()[self.prevOutputs[1]]
        self.outputs[0] = val1 != val2
        self.canvFunc(self.outputs[0])
        return self.outputs
    
class NandGate(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.outputs = [0,]
    def evaluate(self):
        val1 = self.inputs[0].evaluate()[self.prevOutputs[0]]
        val2 = self.inputs[1].evaluate()[self.prevOutputs[1]]
        self.outputs[0] = not (val1 and val2)
        self.canvFunc(self.outputs[0])
        return self.outputs

class NorGate(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.outputs = [0,]
    def evaluate(self):
        val1 = self.inputs[0].evaluate()[self.prevOutputs[0]]
        val2 = self.inputs[1].evaluate()[self.prevOutputs[1]]
        self.outputs[0] = not (val1 or val2)
        self.canvFunc(self.outputs[0])
        return self.outputs
    
class XnorGate(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.outputs = [0,]
    def evaluate(self):
        val1 = self.inputs[0].evaluate()[self.prevOutputs[0]]
        val2 = self.inputs[1].evaluate()[self.prevOutputs[1]]
        self.outputs[0] = val1 == val2
        self.canvFunc(self.outputs[0])
        return self.outputs



class CustomComponent(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)

        self.GATE_MAPPING = {
            "INPUT": Input,
            "OUTPUT": Output,
            "WIRE": Wire,
            "SIGNAL": Signal,
            "NOT": NotGate,
            "AND": AndGate,
            "OR": OrGate,
            "XOR": XorGate,
            "NAND": NandGate,
            "NOR": NorGate,
            "XNOR": XnorGate,
            "CUSTOM": CustomComponent,
        }

        self.components = []
        self.compOutputs = []

    def create_component(self, type_name, name, canvFunc):
        cls = self.GATE_MAPPING.get(type_name)
        if cls:
            comp = cls(name, canvFunc)
            if type_name == "INPUT":
                self.inputs.append(comp)
            elif type_name == "OUTPUT":
                self.compOutputs.append(comp)
                self.outputs.append(0)
            else:
                self.components.append(comp)
            return comp
        else:
            print(f"Nieznany typ bramki: {type_name}")
            return None

    def evaluate(self):
        for i, out in enumerate(self.compOutputs):
            self.outputs[i] = out.evaluate()[0]
        return self.outputs