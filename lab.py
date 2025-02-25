import tkinter as tk
from tkinter import filedialog, Menu, messagebox, PhotoImage
from PIL import Image, ImageTk

window =tk.Tk()

class BMP_Image:
    def __init__(self, editor : tk.Tk):
        self.editor = editor
        editor.geometry("500x500")
        self.icon = PhotoImage(file="ic.png")
        try:
            editor.iconphoto(False, self.icon)
            editor.title("BMP editor")
        except Exception as e:
            print(f"Ошибка загрузки {e}")
        self.image_label = tk.Label(self.editor, bg='gray', width=500, height=500)
        self.image_label.pack(expand=True)
        
        self.menu_bar = Menu(self.editor)
        self.editor.config(menu=self.menu_bar)
        
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Открыть", command=self.open_image)
        self.file_menu.add_command(label="Очистить", command=self.clear_image)
        
        self.file_menu.add_separator()
        
        self.file_menu.add_command(label="Выход", command=self.editor.quit)
        
        self.menu_bar.add_cascade(label="File",menu=self.file_menu)
        
        self.scale_menu = Menu(self.menu_bar, tearoff=0)
        self.scales = {"50%" : 0.5, "100%": 1.0, "150" : 1.5, "200%" : 2.0}
        self.scale_vars = {}
        
        for label, f in self.scales.items():
            self.scale_vars[label] = tk.BooleanVar()
            self.scale_menu.add_radiobutton(label=label, variable=self.scale_vars[label], command=lambda l=label: self.set_scale(l), state="disabled" )
        
        self.menu_bar.add_cascade(label="Scale", menu=self.scale_menu) 
        
        self.original_image = None
        self.current_scale = "100%"  
    def open_image(self):
        file_p = filedialog.askopenfilename(filetypes=[("BMP Files", "*.bmp")])
        if file_p:
            try:
                self.original_image = Image.open(file_p)
                self.set_scale("100%")
                for i in range(len(self.scales)):
                    self.scale_menu.entryconfig(i, state="normal")
            except Exception as e:
                print(f"Ошибка при загрузке фотографии {e}")
    def clear_image(self):
        self.original_image = None
        self.image_label.config(image="")
        for i in range(len(self.scales)):
            self.scale_menu.entryconfig(i, state="disabled")
    
    def set_scale(self, scale):
        if not self.original_image:
            return
        
        for key in self.scale_vars:
            self.scale_vars[key].set(False)
        
        self.scale_vars[scale].set(True)
        self.current_scale = scale
        
        scale_fact = self.scales[scale]
        nw_size = (int(self.original_image.width * scale_fact), int(self.original_image.height * scale_fact))
        
        resiz_image = self.original_image.resize(nw_size, Image.Resampling.LANCZOS)
        self.display_image = ImageTk.PhotoImage(resiz_image)
        self.image_label.config(image=self.display_image)
        self.editor.geometry(f"{nw_size[0]}x{nw_size[1]}")

        
       
BMP_Image(window)
window.mainloop()


