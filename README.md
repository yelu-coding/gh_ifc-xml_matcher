<<<<<<< HEAD
# IFC–DSTV XML Component Matcher with Grasshopper + Hops

This project implements a modular, geometry-aware component matching system between **IFC models** and **DSTV-compliant XML assembly instructions**.  
It is structured as a **Python Flask + Hops server**, fully controllable via **Grasshopper**, and capable of exporting **JSON/CSV result files** for downstream use.

---

## 🧩 Key Features

- ✅ IFC component extraction (GlobalId, position, direction, custom properties)
- ✅ XML parsing of part position and orientation
- ✅ NC file name–based matching (with fallback to geometry-based alignment)
- ✅ Rotation matrix error computation + ambiguity flag
- ✅ JSON + CSV export of match results
- ✅ Modular Hops endpoints for each processing step
- ✅ Grasshopper interface for live input & control

---

## 📁 Folder Structure
```text
GH_IFC_Project/
├── app.py                 # Main Flask + Hops service entry point
├── core/                  # Step-wise processing logic
│   ├── step1_ifc_parser.py
│   ├── step2_xml_parser.py
│   ├── step3_match_id.py
│   └── step4_detected_updated.py
├── data/                  # Example input files (.ifc, .xml)
├── output/                # Exported result files (.json, .csv, .xlsx)
├── gh/                    # Grasshopper Hops interface files
├── LICENSE                # MIT License
├── requirements.txt       # Python dependencies
└── README.md              # You are here
 ```

## 🚀 How to Run (on your own computer)

### ✅ Step-by-step

### 1. Clone or unzip the project to a folder like `D:/GH_IFC_Project`

### 2. Install dependencies

Open **Anaconda Prompt** or **Git Bash**, then:

```bash
cd /d D/GH_IFC_Project
conda activate gh_ifc_env
pip install -r requirements.txt
```

### 3. Start the Hops server

```bash
python app.py
```

You should see:

```text
Running on http://127.0.0.1:5000
Loaded component: ParseIFC at /parse_ifc
Loaded component: ParseXML at /parse_xml
Loaded component: MatchComponents at /match_components
```

### 4. Launch Rhino + Grasshopper

- Start Rhino 7 or 8
- Run `Grasshopper`
- Open a `.gh` file (in this case., `match_ifc_xml_by_nc.gh`)

### 5. Set each Hops node URL

Right-click on each Hops component and set the correct URL:

```text
http://127.0.0.1:5000/parse_ifc
http://127.0.0.1:5000/parse_xml
http://127.0.0.1:5000/match_components
```

### 6. Enter file paths using Panels

- IFC File path (e.g. `D:\GH_IFC_Project\data\example.ifc`)
- XML File path (e.g. `D:\GH_IFC_Project\data\example.xml`)
- Output path: `output/result.json`, `output/result.csv`
- PropertySet and PropertyKey: e.g., `+Träger`, `Position`
> **About PropertySet and PropertyKey**  
> In an IFC file, the component's `Properties` section does not directly store the NC file name. Instead, a specific PropertySet contains a field (PropertyKey) that stores a “position/identifier” value. This value can be mapped against an existing NC file name directory to determine the actual NC file name for that component.  
> - **PropertySet** (e.g., `+Träger`) is the name of the property set in IFC.  
> - **PropertyKey** (e.g., `Position`) is the specific field name within that property set.  
>
> In the IFC.JSON output, the value from this field must be cross-referenced with your existing NC file name directory to identify the correct NC file name.  
>
> In contrast, a DSTV XML file directly stores the NC file name (e.g., `2538.nc`) in the `Reference` field for each component, so there is no need for additional mapping — simply reading the `Reference` location is enough to get the NC file name.
>
> **Example comparison:**
>
> | Format | Field Location | Example Value | Notes |
> |--------|----------------|---------------|-------|
> | IFC    | `Properties["+Träger"]["Position"]` | `2538` | Needs mapping to `2538.nc` using NC file directory |
> | XML    | `Reference`    | `2538.nc`     | NC file name is given directly |


### 7. View output in `output/` folder or load CSV into GH for visualization
=======
\# IFC–DSTV XML Component Matcher with Grasshopper + Hops



