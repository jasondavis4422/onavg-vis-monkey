# -------------------------------------------------
# 1)  Imports & paths
# -------------------------------------------------
import os
import json
import csv   # the CSV that contains the vertex → label mapping
import pathlib

script_dir = pathlib.Path(__file__).parent.resolve()

# ‑‑‑ lookup table that you already have (ico8) ‑‑‑
ico8_path = os.path.join(script_dir, 'lookup_table_ico8.json')

# ‑‑‑ CSV that holds the vertex‑to‑atlas numbers  (VertexParcellationMap.csv) ‑‑‑
csv_path = os.path.join(script_dir, 'VertexParcellationMap.csv')

# ‑‑‑ Where the new JSON files will be written ‑‑‑
dest_destrieux = os.path.join(script_dir, 'ds128_aparc.a2009s.json')
dest_dk        = os.path.join(script_dir, 'ds128_aparc.json')
dest_dkt       = os.path.join(script_dir, 'ds128_aparc.DKTatlas.json')
# -------------------------------------------------
# 2)  Build three dictionaries:  vertex → (Destrieux, DK, DKT) label
# -------------------------------------------------
destrieux_map = {}
dk_map        = {}
dkt_map       = {}

with open(csv_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        v = int(row['Vertex Number'])
        destrieux_map[v] = int(row['Destrieux'])
        dk_map[v]        = int(row['DK Atlas'])
        dkt_map[v]       = int(row['DKT Atlas'])
# The CSV parsing logic follows the structure of the file you supplied [1].

# -------------------------------------------------
# 3)  Load the ico8 lookup table (it is a simple list of ints)
# -------------------------------------------------
with open(ico8_path, 'r') as f:
    ico8_vals = json.load(f)          # e.g. [0, 1, -1, 3, …]

# -------------------------------------------------
# 4)  Helper that converts the ico8 list into the three
#    atlas‑specific integer lists.
# -------------------------------------------------
def map_vertices(src_list, lookup_dict):
    """
    Returns a new list where each element is:
        - the corresponding atlas label if the element exists in lookup_dict,
        - -1 if the element is -1,
        - -1 otherwise (unknown vertex).
    """
    return [
        -1 if v == -1 else lookup_dict.get(v, -1)
        for v in src_list
    ]

destrieux_nums = map_vertices(ico8_vals, destrieux_map)
dk_nums        = map_vertices(ico8_vals, dk_map)
dkt_nums       = map_vertices(ico8_vals, dkt_map)
# This mirrors the “expand_labels” idea from the sample script you gave
# (convert a numeric array → another numeric array) [2].

# -------------------------------------------------
# 5)  Write the three result files as a compact JSON array
# -------------------------------------------------
def write_one_line(data, out_path):
    """Write *data* (a list of ints) to *out_path* on a single line."""
    with open(out_path, 'w', encoding='utf-8') as f:
        # separators removes the space after commas, matching the format you asked for
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

write_one_line(destrieux_nums, dest_destrieux)   # → fs128_aparc.a2009s.json
write_one_line(dk_nums,        dest_dk)        # → fs128_aparc.json
write_one_line(dkt_nums,       dest_dkt)       # → fs128_aparc.DKTatlas.json