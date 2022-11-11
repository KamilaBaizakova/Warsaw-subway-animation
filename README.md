# Warsaw-subway-animation

This animation was made for "Discrete systems simulation" class in my university course in Python.  

Subway animation of 2 existing lines in Warsaw was made by using the FFMPEG technology. Generated 600 png files and then combined them to animation.

The following "simulation" parameters were used:

Because there are two metro lines: there will be more than one train on the first line and n trains on the second line will be introduced into traffic at regular intervals

Parameters (set in the script code): t - time step T - duration of the entire simulation

V - train speed tps - stopping time at the station

The stations (for both lines) will be separated by different distances: d1..dn - distances expressed in km

For each individual time step, one graphic is prepared from: on the map:

marked with the current position of each train. in the table:
condition of each train - en route / at station
information at which station a specific train is located (or between which it is moving)
Finally, we get one animation file using the FFMPEG technology.

Commands before running the script:

We need to create a directory / images_dir

Run the script and when all PNG files have been created, run the FFMPEG command:

ffmpeg -framerate 2 -pattern_type glob -i '* .png' -c: v libx264 -pix_fmt yuv420p -r 24 animation.mp4


Generated animation using Python script 

[Animacja-2linie-10pociagow.webm](https://user-images.githubusercontent.com/72921900/201239198-3065d98e-bbe5-41ff-b0ac-cd39f0b75b5e.webm)

