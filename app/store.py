class DataStore:
    def __init__(self):
        self.spectra_data = {}
        self.min_max_norm_data = {}
        self.z_score_norm_data = {}
        self.comparison_matrix = {"samples": [], "matrix": []}
        self.selected_samples = {}
    
    def add(self, name, raw, min_max, z_score):
        self.spectra_data[name] = raw
        self.min_max_norm_data[name] = min_max
        self.z_score_norm_data[name] = z_score

    def delete(self, name):
        self.spectra_data.pop(name, None)
        self.min_max_norm_data.pop(name, None)
        self.z_score_norm_data.pop(name, None)

data = DataStore()