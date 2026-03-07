import os

# create nested directories
os.makedirs("test_folder/subfolder", exist_ok=True)

# list files and folders
print("Directory contents:")
for item in os.listdir("."):
    print(item)

# find .txt files
print("\nTXT files:")
for file in os.listdir("."):
    if file.endswith(".txt"):
        print(file)
