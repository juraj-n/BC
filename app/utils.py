import csv, io

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