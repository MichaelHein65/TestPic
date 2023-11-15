import tkinter as tk
from tkinter import simpledialog, ttk, messagebox, filedialog
from PIL import Image, ImageDraw, ImageFont
import datetime
import numpy as np
import os
import cv2

PATTERNS = ['Kacheln', 'Streifen', 'Weiss', 'Schwarz', 'Rot', 'Gruen', 'Blau', 'Kreuz', 'Flicker', 'Gamma' , 'Alle', 'Gamma-Bilder']
FORMATS = ['JPEG', 'PNG', 'BMP', 'TIFF']
SIZES = {
    'SD': (720, 576),
    'HD-Ready': (1280, 720),
    'HD Plus': (1600, 900),
    'Full HD': (1920, 1080),
    '2K': (2560, 1440),
    '4K': (3840, 2160),
    '5K': (5120, 2880),
    '8K': (7680, 4320),
    'QHD': (3440, 1440),
    'UXGA': (2560, 1080),
    'Iphone 15 pro': (2556, 1179)
}


class ImageParametersDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Bildschirmformat:").grid(row=0)
        tk.Label(master, text="Muster:").grid(row=1)
        tk.Label(master, text="Format:").grid(row=2)
        tk.Label(master, text="Breite:").grid(row=3)
        tk.Label(master, text="Höhe:").grid(row=4)
        tk.Label(master, text='Target directory').grid(row=5)

        self.size_var = tk.StringVar()
        self.pattern_var = tk.StringVar()
        self.format_var = tk.StringVar()
        self.width_var = tk.StringVar()
        self.height_var = tk.StringVar()
        self.directory = tk.StringVar()

        self.e1 = ttk.Combobox(master, values=list(SIZES.keys()), textvariable=self.size_var, state='readonly')
        self.e2 = ttk.Combobox(master, values=PATTERNS, textvariable=self.pattern_var)
        self.e3 = ttk.Combobox(master, values=FORMATS, textvariable=self.format_var)
        self.e4 = tk.Entry(master, textvariable=self.width_var)
        self.e5 = tk.Entry(master, textvariable=self.height_var)
        dir = tk.filedialog.askdirectory(title='Select directory to save image')
        self.directory.set(dir)
        self.e6 = tk.Entry(master, textvariable=self.directory)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)
        self.e5.grid(row=4, column=1)
        self.e6.grid(row=5, column=1)

        self.e1.bind("<<ComboboxSelected>>", self.update_size)

        return self.e1

    def update_size(self, event):
        size = self.size_var.get()
        if size in SIZES:
            width, height = SIZES[size]
            self.width_var.set(str(width))
            self.height_var.set(str(height))

    def apply(self):
        try:
            width = int(self.e4.get())
            height = int(self.e5.get())
            pattern = self.e2.get()
            format = self.e3.get()
            directory = self.e6.get()

            if width <= 0 or height <= 0:
                raise ValueError

            if pattern not in PATTERNS or format not in FORMATS:
                raise ValueError

            self.result = (width, height, pattern, format, directory)
        except ValueError:
            messagebox.showerror("Error", "Ungültige Eingabe. Bitte erneut versuchen.")
            self.result = None


def create_image(width, height, pattern, format, img_folder=None):
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    pattern_name = ''
    date_str = datetime.datetime.now().strftime('%Y%m%d')
    if (img_folder is None) | (len(img_folder) == 0):
        image_folder = f'{os.getcwd()}/Ziel_Verzeichniss'
    else:
        image_folder = img_folder

    if pattern == 'Kacheln':
        draw_image_tiles(draw, width, height)
        pattern_name = 'Kacheln'

    elif pattern == 'Streifen':
        draw_image_stripes(draw, width, height)
        pattern_name = 'Streifen'

    elif pattern == 'Weiss':
        draw_image_white(draw, width, height)
        pattern_name = 'Weiss'

    elif pattern == 'Schwarz':
        draw_image_black(draw, width, height)
        pattern_name = 'Schwarz'

    elif pattern == 'Rot':
        draw_image_red(draw, width, height)
        pattern_name = 'Rot'

    elif pattern == 'Gruen':
        draw_image_green(draw, width, height)
        pattern_name = 'Gruen'

    elif pattern == 'Blau':
        draw_image_blue(draw, width, height)
        pattern_name = 'Blau'

    elif pattern == 'Kreuz':
        draw_image_cross(draw, width, height)
        pattern_name = 'Kreuz'

    elif pattern == 'Flicker':
        draw_image_flicker(draw, width, height)
        pattern_name = 'Flicker'

    elif pattern == 'Gamma':
        draw_image_gamma(draw, width, height)
        pattern_name = 'Gamma'

    elif pattern == 'Gamma-Bilder':
        #draw_image_all_gamma(100, 100, 'mein_bildordner', '2023-11-05', 'PNG')
        draw_image_all_gamma(width, height, image_folder, date_str, format)
        pattern_name = 'Gammapic'

    if not pattern == 'Gamma-Bilder':
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        image_path = f"{image_folder}/{date_str}-Testbild-{pattern_name}-{width}x{height}.{format.lower()}"
        image.save(image_path, format)


