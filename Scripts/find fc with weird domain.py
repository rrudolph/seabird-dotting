import arcpy

arcpy.env.workspace = r"C:\GIS\Projects\Seabird\BRPE Dotting Database\Sample data Jan 2022\Seabird_Photo_Dotting\Seabird_Photo_Dotting.gdb"

fcs = arcpy.ListFeatureClasses()

for fc in fcs:
	fields = arcpy.ListFields(fc)
	for field in fields:
		if field.domain == "SUBCOLONY_1":
			print(f"Featureclass: {fc} Field Name: {field.name}  Domain Name: {field.domain}")