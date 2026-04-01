import csv, io, statistics, math

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

def calculate_pearson(y1, y2):
    length = min(len(y1), len(y2))
    y1, y2 = y1[:length], y2[:length]

    mu1 = statistics.mean(y1)
    mu2 = statistics.mean(y2)

    numerator = sum((a - mu1) * (b - mu2) for a, b in zip(y1, y2))
    denominator = math.sqrt(sum((a - mu1)**2 for a in y1) * sum((b - mu2)**2 for b in y2))

    if denominator == 0:
        return 0
    else:
        return numerator / denominator