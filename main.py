
def read_files(loc, qua):
    """

    :param loc:
    :param qua:
    :return:
    """
    d = {}
    d2 = {}
    with open(loc, "r") as loc_bes:
        loc_line = ""
        for line in loc_bes:
            if " (a,b) ;" in line:
                start_reading = True
                if not loc_line == "":
                    d.update({header: loc_line})
                header = line.split(" (a,b) ;")[0]
            elif "individual names:" == line:
                start_reading = False
                d.update({header: loc_line})
            elif start_reading:
                loc_line += line
        loc_bes.close()

    with open(qua, "r") as qua_bes:

        for line in qua_bes:
            if line.startswith("1"):
                start_reading = True
            elif line == "":
                start_reading = False
            elif start_reading:
                index, num = line.split("\t")
                d2.update({index: num})
        qua_bes.close()

    return


def main():

    loc_bestand = "CvixLerC9.loc"
    qua_bestand = "CvixLerC9.qua"

    read_files(loc_bestand, qua_bestand)
    return 0


if __name__ == "__main__":
    print("/---------------------------------\\")
    print("|    QTL-opdracht assignment 2    |")
    print("|         Ontwikkeld door:        |")
    print("| Gabe van de Hoeven & Max Nollet |")
    print("\---------------------------------/\n")
    main()
