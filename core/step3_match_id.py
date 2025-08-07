# core/step3_match_id.py

import os
import json
import numpy as np
import pandas as pd
from collections import defaultdict
from scipy.optimize import linear_sum_assignment

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_vector(v):
    v = np.array(v, dtype=float)
    norm = np.linalg.norm(v)
    return v / norm if norm != 0 else v

def compute_rotation_error(R1, R2):
    return np.linalg.norm(R1 - R2)

def compute_best_rotation_matrix(ifc_axis, ifc_refdir, xml_Rx, xml_Ry, ref_matrix=None):
    flips = [-1, 1]
    best_result = {
        'matrix': None,
        'error': float('inf'),
        'flips': (1, 1, 1, 1)
    }

    for fa in flips:
        for fr in flips:
            for fx in flips:
                for fy in flips:
                    try:
                        z_ifc = normalize_vector([fa * x for x in ifc_axis])
                        x_ifc = normalize_vector([fr * x for x in ifc_refdir])
                        y_ifc = normalize_vector(np.cross(z_ifc, x_ifc))
                        x_ifc = normalize_vector(np.cross(y_ifc, z_ifc))
                        B_ifc = np.column_stack((x_ifc, y_ifc, z_ifc))

                        x_xml = normalize_vector([fx * x for x in xml_Rx])
                        y_xml = normalize_vector([fy * x for x in xml_Ry])
                        z_xml = normalize_vector(np.cross(x_xml, y_xml))
                        y_xml = normalize_vector(np.cross(z_xml, x_xml))
                        B_xml = np.column_stack((x_xml, y_xml, z_xml))

                        R = B_xml @ B_ifc.T
                        U, _, Vt = np.linalg.svd(R)
                        R_final = U @ Vt

                        target = ref_matrix if ref_matrix is not None else np.identity(3)
                        err = compute_rotation_error(target, R_final)

                        if err < best_result['error']:
                            best_result.update({
                                'matrix': R_final,
                                'error': err,
                                'flips': (fa, fr, fx, fy)
                            })
                    except:
                        continue

    return best_result['matrix'], best_result['error'], best_result['flips']

def updated_match_components_unique(ifc_data, xml_data, prop_set, prop_key):
    matches = []
    matched_ifc = set()
    matched_xml = set()

    processed_ifcs = []
    for i in ifc_data:
        try:
            nc_name_raw = str(i.get("Properties", {}).get(prop_set, {}).get(prop_key, "")).strip()
            processed_ifcs.append({
                "id": i["GlobalId"],
                "nc_name": f"{nc_name_raw}.nc",
                "axis": i["LocationRotation"]["Axis"],
                "refdir": i["LocationRotation"]["RefDirection"],
                "location": [
                    i["LocationRotation"]["Location"]["X"],
                    i["LocationRotation"]["Location"]["Y"],
                    i["LocationRotation"]["Location"]["Z"]
                ]
            })
        except Exception as e:
            continue

    processed_xml = []
    for x in xml_data:
        try:
            processed_xml.append({
                "id": x["ID"],
                "nc_name": x["Reference"][0].strip(),
                "Rx": x["Rx"],
                "Ry": x["Ry"],
                "base": x["Base"]
            })
        except Exception as e:
            continue

    ifc_groups = defaultdict(list)
    xml_groups = defaultdict(list)
    for i in processed_ifcs:
        ifc_groups[i['nc_name']].append(i)
    for x in processed_xml:
        xml_groups[x['nc_name']].append(x)

    orientation_pairs = []

    for name, ifc_list in ifc_groups.items():
        if name in xml_groups:
            xml_list = xml_groups[name]
            if len(ifc_list) == 1 and len(xml_list) == 1:
                ifc, xml = ifc_list[0], xml_list[0]
                matches.append((ifc, xml, 0, 'unique_nc_name', False))
                matched_ifc.add(ifc['id'])
                matched_xml.add(xml['id'])
                orientation_pairs.append((ifc['axis'], ifc['refdir'], xml['Rx'], xml['Ry']))

    ref_mat = None
    if orientation_pairs:
        ref_mat, _, _ = compute_best_rotation_matrix(*orientation_pairs[0])

    for name, ifc_list in ifc_groups.items():
        xml_list = xml_groups.get(name, [])
        if not xml_list:
            continue

        ifcs_to_match = [i for i in ifc_list if i['id'] not in matched_ifc]
        xmls_to_match = [x for x in xml_list if x['id'] not in matched_xml]

        if len(ifcs_to_match) == 0 or len(xmls_to_match) == 0:
            continue

        cost_matrix = np.zeros((len(ifcs_to_match), len(xmls_to_match)))
        rotation_matrices = [[None for _ in xmls_to_match] for _ in ifcs_to_match]

        for i, ifc in enumerate(ifcs_to_match):
            for j, xml in enumerate(xmls_to_match):
                best_mat, error, flips = compute_best_rotation_matrix(
                    ifc['axis'], ifc['refdir'], xml['Rx'], xml['Ry'], ref_matrix=ref_mat
                )
                cost_matrix[i, j] = error
                rotation_matrices[i][j] = (best_mat, error)

        row_ind, col_ind = linear_sum_assignment(cost_matrix)

        threshold = 1e-4
        for i, j in zip(row_ind, col_ind):
            ifc = ifcs_to_match[i]
            xml = xmls_to_match[j]
            _, err = rotation_matrices[i][j]

            row_similar = np.sum(np.abs(cost_matrix[i, :] - err) < threshold) > 1
            col_similar = np.sum(np.abs(cost_matrix[:, j] - err) < threshold) > 1
            need_check = row_similar or col_similar

            matches.append((ifc, xml, err, 'matrix_direction_match', need_check))
            matched_ifc.add(ifc['id'])
            matched_xml.add(xml['id'])

    return matches

def export_matches_to_files(matches, out_json_path, out_csv_path):
    out_data = []
    for ifc, xml, err, method, need_check in matches:
        out_data.append({
            "IFC_ID": ifc['id'],
            "XML_ID": xml['id'],
            "Error": err,
            "Method": method,
            "NC_Name": ifc.get('nc_name'),
            "IFC_Location": ifc['location'],
            "IFC_Axis": ifc['axis'],
            "IFC_RefDirection": ifc['refdir'],
            "XML_Base": xml['base'],
            "XML_Rx": xml['Rx'],
            "XML_Ry": xml['Ry'],
            "NeedManualCheck": bool(need_check)
        })

    os.makedirs(os.path.dirname(out_json_path), exist_ok=True)
    with open(out_json_path, 'w', encoding='utf-8') as f:
        json.dump(out_data, f, indent=4, ensure_ascii=False)

    df = pd.DataFrame(out_data)
    df.to_csv(out_csv_path, index=False)
    return len(out_data), sum(item['NeedManualCheck'] for item in out_data)

def match_and_export(ifc_json_path, xml_json_path, out_json_path, out_csv_path, prop_set, prop_key):
    ifc_data = load_json(ifc_json_path)
    xml_data = load_json(xml_json_path)
    matches = updated_match_components_unique(ifc_data, xml_data, prop_set, prop_key)
    return export_matches_to_files(matches, out_json_path, out_csv_path)
