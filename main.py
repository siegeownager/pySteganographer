import PIL.Image
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


def append_multiple(nlist, x, y, z):
    """Append x, y and z to list"""
    nlist.append(x)
    nlist.append(y)
    nlist.append(z)


def gen_rgb_list():
    """This function takes our image and constructs a list with discrete R, G and B values as items"""
    global main_image_file
    rgb_list = []
    dimension = grab_dimensions(main_image_file)

    width = dimension[0]
    height = dimension[1]

    for x in range(width):
        for y in range(height):
            rgb_tuple = main_image_file.getpixel((x, y))
            rval, gval, bval = tuple_to_val(rgb_tuple)
            append_multiple(rgb_list, rval, gval, bval)

    return rgb_list


def gen_text_code_list(text):
    """This function generates and returns an ascii list of our string"""
    text_list = []
    lower_text = text.lower()

    # Function to iterate over the characters in the string and add to list
    for c in lower_text:
        if c == ' ':
            new_c = 27  # Set whitespace as numeric code 27
        else:
            new_c = ord(c) - 96  # Subtract 96 so our alphabets start from index 1
        text_list.append(new_c)

    return text_list


def tuple_to_val(tuple):
    """Split tuple into discrete R, G and B values"""
    rval = tuple[0]
    gval = tuple[1]
    bval = tuple[2]
    return rval, gval, bval


def hide_text(text_to_hide):
    """Function to hide our text in the image"""
    global main_image_file

    clear_bits()  # Clear low order bits of image

    text_list = gen_text_code_list(text_to_hide)  # Obtain character list of string
    rgb_list = gen_rgb_list()  # Listify our RGB space

    # Finally, hide our text in the pixels
    rgb_tuple = main_image_file.getpixel((0, 0))  # Get RGB tuple of pixel
    rval, gval, bval = tuple_to_val(rgb_tuple)  # Split tuple into 3 variables

    rgx_index = 0  # Our index for the RGB list begins from 0

    for str_index in range(len(text_list)):
        char_to_encode = text_list[str_index]
        bit_one = (char_to_encode & 16) >> 4
        bit_two = (char_to_encode & 8) >> 3
        bit_three = (char_to_encode & 4) >> 2
        bit_four = (char_to_encode & 2) >> 1
        bit_five = (char_to_encode & 1) >> 0

        print(bit_one, end=" ")
        print(bit_two, end=" ")
        print(bit_three, end=" ")
        print(bit_four, end=" ")
        print(bit_five)


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
    image_button = Button(frame2, text="Hide text", command=lambda: hide_text("Hello world"), width=22)
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
