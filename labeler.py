import glob
import re
import csv

text_files = glob.glob("*.txt")
data = []

for text_file in text_files:
    with open(text_file, 'r') as f:
        print('Reading', text_file)
        for line in f:
            print(line)
            match = re.search('"(.*)"', line)
            if match:
                match = match.group(1)
                rest = line.replace(match, '')
                if rest and len(match) * 2 > len(rest):
                    # Remove inner quotes and label as 1 for dialog
                    data.append([match.replace('"', '' ), 1])
                else:
                    if len(rest) > 2:
                        # Label as 0 for non-dialog
                        data.append([rest, 0])
            else:
                if len(line) > 2:
                    data.append([line, 0])

with open('data.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(data)
