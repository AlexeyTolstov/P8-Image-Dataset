from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

from os import listdir
from PIL import Image


path = "C:/Users/Alex Tolstov/Desktop/IMG_TEST/"

def yolo_to_voc(image_width, image_height, class_id, x_center, y_center, width, height):
    x_min = max(0, float((x_center - width / 2) * image_width))
    y_min = max(0, float((y_center - height / 2) * image_height))
    x_max = min(image_width, int((x_center + width / 2) * image_width))
    y_max = min(image_height, int((y_center + height / 2) * image_height))
    return x_min, y_min, x_max, y_max

for file in listdir(path):
    if not "jpg" in file:
        continue

    img = Image.open(path + file)
    name_txt = file.split(".")[0] + ".txt"
    class_names = ["Truck", "Crane", "Object white", "Object Red", "Cone", "Object Black"]
    
    with open(path + name_txt, "r") as txt_file:
        lines = txt_file.read().split("\n")

        annotation = Element("annotation")
        
        folder = SubElement(annotation, "folder")
        folder.text = "IMG_TEST"

        filename = SubElement(annotation, "filename")
        filename.text = file

        path_elem = SubElement(annotation, "path")
        path_elem.text = path + file

        source = SubElement(annotation, "source")
        database = SubElement(source, "database")
        database.text = "Unknown"

        size = SubElement(annotation, "size")

        image_width = img.width
        image_height = img.height

        width_elem = SubElement(size, "width")
        width_elem.text = str(image_width)

        height_elem = SubElement(size, "height")
        height_elem.text = str(image_height)

        depth = SubElement(size, "depth")
        depth.text = str(3)

        for line in lines:
            if not line:
                continue
            line_lst = line.split(" ")
            class_id = int(line_lst[0])
            x_center = float(line_lst[1])
            y_center = float(line_lst[2])
            width = float(line_lst[3])
            height = float(line_lst[4])

            x_min, y_min, x_max, y_max = yolo_to_voc(image_width, image_height, class_id, x_center, y_center, width, height)

            object_elem = SubElement(annotation, "object")

            truncated = SubElement(object_elem, "truncated")
            truncated.text = str(0)

            difficult_elem = SubElement(object_elem, "difficult")
            difficult_elem.text = str(0)

            segmented = SubElement(annotation, "segmented")
            segmented.text = str(0)

            name = SubElement(object_elem, "name")
            name.text = class_names[class_id]

            pose = SubElement(object_elem, "pose")
            pose.text = "Unspecified"

            bndbox = SubElement(object_elem, "bndbox")

            xmin = SubElement(bndbox, "xmin")
            xmin.text = str(int(x_min))

            ymin = SubElement(bndbox, "ymin")
            ymin.text = str(int(y_min))

            xmax = SubElement(bndbox, "xmax")
            xmax.text = str(int(x_max))

            ymax = SubElement(bndbox, "ymax")
            ymax.text = str(int(y_max))

        xml_string = parseString(tostring(annotation)).toprettyxml(indent="    ")
        print(xml_string)
        with open(path + file.split(".")[0] + ".xml", "w") as xml_file:
            xml_file.write(xml_string)
        # break