
directory = './files/'
file_names = [
    '1.txt',
    '2.txt',
    '3.txt',
]
result = 'out_file.txt'
encod = 'UTF-8'
files_lst = []

for name in file_names:
    with open(directory+name, encoding=encod) as f:
        lines = f.readlines()
        length = len(lines)
        files_lst.append((name, length, lines))

files_lst = sorted(files_lst, key=lambda z: z[1])

with open(directory+result, 'w', encoding=encod) as f:
    for name, length, body in files_lst:
        # print(name, str(length))
        f.write(name + '\n')
        f.write(str(length) + '\n')
        for line in body:
            f.write(line.replace('\n', '') + '\n')
