import os

with open("Install.txt","w") as file:
    for e in os.listdir():  
        if e != "Create_Install_file.py" and e != "Install.txt":
            if "0x" not in e:
                os.rename(e,"0x"+e)
                file.write("0x"+e+"\n")
            else:
                file.write(e+"\n")


