"""
process_file.py — Part 2: one file of package descriptions, uploaded.

A Streamlit app that accepts an uploaded text file with one package description
per line, shows the total for every line, and writes the parsed packages to a
JSON file in the `data/` folder — `data/packaging1.txt` in, `data/packaging1.json`
out.

New here: an uploaded file arrives as **bytes**, not text, so it has to be
decoded before it can be split into lines. And a text file usually ends with a
newline, so the last "line" is empty and must be skipped rather than parsed.

Run it:  Run and Debug -> "Streamlit Run: Current File"   (see README Reference #1)
Test it: pytest tests/test_streamlit.py -k process_file
"""

import json

import streamlit as st

from packaging_parser import calc_total_units, get_unit, parse_packaging


st.title("Process File of Packages")

uploaded_file = st.file_uploader(
    "Upload a package file:",
    type="txt",
    key="package_file",
)

if uploaded_file:
    text = uploaded_file.getvalue().decode("utf-8")
    packages = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        package = parse_packaging(line)
        packages.append(package)
        total = calc_total_units(package)
        unit = get_unit(package)
        st.info(f"{line} ➡️ Total 📦 Size: {total} {unit}")

    output_name = uploaded_file.name.rsplit(".", 1)[0] + ".json"
    output_path = f"data/{output_name}"
    with open(output_path, "w", encoding="utf-8") as output_file:
        json.dump(packages, output_file, indent=2)

    st.success(f"{len(packages)} packages written to {output_path}")
