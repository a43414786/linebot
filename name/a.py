import pickle
import os
class name:
    def __init__(self):
        self.name = []
    def load(self):
        dirs = os.listdir("D:/linebot/name")
        if "name.pickle" in dirs:
            with open("D:/linebot/name/name.pickle","rb") as f:
                self.name = pickle.load(f)
    def dump(self):
        with open("D:/linebot/name/name.pickle","wb") as f:
            pickle.dump(self.name,f)
a=name()
a.load()
print(a.name)
import time
a = time.strftime("%Y%m%d", time.localtime())
print(a)