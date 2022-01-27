# Testing and/or experimental script, you can safely ignore this. 

print("Importing modules")
import arcpy, os
from dateutil.parser import parse

# Hard variables
srcDir = os.path.dirname(os.path.realpath(__file__))
inXML =  srcDir + os.sep + "TEST_SCHEMA_EXPOR.xml"


# Dynamic variables
targetDB = "C:/GIS/Projects/Seabird/BRPE Dotting Database/test.gdb"
surveyDate = "4/7/2019"
surveyArea = "Ampitheatre"

arcpy.env.workspace = targetDB

newFCName = "BRPE_" + parse(surveyDate).strftime("%Y_%m_%d") + "_" + surveyArea

print("Imprting xml")
arcpy.ImportXMLWorkspaceDocument_management(
	target_geodatabase=targetDB, 
	in_file=inXML, 
	import_type="SCHEMA_ONLY", 
	config_keyword="")

print("Copying features")
arcpy.CopyFeatures_management("NewFC", newFCName)

print("Deleting initial import")
arcpy.Delete_management("NewFC")
