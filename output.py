# helper function
def hex_to_rgba(hex_colour, grb=False, add_bg=False, only_rgb=False):
    """
        parses `#FFFFFF` values into (255,255,255,0) values
        could be simplified into a one-liner, but this is clearer
    """
    print(hex_colour)
    r, g, b = (None, None, None)
    if hex_colour[0] == "#":
        hex_colour = hex_colour[1:]
    if len(hex_colour) == 3:
        r = int(hex_colour[0], 16)
        g = int(hex_colour[1], 16)
        b = int(hex_colour[2], 16)
    elif len(hex_colour) == 6:
        r = int(hex_colour[0:2], 16)
        g = int(hex_colour[2:4], 16)
        b = int(hex_colour[4:6], 16)

    a = 0
    if add_bg:
        a = 255

    composites = 4
    if only_rgb:
        composites = 3
    
    return (r,g,b,a)[:composites+1] if not grb else (g,r,b,a)[composites+1]

# output functions

def save_canvas(output, settings):
    import io
    from PIL import Image

    print("working image...")
    old_bg = (255, 255, 255)
    bg_colour = hex_to_rgba(settings["bg_colour"], add_bg=settings["save_bg"])
    print(bg_colour)
    img = Image.open(io.BytesIO(output.encode("utf-8")))
    img = img.convert("RGBA")
    pixels = img.load()

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if pixels[x, y][:3] == old_bg:
                pixels[x, y] = (bg_colour)
    print("done!")

    memory = io.BytesIO()
    img.save(memory, format="png")
    return memory


def save_to_file(output, settings):
    import PIL as pil
    img_memory = save_canvas(output, settings)
    img = pil.Image.open(img_memory)
    img.save("drawing.png", format="png")

def copy_to_clipboard(output, settings):
    import subprocess as sp

    # TODO: save directly to clipboard without file
    
    img_memory = save_canvas(output, settings)
    print("copying file to clipboard...")

    img_data = img_memory.getvalue()

    p = sp.run("xclip -selection clipboard -t image/png -i", stdin=sp.PIPE, stdout=sp.PIPE, shell=True)
    p.communicate(input=img_data)
    print("saved to clipboard")

