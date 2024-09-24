# 读取文件内容
def read_errors_from_file(filename):
    errors = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.split(', ')
            for part in parts:
                if part.startswith('error: '):
                    error_value = part.split('error: ')[1]
                    errors.append(error_value.strip())
    return errors

# 写入文件内容
def write_errors_to_file(errors1, errors2, filename):
    with open(filename, 'w') as file:
        for e1, e2 in zip(errors1, errors2):
            file.write(f"{e1}\t{e2}\n")

# 读取第一个文件的错误
errors_file1 = read_errors_from_file("/media/shorwin/Shorwin/qq/ModaLink_nclt/output_2_2012-02-05.txt")

# 读取第二个文件的错误
errors_file2 = read_errors_from_file("/mnt/data/aotuo/CMPR_nclt/output_2_2012-02-05.txt")

# 确保两个文件中的错误数量相同
min_length = min(len(errors_file1), len(errors_file2))
errors_file1 = errors_file1[:min_length]
errors_file2 = errors_file2[:min_length]

# 写入到第三个文件
write_errors_to_file(errors_file1, errors_file2, 'output.txt')

print("错误已成功写入到output.txt文件中。")












