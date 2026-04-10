class SpectrumData:
    def __init__(self, raw, min_max, z_score, l1):
        self.raw = raw
        self.min_max = min_max
        self.z_score = z_score
        self.l1 = l1

class ComparisonData:
    def __init__(self):
        self.samples = []
        self.metrics = {}

class DataStore:
    def __init__(self):
        self.spectra = {}
        self.comparison = None
    
    def add(self, name, raw, min_max, z_score, l1):
        self.spectra[name] = SpectrumData(raw, min_max, z_score, l1)
        self.comparison = None

    def delete(self, name):
        self.spectra.pop(name, None)
        self.comparison = None

data = DataStore()