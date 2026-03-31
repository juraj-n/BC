import csv, io, statistics

def parse_csv(file):
    #TODO: Propper CSV parsing

    if not file.filename.endswith(".csv"):
        #raise ValueError("Invalid file type")
        return
    
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline = None)
    reader = csv.DictReader(stream)

    x_values = []
    y_values = []
    
    for row in reader:
        try:
            x_values.append(float(row['wavelength_nm']))
            y_values.append(float(row['intensity_au']))
        except:
            continue
    
    return {
        "x": x_values,
        "y": y_values
    }

def min_max_normalize(data): # Min-max normalizácia na interval H(f): <0, 1>
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