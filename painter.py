from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image 
import os
from tkinter.colorchooser import askcolor
import tkinter.ttk as ttk
from tkinter import filedialog
try:
    from PIL import ImageGrab
except:
    pass
import signal 
import time

class Main(tk.Tk):
    DEFAULT_COLOR = 'black'
    ERASER = 'white'
    DEFAULT_COLOR_TOP_PANEL = '#D9D9D9'
    def __init__(self):
        tk.Tk.__init__(self)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.background = Canvas(bg='white',width=587 ,height=435,bd=0, cursor='tcross')
        self.background.place(x=5,y=58)
        self.top_panel = Label(width=75,height=3, relief='groove')
        self.top_panel.place(x=0,y=0)
        self.path_to_icon_menu = os.path.abspath('media/menu.png')
        self.icon_menu = PhotoImage(file=self.path_to_icon_menu)
        self.back_menu = Label(image=self.icon_menu, cursor='hand1')
        self.back_menu.bind('<Button-1>',self.open_menu)
        self.back_menu.place(x=10,y=0)
        self.choose_size_button = tk.Spinbox(textvariable=int,validate="key", wrap=True, width=5, from_=0, to=1000,borderwidth=0)
        self.choose_size_button.place(x=70, y=0)
        self.choose_size_button.bind('<MouseWheel>', self.control_spinbox)
        self.choose_size_button.bind('<Button-4>',self.control_spinbox)
        self.choose_size_button.bind('<Button-5>',self.control_spinbox)
        self.eraser_on = False
        self.color_frame=Frame(bg='black',width=45,height=45,borderwidth=10, cursor='hand1')
        self.color_frame.place(x=165,y=5)
        self.color_frame.bind('<Button-1>', self.choose_color)
        self.path_to_reset = os.path.abspath('media/reset.png')
        self.icon_reset = PhotoImage(file=self.path_to_reset)
        self.reset1 = Label(image=self.icon_reset, cursor='hand1')
        self.reset1.place(x=540,y=0)
        self.reset1.bind('<Button-1>',self.clear_all)
        self.path_to_fiil_icon = os.path.abspath('media/fill.png')
        self.fill_icon = PhotoImage(file=self.path_to_fiil_icon)
        self.fill = Label(image=self.fill_icon, cursor='hand1')
        self.fill.place(x=215,y=0)
        self.fill.bind('<Button-1>', self.fill_all)
        self.path_to_eraser_icon = os.path.abspath('media/eraser.png')
        self.eraser_icon = PhotoImage(file=self.path_to_eraser_icon)
        self.eraser = Label(image=self.eraser_icon, cursor='hand1')
        self.eraser.place(x=270,y=0)
        self.eraser.bind('<Button-1>',self.eraser_func)
        self.path_to_pencil_icon = os.path.abspath('media/pencil.png')
        self.pencil_icon  = PhotoImage(file=self.path_to_pencil_icon)
        self.pencil = Label(image=self.pencil_icon, cursor='hand1',bg='#8B8B8B')
        self.pencil.place(x=330,y=0)
        self.pencil.bind('<Button-1>',self.active_pencil)
        self.path_to_text_icon = os.path.abspath('media/text.png')
        self.text_icon = PhotoImage(file=self.path_to_text_icon)
        self.text = Label(image=self.text_icon,cursor='hand1')
        self.text.place(x=390, y=0)
        self.text.bind('<Button-1>',self.use_text)
        self.setup()   
    def spawn(self,event):
        result = self.spawn_text.get()
        self.label = Label(self,text=result)
        self.label.place(x=self.x-70,y=self.y+45)
        self.spawn_text.destroy()
        self.background.bind('<Button-1>',self.callback)
    def callback(self,event):
        self.x = event.x 
        self.y = event.y
        print('callback at: ', event.x,event.y)
        self.spawn_text = Entry()
        self.spawn_text.place(x=self.x-70,y=self.y+45)
        self.spawn_text.bind('<Return>', self.spawn)
        self.background.bind('<Button-1>',self.spawn)
        if self.spawn_text:
            try:
                self.background.unbind('<Button-1>',self.callback)
            except:
                print('Vrode pashet')
        else:
            self.background.bind('<Button-1>',self.callback)
    def use_text(self,event):
        self.background.bind('<Button-1>',self.callback)
        self.text.config(bg='#8B8B8B')
        self.pencil.config(bg=self.DEFAULT_COLOR_TOP_PANEL)
        self.eraser.config(bg=self.DEFAULT_COLOR_TOP_PANEL)
    def eraser_func(self,event):
        self.activate_button(self.eraser, eraser_mode=True)
        self.eraser.config(bg='#8B8B8B')
        self.pencil.config(bg=self.DEFAULT_COLOR_TOP_PANEL)
        self.text.config(bg=self.DEFAULT_COLOR_TOP_PANEL)
    def active_pencil(self,event):
        self.activate_button(self.pencil)
        self.eraser.config(bg=self.DEFAULT_COLOR_TOP_PANEL)
        self.pencil.config(bg='#8B8B8B')
        self.text.config(bg=self.DEFAULT_COLOR_TOP_PANEL)
        try:
            self.spawn_text.destroy()
            self.background.unbind('<Button-1>',self.callback)
        except:
            print('пытаюсь')
    def control_spinbox(self,event):
        if event.num == 5 or event.delta == -120:
            self.choose_size_button+="1"
        elif event.num == 4 or event.delta == 120:
            self.choose_size_button+=1
    def save(self,event):
        file = filedialog.asksaveasfilename(filetypes=[('Portable Network Graphics','*.png')])
        if file:
            x = self.winfo_rootx() + self.background.winfo_x()
            y = self.winfo_rooty() + self.background.winfo_y()
            x1 = x + self.background.winfo_width()
            y1 = y + self.background.winfo_height()
            try:
                PIL.ImageGrab.grab().crop((x,y,x1,y1)).save(file + '.png')
            except:
                image = Image.open(file)
                size = x1,y1 = image.size
                image.save(file+'png')
    def fill_all(self,event):
        self.clear_all(event)
        self.background.configure(bg=self.color)
    def choose_color(self,e):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]
        self.color_frame.configure(bg=self.color)
    def activate_button(self, some_button, eraser_mode=False):
        self.active_button = some_button
        self.eraser_on = eraser_mode
    def setup(self):
        self.old_x = None
        self.old_y = None
        self.color = self.DEFAULT_COLOR
        self.line_width = self.choose_size_button.get()
        self.eraser_on = False
        self.active_button = self.pencil
        self.background.bind('<B1-Motion>', self.paint)
        self.background.bind('<ButtonRelease-1>',self.reset)
        self.eraser.bind('<Button-1>',self.eraser_func)
        
    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color ='white' if self.eraser_on else self.color
        try:
            if self.old_x and self.old_y:
                self.background.create_line(self.old_x, self.old_y, event.x, event.y,
                                   width=self.line_width, fill=paint_color,
                                   capstyle=ROUND, smooth=TRUE, splinesteps=36)
        except:
            pass
        self.old_x = event.x
        self.old_y = event.y
    def clear_all(self, event):
        self.background.delete('all')
        self.background.configure(bg='white')
        self.spawn_text.destroy()
        try:
            self.label.destroy()
        except:
            pass
    def reset(self,event):
        self.old_x = None
        self.old_y = None
    def open_menu(self,event):
        self.window_menu = Label(bg='#B3B3B3',width=30,height=12, relief='solid')
        self.window_menu.place(x=0,y=0)

        self.path_to_close = os.path.abspath('media/close.png')
        self.close_icon = PhotoImage(file=self.path_to_close)
        self.close_menu = Label(image=self.close_icon, bg='#B3B3B3')
        self.close_menu.place(x=215,y=3)
        self.close_menu.bind('<Enter>',self.hover_close)
        self.close_menu.bind('<Button-1>',self.close_menu_1)
    

        self.path_to_save_icon = os.path.abspath('media/save.png')
        self.save_icon = PhotoImage(file=self.path_to_save_icon)
        self.save_file = Label(image=self.save_icon,bg='#B3B3B3', cursor='hand1')
        self.save_file.place(x=3,y=15)
        self.text_save = Label(text='Save file', bg='#B3B3B3', font=('Arial',27,'bold'), cursor='hand1')
        self.text_save.place(x=65,y=27)
        self.text_save.bind('<Button-1>',self.save)

        self.path_open_icon = os.path.abspath('media/plus.png')
        self.open_icon = PhotoImage(file=self.path_open_icon)
        self.open_file = Label(image=self.open_icon,bg='#B3B3B3', cursor='hand1')
        self.open_file.place(x=10, y=82)
        self.text_open = Label(text='Open file',font=('Arial',27,'bold'), bg='#B3B3B3', cursor='hand1')
        self.text_open.place(x=65, y=85)    

        self.path_to_icon_exit = os.path.abspath('media/exit.png')
        self.icon_exit= PhotoImage(file=self.path_to_icon_exit)
        self.exit = Label(image=self.icon_exit, bg='#B3B3B3', cursor='hand1')
        self.exit.place(x=8,y=140)
        self.exit_text = Label(text='Exit', bg='#B3B3B3', font=('Arial',27, 'bold'), cursor='hand1')
        self.exit_text.place(x=68, y=145)
        self.exit.bind('<Button-1>', self.exit_)
        self.exit_text.bind('<Button-1>',self.exit_)

        self.background.bind('<Button-1>',self.close_menu_1)
        self.top_panel.bind('<Button-1>',self.close_menu_1)
    def exit_(self,event):
        os.kill(os.getpid(), signal.SIGKILL)
    def close_menu_1(self,event):
        self.window_menu.destroy()
        self.save_file.destroy()
        self.text_save.destroy()
        self.open_file.destroy()
        self.text_open.destroy()
        try:
            self.close_menu_hover.destroy()
        except:
            pass
        finally:
            self.close_menu.destroy()
            self.exit.destroy()
            self.exit_text.destroy()
    def hover_close(self,event):
        self.close_menu.destroy()
        self.path_to_close_icon_hover = os.path.abspath('close_hover.png')
        self.close_hover_icon = PhotoImage(file=self.path_to_close_icon_hover)
        self.close_menu_hover = Label(image=self.close_hover_icon,bg='#B3B3B3', cursor='hand1')
        self.close_menu_hover.place(x=215,y=3)
        self.close_menu_hover.bind('<Leave>', self.leave_close)
        self.close_menu_hover.bind('<Button-1>',self.close_menu_1)
    def leave_close(self,event):
        self.close_menu_hover.destroy()
        self.close_icon = PhotoImage(file=self.path_to_close)
        self.path_to_close = os.path.abspath('close.png')
        self.close_icon = PhotoImage(file=self.path_to_close)
        self.close_menu = Label(image=self.close_icon, bg='#B3B3B3')
        self.close_menu.place(x=215,y=3)
        self.close_menu.bind('<Enter>',self.hover_close)
        self.close_menu.bind('<Button-1>',self.close_menu_1)
def app():
    root = Main()
    print(root.winfo_screenwidth(), root.winfo_screenheight())
    root.title('Kript')
    #width_value = root.winfo_screenwidth()
    #height_value = root.winfo_screenheight()
    #root.geometry('%dx%d+0+0'%(width_value,height_value))
    root.minsize(600,500)
    root.geometry('600x500')
    root.configure(bg='white',borderwidth=0)
    root.mainloop()

app()