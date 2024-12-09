import re
import sys

if len(sys.argv) != 2:
    raise ValueError("expected: inputfile")

with open(sys.argv[1]) as infile:
    text = infile.read()

# Part 1
mul_pattern = re.compile(r"mul\((\d+),(\d+)\)")

sum_mul = sum(int(a) * int(b) for a, b in mul_pattern.findall(text))
print("Sum of valid multiplications:", sum_mul)

# Part 2
mul_do_dont_pattern = re.compile(r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))")

mul_enabled = True
enabled_pairs = []
for a, b, do, dont in mul_do_dont_pattern.findall(text):
    if do:
        mul_enabled = True
    elif dont:
        mul_enabled = False
    else:
        if mul_enabled:
            enabled_pairs.append((int(a), int(b)))

sum_enabled = sum(a * b for a, b in enabled_pairs)
print("Sum of enabled multiplications", sum_enabled)
