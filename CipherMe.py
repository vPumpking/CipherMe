#!/bin/python3

#################################### CIPHER  ME ####################################
# Python3 GUI based encryption tool.                                               #
# Written by Martin LOUVEL; CC-0 CREATIVE COMMONS, Free usage allowed for any      #
# purpose with citation of original author.                                        #
# Please refer to README.md for instructions.                                      #
####################################################################################

#### IMPORT ZONE ####
import random
from tkinter import *
import tkinter.filedialog as fs
import tkinter.messagebox as msg
import tkinter.ttk as ttk
import time
import string as str_utils
#####################

##### VARIABLES #####
##### Program - wide variables.
root = Tk() ## GUI root component.
radioVar = StringVar() ## Radiobuttons shared variable.
iPath = "" ## input file path.
oPath = "" ## output file path.

#####################

##### CONSTANTS #####
##### Program constants
## /!\ For the program to work correctly, some constants that uses functions are placed after these functions.
FILETYPES = (
        ('text files', '*.txt'), 
        ('All files', '*')
    )
WRONG_KEYCODE_ERR = "E:Wrong keycode type: " ## error for: keycode does not match the cipher method.
WRONG_MESSAGE_ERR = "E:Wrong message type: " ## error for: message does not match the cipher method.
LACK_METHOD_ERR = "E:Select a method." ## error for: cipher method is not defined.
KEYCODE_OPTIONAL_INF = "I:No keycode needed." ## info for: user asked keycode but it is not required.
MAIN_BUTTONS_COLOR = "#E34E1A" #1A1A1A" ## hex color for buttons background.
GUI_BG_COLOR = "#2C2C2C" ## hex color for window background.
GUI_WIDGET_COLOR = "#252526" ## hex color for widget backgrounds.
COOL_GREY = "#BEBEC7"
MANUAL = '''Choose a file to encrypt/decrypt, then pick a destination path, an\nencryption method, a keycode if needed and decrypt or encrypt.\nIn any case except ROT 13 and PolySquare, keycode must be kept so the file\ncould be decrypted.'''
DEFAULT_HINT = '''Pick a cipher method.'''
ASCII_LOW = str_utils.ascii_lowercase ## ASCII lowercase alphabet.
ASCII_UPP = str_utils.ascii_uppercase ## ASCII uppercase aplhabet.
ASCII_SPE = str_utils.digits + str_utils.punctuation + str_utils.whitespace ## ASCII special characters.
POLSQ_ARR = ("abcde",
           "fghij",
           "klmno",
           "pqrst",
           "uvxyz") ## Polysquare table ("w" is "vv")

#####################

##### FUNCTIONS #####
##### Program functions.

#===== PRIVATE =====#
#===== Private functions are written with an underscore at the beginning of the name, like this: _myfunction()

## Caesar ROT encryption. Takes a string to process on and a keycode int to process from. Returns a string.
def _rot(string:str, keycode:str)  -> str:
    return_string = ""
    unknown_char = 0
    try: ## type exception.
        user_key = int(keycode)
    except:
        _warning(WRONG_KEYCODE_ERR + str(type(keycode)))
        return return_string
    user_key %= len(str_utils.ascii_lowercase) ## if keycode overloads alphabet, it is truncated
    for character in range(0, len(string)):
        unknown_char = 0
        for ascii_char in range(0, len(ASCII_LOW)): ## fetch character in lowercase table
            if string[character] == ASCII_LOW[ascii_char]:
                if ascii_char + user_key >= len(ASCII_LOW):
                    user_key -= len(ASCII_LOW)
                return_string += ASCII_LOW[ascii_char + user_key]
            else:
                unknown_char += 1
        for ascii_char in range(0, len(ASCII_UPP)): ## fetch character in uppercase table
            if string[character] == ASCII_UPP[ascii_char]:
                if ascii_char + user_key >= len(ASCII_UPP):
                    user_key -= len(ASCII_UPP)
                return_string += ASCII_UPP[ascii_char + user_key]
            else:
                unknown_char += 1
        if unknown_char >= len(ASCII_LOW) + len(ASCII_UPP): ## if the character is not recognized, the programm keeps it
            return_string += string[character]
    return return_string

