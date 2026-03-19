import jpype

jpype.startJVM(classpath=['target/LogicSimulator-1.0-SNAPSHOT.jar'])

API = jpype.JClass("pl.pwr.miasi.API")
result = API.getMessage()

print(result)

jpype.shutdownJVM()