This project implements a modular, geometry-aware component matching system between \*\*IFC models\*\* and \*\*DSTV-compliant XML assembly instructions\*\*.  

It is structured as a \*\*Python Flask + Hops server\*\*, fully controllable via \*\*Grasshopper\*\*, and capable of exporting \*\*JSON/CSV result files\*\* for downstream use.



---



\## 🧩 Key Features



\- ✅ IFC component extraction (GlobalId, position, direction, custom properties)

\- ✅ XML parsing of part position and orientation

\- ✅ NC file name–based matching (with fallback to geometry-based alignment)

\- ✅ Rotation matrix error computation + ambiguity flag

\- ✅ JSON + CSV export of match results

\- ✅ Modular Hops endpoints for each processing step

\- ✅ Grasshopper interface for live input \& control



---



\## 📁 Folder Structure

```text

GH\_IFC\_Project/

├── app.py                 # Main Flask + Hops service entry point

├── core/                  # Step-wise processing logic

│   ├── step1\_ifc\_parser.py

│   ├── step2\_xml\_parser.py

│   ├── step3\_match\_id.py

│   └── step4\_detected\_updated.py

├── data/                  # Example input files (.ifc, .xml)

├── output/                # Exported result files (.json, .csv, .xlsx)

├── gh/                    # Grasshopper Hops interface files

├── LICENSE                # MIT License

├── requirements.txt       # Python dependencies

└── README.md              # You are here

&nbsp;```



\## 🚀 How to Run (on your own computer)



\### ✅ Step-by-step



\### 1. Clone or unzip the project to a folder like `D:/GH\_IFC\_Project`



\### 2. Install dependencies



Open \*\*Anaconda Prompt\*\* or \*\*Git Bash\*\*, then:



```bash

cd /d D/GH\_IFC\_Project

conda activate gh\_ifc\_env

pip install -r requirements.txt

```



\### 3. Start the Hops server



```bash

python app.py

```



You should see:



```text

Running on http://127.0.0.1:5000

Loaded component: ParseIFC at /parse\_ifc

Loaded component: ParseXML at /parse\_xml

Loaded component: MatchComponents at /match\_components

```



\### 4. Launch Rhino + Grasshopper



\- Start Rhino 7 or 8

\- Run `Grasshopper`

\- Open a `.gh` file (in this case., `match\_ifc\_xml\_by\_nc.gh`)



\### 5. Set each Hops node URL



Right-click on each Hops component and set the correct URL:



```text

http://127.0.0.1:5000/parse\_ifc

http://127.0.0.1:5000/parse\_xml

http://127.0.0.1:5000/match\_components

```



\### 6. Enter file paths using Panels



\- IFC File path (e.g. `D:\\GH\_IFC\_Project\\data\\example.ifc`)

\- XML File path (e.g. `D:\\GH\_IFC\_Project\\data\\example.xml`)

\- Output path: `output/result.json`, `output/result.csv`

\- PropertySet and PropertyKey: e.g., `+Träger`, `Position`

> \*\*About PropertySet and PropertyKey\*\*  

> In an IFC file, the component's `Properties` section does not directly store the NC file name. Instead, a specific PropertySet contains a field (PropertyKey) that stores a “position/identifier” value. This value can be mapped against an existing NC file name directory to determine the actual NC file name for that component.  

> - \*\*PropertySet\*\* (e.g., `+Träger`) is the name of the property set in IFC.  

> - \*\*PropertyKey\*\* (e.g., `Position`) is the specific field name within that property set.  

>

> In the IFC.JSON output, the value from this field must be cross-referenced with your existing NC file name directory to identify the correct NC file name.  

>

> In contrast, a DSTV XML file directly stores the NC file name (e.g., `2538.nc`) in the `Reference` field for each component, so there is no need for additional mapping — simply reading the `Reference` location is enough to get the NC file name.

>

> \*\*Example comparison:\*\*

>

> | Format | Field Location | Example Value | Notes |

> |--------|----------------|---------------|-------|

> | IFC    | `Properties\["+Träger"]\["Position"]` | `2538` | Needs mapping to `2538.nc` using NC file directory |

