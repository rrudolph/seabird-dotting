# Testing and/or experimental script, you can safely ignore this. 
# Testing it out, implemented in the main pyt file

print("Importing modules")
# import arcpy
import yaml, pathlib

def get_config():
    here = pathlib.Path(__file__).parent
    with open(here.joinpath("..","SupportFiles","Dotting_domains.yaml")) as f:
        data = yaml.safe_load(f)
        return data

domain_dict = get_config()
# print(domain_dict)
for domain_name, domain_list in domain_dict.items():
	print(domain_name, "---",domain_list)



# outWorkspace = r"C:\GIS\Projects\Seabird\BRPE Dotting Database\test.gdb"

# for domain, domain_list in domain_dict.items():
# 	# print(type(domain_list))
# 	print(domain, domain_list)

# 	domain_list.sort()

# 	print("Creating domain {}".format(domain))
# 	arcpy.CreateDomain_management(outWorkspace, 
# 		domain,
# 		domain,
# 		"TEXT",
# 		"CODED")

	
# 	for code in domain_list:
# 		print("Adding {} to domain".format(code))
# 		arcpy.AddCodedValueToDomain_management(outWorkspace, domain, code, code)

# print("Done.")