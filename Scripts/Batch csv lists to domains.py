# Testing and/or experimental script, you can safely ignore this. 

print("Importing modules")
import arcpy, csv, glob, os

outWorkspace = r"C:\GIS\Projects\Seabird\BRPE Dotting Database\Seabird_Photo_Dotting.gdb"
csvDir = r"C:\GIS\Projects\Seabird\BRPE Dotting Database\domains"


for csvFile in glob.iglob(os.path.join(csvDir, "*.csv")):
	print(csvFile)
	domainName = csvFile.split("\\")[-1].split(".")[0]
	print(domainName)


	print("Generating domain list")
	descList = []
	with open(csvFile) as csv_file:
	    csv_reader = csv.reader(csv_file, delimiter=',')
	    for row in csv_reader:
	    	print(row[0])
	    	descList.append(row[0])

	print(descList)

	descList.sort()

	print("Creating domain")
	arcpy.CreateDomain_management(outWorkspace, 
		domainName,
		domainName,
		"TEXT",
		"CODED")

	
	for code in descList:
		print("Adding {} to domain".format(code))
		arcpy.AddCodedValueToDomain_management(outWorkspace, domainName, code, code)

print("Done.")