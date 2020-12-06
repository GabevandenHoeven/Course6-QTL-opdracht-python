
def read_files(loc, qua):
    """ This function reads a loc and a qua file and puts the contents in dictionaries

    :param loc: string - The filename of the loc file
    :param qua: string - The filename of the qua file

    :return d: dict - The dictionary for the loc file. The keys are the gen names and the values a list with the bands
    :return d2: dict - The dictionary for the qua file. The keys are the positions and the values the numbers

    """
    d = {}
    d2 = {}
    loc_line = ""
    bands = []
    start_reading = False
    with open(loc, "r") as loc_bes:
        for line in loc_bes:
            if " (a,b) ;" in line:
                start_reading = True
                if not loc_line == "":
                    for c in loc_line:
                        if not c == " ":
                            bands.append(c)
                    d.update({header: bands})
                    bands = []
                    loc_line = ""
                header = line.split(" (a,b) ;")[0]
            elif "individual names:" in line:
                start_reading = False
                for c in loc_line:
                    if not c == " ":
                        bands.append(c)
                d.update({header: bands})
            elif start_reading:
                loc_line += line.strip("\n")
        loc_bes.close()

    start_reading = False
    with open(qua, "r") as qua_bes:
        for line in qua_bes:
            if line.startswith("1"):
                start_reading = True
            elif line == "":
                start_reading = False
            if start_reading:
                index, num = line.split("\t")
                index = int(index)
                num = num.replace("\n", "")
                d2.update({index: num})
        qua_bes.close()

    return d, d2


if __name__ == "__main__":
    # print("/---------------------------------\\")
    # print("|    QTL-opdracht assignment 2    |")
    # print("|         Ontwikkeld door:        |")
    # print("| Gabe van de Hoeven & Max Nollet |")
    # print("\---------------------------------/\n")

    loc_bestand = "CvixLerC9.loc"
    qua_bestand = "CvixLerC9.qua"

    read_files(loc_bestand, qua_bestand)
