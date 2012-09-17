"""W3C XML Schema Compiler"""

__version__="$Revision: 1.6 $"
# $Id: __init__.py,v 1.6 2004-07-01 13:26:18 ht Exp $

# I force every schema document to be validated, either by the
# DTD or the schema for schemas, so there is no need to check for
# required daughters, attributes, etc.

# SSchema is the equivalent of the REC's 'schema component'.
# Schema is an implementation artefact -- it holds all the components
# which share a target namespace
# During schema document reading, the 'current' schema is the one being
# worked on.

# There are _3_ layers of representation here:
# 1) The XML elements themselves, instances of 'element',
#    usually held in a variable/property called 'elt' [implemented in XML]
# 2) Their normalised internal form, instances of e.g. complexTypeElt or anyElt
#    usually held in a variable/property called 'xrpr' [implemented in
#    XMLSchemaElt]
# 3) The corresponding schema component, instances of e.g. complexType or any,
#    usually held in a variable/property called 'component'

# The paradigm is that xxxElt.__init__ plugs in the schema and provides empty
# lists/dicts for daughters/attrs to go in, xxxElt.init (called once
# all daughters/attrs have been processed) creates and attaches component(s),
# component.init copies literal properties and attaches sub-components where
# possible

# Most components have properties with names based on those in the REC
# If a property is component-valued, it will have a clause in the
# component's class's __getattr_, which attempts to dereference the
# corresponding <prop>Name property, c.f. basetype/basetypeName for simpleType

# I've innovated one component not in the REC, namely attributeUse,
# parallel to particle

# Thinking about the interaction between lazy chasing of references and
# SVC constraints -- I think the REC isn't capable of a consistent
# interpretation here.  My inclination is to implement SVCs on an
# as-used basis.  I could try putting a 'checked' attribute on every component,
# dividing the computed attributes into literals and non-literals, and
# testing 'checked' before returning _any_ non-literals.
# Note that anything along this line means that schema errors may occur
# in the midst of instance validation :-(  What's the desired interaction
# with lax validation/validation outcome?

# This file contains global constants only --
# all the action is in the class files in this package

# Constants

__all__=["AbInitio",
        "Annotation",
        "AnyAttribute",
        "Attribute",
        "AttributeGroup",
        "AttributeUse",
        "ComplexType",
        "Component",
        "DDummy",
        "Element",
        "Facet",
        "Group",
        "Init",
        "KCons",
        "List",
        "ListFacet",
        "NumFacet",
        "Particle",
        "QName",
        "Restriction",
        "SSchema",
        "Schema",
        "SchemaError",
        "SimpleType",
        "SimType",
        "Type",
        "Union",
        "Ur",
        "VMapping",
        "Wildcard"]

XMLSchemaNS="http://www.w3.org/2001/XMLSchema"
XMLSchemaInstanceNS = "http://www.w3.org/2001/XMLSchema-instance"
XMLNS='http://www.w3.org/XML/1998/namespace'
AST='anySimpleType'

builtinLists=[('NMTOKENS','NMTOKEN',0),
              ('ENTITIES','ENTITY',0),
              ('NOTATIONS','NOTATION',0),
              ('IDREFS','IDREF',3)]

vss="$Revision: 1.6 $ of $Date: 2004-07-01 13:26:18 $".split()

versionString="%s of %s %s"%(vss[1],vss[5],vss[6])

# Globals

eltClasses={}                           # initialised in elts.Init.init

psviIndMap={}                           # initialised in Init.init
builtinTypeNames=[]                     # initialised in Init.init
builtinPats=[]                     # initialised in Init.init
auxComponentMap={}                         # initialised in Init.init

abInitioTypes=[]                        # initialised in AbInitio.init

simpleTypeMap={}                        # initialised in setupIndRefl

def init():
  from Init import init
  from XSV.compile.NumFacet import init as nfInit
  init()
  nfInit()
  import XSV.validate as validate
  validate.cInit()

# $Log: __init__.py,v $
# Revision 1.6  2004-07-01 13:26:18  ht
# break an import loop
#
# Revision 1.5  2002/12/01 21:54:59  ht
# add and inherit idt (identity constraint type) to type defs
#
# Revision 1.4  2002/11/25 10:39:01  ht
# pervasive changes to shift to using values for simple types where required by REC
#
# Revision 1.3  2002/09/23 21:47:19  ht
# move to string methods from string library
#
# Revision 1.2  2002/08/21 08:55:30  ht
# add global
#
# Revision 1.1  2002/06/28 09:40:23  ht
# XSV as package: components
#
