# Author: Erwin-Iosef
# Date: 2/Feb/2025
# commented lines are for debugging purposes
import os
import shutil
#Set your directory where your non-colourable icons are:

svg_mod='''<defs>
  <style id="current-color-scheme" type="text/css">
    .ColorScheme-Text { color:#444444; }
    .ColorScheme-Highlight { color:#4285f4; }
    .ColorScheme-NeutralText { color:#ff9800; }
    .ColorScheme-PositiveText { color:#4caf50; }
    .ColorScheme-NegativeText { color:#f44336; }
  </style>
</defs>'''

def mainctrl(SVG_DIR):
    for (root,dirs,files) in os.walk(SVG_DIR):
        for file in files:
            file=os.path.join(root,file)
            if os.path.islink(file) or os.path.getsize(file)==0:
                continue
            if file.endswith(".svg"):
                #print(file)
                CheckSVG(file)

def CheckSVG(refsvg):
    modcheck=['class="ColorScheme-Text"', "fill:currentColor", svg_mod ]
    
    with open(refsvg, 'r+', encoding="utf-8") as svgfile:
        lines=svgfile.readlines()
        linesjoined=''.join(lines)
                    
        if  all(string in linesjoined for string in modcheck):
            print(f"{refsvg} This file already modified")
            return

        elif "fill:#444444" in linesjoined:
            svgfile.seek(0)
            content=ModSVG(refsvg,lines,linesjoined)
            #print(content)
            svgfile.truncate(0)
            svgfile.writelines(content)
            print(f"{refsvg} rewritten successfully")

def ModSVG(refsvg,lines,linesjoined):
        content=[]
        exceptlines=['success','error','warning']
        for line in lines:
                # Lines of SVGs which contain these classes are not modified, such as full-coloured battery icons.
                if any(string in line for string in exceptlines):
                    content.append(line)
                    #print(f"{refsvg} exception string found skipping")
                    continue
                
                elif line.strip().startswith("<svg"):
                    content.append(line + svg_mod + '\n')    
                    continue
                
                elif 'class="ColorScheme-Text"' not in line.strip():
                    line=line.replace('style="fill:#444444"','class="ColorScheme-Text" style="fill:currentColor"')
                    line=line.replace('style="opacity:0.35;fill:#444444"','class="ColorScheme-Text" style="opacity:.35;fill:currentColor"')
                    
                if "fill:currentColor" not in line.strip():
                    #print("added fill:#4444444")
                    line=line.replace("fill:#444444",'fill:currentColor')
                    
                content.append(line)
        #print(content)
        return content

def Backup(SVG_DIR):
    backup=input("Create backup of SVG directory?(y or n) ")
    if backup=="y":
        try:
            backupfolder="svgsbak"
            backupdir=os.path.join(SVG_DIR,os.pardir,backupfolder)
            backupdir=os.path.abspath(backupdir)
            shutil.copytree(SVG_DIR,backupdir,symlinks=True)
        except FileExistsError:
            overwrite=input("Directory already exists. Overwrite?(y or n) ")
            if overwrite=="y":
                shutil.rmtree(backupdir)
                shutil.copytree(SVG_DIR,backupdir,dirs_exist_ok=True,symlinks=True)
            elif overwrite=="n":
                return
            else:
                overwrite=input("Directory already exists. Overwrite?(y or n) ")
        finally:
                print(f"Backupfolder {backupdir} is created")
    elif backup=="n":
        return
    else: 
        backup=input("Create backup of SVG directory?(y or n) ")

def startup():
    SVG_DIR=input("Input your SVG directory here(copy and paste absolute path):")
    if os.path.exists(SVG_DIR)==False:
        raise ValueError("Invalid path!")
        exit()
        
    sure=input(f"{SVG_DIR} \n Is this path correct?(y) ")
    if sure=="y":    
        start=input("Begin?(y or n) ")
        if start=="y":
            Backup(SVG_DIR)
            mainctrl(SVG_DIR)
        elif start=="n":
            exit()
        else:
            start=input("Begin?(y or n) ")
    else:
        SVG_DIR=input("Input your SVG directory here(copy and paste absolute path):")
        
startup()
