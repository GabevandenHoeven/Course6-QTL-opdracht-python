
def read_loc_file(loc):
    """ This function reads a loc file and puts the contents in dictionary

    :param loc: string - The filename of the loc file
    :return dic: dict - The dictionary for the loc file. The keys are the gen names and the values a list with the bands

    """
    dic = {}
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
                    dic.update({header: bands})
                    bands = []
                    loc_line = ""
                header = line.split(" (a,b) ;")[0]
            elif "individual names:" in line:
                start_reading = False
                for c in loc_line:
                    if not c == " ":
                        bands.append(c)
                dic.update({header: bands})
            elif start_reading:
                loc_line += line.strip("\n")
        loc_bes.close()

    return dic


def read_qua_file(qua):
    """ This function reads a qua file and puts the contents in a dictionary

    :param qua: string - The filename of the qua file
    :return dic2: dict - The dictionary for the qua file. The keys are the positions and the values the numbers
    """
    dic2 = {}
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
                dic2.update({index: num})
        qua_bes.close()

    return dic2


if __name__ == "__main__":
    print("/---------------------------------\\")
    print("|    QTL-opdracht assignment 2    |")
    print("|         Ontwikkeld door:        |")
    print("| Gabe van de Hoeven & Max Nollet |")
    print("\\---------------------------------/\n")

    loc_bestand = "CvixLerC9.loc"
    qua_bestand = "CvixLerC9.qua"

    d = read_loc_file(loc_bestand)
    d2 = read_qua_file(qua_bestand)
