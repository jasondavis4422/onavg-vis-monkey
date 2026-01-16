import os
import json
import numpy as np

# -------------------------------------------------
# Paths (unchanged)
script_dir = os.path.dirname(os.path.abspath(__file__))
destrieux_file_path = os.path.join(script_dir, 'ds128_aparc.a2009s.json')
dk_file_path        = os.path.join(script_dir, 'ds128_aparc.json')
dkt_file_path       = os.path.join(script_dir, 'ds128_aparc.DKTatlas.json')

# -------------------------------------------------
# Load the JSON files as Python lists (list of ints)
with open(destrieux_file_path, 'r') as f:
    destrieux_data = json.load(f)   # e.g. [0, 1, 2, …]

with open(dk_file_path, 'r') as f:
    dk_data = json.load(f)

with open(dkt_file_path, 'r') as f:
    dkt_data = json.load(f)

# -------------------------------------------------
# Static name lists (copied from your original script)
DKT31_numbers = [-1, 2, 3] + list(range(5, 32)) + [34, 35]
DKT31_names = [
    'N/A', 'caudal anterior cingulate', 'caudal middle frontal', 'cuneus',
    'entorhinal', 'fusiform', 'inferior parietal', 'inferior temporal',
    'isthmus cingulate', 'lateral occipital', 'lateral orbitofrontal',
    'lingual', 'medial orbitofrontal', 'middle temporal', 'parahippocampal',
    'paracentral', 'pars opercularis', 'pars orbitalis', 'pars triangularis',
    'pericalcarine', 'postcentral', 'posterior cingulate', 'precentral',
    'precuneus', 'rostral anterior cingulate', 'rostral middle frontal',
    'superior frontal', 'superior parietal', 'superior temporal',
    'supramarginal', 'transverse temporal', 'insula'
]

destrieux_numbers = [-1] + list(range(1, 75))   # -1 … 74
destrieux_names = [
    'N/A','G_and_S_frontomargin','G_and_S_occipital_inf','G_and_S_paracentral',
    'G_and_S_subcentral','G_and_S_transv_frontopol','G_and_S_cingul-Ant',
    'G_and_S_cingul-Mid-Ant','G_and_S_cingul-Mid-Post','G_and_S_cingul-Post-dorsal',
    'G_cingul-Post-ventral','G_cuneus','G_front_inf-Opercular','G_front_inf-Orbital',
    'G_front_inf-Triangul','G_front_middle','G_front_superior','G_Ins_lg_and_S_cent_ins',
    'G_insular_short','G_occipital_middle','G_occipital_sup','G_oc-temp_lat-fusifor',
    'G_oc-temp_med-Lingual','G_oc-temp_med-Parahip','G_orbital','G_parietal_inferior_angular',
    'G_parietal_inferior_supramar','G_parietal_superior','G_postcentral','G_precentral',
    'G_precuneus','G_rectus','G_subcallosal','G_temp_sup-G_T_transv','G_temp_sup-Lateral',
    'G_temp_sup-Plan_polar','G_temp_sup-Plan_tempo','G_temporal_inferior','G_temporal_middle',
    'Lat_Fis-ant-Horizont','Lat_Fis-ant-Vertical','Lat_Fis-post','Pole_occipital','Pole_temporal',
    'S_calcarine','S_central','S_cingul-Marginalis','S_circular_insula_ant','S_circular_insula_inf',
    'S_circular_insula_sup','S_collateral_transverse_ant','S_collateral_transverse_post',
    'S_front_inf','S_front_middle','S_front_sup','S_interm_prim-Jensen','S_intrapariet_and_P_trans',
    'S_oc_middle_and_Lunatus','S_occipital_sup_transversal','S_occipital_ant','S_oc_temp_lat',
    'S_oc_temp_med_and_Lingual','S_orbital_lateral','S_orbital_med-olfact','S_orbital-H_Shaped',
    'S_parieto_occipital','S_pericallosal','S_postcentral','S_precentral-inf-part',
    'S_precentral-sup-part','S_suborbital','S_subparietal','S_temporal_inf','S_temporal_sup',
    'S_temporal_transverse'
]

# -------------------------------------------------
# Helper to build a *number → name* dictionary
def make_num2name_dict(numbers, names):
    """Return {num: name, ...}.  Missing numbers will raise an error when the
    lists have different lengths."""
    if len(numbers) != len(names):
        raise ValueError("numbers and names must be the same length")
    return dict(zip(numbers, names))

# Dictionaries for the two atlases
dkt_num2name = make_num2name_dict(DKT31_numbers, DKT31_names)
destrieux_num2name = make_num2name_dict(destrieux_numbers, destrieux_names)

# -------------------------------------------------
def expand_labels(num_array, lookup_dict, default="UNKNOWN"):
    """
    Convert an iterable of numeric codes into their string names
    using ``lookup_dict`` (num → name).

    * ``num_array`` can be a list, NumPy array, etc.
    * If a code is not present in ``lookup_dict`` the ``default`` value is used.
    """
    # Ensure a 1‑D NumPy array of ints for easy iteration
    num_array = np.asarray(num_array, dtype=int).ravel()
    # Map each number → name, falling back to ``default`` when missing
    return np.array([lookup_dict.get(int(i), default) for i in num_array])

# -------------------------------------------------
# Generate the label strings using the safe dictionary version
dk_labels       = expand_labels(dk_data,  dkt_num2name)          # DK uses the DKT31 mapping
dkt_labels      = expand_labels(dkt_data, dkt_num2name)          # DKT atlas
destrieux_labels = expand_labels(destrieux_data, destrieux_num2name)

# -----------------------------------------------------------------
def write_labels_one_line(labels, filename):
    """
    Write *labels* to *filename* as a compact JSON array on a single line.

    Example output:
        ["precentral","postcentral","gyrus",...]
    """
    # Convert possible NumPy array → plain Python list
    if isinstance(labels, np.ndarray):
        labels = labels.tolist()

    # Ensure every element is a plain string (helps with NumPy scalar types)
    labels = [str(l) for l in labels]

    out_path = os.path.join(script_dir, filename)
    with open(out_path, "w", encoding="utf-8") as f:
        # separators=(',', ':') removes the space after commas
        json.dump(labels, f, ensure_ascii=False, separators=(',', ':'))

# -----------------------------------------------------------------
# Write the results as JSON files
write_labels_one_line(dk_labels,       "dk_labels.json")
write_labels_one_line(dkt_labels,      "dkt_labels.json")
write_labels_one_line(destrieux_labels, "destrieux_labels.json")