import subprocess
import shutil
import re


def read_loc_file(loc_file):
    """ This function reads a loc file and puts the contents in dictionary.

    :param loc_file: string - The filename of the loc file.
    :return dictionary: dict - The dictionary for the loc file.
    The keys are the marker names and the values a list with the loci.

    """
    dictionary = {}
    loc_line = ""
    loci = []
    start_reading = False
    print("Reading .loc-file . . .", end=" ")
    with open(loc_file, "r") as loc_bes:
        for line in loc_bes:
            # If the line contains " (a,b) ;", it is a header.
            if " (a,b) ;" in line:
                start_reading = True
                # When loc_line is not empty, the loci will be saved in a list.
                if not loc_line == "":
                    for c in loc_line:
                        if not c == " ":
                            loci.append(c)
                    # The dictionary is updated with a key-value pair of the marker name and a list of loci.
                    dictionary.update({header: loci})
                    loci = []
                    loc_line = ""
                # The header is saved.
                header = line.split(" (a,b) ;")[0]
            # If the line contains "individual names", it means that all the markers have been read.
            # To make sure we don't get any other information start_reading is put to False.
            elif "individual names:" in line:
                start_reading = False
                for c in loc_line:
                    if not c == " ":
                        loci.append(c)
                # Here, the dictionary will be updated for the last time.
                dictionary.update({header: loci})
            # If the line does not contain " (a,b) ;", and start_reading is true, the line is added to loc_line.
            elif start_reading:
                loc_line += line.strip("\n")
    print("done!")
    return dictionary


def read_qua_file(qua_file):
    """ This function reads a qua file and puts the contents in a dictionary.

    :param qua_file: string - The filename of the qua file.
    :return qua_list: list - The list for the qua file. It contains the numbers in order of the loci.

    """
    qua_list = []
    start_reading = False
    print("Reading .qua-file . . .", end=" ")
    with open(qua_file, "r") as qua_bes:
        for line in qua_bes:
            # If the line startswith "1", the numbers that follow will have to be saved.
            if line.startswith("1"):
                start_reading = True
            # If the line is empty, there are no more numbers so you don't want to save anything anymore.
            elif line == "":
                start_reading = False
            if start_reading:
                # Splits the line in 2 pieces and takes the second one (0, 1), and put it in the list.
                num = line.split("\t")[1]
                num = num.replace("\n", "")
                qua_list.append(num)
    print("done!")
    return qua_list


def converting_values(loc, qua):
    """ A function that links the numbers from the qua_list to the a's and b's of the respective markers.
    It returns a 2D tuple.

    :param loc: dict - Dictionary with the marker names and loci.
    :param qua: list - List with numbers
    :return values: 2D tuple - A tuple with for every marker a tuple,
        containing the marker name, a tuple with values of a and a tuple with values of b.

    """
    markers = loc.keys()
    values = list()
    print("Converting values . . .", end=" ")
    # Runs over all markers in the dictionary.
    for marker in markers:
        loci = loc.get(marker)
        teller = 0
        a_loci = []
        b_loci = []
        for locus in loci:
            # Converts all loci to the respective value from the qua list.
            if locus == "a" or locus == "b":
                value = qua[teller]
                if value != "-":
                    if locus == "a":
                        a_loci.append(float(value))
                    else:
                        b_loci.append(float(value))
                teller += 1
        # Store values with marker in 2d-list.
        values.append((marker, tuple(a_loci), tuple(b_loci)))
    print("done!")
    return tuple(values)


def calculations(values):
    """Calculates the p-values using R on the commandline.

    :param values: 2D tuple - A tuple with for every marker a tuple,
        containing the marker name, a tuple with values of a and a tuple with values of b.
    :return p-values: 2D tuple - A tuple with for every marker the marker name and the p-value.

    """
    if shutil.which("Rscript") is not None:
        p_values = list()
        pattern = re.compile(r"\[\d\]\s(\d\.?\d*e?-?\d*)")
        marker_count = len(values)
        counter = 1
        for marker, a, b in values:
            # Display status of calculating p-values.
            print(f"\rCalculating P-values: {counter}/{marker_count}"
                  + f" ({round(100 / marker_count * counter, 1)}%) . . .", end="")
            # Conducts the ANOVA test and returns the p-value from the commandline.
            anova_test = subprocess.run(['Rscript', '-e', "summary(aov(waarde~loci, "
                                         + f" data=data.frame(waarde=c(c{a}, c{b}), "
                                         + f"loci=factor(rep(c('a', 'b'), times=c({len(a)},  "
                                         + f"{len(b)}))))))[[1]][['Pr(>F)']]"], stdout=subprocess.PIPE)
            p_value = pattern.findall(anova_test.stdout.decode("UTF-8"))[0]
            p_values.append((marker, p_value))
            counter += 1
        print(" done!")
        return tuple(p_values)
    else:
        print("Program 'Rscript' not found! Is 'R' installed correctly?")
        exit()



def write_to_file(p_values):
    """Writes the p-values to a file.

    :param p_values: 2D tuple - A tuple with for every marker the marker name and the p-value.
    :return:

    """
    print("Saving results . . .", end=" ")
    with open("markers_with_p-values.txt", "w") as file:
        file.write("marker\tp-value\n")
        for marker, p_value in p_values:
            file.write(f"{marker}\t{p_value}\n")
    print("done!\n\n")

    return 0


def main():
    print("/----------------------------------\\")
    print("|    QTL-opdracht assignment 02    |")
    print("|         Ontwikkeld door:         |")
    print("| Gabe van den Hoeven & Max Nollet |")
    print("\\----------------------------------/\n")

    loc_bestand = "CvixLerC9.loc"
    qua_bestand = "CvixLerC9.qua"

    loc = read_loc_file(loc_bestand)
    qua = read_qua_file(qua_bestand)
    values = converting_values(loc, qua)
    p_values = calculations(values)
    write_to_file(p_values)


main()
