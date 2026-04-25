import csv, io, statistics
import numpy as np

ZONES = [
    {"name": "Z1", "x0": 250, "x1": 300},
    {"name": "Z2", "x0": 300, "x1": 325},
    {"name": "Z3", "x0": 325, "x1": 345},
    {"name": "Z4", "x0": 345, "x1": 380},
    {"name": "Z5", "x0": 380, "x1": 410},
    {"name": "Z6", "x0": 410, "x1": 450},
    {"name": "Z7", "x0": 450, "x1": 500},
    {"name": "Z8", "x0": 500, "x1": 550},
]

def parse_sp(file):
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)

    x_values = []
    y_values = []
    in_data_section = False

    for line in stream:
        line = line.strip()
        
        if line == "#DATA":
            in_data_section = True
            continue
        
        if not in_data_section:
            continue

        try:
            parts = line.split("\t")
            x_values.append(float(parts[0]))
            y_values.append(float(parts[1]))
        except (ValueError, IndexError):
            continue

    return {
        "x": x_values,
        "y": y_values
    }

def parse_csv(file):
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    reader = csv.reader(stream, delimiter=";")
    next(reader, None) #Skips "header" row

    x_values = []
    y_values = []

    for row in reader:
        try:
            x_raw = row[14].replace(",", ".").strip()
            y_raw = row[15].replace(",", ".").strip()

            if not x_raw or not y_raw:
                continue

            x = float(x_raw)
            y = float(y_raw)
        except(ValueError, IndexError):
            continue

        x_values.append(x)
        y_values.append(y)

    if not x_values or not y_values:
        return None

    return {
        "x": x_values,
        "y": y_values
    }

def min_max_normalize(data):
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

def z_score_normalize(data):
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
    x_values = np.asarray(data["x"], dtype=float)
    y_values = np.asarray(data["y"], dtype=float)

    if len(y_values) < 2:
        return data

    total_area = np.trapezoid(np.abs(y_values), x_values)

    if total_area == 0:
        norm_y = np.zeros_like(y_values)
    else:
        norm_y = y_values / total_area

    return {
        "x": data["x"],
        "y": norm_y.tolist()
    }

def calculate_matrix(spectra, selected, metric_fn, normalization="z_score"):
    n = len(selected)
    matrix = [[None] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i, n):
            a, b = selected[i], selected[j]
            x_a = getattr(spectra[a], normalization)["x"]
            y_a = getattr(spectra[a], normalization)["y"]
            x_b = getattr(spectra[b], normalization)["x"]
            y_b = getattr(spectra[b], normalization)["y"]
            
            value = round(metric_fn(x_a, y_a, x_b, y_b), 3)
            matrix[i][j] = value
            matrix[j][i] = value

    return matrix

def area_difference(x1, y1, x2, y2):
    x_aligned, y1, y2 = align(x1, y1, x2, y2)

    area1 = np.trapezoid(y1, x_aligned)
    area2 = np.trapezoid(y2, x_aligned)

    return abs(float(area1 - area2) * 100)

def pearson_coeff(x1, y1, x2, y2):
    _, y1, y2 = align(x1, y1, x2, y2)
    
    r = np.corrcoef(y1, y2)[0, 1]
    
    return 0.0 if np.isnan(r) else float(r)

def euclidean_distance(x1, y1, x2, y2):
    _, y1, y2 = align(x1, y1, x2, y2)

    return float(np.linalg.norm(y1 - y2))

def cosine_similarity(x1, y1, x2, y2):
    _, y1, y2 = align(x1, y1, x2, y2)

    mag1, mag2 = np.linalg.norm(y1), np.linalg.norm(y2)

    if mag1 == 0 or mag2 == 0:
        return 0.0
    
    return float(np.dot(y1, y2) / (mag1 * mag2))

def spectral_angle_mapper(x1, y1, x2, y2):
    cos_sim = cosine_similarity(x1, y1, x2, y2)
    return float(np.arccos(np.clip(cos_sim, -1.0, 1.0)))

def align(x1, y1, x2, y2):
    x1, y1 = np.asarray(x1, dtype=float), np.asarray(y1, dtype=float)
    x2, y2 = np.asarray(x2, dtype=float), np.asarray(y2, dtype=float)

    min_wavelen = max(x1[0], x2[0])
    max_wavelen = min(x1[-1], x2[-1])
    n_points = max(len(x1), len(x2))

    x_common = np.linspace(min_wavelen, max_wavelen, n_points)

    return x_common, np.interp(x_common, x1, y1), np.interp(x_common, x2, y2)

def create_residual(l1, name_a, name_b):
    x_common, y_a_aligned, y_b_aligned = align(
        l1[name_a]["x"], l1[name_a]["y"],
        l1[name_b]["x"], l1[name_b]["y"]
    )
    return {
        "Rozdiel": {
            "x": x_common.tolist(),
            "y": (y_a_aligned - y_b_aligned).tolist(),
            "color": "red",
            "dash": "dash",
            "width": 3
        },
        name_a: l1[name_a],
        name_b: l1[name_b]
    }

def split_by_zones(data):
    x = np.array(data["x"])
    y = np.array(data["y"])

    result = {}
    for zone in ZONES:
        mask = (x >= zone["x0"]) & (x < zone["x1"])
        result[zone["name"]] = {
            "x": x[mask],
            "y": y[mask]
        }
    return result

def zones_coeffs(z_score, l1, min_max, name_a, name_b):
    l1_zones_a = split_by_zones(l1[name_a])
    l1_zones_b = split_by_zones(l1[name_b])

    results = []
    for zone_name in l1_zones_a:    
        l_a = l1_zones_a[zone_name]
        l_b = l1_zones_b[zone_name]

        s = spectral_angle_mapper(l_a["x"], l_a["y"], l_b["x"], l_b["y"])
        area_dif = area_difference(l_a["x"], l_a["y"], l_b["x"], l_b["y"])

        results.append({
            "name": zone_name,
            "sam": s,
            "area_dif": area_dif
            })

    return results