## ROT13 encryption.
def _rot13_encryption(string:str)  -> str:
    return _rot(string, 13)

## Caesar Code encryption. Takes a string to process on and a keycode int to process from. Returns a string.
def _caesar_encryption(string:str, keycode:str)  -> str:
    return_string = ""
    unknown_char = 0
    try: ## type exception.
        user_key = int(keycode)
    except:
        _warning(WRONG_KEYCODE_ERR + str(type(keycode)))
        return return_string
    user_key %= len(str_utils.ascii_lowercase) ## if keycode overloads alphabet, it is truncated
    for character in range(0, len(string)):
        unknown_char = 0
        for ascii_char in range(0, len(ASCII_LOW)): ## fetch character in lowercase table
            if string[character] == ASCII_LOW[ascii_char]:
                if ascii_char + user_key >= len(ASCII_LOW):
                    user_key -= len(ASCII_LOW)
                return_string += ASCII_LOW[ascii_char + user_key]
            else:
                unknown_char += 1
        for ascii_char in range(0, len(ASCII_UPP)): ## fetch character in uppercase table
            if string[character] == ASCII_UPP[ascii_char]:
                if ascii_char + user_key >= len(ASCII_UPP):
                    user_key -= len(ASCII_UPP)
                return_string += ASCII_UPP[ascii_char + user_key]
            else:
                unknown_char += 1
        if unknown_char >= len(ASCII_LOW) + len(ASCII_UPP): ## if the character is not recognized, it is replaced by a space.
            return_string += " "
    return return_string

## Vigenère Code encryption. Takes a string to process on and a keycode int to process from. Returns a string.
def _vigenere_encryption(string:str, keycode:str) -> str:
    return_string = ""
    unknown_char = 0
    wrong_char = 0
    matching_code = ""
    string_index = ""
    keycode_index = ""
    user_key = keycode.lower()
    lower_string = string.lower()
    for char in ASCII_SPE: ## handle special characters.
        if char in lower_string:
            lower_string = lower_string.replace(char, "")
    for letter in range(0, len(user_key)): ## check if keycode only has letters.
        unknown_char = 0
        for ascii_char in range(0, len(ASCII_LOW)):
            if not user_key[letter] == ASCII_LOW[ascii_char]:
                unknown_char += 1
        if unknown_char >= len(ASCII_LOW):
            wrong_char += 1
    if wrong_char:
        _warning(WRONG_KEYCODE_ERR + "keycode has non-alphabetic characters.")
        return return_string
    for letter in range(0, len(lower_string)): ## check if message only has letters.
        unknown_char = 0
        for ascii_char in range(0, len(ASCII_LOW)):
            if not lower_string[letter] == ASCII_LOW[ascii_char]:
                unknown_char += 1
        if unknown_char >= len(ASCII_LOW):
            wrong_char += 1
    if wrong_char:
        _warning(WRONG_MESSAGE_ERR + "message has non-alphabetic characters.")
        return return_string
    code_index = 0
    for letter in range(0, len(lower_string)): ## apply keycode to message legth.
        matching_code += user_key[code_index]
        if code_index < len(user_key) - 1:
            code_index += 1
        else:
            code_index = 0
    for letter in range(0, len(lower_string)): ## get the index of each letter (message).
        unknown_char = 0
        for ascii_char in range(0, len(ASCII_LOW)):
            if not lower_string[letter] == ASCII_LOW[ascii_char]:
                unknown_char += 1
            else:
                string_index += str(ascii_char) + "."
    string_index = string_index.split(".") ## turn the string into a list of values.
    for letter in range(0, len(matching_code)): ## get the index of each letter (keycode).
        unknown_char = 0
        for ascii_char in range(0, len(ASCII_LOW)):
            if not matching_code[letter] == ASCII_LOW[ascii_char]:
                unknown_char += 1
            else:
                keycode_index += str(ascii_char) + "."
    keycode_index = keycode_index.split(".")
    for letter in range(0, len(lower_string)): ## proceed encryption operation CodeIndex = (KeyIndex  +  MessageIndex)  %  alphabetLength.
        return_string += ASCII_LOW[((int(string_index[letter]) + int(keycode_index[letter])) % len(ASCII_LOW))]
    return return_string

