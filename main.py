import os
location = "/".join(str(os.path.abspath(__file__)).split("/")[:-1]) + "/"
print(location)

import PIL as pil
import tkinter as tk

from settings import *
from output import *


class DrawshotApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, *kwargs)
        self.parent = parent
        self.settings = get_settings()  # from file
        self.cli_enabled = False

        self.cur_pos = None, None
        self.last_pos = None, None
        self.draw_modus = "freehand"

        self.traces = list()
        self.last_trace = list()  # list of points, later packed into self.traces

        
        # init canvas properties
        self.x =self.settings["default_x"]
        self.y =self.settings["default_y"]
        self.bg_colour =self.settings["bg_colour"]
        self.trace_colour =self.settings["default_trace_colour"]
        self.snap_center =self.settings["snap_center"]
        self.save_bg =self.settings["save_bg"]

        # where to position window
        if self.snap_center:  # center of screen
            self.x_0 = (root.winfo_screenwidth() - self.x) // 2
            self.y_0 = (root.winfo_screenheight() - self.y) // 2
        else:  # snap to mouse
           self.x_0 = root.winfo_pointerx() - root.winfo_vrootx()
           self.y_0 = root.winfo_pointery() - root.winfo_vrooty()

        DEFAULT_DRAW_CANVAS = f"{self.x}x{self.y}+{self.x_0}+{self.y_0}"

        parent.geometry(DEFAULT_DRAW_CANVAS)  # i think this actually includes window borders, which messes with the size
        parent.title("Drawshot")

        

        # the chalkboard is what is actually given as an output
        self.chalkboard = tk.Canvas(self, bg=self.bg_colour, bd=0, highlightthickness=0)

        # bindings: i/o
        self.chalkboard.bind("<B1-Motion>", self.movement)
        self.chalkboard.bind("<Button-1>", self.new_trace)
        self.chalkboard.bind("<ButtonRelease-1>", self.reset_mouse)
        parent.bind("<Control-z>", self.undo_trace) # keypresses don't seem to work on the canvas or the frame
        parent.protocol("WM_DELETE_WINDOW", self.close_window)  # pressing the X button or Alt+F4
        parent.protocol("<Escape>", self.close_window)
        parent.bind("<Return>", self.command_modus)

        self.chalkboard.pack(expand=True, fill=tk.BOTH)


    def movement(self, event):
        if self.draw_modus=="freehand" or end_of_trace:
            self.last_pos = self.cur_pos
        self.cur_pos = event.x, event.y

        if self.last_pos == (0, 0):  # update last position to start of trace, allowing traces to jump
                self.last_pos = self.cur_pos
        if self.last_pos == self.cur_pos:  # allows user to make single (visible) dots
                self.cur_pos = self.last_pos[0]+1, self.last_pos[1]

        # appending each point to the last_trace stack, stored as a number by tkinter
        if self.draw_modus=="freehand":
            self.last_trace.append(
                self.chalkboard.create_line(*self.last_pos, *self.cur_pos, fill=self.trace_colour, width=5, smooth=tk.TRUE, capstyle=tk.ROUND, splinesteps=1)
            )
        elif self.draw_modus=="straight_line":
            pass
            

    def new_trace(self, event):
        print("starting new trace...")
        self.last_pos = event.x, event.y
        self.cur_pos = event.x, event.y

    def reset_mouse(self, event):
        print("released mouse, saving trace")
        self.traces.append([point for point in self.last_trace])
        self.last_trace.clear()

    def undo_trace(self, event):
        if self.traces:
            print("undoing a trace...")
            for point in self.traces[-1]:
                    # print("gone point")
                    self.chalkboard.delete(point)
            self.traces.pop()
            print("trace gone!")
        else: 
            print("nothing to undo!")


    def command_modus(self, event):
        print("cli enabled")
        if not self.cli_enabled: 
            # show cli and let user write
            self.text_input = tk.Entry(self)
            self.text_input.place(height=20,width=100)
            self.text_input.focus()
            self.cli_enabled = True
        else:
            # parse input, vi style in mind
            ui = self.text_input.get()
            print(self.text_input.get())
            
            parse_ui(ui)

            # hide cli
            self.text_input.place_forget()
            self.cli_enabled = False 



    def close_window(self):
        output = self.chalkboard.postscript(colormode="color")
        # FIXME saving to file is required for clipboard
        if self.settings["save_to_file"]:
            save_to_file(output, self.settings)
        if self.settings["save_to_clipboard"]:
            copy_to_clipboard(output, self.settings)

        root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    DrawshotApp(root).pack(side="top", fill="both", expand=True)
    try:
        root.mainloop()
    except:
        exit()



