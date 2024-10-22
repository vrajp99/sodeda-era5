from pathlib import Path
import orjsonl 

class Dataset():
    def __init__(self, deskriptor_set, flow):
        self.deskriptor_set = deskriptor_set
        if isinstance(deskriptor_set,(str,Path)):
            self.deskriptor_set = orjsonl.load(deskriptor_set)
        self.flow = flow

    def __len__(self):
        return len(self.deskriptor_set)
    
    def __getitem__(self, index):
        deskriptor = self.deskriptor_set[index]
        return self.flow(**deskriptor)