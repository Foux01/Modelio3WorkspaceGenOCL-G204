"""
=========================================================
                       GenOCL.py
 Generate a USE OCL specification from a UML package
=========================================================

FILL THIS SECTION AS SHOWN BELOW AND LINES STARTING WITH ###
@author Xuan Shong TI WONG SHI <xuan.ti@mydomain.com>
@author Maria Shohie CEZAR LOPEZ DE ANDERA <maria.cezar@ujf-grenoble.fr>
@group  G99

Current state of the generator
----------------------------------
FILL THIS SECTION 
Explain which UML constructs are supported, which ones are not.
What is good in your generator?
What are the current limitations?

Current state of the tests
--------------------------
FILL THIS SECTION 
Explain how did you test this generator.
Which test are working? 
Which are not?

Observations
------------
Additional observations could go there
"""


#---------------------------------------------------------
#   Helpers on the source metamodel (UML metamodel)
#---------------------------------------------------------
# The functions below can be seen as extensions of the
# modelio metamodel. They define useful elements that 
# are missing in the current metamodel but that allow to
# explorer the UML metamodel with ease.
# These functions are independent from the particular 
# problem at hand and could be reused in other 
# transformations taken UML models as input.
#---------------------------------------------------------

# example
def isAssociationClass(element):
    """ 
    Return True if and only if the element is an association 
    that have an associated class, or if this is a class that
    has a associated association. (see the Modelio metamodel
    for details)
    """
   
 
#---------------------------------------------------------
#   Application dependent helpers on the source metamodel
#---------------------------------------------------------
# The functions below are defined on the UML metamodel
# but they are defined in the context of the transformation
# from UML Class diagramm to USE OCL. There are not
# intended to be reusable. 
#--------------------------------------------------------- 

# example
def associationsInPackage(package):
    """
    Return the list of all associations that start or
    arrive to a class which is recursively contained in
    a package.
    """
    listAssoc = [] 
    for e in package:
        for classes in  e.origin.ownedElement :
            for assoc in classes.compositionChildren :
                for lesAssoc in  assoc.compositionChildren:
                    if isinstance(lesAssoc, Association) and not isinstance(lesAssoc, ClassAssociation):
                        if not lesAssoc.linkToClass :
                            if lesAssoc not in listAssoc:
                                listAssoc.append(lesAssoc)
    return listAssoc
    

    
#---------------------------------------------------------
#   Helpers for the target representation (text)
#---------------------------------------------------------
# The functions below aims to simplify the production of
# textual languages. They are independent from the 
# problem at hand and could be reused in other 
# transformation generating text as output.
#---------------------------------------------------------


# for instance a function to indent a multi line string if
# needed, or to wrap long lines after 80 characters, etc.

#---------------------------------------------------------
#           Transformation functions: UML2OCL
#---------------------------------------------------------
# The functions below transform each element of the
# UML metamodel into relevant elements in the OCL language.
# This is the core of the transformation. These functions
# are based on the helpers defined before. They can use
# print statement to produce the output sequentially.
# Another alternative is to produce the output in a
# string and output the result at the end.
#---------------------------------------------------------



# examples

def umlEnumeration2OCL(enumeration):
    """
    Generate USE OCL code for the enumeration
    """
    print "enum " + enumeration.name + " {"
    for attribut in enumeration.value :
        if attribut == enumeration.value[-1]:
            print "\t" + attribut.name 
        else :
            print "\t" + attribut.name + ","
    print "}"
    
   
def umlClasse2OCL(classe):
    """
    Generate USE OCL basic type. Note that
    type conversions are required.
    """
    if classe.linkToAssociation : #gere les associationClass
        print "associationclass "+classe.name + umlHeritageClass2OCL(classe)
        print "between"
        for roles in classe.linkToAssociation.associationPart.end:
            umlRoles2OCL(roles)
    else :
        print "class "+classe.name + umlHeritageClass2OCL(classe)  
    if len(classe.ownedAttribute)!=0: #gere les attributs
        umlAttribute2OCL(classe.ownedAttribute)
    if len(classe.ownedOperation)!=0: #gere les operations
        umlOperation2OCL(classe.ownedOperation)
    print "end"
    
def umlHeritageClass2OCL(classeBase):
    heritage = ""
    for parent in classeBase.parent:
        heritage +=  " < " + parent.superType.name
    return heritage
    
def umlAttribute2OCL(attributes):
    print "attributes"
    for attribute in attributes:
        print "\t"+attribute.name+" : "+ umlType2OCL(attribute.type) 

def umlType2OCL(type):
    """
    Generate USE OCL basic type. Note that
    type conversions are required.
    """
    if type.name == "integer" :
        return "Integer"
    elif type.name == "boolean" :
        return "Boolean"
    elif type.name == "string" :
        return "String"
    return type.name
    
def umlOperation2OCL(operations):
    print "operations"
    for operation in operations:
        print "\t"+operation.name+"() : "
    
   
def umlAssociation2OCL(association):
    """
    association IsInBedroom
    between
        Bathroom[0..3] role bathrooms
        Bedroom[0..1] role bedroom
    end
    """
    print "association " + association.name
    print "between"
    for roles in association.end:
        umlRoles2OCL(roles)
    print "end"

def umlRoles2OCL(roles):
    if roles.multiplicityMax == "*" or roles.multiplicityMax == roles.multiplicityMin:
        print "\t" + roles.oppositeOwner.owner.name + "["+ roles.multiplicityMax +"] role " + roles.name
    else :
        print "\t" + roles.oppositeOwner.owner.name + "[" + roles.multiplicityMin + ".." + roles.multiplicityMax + "] role " +  roles.name
    #roles.oppositeOwner.owner.name // roles.target.name


def package2OCL(package):
    """
    Generate a complete OCL specification for a given package.
    The inner package structure is ignored. That is, all
    elements useful for USE OCL (enumerations, classes, 
    associationClasses, associations and invariants) are looked
    recursively in the given package and output in the OCL
    specification. The possibly nested package structure that
    might exist is not reflected in the USE OCL specification
    as USE is not supporting the concept of package.
    """




#---------------------------------------------------------
#           User interface for the Transformation 
#---------------------------------------------------------
# The code below makes the link between the parameter(s)
# provided by the user or the environment and the 
# transformation functions above.
# It also produces the end result of the transformation.
# For instance the output can be written in a file or
# printed on the console.
#---------------------------------------------------------

# (1) computation of the 'package' parameter
# (2) call of package2OCL(package)
# (3) do something with the result


if len(selectedElements)==0:   
# indentation is important since they are no { }
    print indent(4)+"Ah no, sorry. You have no selected elements."
    print indent(8,'*')+'Play again.'
    print indent(8,character='')+'Please!'

else:
    for e in selectedElements:
        classes = e.origin.ownedElement
    for element in classes:
        if isinstance(element, Class):
            umlClasse2OCL(element)
        if isinstance(element, Enumeration):
            umlEnumeration2OCL(element)
    associations = associationsInPackage(selectedElements)
    for association in associations:
        umlAssociation2OCL(association)
    