## PolySquare encryption. Takes a string to process on. Returns a string.
def _polysquare_encryption(string:str) -> str:
    return_string = ""
    unknown_char = 0
    wrong_char = 0
    lower_string = string.lower()
    for char in ASCII_SPE: ## handle special characters.
        if char in lower_string:
            lower_string = lower_string.replace(char, "")
    for letter in range(0, len(lower_string)): ## check if message only has letters.
        unknown_char = 0
        for ascii_char in range(0, len(ASCII_LOW)):
            if not lower_string[letter] == ASCII_LOW[ascii_char]:
                unknown_char += 1
        if unknown_char >= len(ASCII_LOW):
            wrong_char += 1
    if wrong_char:
        _warning(WRONG_MESSAGE_ERR + "message has non-alphabetic characters.")
        return return_string
    lower_string = lower_string.replace("w", "vv") ## convert `w` into `vv` to match cipher table.
    for letter in lower_string: ## cipher message with cipher table.
        for line in range(0, len(POLSQ_ARR)):
            for row in range(0, len(POLSQ_ARR[line])):
                if POLSQ_ARR[line][row] == letter:
                    return_string += (str(line + 1) + str(row + 1))
    return return_string

## ROT13 decryption. Takes a string to process on. Returns a string.
def _rot13_decryption(string:str) -> str:
    return _rot13_encryption(string)

## Caesar Code decryption. Takes a string to process on and a keycode to process from. Returns a string.
def _caesar_decryption(string:str, keycode:str) -> str:
    return_string = _caesar_encryption(string, -keycode)
    return return_string

## Vigenère Code decryption. Takes a string to process on and a keycode to process from. Returns a string.
def _vigenere_decryption(string:str, keycode:str) -> str:
    return_string = string
    for x in range(0, len(ASCII_LOW) - 1): ## encrypt it [alphabet - 1] times to get the result.
        return_string = _vigenere_encryption(return_string, keycode)
    return return_string

## PolySquare decryption. Takes a string to process on. Returns a string.
def _polysquare_decryption(string:str) -> str:
    return_string = ""
    wrong_char = 0
    previous_line = 0
    lower_string = string.lower()
    for letter in string: ## check if message only has digits.
        if not letter in str_utils.digits:
            wrong_char = 1
    if wrong_char:
        _warning(WRONG_MESSAGE_ERR + "message has non-numeral characters.")
        return return_string
    string_array = [string[i:i+2] for i in range(0, len(string), 2)] ## split the string in groups of 2 digits.
    for letter in string_array: ## message decryption using cipher table.
        return_string += POLSQ_ARR[(int(letter[0]) - 1)][int(letter[1]) - 1]
    return return_string

## Opens a file using its path, and returns it as a string. Returns 1 for failure.
def _read_file(path:str) -> str:
    return_string = ""
    try:
        with open(path, "r") as file:
            for line in file.readlines():
                return_string += (line + "\n")
    except FileNotFoundError:
        _warning("No such file or wrong data type (must be plain text).")
        return 1
    return return_string

## Writes a string into a file at a specified path. If the file exists, its content is removed. Returns 0 for success and 1 for failure.
def _edit_file(path:str, string:str) -> int:
    try:
        with open(path, "w") as file:
            file.write(string)
    except FileNotFoundError:
        _warning("No such file or wrong data type (must be plain text).")
        return 1
    except PermissionError:
        _warning("Missing privileges to write in " + path + ".")
        return 1
    return 0

## Returns a string with [length] caracters, randomly taken in the [letters] string.
def _random_text(letters:str, length:int) -> str:
    return_string = ""
    for i in range(0, length + 1):
        return_string += letters[random.randint(0, len(letters) - 1)]
    return return_string

## Shows an error dialog, then quits.
def _critical(error:str):
    msg.showerror("SOMETHING WENT WRONG", error)
    exit(1)

