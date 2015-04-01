#GROUP204
#SQL->UML

#recuperation du fichier xml place tout dans root et on parcours root
from xml.etree.ElementTree import ElementTree
tree = ElementTree()

#tree.parse("C:\Users\MORJARET fixe\Documents\GitHub\Modelio3WorkspaceGenOCL-G204\macros\library.xml")
tree.parse("C:\Users\laetitia\Desktop\IDM\Modelio3WorkspaceGenOCL-G204\macros\library.xml")

root = tree.getroot()


#creation du model UML

fact = theUMLFactory()
myp = instanceNamed(Package,"MyPackage")
#fact.delete()


def createClass(nameClass):

    try:
        trans = theSession().createTransaction("Class " + nameClass)
        c1 = fact.createClass(nameClass,myp)
        trans.commit()
        trans.close()
    except:
        trans.rollback()
        raise
    
    trans.close()
        
  
def createAttribute(nameClass,nameAttribut,typeAttribut):
    try:
        trans = theSession().createTransaction("Attribut " + nameAttribut)
        class_ = instanceNamed(Class,nameClass)
        a = fact.createAttribute()
        a.setName(nameAttribut)
        a.setOwner(class_)
        #a.setDataType(typeAttribut)
        a.setType(integer)
        trans.commit()
        trans.close()
    except:
        trans.rollback()
        trans.close()
        raise
        
        
        
for element in root:
    #print (element.tag)
    for table in element:
        Name = table.attrib.get("name")
        print Name
        createClass(Name)
        for attribute in table:
            if (attribute.tag == "column"):
                createAttribute(Name,attribute.attrib.get("name"),attribute.attrib.get("type"))
                print attribute.attrib.get("name")
                print attribute.attrib.get("type")
        
        