def draw_image_tiles(draw, width, height):
    tile_size = 5
    for i in range(height):
        for j in range(width):
            if (i // tile_size + j // tile_size) % 2 == 0:
                draw.point((j, i), fill=(0, 0, 0))
            else:
                draw.point((j, i), fill=(255, 255, 255))


def draw_image_stripes(draw, width, height):
    stripe_width = 5
    for i in range(height):
        for j in range(width):
            if j // stripe_width % 2 == 0:
                draw.point((j, i), fill=(0, 0, 0))
            else:
                draw.point((j, i), fill=(255, 255, 255))


def draw_image_white(draw, width, height):
    for i in range(height):
        for j in range(width):
            draw.point((j, i), fill=(255, 255, 255))


def draw_image_black(draw, width, height):
    for i in range(height):
        for j in range(width):
            draw.point((j, i), fill=(0, 0, 0))


def draw_image_red(draw, width, height):
    for i in range(height):
        for j in range(width):
            draw.point((j, i), fill=(255, 0, 0))


def draw_image_green(draw, width, height):
    for i in range(height):
        for j in range(width):
            draw.point((j, i), fill=(0, 255, 0))


def draw_image_blue(draw, width, height):
    for i in range(height):
        for j in range(width):
            draw.point((j, i), fill=(0, 0, 255))


def draw_image_cross(draw, width, height):
    frame_distance1 = 0
    frame_distance2 = 50
    diagonal_color = (0, 255, 0)  # Green
    circle_center = (width // 2, height // 2)
    circle_radius = 10

    # Draw frame 1
    draw.rectangle([(frame_distance1, frame_distance1), (width - frame_distance1 - 1, height - frame_distance1 - 1)],
                   outline=(0, 255, 0))

    # Draw frame 2
    draw.rectangle([(frame_distance2, frame_distance2), (width - frame_distance2, height - frame_distance2)],
                   outline=(0, 255, 0))

    # Draw diagonals
    draw.line([(0, 0), (width, height)], fill=diagonal_color)
    draw.line([(0, height), (width, 0)], fill=diagonal_color)

    # Draw circle outline
    draw.ellipse([(circle_center[0] - circle_radius, circle_center[1] - circle_radius),
                  (circle_center[0] + circle_radius, circle_center[1] + circle_radius)], outline=diagonal_color)


def draw_image_flicker(draw, width, height):
    image_data = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            if (i + j) % 2 == 0:
                image_data[i, j] = [255, 0, 255]  # Magenta (R und B an, G aus)
            else:
                image_data[i, j] = [0, 255, 0]  # Grün (G an, R und B aus)

    for i in range(height):
        for j in range(width):
            draw.point((j, i), fill=tuple(image_data[i, j]))


def draw_image_gamma(draw, width, height):
    # Definiere die Anzahl der Streifen
    num_strips = 4

    # Berechne die Höhe eines Streifens
    strip_height = height // num_strips

    # Definiere die Farben für die Streifen
    colors = [(255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)]

    # Zeichne jeden Streifen
    for i in range(num_strips):
        for x in range(width):
            # Berechne die Helligkeit basierend auf der Position im Streifen
            brightness = int((x / width) * 255)
            # Mische die Farbe mit Schwarz basierend auf der Helligkeit
            strip_color = tuple(brightness if c > 0 else 0 for c in colors[i])
            # Zeichne eine vertikale Linie mit der berechneten Farbe
            draw.line([(x, strip_height * i), (x, strip_height * (i + 1) - 1)], fill=strip_color)

    # Zeichne den Rest des Bildes, wenn die Höhe nicht durch 4 teilbar ist
    remaining_height = height % num_strips
    if remaining_height > 0:
        y_start = strip_height * num_strips
        draw.rectangle([(0, y_start), (width, height)], fill=(0, 0, 0))


def draw_image_all_gamma(width, height, image_folder, date_str, image_format):
    # Der Pfad für das Unterverzeichnis 'Gammabilder' relativ zum übergebenen 'image_folder'
    gamma_images_path = os.path.join(image_folder, 'Gammabilder')

    # Überprüfe, ob das Unterverzeichnis existiert, und erstelle es, wenn nicht
    if not os.path.exists(gamma_images_path):
        os.makedirs(gamma_images_path)

    # Erstelle für jeden Gamma-Wert ein Bild
    for gamma in range(0, 256, 5):
        # Erzeuge ein Bild der gegebenen Größe mit der aktuellen Helligkeitsstufe
        image_array = np.full((height, width, 3), gamma, dtype=np.uint8)  # Achtung: (Höhe, Breite), nicht (Breite, Höhe)
        image = Image.fromarray(image_array)  # Konvertiere das NumPy-Array in ein PIL-Bildobjekt

        image_path = f"{image_folder}/Gammabilder/{date_str}-Gammabild-{gamma}-{width}x{height}.{image_format.lower()}"
        image.save(image_path)


def create_all_images(width, height, format, directory=None):
    for pattern in PATTERNS[:-1]:  # Exclude 'Alle'
        create_image(width, height, pattern, format, directory)


def position_window(root):
    # Bildschirmgröße ermitteln
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Fenstergröße festlegen
    window_width = 400  # Breite des Fensters
    window_height = 300  # Höhe des Fensters

    # Fensterposition berechnen
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Fensterposition und Größe festlegen
    root.attributes('-topmost', True)
    root.geometry(f"{window_width}x{window_height}+{x+200}+{y+200}")
    root.after_idle(root.attributes, '-topmost', False)


def create_test_image():
    root = tk.Tk()
    root.withdraw()

    while True:
        dialog = ImageParametersDialog(root)
        if dialog.result is None:
            break

        width, height, pattern, format, directory = dialog.result

        if pattern == 'Alle':
            create_all_images(width, height, format, directory)
        else:
            create_image(width, height, pattern, format, directory)


if __name__ == '__main__':
    create_test_image()
