import PIL
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.filedialog import askopenfilename

WINDOW_SIZE = '300x100'
image_file = PIL.Image.new('RGB', (0, 0))


def generate_histogram(root):
    """Function to generate the histogram for our image"""
    global image_file
    image_file = get_image_file()
    width, height = grab_dimensions(image_file)
    R_array, G_array, B_array = initialize_color_arrays()
    create_buckets(image_file, width, height, R_array, G_array, B_array)

    plot_graph(R_array, 'red')
    plot_graph(G_array, 'green')
    plot_graph(B_array, 'blue')

    display_plots()


def set_image_file(image):
    """This function sets the image object to the right value"""
    global image_file
    image_file = PIL.Image.open(image)


def get_image_file():
    """This function simply returns the global image variable"""
    global image_file
    return image_file


def open_image(root):
    """This function opens the image file and calls the set_image_file function"""
    root.withdraw()
    set_image_file(askopenfilename(filetypes=(("Image Files", "*.jpg *.jpeg *.png"),)))
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
    root = Tk()

    root.geometry(WINDOW_SIZE)

    frame1 = Frame(root)  # Image Select button
    frame2 = Frame(root)  # Generate histogram button

    root.title("Image Histogram Viewer")

    # Button that executes the function to load the log file(s)
    button_default_text = StringVar()
    button_default_text.set("Select Image")
    x = 5
    select_button = Button(frame1, textvariable=button_default_text, command=lambda: open_image(root), width=22)
    select_button.pack()

    # Button that calls the conversion function
    convert_button = Button(frame2, text="Generate Histogram", command=lambda: generate_histogram(root), width=22)
    convert_button.pack()

    frame1.pack(padx=10, pady=10)
    frame2.pack(padx=1, pady=1)
    root.mainloop()


def main():
    generate_ui()


if __name__ == "__main__":
    main()
