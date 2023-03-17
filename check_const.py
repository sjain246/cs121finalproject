import csv
all_vals = set()
with open('allvals.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            all_vals = set(row)
        line_count += 1

curr_vals = set()
with open('curr_vals.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            curr_vals = set(row)
        line_count += 1
for val in curr_vals:
    if val not in all_vals:
        print(val)