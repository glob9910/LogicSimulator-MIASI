import tkinter as tk
from gui import App
import jpype



if __name__ == "__main__":
    jpype.startJVM(classpath=['target/LogicSimulator-1.0-SNAPSHOT-jar-with-dependencies.jar'])

    API = jpype.JClass("pl.pwr.miasi.API")


    root = tk.Tk()
    app = App(root, API.parse)
    root.mainloop()


    jpype.shutdownJVM()