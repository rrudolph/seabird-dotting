# Code for quickly matching the invasive species geodatabase domain with a pick-list in the
# trimble data dictionary.  Specify the domain name to processes below. Output will be a csv
# file. Open this file in a text editor such as Sublime Text.  Paste in values (including the commas)
# into the batch values field in the data dictionary editor. 

print("Importing arcpy module")
import arcpy
arcpy.env.overwriteOutput = True
inWorkspace = r"C:\GIS\Projects\Seabird\BRPE Dotting Database\BRPE_Dotting_ver2.gdb"
outFolder = r"C:\GIS\Projects\Seabird\BRPE Dotting Database\domains\\"

outWorkspace = r"C:\GIS\Projects\Seabird\BRPE Dotting Database\FreshDB.gdb"

arcpy.env.workspace = inWorkspace

domainList = arcpy.da.ListDomains(inWorkspace)

for domain in domainList:
	print(domain.name)

	domainName = domain.name

	outTable = inWorkspace + "/" + domainName + "_DomainToTable"

	print("Running table to domain...")
	arcpy.DomainToTable_management(in_workspace=inWorkspace,
	domain_name=domainName,
	out_table=outTable,
	code_field="Code",
	description_field="Description",
	configuration_keyword="")


	print("Using search cursor to extract domain items...")
	itemsDict = {}
	with arcpy.da.SearchCursor(outTable, ["Code","Description"]) as cursor:
		for row in cursor:
			code = row[0]
			desc = row[1]
			print(desc, code)
			itemsDict.update({desc: desc})

	# print(items)

	print("Creating domain")

	arcpy.CreateDomain_management(outWorkspace, domainName, domainName, 
                              "TEXT", "CODED")

	print(itemsDict)

	for code in itemsDict:
		arcpy.AddCodedValueToDomain_management(outWorkspace, domainName, code, code)

print("Done.")