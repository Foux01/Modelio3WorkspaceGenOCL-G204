#GROUP204
from xml.etree.ElementTree import ElementTree
tree = ElementTree()

tree.parse("C:\Users\laetitia\Desktop\IDM\Modelio3WorkspaceGenOCL-G204\macros\library.xml")

root = tree.getroot()

for element in root:
    print (element.tag)
    for table in element:
        print (table.attrib.get("name"))