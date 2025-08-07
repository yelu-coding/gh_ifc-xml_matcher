import os
import xml.etree.ElementTree as ET
import json

def parse_wia_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    assembly_info = []
    for part in root.findall("./ASSEMBLY/PART"):
        part_info = {
            "ID": part.get("ID"),
            "Name": part.get("NAME"),
            "Type": part.get("TYPE"),
            "Base": [
                float(part.find("./FRAME/BASE").get("X")),
                float(part.find("./FRAME/BASE").get("Y")),
                float(part.find("./FRAME/BASE").get("Z"))
            ],
            "Rx": [
                float(part.find("./FRAME/RX").get("X")),
                float(part.find("./FRAME/RX").get("Y")),
                float(part.find("./FRAME/RX").get("Z"))
            ],
            "Ry": [
                float(part.find("./FRAME/RY").get("X")),
                float(part.find("./FRAME/RY").get("Y")),
                float(part.find("./FRAME/RY").get("Z"))
            ],
            "Reference": [
                part.find("./REFERENCE").get("FILE_NAME")
            ]
        }
        assembly_info.append(part_info)

    return assembly_info

def save_to_directory(data, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def parse_and_save_xml_simple(xml_file_path, output_path):
    """
    解析 XML 并保存为 JSON（不排序）
    """
    assembly_data = parse_wia_file(xml_file_path)
    save_to_directory(assembly_data, output_path)
    return "Success"
