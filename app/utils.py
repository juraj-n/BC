import csv

def parse_csv(file):
    #TODO: Propper CSV parsing
    if not file.filename.endswith(".csv"):
        #raise ValueError("Invalid file type")
        return
    
    data = []
    stream = file.stream.read().decode("utf-8").splitlines()
    reader = csv.reader(stream)

    for row in reader:
        try:
            x = float(row[0])
            y = float(row[1])
            data.append([x,y])
        except:
            continue

    return data