# generate_test.py

import os

test_folder_name = 'test_zebra_train'

image_files = []
os.chdir(os.path.join("data", test_folder_name))
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".jpg"):
        image_files.append(f"data/{test_folder_name}/" + filename)

os.chdir("..") # /<base dir>/data
with open("test.txt", "w") as file:
    for image in image_files:
        file.write(image)
        file.write("\n")

os.chdir("..") # /<base dir>