## Shows a warning dialog.
def _warning(error:str):
    msg.showwarning("WARNING", error)
#===================#
#===== PUBLIC ======#
#===== Public functions have no syntaxic rules.

## Writes the encrypted version of a "fromfile" file into a "tofile" file, using one of the 4 ciphers [int from 1 to 4 included], with keycode.
def cipher_file(fromfile:str, tofile:str, cipher:int, keycode:str):
    file_content = _read_file(fromfile).replace("\n", "")
    if file_content == 1:
        _warning("Could not open the file to cipher. Aborting.")
        return 1
    file_content_encrypted = ""
    match cipher:
        case 1:
            file_content_encrypted = _rot13_encryption(file_content)
        case 2:
            file_content_encrypted = _caesar_encryption(file_content, keycode)
        case 3:
            file_content_encrypted = _vigenere_encryption(file_content, keycode)
        case 4:
            file_content_encrypted = _polysquare_encryption(file_content)
        case _:
            _warning("Choose a valid cipher method.")
            return 1
    write_result = _edit_file(tofile, file_content_encrypted)
    if write_result == 1:
        _warning("Could not edit the destination file. Aborting.")
        return 1
    msg.showinfo("TASK FINISHED", "Processed 1 encryption task.")
    return 0

## Writes the decrypted version of a "fromfile" file into a "tofile" file, using one of the 4 cipher [int from 1 to 4 included], with keycode.
def decrypt_file(fromfile:str, tofile:str, cipher:int, keycode:str):
    file_content = _read_file(fromfile)
    if file_content == 1:
        _warning("Could not open the file to decrypt. Aborting.")
        return 1
    file_content = file_content.replace("\n", "")
    file_content_decrypted = ""
    match cipher:
        case 1:
            file_content_decrypted = _rot13_decryption(file_content)
        case 2:
            file_content_decrypted = _caesar_decryption(file_content, int(keycode))
        case 3:
            file_content_decrypted = _vigenere_decryption(file_content, keycode)
        case 4:
            file_content_decrypted = _polysquare_decryption(file_content)
        case _:
            _warning("Choose a valid cipher method.")
            return 1
    write_result = _edit_file(tofile, file_content_decrypted)
    if write_result == 1:
        _warning("Could not edit the destination file. Aborting.")
        return 1
    msg.showinfo("TASK FINISHED", "Processed 1 decryption task.")
    return 0

#===================#
#####################

## Dynamic constants (relying on functions).
ROT13_HINT = '''ROT13:\n\nReplaces each letter with the one 13 places away in the alphabet. Keeps all special characters.\n\nSPECIFICATIONS:\nAll characters supported, no keycode needed.\n\nEXAMPLE:\n`Hello, World!`\nbecomes\n`''' + _rot13_encryption("Hello, World!") + "`"
CAESAR_HINT = '''CAESAR'S CIPHER:\n\nReplaces each letter with the one [keycode] places away in the alphabet. All special characters are replaced with whitespaces.\n\nSPECIFICATIONS:\nEnglish characters only, keycode needed.\n\nEXAMPLE:\n`Hello, World!` with keycode = 3\nbecomes\n`''' + _caesar_encryption("Hello, World!", "3") + "`"
VIGENERE_HINT = '''VIGENERE CIPHER:\n\nUses combination between a message and a [keycode] keyword to blur eventual letter frequency. This cipher is hard to decrypt without the key. All special characters are removed and all letters are turned into lowercase.\n\nSPECIFICATIONS:\nEnglish characters only, keycode needed.\n\nEXAMPLE:\n`Hello, World!` with keycode = `code`\nbecomes\n`''' + _vigenere_encryption("Hello, World!", "code") + "`"
POLYSQUARE_HINT = '''POLYBIUS SQUARE:\n\nUses an array of 25 letters (fixed alphabet) in which columns and rows are identified by a number from 1 to 5. Each letter is encrypted by combining the number of the column to the one of the row. All special characters are removed and `w` is turned into `vv`. All letters are turned into lowercase.\n\nSPECIFICATIONS:\nEnglish characters only, no keycode needed.\n\nEXAMPLE:\n`Hello, World!`\nbecomes\n`32 51 23 23 53 25 25 53 34 23 41`'''

