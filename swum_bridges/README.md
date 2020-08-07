# SWUM Bridges
The bridges layer of SWUM connects identifiers processed by SWUM with their representation in the source srcML archive, using the unique numeric ID that SWUM assigns to each identifier.

# Installation
1. Install Python dependencies.
```
pip install lxml
```

# Usage
```
python swum_bridges.py srcml_file swum_id
```

## Input
The program accepts a srcML archive (which has been modified by SWUM to include IDs) and the SWUM ID of the identifier to bridge between SWUM and srcML.

## Output
The xml element in the srcML archive corresponding to the identifier is printed to stdout.
