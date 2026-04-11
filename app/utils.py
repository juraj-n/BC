import csv, io, statistics
import numpy as np

def parse_csv(file):
    #TODO: Propper CSV parsing
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline = None)
    reader = csv.DictReader(stream)

    x_values = []
    y_values = []
    
    for row in reader:
        try:
            x_values.append(float(row["wavelength_nm"]))
            y_values.append(float(row["intensity_au"]))
        except:
            continue
    
    return {
        "x": x_values,
        "y": y_values
    }

def min_max_normalize(data): # Min-max normalizácia na interval <0, 1>
    y_values = data["y"]

    if not y_values:
        return data
    
    y_min = min(y_values)
    y_max = max(y_values)

    if y_min == y_max:
        norm_y = [0 for value in y_values]
    else:
        norm_y = [(y - y_min) / (y_max - y_min) for y in y_values]

    return {
        "x": data["x"],
        "y": norm_y
    }

def z_score_normalize(data): # Normalizácia podľa smerodajnej odchýlky
    y_values = data["y"]

    if len(y_values) < 2:
        return data
    
    mean = statistics.mean(y_values)
    stdev = statistics.stdev(y_values)

    if stdev == 0:
        norm_y = [0 for value in y_values]
    else:
        norm_y = [(y - mean) / stdev for y in y_values]
    
    return {
        "x": data["x"],
        "y": norm_y
    }

def l1_normalize(data):
    y_values = data["y"]

    if len(y_values) < 2:
        return data
    
    total_area = sum(abs(y) for y in y_values)

    if total_area == 0:
        norm_y = [0 for value in y_values]
    else:
        norm_y = [y / total_area for y in y_values]

    return {
        "x": data["x"],
        "y": norm_y
    }

def calculate_matrix(spectra, selected, metric_fn, normalization="z_score"):
    matrix = []
    for a in selected:
        row = []
        for b in selected:
            x_a = getattr(spectra[a], normalization)["x"]
            y_a = getattr(spectra[a], normalization)["y"]
            x_b = getattr(spectra[b], normalization)["x"]
            y_b = getattr(spectra[b], normalization)["y"]
            row.append(round(metric_fn(x_a, y_a, x_b, y_b), 3))
        matrix.append(row)

    return matrix

def pearson_coeff(x1, y1, x2, y2):
    y1, y2 =_align(x1, y1, x2, y2)
    
    r = np.corrcoef(y1, y2)[0, 1]
    
    return 0.0 if np.isnan(r) else float(r)

def euclidean_distance(x1, y1, x2, y2):
    y1, y2 = _align(x1, y1, x2, y2)

    return float(np.linalg.norm(y1 - y2))

def cosine_similarity(x1, y1, x2, y2):
    y1, y2 = _align(x1, y1, x2, y2)

    mag1, mag2 = np.linalg.norm(y1), np.linalg.norm(y2)

    if mag1 == 0 or mag2 == 0:
        return 0.0
    
    return float(np.dot(y1, y2) / (mag1 * mag2))

def spectral_angle_mapper(x1, y1, x2, y2):
    cos_sim = cosine_similarity(x1, y1, x2, y2)
    return float(np.arccos(np.clip(cos_sim, -1.0, 1.0)))

def _align(x1, y1, x2, y2):
    x1, y1 = np.asarray(x1, dtype=float), np.asarray(y1, dtype=float)
    x2, y2 = np.asarray(x2, dtype=float), np.asarray(y2, dtype=float)

    min_wavelen = max(x1[0], x2[0])
    max_wavelen = min(x1[-1], x2[-1])
    n_points = max(len(x1), len(x2))

    x_common = np.linspace(min_wavelen, max_wavelen, n_points)

    return np.interp(x_common, x1, y1), np.interp(x_common, x2, y2)