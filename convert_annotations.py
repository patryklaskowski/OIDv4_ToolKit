# convert_annotations.py

import os
import cv2
from tqdm import tqdm

def convert(file_name, coords):
  '''Turns labels from not normalized absolute bbox coordinates:

  <class_name> <x_min> <y_min> <x_max> <y_max>

  into normalized (relative to image size) YOLO format coordinates.

  <object-class> <x> <y> <width> <height>

  where:
    (x, y): center of rectangle
    width, height: rectangle dimentions.

  It assume that called from inside:
  /content/OIDv4_ToolKit/OID/Dataset/<purpose>/<class>/Label
  and that actual .jpg images are stored on path:
  /content/OIDv4_ToolKit/OID/Dataset/<purpose>/<class>
  '''
  os.chdir("..")
  image = cv2.imread(file_name + ".jpg")

  coords[2] -= coords[0]
  coords[3] -= coords[1]
  x_diff = int(coords[2]/2)
  y_diff = int(coords[3]/2)
  coords[0] = coords[0]+x_diff
  coords[1] = coords[1]+y_diff
  coords[0] /= int(image.shape[1])
  coords[1] /= int(image.shape[0])
  coords[2] /= int(image.shape[1])
  coords[3] /= int(image.shape[0])

  os.chdir("Label")
  return coords


def main():
  # /content/OIDv4_ToolKit
  ROOT_DIR = os.getcwd()
  classes = {}
  with open("classes.txt", "r") as file:
      for idx, cls in enumerate(file):
          cls = cls.strip("\n")
          classes[cls] = idx

  # /content/OIDv4_ToolKit/OID/Dataset
  toolkit_dataset_dir = os.path.join(ROOT_DIR, 'OID', 'Dataset')
  os.chdir(toolkit_dataset_dir)

  purpose_dirs = os.listdir(os.curdir)
  # purpose: {train, test, validation}
  for purpose in purpose_dirs:
    purpose_path = os.path.join(toolkit_dataset_dir, purpose)
    if os.path.isdir(purpose_path):
      os.chdir(purpose_path)
      print(f'> Currently in subdirectory: {purpose}')

      # Each purpose may have many class directories
      class_dirs = os.listdir(os.getcwd())
      # class_dir: {class_1, class_2_class_3, ...}
      for class_dir in class_dirs:
        class_path = os.path.join(purpose_path, class_dir)
        if os.path.isdir(class_path):
          os.chdir(class_path)
          print(f'> Converting annotations for class: {class_dir}')
          os.chdir('Label')

          for _file in tqdm(os.listdir(os.curdir)):
            file_name, file_extension = os.path.splitext(_file)
            if file_extension.endswith('.txt'):
              single_image_annotations = []

              # Open _file to get the oryginal coordinates
              with open(_file, 'r') as f:
                for line in f:
                  for key in classes:
                    # Important thing is that the muli-word labels are separated with " " instead of "_".
                    line = line.replace(key.replace('_', ' '), str(classes[key]))
                  # List of 5 values: <class_name> <x_min> <y_min> <x_max> <y_max>
                  values = line.split()
                  coords = np.asarray([float(values[1]), float(values[2]), float(values[3]), float(values[4])])
                  coords = convert(file_name, coords)
                  values[1], values[2], values[3], values[4] = coords[0], coords[1], coords[2], coords[3]
                  # New list of 5 values: <object-class> <x> <y> <width> <height>
                  newline = str(values[0]) + " " + str(values[1]) + " " + str(values[2]) + " " + str(values[3]) + " " + str(values[4])
                  # Add modified line
                  single_image_annotations.append(newline)

              # Create new _file on path /content/OIDv4_ToolKit/OID/Dataset/<purpose>/<class>
              os.chdir("..")
              with open(_file, "w") as outfile:
                for line in single_image_annotations:
                  outfile.write(f'{line}\n')
              os.chdir("Label")


  os.chdir(ROOT_DIR)

if __name__ == '__main__':
  main()
