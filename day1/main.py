import sys
from collections import defaultdict

if len(sys.argv) != 2:
    raise ValueError("1 argument expected: inputfile")

with open(sys.argv[1]) as infile:
    id_tuples = [tuple(map(int, (line.strip().split("   ")))) for line in infile]
    l1 = sorted([tup[0] for tup in id_tuples])
    l2 = sorted([tup[1] for tup in id_tuples])

# Part One
total_distance = sum(abs(i1 - i2) for i1, i2 in zip(l1, l2))

print("Total Distance: " + str(total_distance))

# Part Two
right_el_count = defaultdict(int)
for el in l2:
    right_el_count[el] += 1

similarity_score = sum(el * right_el_count[el] for el in l1)

print("Similarity Score: " + str(similarity_score))
