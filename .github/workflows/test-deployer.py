#!/usr/bin/python3

import sys
import os
import json
import re

# ./test-deployer [flag] [parameter]
#
# flag = --generate [type]    (generate the .json file from test type)
# flag = --replace [path]  (replace the main.c from the .json path)
#


if len(sys.argv) <= 2:
	print("\n")
	print("Wrong arguments")
	print("Use: ./test-deployer [flag] [parameter]")
	print("\n")
	sys.exit(1)

else:
	if sys.argv[1] == "--generate":
		# Get the directory path and list from input argument
		path = "./tests/" + sys.argv[2] + "/"
		dir_list = os.listdir(path)
		print(len(dir_list), "test files detected in " + sys.argv[2] + " folder")
		
		dummy_dict = {
		  "include": []
		}

		for file in dir_list:
			var_name = file
			var_type = sys.argv[2]
			var_path = path + file
			inner_dict = {"name": var_name, "type": var_type, "path": var_path}
			dummy_dict["include"].append(inner_dict)

		# Convert into JSON:
		target_json = json.dumps(dummy_dict)
		
		# Write into file
		with open("./.github/workflows/test-list.json","w") as json_file: 
			json_file.write(target_json)
		json_file.close()

		print("JSON file created successfully for " + sys.argv[2] + " folder")
		sys.exit(0)


	elif sys.argv[1] == "--replace":

		main_path = "main.c" 
		test_path = sys.argv[2]

		# open both files 
		with open(test_path,"r") as src_file, open(main_path,"w") as dst_file: 
			# read content from first file 
			for line in src_file: 
				# Search for the "#define _MAIN_" directive
				directive_flag = re.search("#define _MAIN_", line)				
				# If the directive was found, then skip this iteration to not copy this line.
				if directive_flag is not None:
					continue
				# write content to second file 
				dst_file.write(line)
			print("Main file replaced by the test file successfully")

		src_file.close()
		dst_file.close()

		sys.exit(0)

	else:
		print("\n")
		print("Wrong arguments")
		print("\n")
		print("Use: ./test-deployer [flag] [parameter]")
		print("\n")
		sys.exit(1)









