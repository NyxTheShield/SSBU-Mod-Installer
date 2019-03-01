import imgui
import imguihelper
import os
import _nx
import runpy
import sys
from imgui.integrations.nx import NXRenderer
from nx.utils import clear_terminal
import sys
import os
import time

def _isValidHex(s):
    try:
        int(s, 16)
        return True
    except:
        return False

def getFileBaseName(path):
    filename = os.path.split(path)[-1]
    return filename.split('.')[0]

def installMod(archive, modFilename):
    offset = int(getFileBaseName(modFilename), 16)
    archive.seek(offset)
    with open(modFilename, 'rb') as f:
        modContents = f.read()
        modSize = len(modContents)
        backup = archive.read(modSize)
        if not os.path.exists(modFilename + '.backup'):
            with open(modFilename + '.backup', 'wb') as f_backup:
                f_backup.write(backup)
        archive.seek(offset)
        archive.write(modContents)
    print("Mod '{}' successfully installed".format(modFilename))

def uninstallMod(archive, modFilename):
    offset = int(getFileBaseName(modFilename), 16)
    archive.seek(offset)
    with open(modFilename, 'rb') as f:
        modContents = f.read()
        modSize = len(modContents)
        backup = archive.read(modSize)
        archive.seek(offset)
        archive.write(modContents)
    os.remove(modFilename)
    print("Mod '{}' successfully uninstalled".format(modFilename))

sys.argv = [""]  # workaround needed for runpy

def colorToFloat(t):
    nt = ()
    for v in t:
        nt += ((1/255) * v, )
    return nt

# (r, g, b)
FOLDER_COLOR = colorToFloat((230, 126, 34))
PYFILE_COLOR = colorToFloat((71, 123, 209))
FILE_COLOR = colorToFloat((41, 128, 185))
TILED_DOUBLE = 1
state = "file_manager"


def run_python_module(mod: str, mode):
    # clear both buffers
    imguihelper.clear()
    imguihelper.clear()
    _nx.gfx_set_mode(TILED_DOUBLE)
    clear_terminal()
    if not os.path.exists("data.arc"):
        print("Make sure you're running the script beside your data.arc")
        renderer.shutdown()
    else:
        with open('data.arc', 'r+b') as archive:
            if not os.path.exists(mod):
                print("'{}' not valid mod path".format(mod))
                renderer.shutdown()
            fileName = getFileBaseName(mod)
            if not _isValidHex(fileName):
                print("Filename '{}' not valid hex number".format(fileName))
                renderer.shutdown()

            if mode == 1:
                installMod(archive, mod)
            else:
                uninstallMod(archive, mod)
            global state
            state = "installed"
    imguihelper.initialize()
    

def main():
    global state
    ctime = 0
    renderer = NXRenderer()
    if os.path.isdir("sdmc:/ReiNX"):
        currentDir = "sdmc:/ReiNX/titles/01006A800016E000/romfs"
        os.chdir(currentDir)
    else:
        currentDir = "sdmc:/Atmosphere/titles/01006A800016E000/romfs"
        os.chdir(currentDir)

    while True:
        while state == "file_manager":
            renderer.handleinputs()

            imgui.new_frame()

            width, height = renderer.io.display_size
            imgui.set_next_window_size(width, height)
            imgui.set_next_window_position(0, 0)
            imgui.begin("", 
                flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_SAVED_SETTINGS
            )
            
            imgui.text("   __________ ____  __  __   __  _______  ____     _____   ________________    __    __    __________  ")
            imgui.text("  / ___/ ___// __ )/ / / /  /  |/  / __ \/ __ \   /  _/ | / / ___/_  __/   |  / /   / /   / ____/ __ \ ")
            imgui.text("  \__ \\__ \/ __  / / / /  / /|_/ / / / / / / /   / //  |/ /\__ \ / / / /| | / /   / /   / __/ / /_/ / ")
            imgui.text(" ___/ /__/ / /_/ / /_/ /  / /  / / /_/ / /_/ /  _/ // /|  /___/ // / / ___ |/ /___/ /___/ /___/ _, _/  ")
            imgui.text("/____/____/_____/\____/  /_/  /_/\____/_____/  /___/_/ |_//____//_/ /_/  |_/_____/_____/_____/_/ |_|   ")
            imgui.text("") 
            imgui.text("Created by NyxTheShield")
            imgui.text("Based on jam1garner Mod Installer")
            imgui.text("")
            imgui.text("Select the Mod to Install!")

            dirs = []
            files = []
            backups = []
            
            for e in os.listdir():
                if os.path.isdir(e):
                    dirs.append(e)
                else:
                    if not e.endswith(".exe") and not e.endswith(".bat") and not e.endswith(".backup") and not e.endswith(".arc"):
                        files.append(e)
                    if e.endswith(".backup"):
                        backups.append(e)
            
            dirs = sorted(dirs)
            files = sorted(files)
            backups = sorted(backups)
                
            for e in files:
                if not e.endswith(".exe") and not e.endswith(".bat") and not e.endswith(".backup") and not e.endswith(".arc"):
                    imgui.push_style_color(imgui.COLOR_BUTTON, *PYFILE_COLOR)
                if imgui.button("Install "+e, width=400, height=60) and not e.endswith(".exe") and not e.endswith(".bat") and not e.endswith(".backup") and not e.endswith(".arc"):
                    ctime = time.time()
                    run_python_module(e, 1)

                imgui.pop_style_color(1)

            for e in backups:
                if e.endswith(".backup"):
                    imgui.push_style_color(imgui.COLOR_BUTTON, *FOLDER_COLOR)
                if imgui.button("Uninstall "+e, width=400, height=60) and e.endswith(".backup"):
                    ctime = time.time()
                    run_python_module(e, 2)

                imgui.pop_style_color(1)

            
            imgui.end()
            imgui.render()
            renderer.render()

        while state == "installed":

            imgui.new_frame()

            width, height = renderer.io.display_size
            imgui.set_next_window_size(width, height)
            imgui.set_next_window_position(0, 0)
            imgui.begin("", 
                flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_SAVED_SETTINGS
            )
            
            if time.time()- ctime > 5:
                state = "file_manager"
                ctime = 0
            imgui.text("    __  ___          __   ____           __        ____         __   _____                                ____      ____      ____")
            imgui.text("   /  |/  /___  ____/ /  /  _/___  _____/ /_____ _/ / /__  ____/ /  / ___/__  _______________  __________/ __/_  __/ / /_  __/ / /")
            imgui.text("  / /|_/ / __ \/ __  /   / // __ \/ ___/ __/ __ `/ / / _ \/ __  /   \__ \/ / / / ___/ ___/ _ \/ ___/ ___/ /_/ / / / / / / / / / /") 
            imgui.text(" / /  / / /_/ / /_/ /  _/ // / / (__  ) /_/ /_/ / / /  __/ /_/ /   ___/ / /_/ / /__/ /__/  __(__  |__  ) __/ /_/ / / / /_/ /_/_/")
            imgui.text("/_/  /_/\____/\__,_/  /___/_/ /_/____/\__/\__,_/_/_/\___/\__,_/   /____/\__,_/\___/\___/\___/____/____/_/  \__,_/_/_/\__, (_|_)")   
            imgui.text("                                                                                                                    /____/  ")     

            imgui.end()
            imgui.render()
            renderer.render()
    



if __name__ == "__main__":
    main()

