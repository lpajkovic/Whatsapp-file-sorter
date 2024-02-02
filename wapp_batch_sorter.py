import os
import re
import shutil
from tkinter import *
from tkinter import filedialog

class WappBatch:
    def __init__(self, root):
        self.root=root
        root.title("Whatsapp File Sorter")
        
        self.src_dir=StringVar()
        
        self.selectButton=Button(root, text="Select folder", command=self.open_folder)
        self.selectButton.grid(row=0, column=0, padx=5, pady=5)
        
        self.labelPath=Label(root, text="", fg="red")
        self.labelPath.grid(row=0, column=1, padx=5, pady=5)
        
        self.items=[]
        
        self.copyButton=Button(root, text="Copy files", command=lambda:self.execute("copy"))
        self.copyButton.grid(row=1, column=2, padx=5, pady=5)
        
        self.moveButton=Button(root, text="Move files", command=lambda:self.execute("move"))
        self.moveButton.grid(row=1, column=4, padx=5, pady=5)
        
    def YM_extract(self,filename):
        search_pattern=r"IMG_(\d{4})(\d{2})"
        match=re.search(search_pattern,filename)
    
        #returns year and month
        return match.group(1), match.group(2).lstrip("0") if match else (None, None)
        
    def open_folder(self):
        path=filedialog.askdirectory(title="Select folder")
        
        if path:
            self.labelPath.config(text=f"Output folder: {path}")
            self.src_dir.set(path)
            self.get_files()
            
    def get_files(self):
        
        dir_path=self.src_dir.get()
        try:
            for item in os.listdir(dir_path):
                full_path=os.path.join(dir_path, item)
                if os.path.isfile(full_path):
                    self.items.append(item)
            #return [item for item in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path,item))]
    
        except OSError as e:
            print("Error: {e}")
            return None
        
    def create_folder(self,folder_name, parent_folder):
        folder=os.path.join(parent_folder, folder_name)
        os.makedirs(folder, exist_ok=True)
        
        return folder
    
    def execute(self, operation):
        
        for item in self.items:
            year, month=self.YM_extract(item)
            item_path=os.path.join(self.src_dir.get(), item)
            year_path=self.create_folder(year, self.src_dir.get())
            month_path=self.create_folder(month, year_path)
    
            if item.endswith(".jpg"):
                if(operation=="move"):
                    shutil.move(item_path, month_path)
                if(operation=="copy"):
                    shutil.copy2(item_path, month_path)
                    
        os.startfile(self.src_dir.get())

window=Tk()
app=WappBatch(window)
window.mainloop()
        
                
                
                