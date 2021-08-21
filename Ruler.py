from pakages import Southeros
from pakages import Message
import sys


def register_all_kingdoms():
    """Registers all the Kingdoms of Southeros
    Returns:
        Southeros Object: Southeros Class Object
    """
    kingdoms = [("SPACE", "GORILLA"), ("LAND", "PANDA"), ("WATER", "OCTOPUS"),
                ("ICE", "MAMMOTH"), ("AIR", "OWL"), ("FIRE", "DRAGON")]
    southeros = Southeros(kingdoms)
    return southeros


def get_kingdom_and_message(text):
    """Splits the given text to two parts using first space, first part being the kingdom name
        and second part being the text message sent to the kingdom
    Args:
        text (string): string to be splitted
    Returns:
        tuple: first being the name and second being the message
    """
    splitted_text = text.split(',')
    kingdom_name = splitted_text[0].upper()
    #print(kingdom_name)
    ciphered_text = ""
    for c in splitted_text[1:]:
        ciphered_text += c
    return kingdom_name, ciphered_text


def main():
    """main function of the Tame of Thrones"""
    southeros = register_all_kingdoms()  # registers all the kindoms of Southeros
    space_kingdom = southeros.get_kingdom("SPACE")  # gets the space kingdom object
    # print("-------------", sys.argv)
    input_file = sys.argv[1]  # file location

    # parse the file and process the command
    with open(input_file, encoding='utf-8') as fp:
        Lines = fp.readlines()
        for line in Lines:
            kingdom_name, ciphered_text = get_kingdom_and_message(line)  # retrieving kingdom name and message
            kingdom = southeros.get_kingdom(kingdom_name)  # gets the kingdom to which message should be sent
            message = Message(space_kingdom, kingdom, ciphered_text)  # Creates the message
            space_kingdom.send_message(message)  # sends the message

    # print the output
    ruler = southeros.ruler()  # get the ruler of Southeros
    print("Who is the ruler of Southeros?")
    if ruler is None:
        print("Output :: NONE\n")  # no ruler got majority
        print("Allies of Ruler?\n")
        print("Output :: NONE\n")
    else:
        #print(ruler.name(), end=" ")  # found a majority ruler
        print("OUTPUT :: King Shan\n")
        print("Allies of Ruler?")
        print("OUTPUT :: ", end="")
        for kingdom_name in ruler.get_allies():  # found it's allies
            print(kingdom_name, end=",")
        print()


if __name__ == "__main__":
    main()