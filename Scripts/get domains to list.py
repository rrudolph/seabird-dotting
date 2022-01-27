import arcpy  
from itertools import permutations

domains = arcpy.da.ListDomains(r"C:\GIS\Projects\Seabird\BRPE Dotting Database\Seabird_Photo_Dotting.gdb")

# for domain in domains:
# 	# if domain.name == "TYPE":
# 	typeList = [val for val, desc in domain.codedValues.items()]

# 	print(typeList)


species_list = ['BRANDTS CORMORANT', 'BROWN BOOBY', 'BROWN PELICAN', 'DOUBLECRESTED CORMORANT', 'OTHER', 'PELAGIC CORMORANT', 'WESTERN GULL']
nest_type = ['ABANDONED NEST', 'BROOD', 'CHICKS IN NEST', 'EMPTY NEST', 'PARTIALLY BUILT NEST', 'SITE', 'WELL BUILT NEST']
bird_type = ['ADULT', 'DEAD', 'JUVENILE', 'ROOSTING OUT OF NESTING AREA', 'UNKNOWN']
chick_type = ['0-5WK OLD CHICK', '6-8WK OLD CHICK', '9+WK OLD CHICK', 'CHICK', 'DEAD']

for species in species_list:
	for bird in bird_type:
		for nest in nest_type:
			for chick in chick_type:
				if species == 'BROWN PELICAN':
					print(f"{species} - {bird} - {nest} - {chick}")
				else:
					print(f"{species} - {bird} - {nest}")
					break
					

# # Create a table in memory to hold the codes and their descriptions for a particular domain. 
# tempTable = 'in_memory/getCodes'
# getCodes = arcpy.DomainToTable_management(r'C:\GIS\Projects\Seabird\BRPE Dotting Database\test.gdb', 'TYPE',tempTable , 'Code', 'Description')  

# codeList = []
# with arcpy.da.SearchCursor(getCodes, ["Code"]) as cursor:
# 	for row in cursor:
# 		code = row[0]
# 		print(code)
# 		codeList.append(code)



# #Create an empty dictionary. 
# d = {}  
# #Create a cursor to loop through the table holding the domain and code info 
# rows = arcpy.SearchCursor(cvdTable)  
# # Loop through each row in the table. 
# for row in rows:   
# 	print(row)
# 	# For each row in the table populate the key with the code field and the value from the description field  
# 	d[row.codeField] = row.descriptionField 

# 	#Cleanup 
# 	del row
# 	 del rows  # Create a search cursor on the table with the domain 
# 	rows2 = arcpy.SearchCursor(r'C:\vancouver.gdb\TESTFC') 
# 	# Loop through the records in the table. 
# 	for row2 in rows2:   
# 	# Print the dictionary value for each code that is returned from this search cursor   
# 	print d[row2.PipeType] #Cleanup del row del rows   