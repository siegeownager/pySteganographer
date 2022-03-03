import PIL
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.filedialog import askopenfilename
import sys

# Our 2 image file objects
main_image_file = PIL.Image.new('RGB', (0, 0))

# Size of the window for our program
WINDOW_SIZE = '300x100'


def max_info_size():
    """This function will tell us what the maximum size of the information that can be stored is"""
    global main_image_file
    dimensions = grab_dimensions(main_image_file)


def print_bits():
    """Function to check our RGB values of the image pixels"""
    global main_image_file
    dimensions = grab_dimensions(main_image_file)
    width = dimensions[0]
    height = dimensions[1]

    # Print the RGB values of each pixel location
    for x in range(width):
        for y in range(height):
            rgb_tuple = main_image_file.getpixel((x, y))
            print(rgb_tuple)

def trigger():
    print(0, end=" :")
    hide_text(0)
    print(1, end=" :")
    hide_text(1)
    print(2, end=" :")
    hide_text(2)
    print(3, end=" :")
    hide_text(3)
    print(4, end=" :")
    hide_text(4)
    print(5, end=" :")
    hide_text(5)
    print(6, end=" :")
    hide_text(6)
    print(7, end=" :")
    hide_text(7)

def hide_text(text_to_hide):
    global main_image_file
    # For testing purpose, use numbers for now
    num = str(text_to_hide)
    normalized_num_code = ord(num) - 48
    #print(normalized_num_code)

    # Call function to clear out low order bits
    clear_bits()

    # Finally hide our number in the pixels
    rgb_tuple = main_image_file.getpixel((0, 0))
    rval = rgb_tuple[0]
    gval = rgb_tuple[1]
    bval = rgb_tuple[2]

    # Next come up with a way to break our number
    # Generate three masks
    rmask = normalized_num_code >> 2
    gmask = (normalized_num_code & 2) >> 1
    bmask = normalized_num_code & 1
    print(rmask, end=" ")
    print(gmask, end=" ")
    print(bmask)

    #encoded_rgb_tuple = (rmask, gmask, bmask)

    #main_image_file.putpixel((0, 0), encoded_rgb_tuple)
    #print_bits()


def set_image_file(image, image_file):
    """This function sets the image object to the right value"""
    global main_image_file

    # Set the right image file object based on which button was pressed
    if image_file == "main":
        main_image_file = PIL.Image.open(image).convert('RGB')
    else:
        print("Something unexpected happened!")
        sys.exit()


def get_image_file(image_file):
    """This function simply returns the image variable"""
    return image_file


def open_image(root, image_file):
    """This function opens the image file and calls the set_image_file function"""
    root.withdraw()
    set_image_file(askopenfilename(filetypes=(("Image Files", "*.jpg *.jpeg *.png"),)), image_file)
    root.deiconify()


def grab_dimensions(image):
    """This function grabs the dimensions of the image"""
    width, height = image.size
    return width, height


def new_rgb_tuple_gen(rgb_tuple):
    """This function ingests our RGB tuple and regenerates a new one with low order bits removed"""
    rval = rgb_tuple[0]
    gval = rgb_tuple[1]
    bval = rgb_tuple[2]

    new_rval = rval & 254
    new_gval = gval & 254
    new_bval = bval & 254

    new_rgb_tuple = (new_rval, new_gval, new_bval)
    return new_rgb_tuple


def clear_bits():
    """Function to clear the low order bits of our image"""
    global main_image_file
    dimensions = grab_dimensions(main_image_file)
    width = dimensions[0]
    height = dimensions[1]

    # Print the RGB values of each pixel location
    for x in range(width):
        for y in range(height):
            rgb_tuple = main_image_file.getpixel((x, y))
            new_rgb_tuple = new_rgb_tuple_gen(rgb_tuple)
            main_image_file.putpixel((x, y), new_rgb_tuple)


def generate_ui():
    """Function to generate our GUI using tkinter"""
    global main_image_file
    global second_image_file

    # Variables, text, etc. for temporary use
    secret_text = 'abc'

    root = Tk()

    root.geometry(WINDOW_SIZE)

    # The frame variables for our 3 buttons
    frame1, frame2, frame3 = Frame(root), Frame(root), Frame(root)

    # This button will be temporary, just for generating our sample image
    frame4 = Frame(root)

    root.title("Image Steganographer")

    # Button to select our main image
    button_default_text = StringVar()
    button_default_text.set("Select main image")
    select_button_main = Button(frame1, textvariable=button_default_text, command=lambda: open_image(root, "main"),
                                width=22)
    select_button_main.pack()

    # Button to hide our text
    image_button = Button(frame2, text="Hide text", command=lambda: trigger(), width=22)
    image_button.pack()

    frame1.pack(padx=10, pady=10)
    frame2.pack(padx=1, pady=1)
    root.mainloop()

    # Button to select the image that we want to hide
    # button_default_text = StringVar()
    # button_default_text.set("Select image to hide")
    # select_button_secondary = Button(frame2, textvariable=button_default_text,
    #                                 command=lambda: open_image(root, "secondary"), width=22)
    # select_button_secondary.pack()

    # Button to generate our sample images of necessary sizes
    # image_button = Button(frame4, text="Generate Sample", command=lambda: sample_generate(secret_text), width=22)
    # image_button.pack()

    # Temporary button to hide text inside an image
    # hide_button = Button(frame4, text="Hide Text", command=lambda: sample_generate(secret_text), width=22)
    # hide_button.pack()


def main():
    generate_ui()


if __name__ == "__main__":
    main()