> | XML    | `Reference`    | `2538.nc`     | NC file name is given directly |





\### 7. View output in `output/` folder or load CSV into GH for visualization


>>>>>>> 8e56529 (Update project)

---


<<<<<<< HEAD
## 🎛️ Hops Node Interface: match_components

This Hops component performs orientation-aware matching between IFC and XML components.

| Param Name | Meaning                                                          |
| ---------- | ---------------------------------------------------------------- |
| `I`        | Path to parsed IFC JSON file (from `/parse_ifc`)                 |
| `X`        | Path to parsed XML JSON file (from `/parse_xml`)                 |
| `J`        | Output JSON path (e.g. `output/matched.json`)                    |
| `C`        | Output CSV path (e.g. `output/matched.csv`)                      |
| `PSet`     | PropertySet in IFC used to extract NC file name (e.g. `+Träger`) |
| `PKey`     | Key in the PropertySet (e.g. `Position`)                         |
> These are needed to dynamically extract the NC filename from the IFC properties:
>
> ```python
> i.get("Properties", {}).get(PSet, {}).get(PKey)
> ```


![Hops Node Example](gh/hops_match_input.png)


### OUTPUT
| Param Name | Meaning                          |                              |
| ---------- | -------------------------------- | ---------------------------- |
| `R`        | Matching summary (\`✅ Matched: X | ⚠️ Manual Check Needed: Y\`) |


## 📊 Sample Output

output/result.xlsx or output/matched.csv

| IFC\_ID | XML\_ID | Error   | Method                   | NC\_Name | NeedManualCheck |
| ------- | ------- | ------- | ------------------------ | -------- | --------------- |
| ...     | ...     | 0.00001 | unique\_nc\_name         | 1234.nc  | False           |
| ...     | ...     | 0.00321 | matrix\_direction\_match | 2538.nc  | True            |
NeedManualCheck = True indicates multiple near-identical matches by matrix.


## 📄 License
MIT License © 2025 Ye Lu


## 📬 Contact / Feedback
If you'd like to contribute, report an issue, or collaborate, feel free to contact [Ye Lu](https://github.com/yelu-coding) or open a GitHub issue.
=======



\## 🎛️ Hops Node Interface: match\_components



This Hops component performs orientation-aware matching between IFC and XML components.



| Param Name | Meaning                                                          |

| ---------- | ---------------------------------------------------------------- |

| `I`        | Path to parsed IFC JSON file (from `/parse\_ifc`)                 |

| `X`        | Path to parsed XML JSON file (from `/parse\_xml`)                 |

| `J`        | Output JSON path (e.g. `output/matched.json`)                    |

| `C`        | Output CSV path (e.g. `output/matched.csv`)                      |

| `PSet`     | PropertySet in IFC used to extract NC file name (e.g. `+Träger`) |

| `PKey`     | Key in the PropertySet (e.g. `Position`)                         |

> These are needed to dynamically extract the NC filename from the IFC properties:

>

> ```python

> i.get("Properties", {}).get(PSet, {}).get(PKey)

> ```





!\[Hops Node Example](gh/hops\_match\_input.png)





\### OUTPUT

| Param Name | Meaning                          |                              |

| ---------- | -------------------------------- | ---------------------------- |

| `R`        | Matching summary (\\`✅ Matched: X | ⚠️ Manual Check Needed: Y\\`) |





\## 📊 Sample Output



output/result.xlsx or output/matched.csv



| IFC\\\_ID | XML\\\_ID | Error   | Method                   | NC\\\_Name | NeedManualCheck |

| ------- | ------- | ------- | ------------------------ | -------- | --------------- |

| ...     | ...     | 0.00001 | unique\\\_nc\\\_name         | 1234.nc  | False           |

| ...     | ...     | 0.00321 | matrix\\\_direction\\\_match | 2538.nc  | True            |

NeedManualCheck = True indicates multiple near-identical matches by matrix.





\## 📄 License

MIT License © 2025 Ye Lu





\## 📬 Contact / Feedback

If you'd like to contribute, report an issue, or collaborate, feel free to contact \[Ye Lu](https://github.com/yelu-coding) or open a GitHub issue.













>>>>>>> 8e56529 (Update project)










