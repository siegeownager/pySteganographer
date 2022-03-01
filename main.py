import PIL
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.filedialog import askopenfilename
import sys

# Our 2 image file objects
main_image_file = PIL.Image.new('RGB', (0, 0))
second_image_file = PIL.Image.new('RGB', (0, 0))

# Size of the window for our program
WINDOW_SIZE = '300x150'


def steganographize(root):
    """Function to generate the new steganographized image"""
    image_file = get_image_file()
    width, height = grab_dimensions(image_file)
    R_array, G_array, B_array = initialize_color_arrays()
    create_buckets(image_file, width, height, R_array, G_array, B_array)

    plot_graph(R_array, 'red')
    plot_graph(G_array, 'green')
    plot_graph(B_array, 'blue')

    display_plots()


def set_image_file(image, image_file):
    """This function sets the image object to the right value"""
    global main_image_file
    global second_image_file

    # Set the right image file object based on which button was pressed
    if image_file == "main":
        main_image_file = PIL.Image.open(image)
    elif image_file == "secondary":
        second_image_file = PIL.Image.open(image)
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


def plot_graph(color_array, color):
    """This function generates our histogram"""
    x_array = list(range(256))
    plt.plot(x_array, color_array, color)


def display_plots():
    """This function displays our histogram"""
    plt.show()


def grab_dimensions(image):
    """This function grabs the dimensions of the image"""
    width, height = image.size
    return width, height


def initialize_color_arrays():
    """This function generates and returns the 3 color arrays"""
    R_array = [0] * 256
    G_array = [0] * 256
    B_array = [0] * 256
    return R_array, G_array, B_array


def create_buckets(image, width, height, R_array, G_array, B_array):
    """"This function parses the image and fills the color arrays"""
    test_pixel = image.getpixel((0, 0))  # Check to see if the returned tuple also has an alpha value

    if len(test_pixel) == 3:
        for i in range(height):
            for j in range(width):
                red_val, green_val, blue_val = image.getpixel((j, i))
                R_array[red_val] += 1
                G_array[green_val] += 1
                B_array[blue_val] += 1

    else:
        for i in range(height):
            for j in range(width):
                red_val, green_val, blue_val, alpha_val = image.getpixel((j, i))
                R_array[red_val] += 1
                G_array[green_val] += 1
                B_array[blue_val] += 1

    return R_array, G_array, B_array


def generate_ui():
    """Function to generate our GUI using tkinter"""
    global main_image_file
    global second_image_file

    root = Tk()

    root.geometry(WINDOW_SIZE)

    # The frame variables for our 3 buttons
    frame1, frame2, frame3 = Frame(root), Frame(root), Frame(root)

    root.title("Image Steganographer")

    # Button to select our main image
    button_default_text = StringVar()
    button_default_text.set("Select main image")
    select_button_main = Button(frame1, textvariable=button_default_text, command=lambda: open_image(root, "main"),
                                width=22)
    select_button_main.pack()

    # Button to select the image that we want to hide
    button_default_text = StringVar()
    button_default_text.set("Select image to hide")
    select_button_secondary = Button(frame2, textvariable=button_default_text,
                                     command=lambda: open_image(root, "secondary"), width=22)
    select_button_secondary.pack()

    # Button that calls the conversion function
    convert_button = Button(frame3, text="Steganographize", command=lambda: steganographize(root), width=22)
    convert_button.pack()

    frame1.pack(padx=10, pady=10)
    frame2.pack(padx=1, pady=1)
    frame3.pack(padx=10, pady=10)
    root.mainloop()


def main():
    generate_ui()


if __name__ == "__main__":
    main()
