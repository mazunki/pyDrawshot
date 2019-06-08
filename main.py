import PIL as pil
import tkinter as tk

DEFAULT_DRAW_CANVAS = "600x100"

root = tk.Tk()
root.geometry(DEFAULT_DRAW_CANVAS)

cur_pos = 0,0
last_pos = 0, 0

traces = list()
last_trace = list()

def movement(event):
	global last_pos, cur_pos, last_trace
	last_pos = cur_pos
	cur_pos = event.x, event.y
	if last_pos == (0, 0):
		last_pos = cur_pos
	if last_pos == cur_pos:
		cur_pos = last_pos[0]+1, last_pos[1]
	last_trace.append(
		window.create_line(*last_pos, *cur_pos, fill="black", width=5, smooth=tk.TRUE, capstyle=tk.ROUND, splinesteps=1)
	)

def new_trace(event):
	global last_pos, cur_pos
	print("new")
	last_pos = 0, 0
	cur_pos = 0, 0

def reset_mouse(event):
	global last_trace
	print("released mouse")
	traces.append([point for point in last_trace])
	last_trace.clear()

def undo_trace(event):
	print("undo")
	global traces
	print(traces)
	if traces:
		for point in traces[-1]:
			print("gone point")
			window.delete(point)
		print("\n"*10)
		traces.pop()

def close_window():
	global output
	output = window.postscript(colormode="color")
	root.destroy()


window = tk.Canvas(root)
window.bind("<B1-Motion>", movement)
window.bind("<Button-1>", new_trace)
window.bind("<ButtonRelease-1>", reset_mouse)
root.bind("<Control-z>", undo_trace)
window.pack(expand=True, fill=tk.BOTH)

root.protocol("WM_DELETE_WINDOW", close_window)

root.mainloop()


# save to file
import io
from PIL import Image

img = Image.open(io.BytesIO(output.encode("utf-8")))
img.save("drawing.jpg", "jpeg")
print(img)

# copy to clipboard
import subprocess as sp
with open("drawing.jpg", "rb") as img_data:
	sp.run("xclip -selection clipboard -t image/jpeg -i drawing.jpg", shell=True)