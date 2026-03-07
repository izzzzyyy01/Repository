import shutil
import os

# copy file
shutil.copy("sample.txt", "sample_backup.txt")
print("File copied.")

# delete file safely
if os.path.exists("sample_backup.txt"):
    os.remove("sample_backup.txt")
    print("Backup file deleted.")
else:
    print("File not found.")
