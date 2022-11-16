import os

import sys
from shutil import copyfile

def walk_dir_by_decompyle3(dir,topdown=True):

	for root, dirs, files in os.walk(dir, topdown):

		for name in files:

			if name.endswith('.pyc'):

				part_name = name[0:-4]

				part_file_name = os.path.join(root, part_name)
				name = os.path.join(root, name)
				print(part_file_name)
				result2 = os.popen('decompyle3 -o %s.py %s.pyc'%(part_file_name,part_file_name)).read()
				if("failed" not in result2):
					os.remove(name) # 删除pyc文件
				else:
					copyfile(part_file_name+".py",part_file_name+"_faild2"+".py") # 给py文件重命名
					os.remove(part_file_name+".py")
def walk_dir_by_uncompyle6(dir,topdown=True):

	for root, dirs, files in os.walk(dir, topdown):

		for name in files:

			if name.endswith('.pyc'):

				part_name = name[0:-4]

				part_file_name = os.path.join(root, part_name)
				name = os.path.join(root, name)
				print(part_file_name)
				result2 = os.popen('uncompyle6 -o %s.py %s.pyc'%(part_file_name,part_file_name)).read()
				if("failed" not in result2):
					os.remove(name) # 删除pyc文件
				else:
					copyfile(part_file_name+".py",part_file_name+"_faild"+".py") # 给py文件重命名
					os.remove(part_file_name+".py")




if __name__ == '__main__':

	dirname = r"D:\Users\Desktop\work\app-audible-converter_muti\work"
	# walk_dir_by_decompyle3(dirname)
	walk_dir_by_uncompyle6(dirname)
	

