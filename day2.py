import os.path
import glob
name=r"C:\Users\Swetha\day5Assignment.py"
max_size=0
file_name=""
def directory_list(name):
    global max_size
    global file_name
    size=0
    lst=glob.glob(f"{name}"+"\\*")
    for item in lst:
        if os.path.isdir(item):
            directory_list(item)
        else:
            size=os.path.getsize(f"{item}")
            if max_size<size:
                max_size=size
                file_name=file_name+os.path.basename(f"{item}")
    return max_size,file_name
print(directory_list(name))
                
