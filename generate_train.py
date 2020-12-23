# generate_train.py

import os 

train_folder_name = 'train_zebra_train'

image_files = []
os.chdir(os.path.join("data", train_folder_name))
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".jpg"):
        image_files.append(f"data/{train_folder_name}/" + filename)

os.chdir("..") # /<base dir>/data
with open("train.txt", "w") as file:
    for image in image_files:
        file.write(image)
        file.write("\n")

os.chdir("..") # /<base dir>