# GUI Scheme:
#
#     root (Tk)
#       ┖╴ upPadding (Frame)
#            ┠╴ leftPadding (Frame)
#            |    ┠╴ title (Label)
#            |    ┠╴ manual (Label)
#            |    ┠╴ inputPadding (Frame)
#            |    |   ┠╴ separator0 (Frame)
#            |    |   ┠╴ inputLabel (Label)
#            |    |   ┠╴ inputPath (Entry)
#            |    |   ┖╴ iExploreButton (Button)
#            |    ┠╴ outputPadding (Frame)
#            |    |   ┠╴ separator1 (Frame)
#            |    |   ┠╴ outputLabel (Label)
#            |    |   ┠╴ outputPath (Entry)
#            |    |   ┖╴ oExploreButton (Button)
#            |    ┠╴ cipherPadding (Frame)
#            |    |   ┠╴ separator2 (Frame)
#            |    |   ┠╴ cipherLabel (Label)
#            |    |   ┠╴ rot13Radio (Radiobutton)
#            |    |   ┠╴ caesarRadio (Radiobutton)
#            |    |   ┠╴ vigenereRadio (Radiobutton)
#            |    |   ┖╴ polysquareRadio (Radiobutton)
#            |    ┠╴ keycodePadding (Frame)
#            |    |   ┠╴ separator3 (Frame)
#            |    |   ┠╴ keycodeLabel (Label)
#            |    |   ┠╴ keycodeEntry (Entry)
#            |    |   ┖╴ kRandomizeButton (Button)
#            |    ┖╴ actionPadding (Frame)
#            |        ┠╴ separator4 (Frame)
#            |        ┠╴ encryptButton (Button)
#            |        ┖╴ decryptButton (Button)
#            ┖╴ rightPadding (Frame)
#                 ┠╴ hint (Text)
#                 ┖╴ hintLabel (Label)

######## MAIN #######
######## Main program.
root.title("CipherMe  -  Cipher text files")
root.configure(background = GUI_BG_COLOR)
root.minsize(800, 600)
radioVar.set(0) ## init variable.

#=== GUI SIGNALS ===#
def signal_encryptButton_pressed():
    cipher_file(inputPath.get(), outputPath.get(), int(radioVar.get()), keycodeEntry.get())

def signal_decryptButton_pressed():
    decrypt_file(inputPath.get(), outputPath.get(), int(radioVar.get()), keycodeEntry.get())

def signal_radio_changed():
    radio = int(radioVar.get())
    match radio:
        case 0:
            hint.config(state = NORMAL)
            hint.delete('1.0', END)
            hint.insert(END, DEFAULT_HINT)
            hint.config(state = DISABLED)
        case 1:
            hint.config(state = NORMAL)
            hint.delete('1.0', END)
            hint.insert(END, ROT13_HINT)
            hint.config(state = DISABLED)
        case 2:
            hint.config(state = NORMAL)
            hint.delete('1.0', END)
            hint.insert(END, CAESAR_HINT)
            hint.config(state = DISABLED)
        case 3:
            hint.config(state = NORMAL)
            hint.delete('1.0', END)
            hint.insert(END, VIGENERE_HINT)
            hint.config(state = DISABLED)
        case 4:
            hint.config(state = NORMAL)
            hint.delete('1.0', END)
            hint.insert(END, POLYSQUARE_HINT)
            hint.config(state = DISABLED)
        case _:
            hint.config(state = NORMAL)
            hint.delete('1.0', END)
            hint.insert(END, DEFAULT_HINT)
            hint.config(state = DISABLED)

def signal_iExplore_pressed():
    iPath = fs.askopenfilename(title = "Select an input file:", filetypes = FILETYPES)
    inputPath.delete(0, END)
    inputPath.insert(0, iPath)

def signal_oExplore_pressed():
    oPath = fs.askopenfilename(title = "Select an output file:", filetypes = FILETYPES)
    outputPath.delete(0, END)
    outputPath.insert(0, oPath)

