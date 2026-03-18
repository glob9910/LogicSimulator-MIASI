import jpype

jpype.startJVM(classpath=['target/LogicSimulator-1.0-SNAPSHOT.jar'])

MyClass = jpype.JClass("MyClass")
result = MyClass.getMessage()

print(result)

jpype.shutdownJVM()