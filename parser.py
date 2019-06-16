
def parse_command(self, uic, gamut=None):  # gamut:= synonym of range
    import re

    if uic[0]=="b":
        print("change color mode")
        colour = f"#{uic[1:]}"
        self.trace_colour = colour


    elif uic[0]=="r":
        #uic = re.sub("\^(+)")
        gamut = re.search("^(?:(?!brogc).+)+", uic[1:])[0]
        gamut = re.split("--", gamut)
        print(gamut)

        colour = re.search("c[0-9a-fA-F]{6}", uic)[0][1:]
        
        for strokes in [int(item) for item in range(int(gamut[0]), int(gamut[1])+1)]:
            for point in self.traces[strokes]:
                self.chalkboard.itemconfig(point, fill="#"+colour)

    elif uic[0]=="o":
        pass

    elif uic[0]=="g":
        pass

    else:
        print("It's dangerous to travel alone. Take this!")
        #print(HELP_SHEET)