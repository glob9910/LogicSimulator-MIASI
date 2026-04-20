class LogicComponent:
    def __init__(self, name, canvFunc):
        self.name = name
        self.canvFunc = canvFunc
        self.inputs = []  # Tu będą podłączone inne komponenty
        self.prevOutputs = []
        self.outputs = []   # Cache wyniku

    def evaluate(self, out_num):
        # Ta metoda zostanie nadpisana w konkretnych klasach
        raise NotImplementedError



class Input(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.inputs = [None,]
        self.prevOutputs = [0,]
        self.outputs = [False,]
    def set_value(self, val):
        self.outputs[0] = True if val else False
        self.canvFunc(self.outputs[0])
    def evaluate(self, out_num):
        if self.inputs[0] is not None:
            self.outputs[0] = self.inputs[0].evaluate(self.prevOutputs[0])
        return self.outputs[out_num]
    
class Output(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.inputs = [None,]
        self.prevOutputs = [0,]
        self.outputs = [False,]
    def evaluate(self, out_num):
        self.outputs[0] = self.inputs[0].evaluate(self.prevOutputs[0])
        self.canvFunc(self.outputs[0])
        return self.outputs[out_num]
    
class Virtual(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.inputs = [None,]
        self.prevOutputs = [0,]
        self.outputs = [False,]
    def evaluate(self, out_num):
        self.outputs[0] = self.inputs[0].evaluate(self.prevOutputs[0])
        self.canvFunc(self.outputs[0])
        return self.outputs[out_num]
    
class Signal(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.inputs = [None,]
        self.prevOutputs = [0,]
        self.outputs = [False,]
    def evaluate(self, out_num):
        self.outputs[0] = self.inputs[0].evaluate(self.prevOutputs[0])
        self.canvFunc(self.outputs[0])
        return self.outputs[out_num]

class NotGate(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.inputs = [None,]
        self.prevOutputs = [0,]
        self.outputs = [True,]
    def evaluate(self, out_num):
        val = self.inputs[0].evaluate(self.prevOutputs[0])
        self.outputs[0] = not val
        self.canvFunc(self.outputs[0])
        return self.outputs[out_num]

class AndGate(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.inputs = [None, None]
        self.prevOutputs = [0, 0]
        self.outputs = [False,]
    def evaluate(self, out_num):
        val1 = self.inputs[0].evaluate(self.prevOutputs[0])
        val2 = self.inputs[1].evaluate(self.prevOutputs[1])
        self.outputs[0] = val1 and val2
        self.canvFunc(self.outputs[0])
        return self.outputs[out_num]

class OrGate(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.inputs = [None, None]
        self.prevOutputs = [0, 0]
        self.outputs = [False,]
    def evaluate(self, out_num):
        val1 = self.inputs[0].evaluate(self.prevOutputs[0])
        val2 = self.inputs[1].evaluate(self.prevOutputs[1])
        self.outputs[0] = val1 or val2
        self.canvFunc(self.outputs[0])
        return self.outputs[out_num]
    
class XorGate(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.inputs = [None, None]
        self.prevOutputs = [0, 0]
        self.outputs = [False,]
    def evaluate(self, out_num):
        val1 = self.inputs[0].evaluate(self.prevOutputs[0])
        val2 = self.inputs[1].evaluate(self.prevOutputs[1])
        self.outputs[0] = val1 != val2
        self.canvFunc(self.outputs[0])
        return self.outputs[out_num]
    
class NandGate(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.inputs = [None, None]
        self.prevOutputs = [0, 0]
        self.outputs = [True,]
    def evaluate(self, out_num):
        val1 = self.inputs[0].evaluate(self.prevOutputs[0])
        val2 = self.inputs[1].evaluate(self.prevOutputs[1])
        self.outputs[0] = not (val1 and val2)
        self.canvFunc(self.outputs[0])
        return self.outputs[out_num]

class NorGate(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.inputs = [None, None]
        self.prevOutputs = [0, 0]
        self.outputs = [True,]
    def evaluate(self, out_num):
        val1 = self.inputs[0].evaluate(self.prevOutputs[0])
        val2 = self.inputs[1].evaluate(self.prevOutputs[1])
        self.outputs[0] = not (val1 or val2)
        self.canvFunc(self.outputs[0])
        return self.outputs[out_num]
    
class XnorGate(LogicComponent):
    def __init__(self, name, canvFunc):
        super().__init__(name, canvFunc)
        self.inputs = [None, None]
        self.prevOutputs = [0, 0]
        self.outputs = [True,]
    def evaluate(self, out_num):
        val1 = self.inputs[0].evaluate(self.prevOutputs[0])
        val2 = self.inputs[1].evaluate(self.prevOutputs[1])
        self.outputs[0] = val1 == val2
        self.canvFunc(self.outputs[0])
        return self.outputs[out_num]



class CustomComponent(LogicComponent):
    def __init__(self, name, canvFunc=lambda a: None):
        super().__init__(name, canvFunc)

        self.GATE_MAPPING = {
            "INPUT": Input,
            "OUTPUT": Output,
            "VIRTUAL": Virtual,
            "SIGNAL": Signal,
            "NOT": NotGate,
            "AND": AndGate,
            "OR": OrGate,
            "XOR": XorGate,
            "NAND": NandGate,
            "NOR": NorGate,
            "XNOR": XnorGate,
        }

        self.components = []
        self.compOutputs = []

    def create_component(self, type_name, name, canvFunc=lambda a: None):
        cls = self.GATE_MAPPING.get(type_name)
        if cls:
            comp = cls(name, canvFunc)
            if type_name == "INPUT":
                self.inputs.append(comp)
                self.prevOutputs.append(0)
            elif type_name == "OUTPUT":
                self.compOutputs.append(comp)
                self.outputs.append(False)
            else:
                self.components.append(comp)
            return comp
        else:
            print(f"Nieznany typ bramki: {type_name}")
            return None

    def evaluate(self, out_num):
        for i, out in enumerate(self.compOutputs):
            self.outputs[i] = out.evaluate(0)
        return self.outputs[out_num]