def signal_keyCodeRandomize_pressed():
    radio = int(radioVar.get())
    keycodeEntry.delete(0, END) ## clean text zone.
    if radio  ==  0:
        keycodeEntry.insert(0, LACK_METHOD_ERR) ## tells user to choose a cipher method.
    elif radio == 1:
        keycodeEntry.insert(0, KEYCODE_OPTIONAL_INF) ## tells user that ROT13 works without a keycode.
    elif radio == 2:
        keycodeEntry.insert(0, str(random.randint( - 26, 26))) ## chooses a keycode between  - 255 and 255.
    elif radio == 3:
        keycodeEntry.insert(0, _random_text(ASCII_LOW, random.randint(0, 16))) ## uses _random_text() to generate text.
    elif radio == 4:
        keycodeEntry.insert(0, KEYCODE_OPTIONAL_INF) ## tells user that PolySquare works without a keycode.
    else:
        _critical("Error: could'nt figure out what cipher method `" + str(radio) + "` is.") ## if an unknown radio id is given, program ends with an error.
        
#===================#

upPadding = Frame(root, bg = GUI_BG_COLOR)
leftPadding = Frame(upPadding, bg = GUI_BG_COLOR)
title = Label(leftPadding, text = "CIPHER ME", fg = "white", bg = GUI_BG_COLOR, font = ("SegoeUI 20 bold")) ## Display a title on top.
manual = Label(leftPadding, text = MANUAL, fg = "white", bg = GUI_BG_COLOR) ## Displays hint.
inputPadding = Frame(leftPadding, bg = GUI_BG_COLOR)
separator0 = Frame(inputPadding, bg = GUI_BG_COLOR)
inputLabel = Label(inputPadding, text = "1  -  INPUT FILE", fg = "white", bg = GUI_BG_COLOR, font = ("SegoeUI 10 bold"))
inputPath = Entry(inputPadding, bg = GUI_WIDGET_COLOR, fg = COOL_GREY, width = 30)
iExploreButton = Button(inputPadding, bg = GUI_WIDGET_COLOR, fg = "white", text = "Explore...", relief = "flat", borderwidth = 0, highlightthickness = 0, command = signal_iExplore_pressed)
outputPadding = Frame(leftPadding, bg = GUI_BG_COLOR)
separator1 = Frame(outputPadding, bg = GUI_BG_COLOR)
outputLabel = Label(outputPadding, text = "2  -  OUTPUT FILE", fg = "white", bg = GUI_BG_COLOR, font = ("SegoeUI 10 bold"))
outputPath = Entry(outputPadding, bg = GUI_WIDGET_COLOR, fg = COOL_GREY, width = 30)
oExploreButton = Button(outputPadding, bg = GUI_WIDGET_COLOR, fg = "white", text = "Explore...", relief = "flat", borderwidth = 0, highlightthickness = 0, command = signal_oExplore_pressed)
cipherPadding = Frame(leftPadding, bg = GUI_BG_COLOR)
separator2 = Frame(cipherPadding, bg = GUI_BG_COLOR)
cipherLabel = Label(cipherPadding, text = "3  -  CIPHER METHOD (See Description*)", fg = "white", bg = GUI_BG_COLOR, font = ("SegoeUI 10 bold"))
rot13Radio = Radiobutton(cipherPadding, text = "ROT 13 Code", fg = "white", selectcolor = GUI_WIDGET_COLOR, bg = GUI_BG_COLOR, value = 1, variable = radioVar, relief = "flat", borderwidth = 0, highlightthickness = 0, command = signal_radio_changed)
caesarRadio = Radiobutton(cipherPadding, text = "Caesar's Cipher", fg = "white", selectcolor = GUI_WIDGET_COLOR, bg = GUI_BG_COLOR, value = 2, variable = radioVar, relief = "flat", borderwidth = 0, highlightthickness = 0, command = signal_radio_changed)
vigenereRadio = Radiobutton(cipherPadding, text = "Vigenère Cipher", fg = "white", selectcolor = GUI_WIDGET_COLOR, bg = GUI_BG_COLOR, value = 3, variable = radioVar, relief = "flat", borderwidth = 0, highlightthickness = 0, command = signal_radio_changed)
polysquareRadio = Radiobutton(cipherPadding, text = "Polybius Square", fg = "white", selectcolor = GUI_WIDGET_COLOR, bg = GUI_BG_COLOR, value = 4, variable = radioVar, relief = "flat", borderwidth = 0, highlightthickness=0, command = signal_radio_changed)
keycodePadding = Frame(leftPadding, bg = GUI_BG_COLOR)
separator3 = Frame(keycodePadding, bg = GUI_BG_COLOR)
keycodeLabel = Label(keycodePadding, text = "4  -  KEYCODE\n(Cipher factor, see Description*)", fg = "white", bg = GUI_BG_COLOR, font = ("SegoeUI 10 bold"))
keycodeEntry = Entry(keycodePadding, bg = GUI_WIDGET_COLOR, fg = COOL_GREY, width = 20)
kRandomizeButton = Button(keycodePadding, bg = GUI_WIDGET_COLOR, fg="white", text="Randomize", relief = "flat", borderwidth = 0, highlightthickness = 0, command = signal_keyCodeRandomize_pressed)
actionPadding = Frame(leftPadding, bg = GUI_BG_COLOR)
separator4=Frame(actionPadding, bg=GUI_BG_COLOR)
encryptButton = Button(actionPadding, text = "ENCRYPT", bg = MAIN_BUTTONS_COLOR, fg = "white", relief = "flat", borderwidth = 0, highlightthickness = 0, width = 20, height = 2, font = ("SegoeUI 10 bold"), command = signal_encryptButton_pressed)
decryptButton = Button(actionPadding, text = "DECRYPT", bg = MAIN_BUTTONS_COLOR, fg = "white", relief = "flat", borderwidth = 0, highlightthickness = 0, width = 20, height = 2, font = ("SegoeUI 10 bold"), command = signal_decryptButton_pressed)
rightPadding = Frame(upPadding, bg = GUI_BG_COLOR)
hint = Text(rightPadding, height = 32, width = 40, bg = GUI_WIDGET_COLOR, fg = COOL_GREY, relief = "flat", borderwidth = 0, highlightthickness = 0)
hintLabel = Label(rightPadding, text = "*DESCRIPTION:", fg = "white", bg = GUI_BG_COLOR)

