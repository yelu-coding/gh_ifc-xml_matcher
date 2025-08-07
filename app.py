from flask import Flask
import ghhops_server as hs

# 导入核心功能模块
from core.step1_ifc_parser import parse_ifc_and_export
from core.step2_xml_parser import parse_and_save_xml_simple
from core.step3_match_id import match_and_export

# 初始化 Flask 和 Hops
app = Flask(__name__)
hops = hs.Hops(app)

# ✅ Step 1: 解析 IFC 文件并导出为 JSON
@hops.component(
    "/parse_ifc",
    name="ParseIFC",
    description="Parse IFC file and save component info to JSON",
    inputs=[
        hs.HopsString("IFC_File", "F", "Path to the IFC file"),
        hs.HopsString("Output_JSON", "J", "Output JSON file path")
    ],
    outputs=[
        hs.HopsString("Result", "R", "Success or error message")
    ]
)
def hop_parse_ifc(IFC_File, Output_JSON):
    try:
        result = parse_ifc_and_export(IFC_File, Output_JSON)
        return [result]
    except Exception as e:
        return [str(e)]


# ✅ Step 2: 解析 XML 文件并导出 raw/sorted JSON
@hops.component(
    "/parse_xml",
    name="ParseXML",
    description="Parse XML and export raw JSON (no install order)",
    inputs=[
        hs.HopsString("XML_File", "F", "Path to the XML file"),
        hs.HopsString("Output_JSON", "J", "Path to save JSON output")
    ],
    outputs=[
        hs.HopsString("Result", "R", "Success or error message")
    ]
)
def hop_parse_xml(XML_File, Output_JSON):
    try:
        result = parse_and_save_xml_simple(XML_File, Output_JSON)
        return [result]
    except Exception as e:
        return [str(e)]

# ✅ Step 3: 匹配
@hops.component(
    "/match_components",
    name="MatchComponents",
    description="Match IFC and XML components based on property key",
    inputs=[
        hs.HopsString("IFC_JSON", "I", "Path to IFC JSON"),
        hs.HopsString("XML_JSON", "X", "Path to XML JSON"),
        hs.HopsString("Output_JSON", "J", "Path to output matched JSON"),
        hs.HopsString("Output_CSV", "C", "Path to output matched CSV"),
        hs.HopsString("PropertySet", "PSet", "e.g. +Träger"),
        hs.HopsString("PropertyKey", "PKey", "e.g. Position")
    ],
    outputs=[
        hs.HopsString("Result", "R", "Summary of matches and checks")
    ]
)
def hop_match_components(IFC_JSON, XML_JSON, Output_JSON, Output_CSV, PropertySet, PropertyKey):
    try:
        total, to_check = match_and_export(IFC_JSON, XML_JSON, Output_JSON, Output_CSV, PropertySet, PropertyKey)
        return [f"✅ Matched: {total} | ⚠️ Manual Check Needed: {to_check}"]
    except Exception as e:
        return [str(e)]


# ✅ 最后运行 Flask 服务
if __name__ == "__main__":
    app.run(debug=True)
