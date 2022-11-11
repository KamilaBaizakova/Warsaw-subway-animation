# Wywołanie FFMPEG:
# ffmpeg -framerate 1 -pattern_type glob -i '*.png' -c:v libx264 -pix_fmt yuv420p -r 24 out.mp4

from datetime import datetime, timedelta
from os import path

from PIL import Image, ImageDraw, ImageFont

# Pociągi
TRAINS_NUMBER = 2 * 3  # liczba pociągów na obu liniach , MAX = 10 !
START_TIME = "7:00"  # Start pierwszego pociągu (czas "GG:MM")
ADD_TRAIN_AFTER = 15  # Dodaje po tym czasie kolejny pociąg
COLORS = ('blue', 'red', 'green', 'brown', 'purple', 'lightblue', 'black', 'yellow', 'lightgreen', 'orange')

TOTAL_TIME = 600  # Całkowity czas "symulacji" (animacji) w minutach

# FFMPEG
images_dir = 'images_dir'
fonts_dir = '/usr/local/share/fonts/'

LINE_1 = (
    ((497, 98), u"Młociny"),
    ((519, 149), u"Wawrzyszew"),
    ((539, 198), u"Stare Bielany"),
    ((558, 249), u"Słodowiec"),
    ((578, 299), u"Marymont"),
    ((600, 346), u"Plac Wilsona"),
    ((598, 399), u"Dworzec Gdański"),
    ((598, 442), u"Muranów"),
    ((598, 481), u"Ratusz Arsenał"),
    ((598, 527), u"Świętokrzyska"),
    ((598, 578), u"Centrum"),
    ((598, 637), u"Plac Konstytucji"),
    ((600, 688), u"Politechnika"),
    ((580, 739), u"Pole Mokotowskie"),
    ((578, 786), u"Racławicka"),
    ((580, 836), u"Wierzbno"),
    ((578, 889), u"Wilanowska"),
    ((580, 938), u"Służew"),
    ((600, 985), u"Ursynów"),
    ((619, 1040), u"Stokłosy"),
    ((639, 1087), u"Imielin"),
    ((660, 1139), u"Natolin"),
    ((678, 1188), u"Kabaty"),
)

LINE_2 = (
    ((98, 478), u"Chrzanów"),
    ((147, 426), u"Lazurowa"),
    ((198, 426), u"Powstańców Śląskich"),
    ((249, 426), u"Wola Park"),
    ((299, 478), u"Księcia Janusza"),
    ((348, 528), u"Moczydło"),
    ((399, 528), u"Płocka"),
    ((448, 528), u"Wolska"),
    ((499, 528), u"Rondo Daszyńskiego"),
    ((548, 528), u"Rondo ONZ"),
    ((598, 528), u"Świętokrzyska"),
    ((649, 528), u"Nowy Świat"),
    ((698, 528), u"Powiśle"),
    ((799, 528), u"Stadion"),
    ((799, 480), u"Dworzec Wileński"),
    ((828, 426), u"Szwedzka"),
    ((859, 375), u"Targówek"),
    ((889, 328), u"Targówek bis"),
    ((889, 279), u"Zacisze"),
    ((859, 228), u"Kondratowicza"),
    ((828, 175), u"Rembielińska"),
)


# Klasa pociąg
class Train:
    def __init__(self, start_time, color, line):
        self.start_time = start_time
        self.color = color
        self.line = line

    # Zwraca pozycję, a dokładnie ile minut pociąg jest już w ruchu (w trasie)
    def get_position(self, tp):
        minutes = (tp - self.start_time).seconds // 60
        return minutes

    # Zwraca kolor pociągu do celów wizualizacji
    def get_color(self):
        return self.color

    # Zwraca czas w którym pociąg został włączony do ruchu
    def get_st(self):
        return self.start_time

    # Zwraca czas w którym pociąg został włączony do ruchu
    def get_line(self):
        return self.line


# Zwraca pozycję na podstawie przekazanego czasu, uwzględnia powrót pociągu
def get_train_station(pt, line):
    if line == 1:
        current_position = pt % len(LINE_1)
        if (pt // len(LINE_1)) % 2 == 0:  # Parzysty przebieg odpowiada trasie powrotnej
            current_position = len(LINE_1) - current_position - 1
        return current_position
    elif line == 2:
        current_position = pt % len(LINE_2)
        if (pt // len(LINE_2)) % 2 == 0:  # Parzysty przebieg odpowiada trasie powrotnej
            current_position = len(LINE_2) - current_position - 1
        return current_position


# Wyświetla elipsę (okrąg) wskazujący aktualną pozycję pociągu
def draw_train_position(coords, cl, number, text):
    draw = ImageDraw.Draw(im)
    x, y = coords
    draw.ellipse((x - 20, y - 20, x + 20, y + 20), fill=cl, outline='blue')
    font = ImageFont.truetype(path.join(fonts_dir, "Arial.ttf"), size=24)
    draw.text((225, 1250+30*number), f"{text}", font=font, fill=cl)


# Główna część skryptu

assert TRAINS_NUMBER <= 10

t0 = datetime.strptime(START_TIME, '%H:%M')
t = 0
add = ADD_TRAIN_AFTER
trains = list()

while t < TOTAL_TIME:
    im = Image.open("Metro2.png")
    current_time = t0 + timedelta(minutes=t)

    if add == ADD_TRAIN_AFTER and len(trains) < TRAINS_NUMBER:
        add = 0
        trains.append(Train(current_time, COLORS[len(trains)], 1))
        trains.append(Train(current_time, COLORS[len(COLORS) - len(trains)], 2))

    for i, train in enumerate(trains):
        line = train.get_line()
        if line == 1:
            coords, current_station = LINE_1[get_train_station(train.get_position(current_time), 1)]
        elif line == 2:
            coords, current_station = LINE_2[get_train_station(train.get_position(current_time), 2)]
        train_st = datetime.strftime(train.get_st(), "%H:%M")
        text = f"Pociąg ({i+1}) linii nr {line} w trasie od {train_st} obecnie jest na stacji {current_station}"
        draw_train_position(coords, train.get_color(), i+1, text)

    t += 1
    add += 1
    im.save(path.join(images_dir, f"img-{t:06}.png"))