upPadding.pack(side = TOP, expand = True)
leftPadding.pack(side = LEFT, expand = True)
title.pack(side = TOP, expand = False)
manual.pack(side = TOP)
inputPadding.pack(expand = True)
separator0.pack(pady = 20, side = TOP)
inputLabel.pack(side = TOP)
inputPath.pack(side = LEFT)
iExploreButton.pack(side = RIGHT)
outputPadding.pack(expand = True)
separator1.pack(pady = 10, side = TOP)
outputLabel.pack(side = TOP)
outputPath.pack(side = LEFT)
oExploreButton.pack(side = RIGHT)
cipherPadding.pack(expand = True)
separator2.pack(pady = 10, side = TOP)
cipherLabel.pack(side = TOP, pady = 3)
rot13Radio.pack(side = TOP)
caesarRadio.pack(side = TOP)
vigenereRadio.pack(side = TOP)
polysquareRadio.pack(side = TOP)
keycodePadding.pack(expand = True)
separator3.pack(pady = 10, side = TOP)
keycodeLabel.pack(side = TOP, pady = 10)
keycodeEntry.pack(side = LEFT)
kRandomizeButton.pack(side = RIGHT)
actionPadding.pack(expand = True)
separator4.pack(pady = 10, side = TOP)
encryptButton.pack(expand = True, side = LEFT, padx = 3)
decryptButton.pack(expand = True, side = LEFT, padx = 3)
rightPadding.pack(side = RIGHT, expand = True)
hintLabel.pack(side = TOP)
hint.pack(expand = True, padx = 10, pady = 10)

hint.insert(END, DEFAULT_HINT)
hint.config(state = DISABLED)
root.resizable(height  =  False, width  =  False) ## fixed size window.
root.mainloop()