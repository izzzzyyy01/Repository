names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

# enumerate example
print("Enumerate:")
for index, name in enumerate(names):
    print(index, name)

# zip example
print("\nZip:")
for name, score in zip(names, scores):
    print(name, score)

# type checking
value = "123"

if value.isdigit():
    num = int(value)
    print("\nConverted to integer:", num)
