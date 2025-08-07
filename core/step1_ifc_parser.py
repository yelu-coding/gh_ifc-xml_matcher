import ifcopenshell
import ifcopenshell.util.element
import logging
import os
import json

def setup_logging():
    logging.basicConfig(
        filename='ifc_parser.log',
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def get_cartesian_point(ifc_point):
    if ifc_point and hasattr(ifc_point, "Coordinates"):
        return {
            "X": float(ifc_point.Coordinates[0]),
            "Y": float(ifc_point.Coordinates[1]),
            "Z": float(ifc_point.Coordinates[2])
        }
    return None

def get_direction(ifc_direction):
    if ifc_direction and hasattr(ifc_direction, "DirectionRatios"):
        return list(ifc_direction.DirectionRatios)
    return None

def get_local_object_placement(entity):
    if not entity.ObjectPlacement or not hasattr(entity.ObjectPlacement, "RelativePlacement"):
        return None

    placement = entity.ObjectPlacement.RelativePlacement
    if not placement.is_a("IFCAXIS2PLACEMENT3D"):
        return None

    try:
        location = get_cartesian_point(placement.Location) if placement.Location else None
        axis = get_direction(placement.Axis) if placement.Axis else None
        ref_direction = get_direction(placement.RefDirection) if placement.RefDirection else None

        if not location or not axis or not ref_direction:
            return None

        return {
            "Location": location,
            "Axis": axis,
            "RefDirection": ref_direction
        }
    except:
        return None

def parse_ifc_and_export(ifc_file, output_path):
    try:
        model = ifcopenshell.open(ifc_file)
    except:
        return "Failed to open IFC file."

    building_element_types = [
        "IfcPlate", "IfcBeam", "IfcColumn", "IfcMember", "IfcSlab", "IfcWall"
    ]

    physical_entities = []
    for entity_type in building_element_types:
        try:
            entities = model.by_type(entity_type)
        except:
            continue

        for entity in entities:
            try:
                global_id = entity.GlobalId
                properties = ifcopenshell.util.element.get_psets(entity)
                location_rotation = get_local_object_placement(entity)
                physical_entities.append({
                    "GlobalId": global_id,
                    "Type": entity_type,
                    "Properties": properties,
                    "LocationRotation": location_rotation
                })
            except:
                continue

    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(physical_entities, json_file, ensure_ascii=False, indent=4)
    except:
        return "Failed to write JSON."

    return "Success"
