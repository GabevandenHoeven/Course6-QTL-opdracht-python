import subprocess


def read_loc_file(loc_file):
    """ This function reads a loc file and puts the contents in dictionary.

    :param loc_file: string - The filename of the loc file.
    :return dic: dict - The dictionary for the loc file.
    The keys are the marker names and the values a list with the loci.

    """
    dictionary = {}
    loc_line = ""
    loci = []
    start_reading = False
    with open(loc_file, "r") as loc_bes:
        for line in loc_bes:
            if " (a,b) ;" in line:
                # If the line contains " (a,b) ;", it is a header.
                start_reading = True
                if not loc_line == "":
                    # When loc_line is not empty, the loci will be saved in a list.
                    for c in loc_line:
                        if not c == " ":
                            loci.append(c)
                    dictionary.update({header: loci})
                    # The dictionary is updated with a key-value pair of the marker name and a list of loci.
                    loci = []
                    loc_line = ""
                header = line.split(" (a,b) ;")[0]
                # The header is saved.
            elif "individual names:" in line:
                # If the line contains "individual names", it means that all the markers have been read.
                # To make sure we don't get any other information start_reading is put to False
                start_reading = False
                for c in loc_line:
                    if not c == " ":
                        loci.append(c)
                dictionary.update({header: loci})
                # Here, the dictionary will be updated for the last time.
            elif start_reading:
                # If the line does not contain " (a,b) ;", and start_reading is true, the line is added to loc_line.
                loc_line += line.strip("\n")

    return dictionary


def read_qua_file(qua_file):
    """ This function reads a qua file and puts the contents in a dictionary.

    :param qua_file: string - The filename of the qua file.
    :return qua_list: list - The list for the qua file. It contains the numbers in order of the loci.

    """
    qua_list = []
    start_reading = False
    with open(qua_file, "r") as qua_bes:
        for line in qua_bes:
            if line.startswith("1"):
                # If the line startswith "1", the numbers that follow will have to be saved.
                start_reading = True
            elif line == "":
                # If the line is empty, there are no more numbers so you don't want to save anything anymore
                start_reading = False
            if start_reading:
                num = line.split("\t")[1]
                num = num.replace("\n", "")
                qua_list.append(num)
                # Splits the line in 2 pieces and takes the second one (0, 1), and put it in the list

    return qua_list


def converting_values(loc, qua):
    """ A function that links the numbers from the qua_list to the a's and b's of the respective markers.
    It returns a list.

    :param loc: dict - Dictionary with the marker names and loci.
    :param qua: list - List with numbers
    :return : list -

    """
    markers = loc.keys()
    values = list()
    for marker in markers:
        # Runs over all markers in the dictionary
        loci = loc.get(marker)
        teller = 0
        a_loci = []
        b_loci = []
        for locus in loci:
            # Converts all loci to the respective value from the qua list
            if locus == "a" or locus == "b":
                value = qua[teller]
                if value != "-" and value != "0":
                    if locus == "a":
                        a_loci.append(float(value))
                    else:
                        b_loci.append(float(value))
                teller += 1
        # Store values with marker in 2d-list.
        values.append((marker, tuple(a_loci), tuple(b_loci)))
    return tuple(values)


def calculations(values):
    """

    :return:
    """
    for marker, a, b in values:
        dataframe = subprocess.run(['Rscript', '-e', f"data.frame({a}, {b})"], stdout=subprocess.PIPE)
        results = subprocess.run(['Rscript', '-e', f"aov(a ~ b, data = {dataframe}"])
        print(dataframe.stdout.decode("UTF-8"))
        print(results)
        break

    return 0


def main():
    print("/---------------------------------\\")
    print("|    QTL-opdracht assignment 2    |")
    print("|         Ontwikkeld door:        |")
    print("| Gabe van de Hoeven & Max Nollet |")
    print("\\---------------------------------/\n")

    loc_bestand = "CvixLerC9.loc"
    qua_bestand = "CvixLerC9.qua"

    loc = read_loc_file(loc_bestand)
    qua = read_qua_file(qua_bestand)
    values = converting_values(loc, qua)
    calculations(values)


main()
