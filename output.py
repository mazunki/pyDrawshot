# output functions

def save_canvas_to_file(output, **settings):
    import io
    from PIL import Image

    print("saving to file...")
    img = Image.open(io.BytesIO(output.encode("utf-8")))

    print("img:", img)

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            print(img.getpixel((x,y)))
            if hex(img.getpixel((x,y))) == hex("#2222222"):
                print("found some gray")

    img.save("drawing.png", "png")
    print("file saved!")


def copy_to_clipboard(output):
    import subprocess as sp

    # TODO: save directly to clipboard without file
    
    print("copying file to clipboard...")
    with open("drawing.png", "rb") as img_data:
            sp.run("xclip -selection clipboard -t image/png -i drawing.png", shell=True)
    print("saved to clipboard")

