import shutil
import os

# create folder
os.makedirs("archive", exist_ok=True)

# move file
if os.path.exists("sample.txt"):
    shutil.move("sample.txt", "archive/sample.txt")
    print("File moved to archive.")

# copy back
shutil.copy("archive/sample.txt", "sample_copy.txt")
print("File copied back.")
