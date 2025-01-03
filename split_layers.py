
from lxml import etree as ET

# Path to the XML file
xml_file_path = "design/2025_mikey_misha/moon_layout_2025.svg"

# Parse the XML file
tree = ET.parse(xml_file_path)

# Get the root element
root = tree.getroot()

# Now you can work with the XML data
# For example, you can access elements and attributes using the root element

# get all direct children of root that have layer in their id with lxml
layers = root.xpath(".//*[contains(@id, 'layer')]")

# create a new xml document with the same root element
new_root = ET.Element(root.tag, nsmap=root.nsmap)

# add the root properties to the new root
for key, value in root.items():
    new_root.set(key, value)

# for each layer, add to the new root and save to a new file
for layer in layers:
    new_root.append(layer)
    new_tree = ET.ElementTree(new_root)
    new_tree.write(f"design/2025_mikey_misha/{layer.attrib['{http://www.inkscape.org/namespaces/inkscape}label']}.svg", pretty_print=True)
    new_root.remove(layer)
