"""
Author: Rocky Rudolph
Date: 7/1/2019
Purpose: Custom tools for seabird "dotting" data collection.  ArcMap was the chosen software
to dot stitched photos of seabird colonies on Anacapa and Santa Barbara Islands.  Each stitched photo
will be dotted in an mxd file.  These tools will assist data entry staff automate with processes that help 
create a consistent dataset. Can be used with ArcGIS Pro.

"""

import arcpy
import os
import datetime
import pathlib
import random
import subprocess
from dateutil.parser import parse

def msg(string):
    print(string)
    arcpy.AddMessage(string)

def find_python2():
    possible_versions = range(4,10)
    for ver in possible_versions:
        path  = r"C:\Python27\ArcGIS10.{}\python.exe".format(ver)
        # print(path)
        if os.path.exists(path):
            return path

try:
    import yaml
except:

    py_path = find_python2()

    if py_path:
        msg(py_path)

        # implement pip as a subprocess:
        subprocess.check_call([py_path, '-m', 'pip', 'install', 'pyyaml'])

    else:
        msg("Error importing pyyaml or couldn't find python path")





class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Seabird Dotting Tools"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [
            GenerateNewGDB,
            CreateNewDotting,
            CalculateFields,
            GenerateXLS
        ]

class GenerateNewGDB(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Generate New Geodatabase"
        self.description = "Creates a new blank geodatabase with pick list domains. Will need to create a new dotting file afterwards."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        param0 = arcpy.Parameter(
        displayName="File Folder Path",
        name="path",
        datatype="GPString",
        parameterType="Required",
        direction="Input")


        param1 = arcpy.Parameter(
        displayName="Geodatabase Name",
        name="gdb_name",
        datatype="GPString",
        parameterType="Required",
        direction="Input")


        params = [param0, param1]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        # Dynamic variables
        path = parameters[0].valueAsText
        gdb_name = parameters[1].valueAsText

        def get_config():
            here = pathlib.Path(__file__).parent
            with open(here.joinpath("SupportFiles","Dotting_domains.yaml")) as f:
                return yaml.safe_load(f)
                

        domain_dict = get_config()

        if not gdb_name.endswith(".gdb"):
            gdb_name = gdb_name + ".gdb"

        out_gdb = os.path.join(path, gdb_name)
        msg("Creating file geodatabase: {}".format(out_gdb))

        arcpy.management.CreateFileGDB(path, gdb_name, "CURRENT")

        for domain, domain_list in domain_dict.items():

            domain_list.sort()

            msg("Creating domain {}".format(domain))
            arcpy.CreateDomain_management(out_gdb, 
                domain,
                domain,
                "TEXT",
                "CODED")
            
            for code in domain_list:
                msg("Adding {} to domain".format(code))
                arcpy.AddCodedValueToDomain_management(out_gdb, domain, code, code)

        msg("Done.")

        return



class CreateNewDotting(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create New Dotting File"
        self.description = "Creates a new featureclass to start dotting a survey area."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        param0 = arcpy.Parameter(
        displayName="Target Database",
        name="targetDB",
        datatype="GPString",
        parameterType="Required",
        direction="Input")

        param1 = arcpy.Parameter(
        displayName="Survey Date",
        name="surveyDate",
        datatype="GPDate",
        parameterType="Required",
        direction="Input")

        param2 = arcpy.Parameter(
        displayName="Survey Area",
        name="surveyArea",
        datatype="GPString",
        parameterType="Required",
        direction="Input")

        # param0.value = r"C:\GIS\Projects\Seabird\BRPE Dotting Database\test.gdb"

        params = [param0, param1, param2]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        # Hard variables
        srcDir = os.path.dirname(os.path.realpath(__file__))

        # Dynamic variables
        targetDB = parameters[0].valueAsText
        surveyDate = parameters[1].valueAsText
        surveyArea = parameters[2].valueAsText

        arcpy.env.workspace = targetDB
        srcDir = os.path.dirname(os.path.realpath(__file__))
        templateFC = os.path.join(srcDir,"SupportFiles", "Template.gdb", "TemplateFC")

        newFCName = "Dot_" + surveyArea + "_" + parse(surveyDate).strftime("%Y_%m_%d")
        newFCName = newFCName.replace(" ", "")

        geometry_type = "POINT"
        has_m = "DISABLED"
        has_z = "DISABLED"

        # Use Describe to get a SpatialReference object
        spatial_ref = arcpy.Describe(templateFC).spatialReference

        # Execute CreateFeatureclass
        msg("Creating featureclass {}".format(newFCName))
        arcpy.CreateFeatureclass_management(targetDB, newFCName, geometry_type, templateFC, 
                                            has_m, has_z, spatial_ref)

        # domNames = ["BIRD", "CHICK_CLASS", "DOTTER_ID", "ISLAND", "NEST", "SPECIES", "SUBCOLONY"]
        domNames = [domain.name for domain in arcpy.da.ListDomains(targetDB)]
        msg("Domains:")
        msg(domNames)
        for dom in domNames:
            if dom == "SUBCOLONY_1":
                msg("Skipping bogus SUBCOLONY_1 domain")
                pass
            else:
                msg("Assigning domain {} to field of same name".format(dom))
                arcpy.AssignDomainToField_management(newFCName, dom, dom)

        msg("Done.")
        return


class CalculateFields(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Calculate Fields"
        self.description = "Batch calculates common fields in a dotting file."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        param0 = arcpy.Parameter(
        displayName="Input Featureclass",
        name="inFC",
        datatype="GPString",
        parameterType="Required",
        direction="Input")

        param1 = arcpy.Parameter(
        displayName="Survey Date",
        name="DATE",
        datatype="GPDate",
        parameterType="Optional",
        direction="Input")

        param2 = arcpy.Parameter(
        displayName="Analisys Date",
        name="DOTTED_DATE",
        datatype="GPDate",
        parameterType="Optional",
        direction="Input")

        param3 = arcpy.Parameter(
        displayName="Dotter ID",
        name="DOTTER_ID",
        datatype="GPString",
        parameterType="Optional",
        direction="Input")
        param3.filter.type="ValueList"

        param4 = arcpy.Parameter(
        displayName="Island",
        name="ISLAND",
        datatype="GPString",
        parameterType="Optional",
        direction="Input")
        param4.filter.type="ValueList"

        param5 = arcpy.Parameter(
        displayName="Subcolony",
        name="SUBCOLONY",
        datatype="GPString",
        parameterType="Optional",
        direction="Input")
        param5.filter.type="ValueList"

        param6 = arcpy.Parameter(
        displayName="Species",
        name="SPECIES",
        datatype="GPString",
        parameterType="Optional",
        direction="Input")
        param6.filter.type="ValueList"

        param7 = arcpy.Parameter(
        displayName="Photo Path",
        name="PHOTO_PATH",
        datatype="GPString",
        parameterType="Optional",
        direction="Input")
        
        params = [param0, param1, param2, param3, param4, param5, param6, param7]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        def getDomainList(inputDB, domainName):
            domains = arcpy.da.ListDomains(inputDB)
            for domain in domains:
                if domain.name == domainName:
                    typeList = [val for val, desc in domain.codedValues.items()]
                    typeList.sort()
                    return typeList

        inDB = arcpy.Describe(parameters[0].valueAsText).path
        if parameters[0].altered:
            parameters[3].filter.list = getDomainList(inDB, "DOTTER_ID")
            parameters[4].filter.list = getDomainList(inDB, "ISLAND")
            parameters[5].filter.list = getDomainList(inDB, "SUBCOLONY")
            parameters[6].filter.list = getDomainList(inDB, "SPECIES")

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        
        def calcField(field, contents):
            msg("Calculating field " + str(field))
            arcpy.CalculateField_management(
                in_table=inFC, 
                field=field, 
                expression='"{}"'.format(contents), 
                expression_type="PYTHON_9.3", 
                code_block="")


        # Dynamic variables
        inFC = parameters[0].valueAsText
        SURVEY_DATE = parse(str(parameters[1].value)).strftime("%m/%d/%Y")
        DOTTED_DATE = parse(str(parameters[2].value)).strftime("%m/%d/%Y")
        DOTTER_ID = parameters[3].valueAsText
        ISLAND = parameters[4].valueAsText
        SUBCOLONY = parameters[5].valueAsText
        SPECIES = parameters[6].valueAsText
        PHOTO_PATH = parameters[7].valueAsText

        if SURVEY_DATE is not None:
            calcField("SURVEY_DATE", SURVEY_DATE)

        if DOTTED_DATE is not None:
            calcField("DOTTED_DATE", DOTTED_DATE)

        if DOTTER_ID is not None:
            calcField("DOTTER_ID", DOTTER_ID)

        if ISLAND is not None:
            calcField("ISLAND", ISLAND)

        if SUBCOLONY is not None:
            calcField("SUBCOLONY", SUBCOLONY)

        if SPECIES is not None:
            calcField("SPECIES", SPECIES)

        if PHOTO_PATH is not None:
            calcField("PHOTO_PATH", PHOTO_PATH)

        msg("Done.")
        return


class GenerateXLS(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Merge and Generate Spreadsheet"
        self.description = "Creates a merged MS Excel spreadsheet of all featureclasses from the target database."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        param0 = arcpy.Parameter(
        displayName="Input database(s)",
        name="inputDB",
        datatype="GPString",
        parameterType="Required",
        direction="Input",
        multiValue=True)

        param1 = arcpy.Parameter(
        displayName="Output Directory",
        name="outDir",
        datatype="GPString",
        parameterType="Required",
        direction="Input")

        param2 = arcpy.Parameter(
        displayName="Overwrite Output?",
        name="Overwrite",
        datatype="GPBoolean",
        parameterType="Optional",
        direction="Input")  

        params = [param0, param1, param2]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        
        inputDBs = parameters[0].valueAsText.replace("'", "").split(";")

        outDir = parameters[1].valueAsText
        Overwrite = parameters[2].valueAsText
        msg("Overwrite output setting: " + str(Overwrite))

        if Overwrite == "true":
            arcpy.env.overwriteOutput = True
        else:
            arcpy.env.overwriteOutput = False

        now = datetime.datetime.today()

        outName = "Seabird_Dotting_Export_Table_" + now.strftime("%Y_%m_%d_%H_%M") + ".xls"
        msg(outName)
        outFile = os.path.join(outDir, outName)
        mergeList = []

        tempFC = "in_memory/Merge"

        for inputDB in inputDBs:

            arcpy.env.workspace = inputDB
            fcs = arcpy.ListFeatureClasses()

            for fc in fcs:
                msg("Creating merge list for " + fc)
                mergeList.append(os.path.join(inputDB, fc))

        msg("Merging: {}".format(mergeList))
        arcpy.Merge_management(
            inputs=mergeList, 
            output=tempFC
            )

        msg("Generating xls: " + outFile)
        arcpy.TableToExcel_conversion(tempFC, outFile)

        msg("Deleting temp data")
        arcpy.Delete_management(tempFC)
        del tempFC


        msg("Done.")
        return
