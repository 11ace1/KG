import tkinter as tk
from tkinter import filedialog, Menu, messagebox, PhotoImage
from PIL import Image, ImageTk

window =tk.Tk()
# основной класс фоторедактора
class BMP_Image:
    def __init__(self, editor : tk.Tk):
        self.cached_images={}
        self.editor = editor
        self.editor.option_add("*tearOff", False)
        editor.geometry("500x500")
        self.icon = PhotoImage(file="ic.png")
        try:
            editor.iconphoto(False, self.icon)
            editor.title("BMP editor")
        except Exception as e:
            messagebox.showinfo("Ошибка", f"Ошибка загрузки {e}")
        self.image_label = tk.Label(self.editor)
        self.image_label.pack(expand=True)
        
        # создание меню File
        self.menu_bar = Menu(self.editor)
        self.editor.config(menu=self.menu_bar)
        # создание пунктов подменю по открытию, очистке окна и выходу из программы
        self.file_menu = Menu(self.menu_bar)
        self.file_menu.add_command(label="Открыть", command=self.open_image)
        self.file_menu.add_command(label="Очистить", command=self.clear_image)

        self.file_menu.add_separator()
        
        self.file_menu.add_command(label="Выход", command=self.editor.quit)
        
        self.menu_bar.add_cascade(label="File",menu=self.file_menu)
        
        self.scale_menu = Menu(self.menu_bar)
        self.scales = {"50%" : 0.5, "100%": 1.0, "150" : 1.5, "200%" : 2.0}
        self.scale_vars = {}
        # создание пунктов подменю Scale
        for label, f in self.scales.items():
            self.scale_vars[label] = tk.BooleanVar()
            self.scale_menu.add_radiobutton(label=label, variable=self.scale_vars[label], command=lambda l=label: self.set_scale(l), state="disabled", activebackground='blue' )
        
        self.menu_bar.add_cascade(label="Scale", menu=self.scale_menu) 
        
        self.original_image = None
        self.current_scale = "100%"  
    # Открытие изображение
    def open_image(self):
        file_p = filedialog.askopenfilename(filetypes=[("BMP Files", "*.bmp")])
        if file_p:
            try:
                self.original_image = Image.open(file_p)
                self.set_scale("100%")
                self.cached_images.clear()
                for i in range(len(self.scales)):
                    self.scale_menu.entryconfig(i, state="normal")
            except Exception as e:
                messagebox.showinfo("Ошибка", f"Ошибка при загрузке фотографии {e}")
    # Очистка окна
    def clear_image(self):
        self.original_image = None
        self.image_label.config(image="")
        self.cached_images.clear()
        for i in range(len(self.scales)):
            self.scale_menu.entryconfig(i, state="disabled" )
    # Масшабирование 
    def set_scale(self, scale):
        if not self.original_image:
            return
        
        for key in self.scale_vars:
            self.scale_vars[key].set(False)
        self.scale_vars[scale].set(True)
        
        if scale in self.cached_images:
            self.display_image = self.cached_images[scale]
        else:
            scale_fact = self.scales[scale]
            nw_size = (int(self.original_image.width * scale_fact), int(self.original_image.height * scale_fact))
            resiz_image = self.original_image.resize(nw_size, Image.Resampling.LANCZOS)
            self.display_image = ImageTk.PhotoImage(resiz_image)
            self.cached_images[scale] = self.display_image
        
        self.image_label.config(image=self.display_image)
        
        for i, (label, _) in enumerate(self.scales.items()):
            self.scale_menu.entryconfig(i, state='normal')
            if label == scale:
                self.scale_menu.entryconfig(i,state="disabled")
        
        self.editor.geometry(f"{self.display_image.width()}x{self.display_image.height()}")

        
       
BMP_Image(window)
window.mainloop()


