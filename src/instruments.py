#!/usr/local/bin/python3
# coding=utf-8

GM_INSTRUMENTS = {

    # Piano

    0 : 'Acoustic Grand Piano',
    1 : 'Bright Acoustic Piano',
    2 : 'Electric Grand Piano',
    3 : 'Honky-tonk Piano',
    4 : 'Electric Piano 1',
    5 : 'Electric Piano 2',
    6 : 'Harpsichord', #yes
    7 : 'Clavinet',

  # Chromatic Percussion

    8 : 'Celesta',
    9 : 'Glockenspiel',
   10 : 'Music Box',
   11 : 'Vibraphone',
   12 : 'Marimba', #no
   13 : 'Xylophone', #no
   14 : 'Tubular Bells', #no
   15 : 'Dulcimer',

  # Organ

   16 : 'Drawbar Organ',
   17 : 'Percussive Organ',
   18 : 'Rock Organ',
   19 : 'Church Organ',
   20 : 'Reed Organ',
   21 : 'Accordion', #no
   22 : 'Harmonica', #no
   23 : 'Tango Accordion', #no

  # Guitar

   24 : 'Acoustic Guitar (nylon)',
   25 : 'Acoustic Guitar (steel)', #yes
   26 : 'Electric Guitar (jazz)', #yes
   27 : 'Electric Guitar (clean)', #yes
   28 : 'Electric Guitar (muted)',
   29 : 'Overdriven Guitar',
   30 : 'Distortion Guitar', #yes
   31 : 'Guitar Harmonics',

  # Bass

   32 : 'Acoustic Bass',
   33 : 'Electric Bass (finger)',
   34 : 'Electric Bass (pick)',
   35 : 'Fretless Bass',
   36 : 'Slap Bass 1',
   37 : 'Slap Bass 2',
   38 : 'Synth Bass 1',
   39 : 'Synth Bass 2',
   
  # Strings
   
   40 : 'Violin',
   41 : 'Viola',
   42 : 'Cello',
   43 : 'Contrabass',
   44 : 'Tremolo Strings',
   45 : 'Pizzicato Strings',
   46 : 'Orchestral Harp',
   47 : 'Timpani',
   
  # Ensemble
   
   48 : 'String Ensemble 1',
   49 : 'String Ensemble 2',
   50 : 'Synth Strings 1',
   51 : 'Synth Strings 2',
   52 : 'Choir Aahs', # (Starlight Vox)
   53 : 'Voice Oohs',
   54 : 'Synth Choir',
   55 : 'Orchestra Hit',
   
  # Brass
  
   56 : 'Trumpet',
   57 : 'Trombone',
   58 : 'Tuba',
   59 : 'Muted Trumpet',
   60 : 'French Horn',
   61 : 'Brass Section',
   62 : 'Synth Brass 1',
   63 : 'Synth Brass 2',
   
  # Reed
   
   64 : 'Soprano Sax',
   65 : 'Alto Sax',
   66 : 'Tenor Sax',
   67 : 'Baritone Sax',
   68 : 'Oboe',
   69 : 'English Horn',
   70 : 'Bassoon',
   71 : 'Clarinet',
   
  # Pipe
   
   72 : 'Piccolo',
   73 : 'Flute',
   74 : 'Recorder',
   75 : 'Pan Flute',
   76 : 'Blown bottle', # (Airways)
   77 : 'Shakuhachi',
   78 : 'Whistle',
   79 : 'Ocarina',
   
  # Synth Lead
   
   80 : 'Lead 1 (square)',
   81 : 'Lead 2 (sawtooth)',
   82 : 'Lead 3 (calliope)',
   83 : 'Lead 4 (chiff)',
   84 : 'Lead 5 (charang)',
   85 : 'Lead 6 (voice)',
   86 : 'Lead 7 (fifths)',
   87 : 'Lead 8 (bass + lead)',
   
  # Synth Pad

   88 : 'Pad 1 (new age)', #yes - super cool (Sea of Glass)
   89 : 'Pad 2 (warm)', #no
   90 : 'Pad 3 (polysynth)',
   91 : 'Pad 4 (choir)',
   92 : 'Pad 5 (bowed)', #yes - (Rain Clouds)
   93 : 'Pad 6 (metallic)', #yes - super cool (Sea of Glass)
   94 : 'Pad 7 (halo)',
   95 : 'Pad 8 (sweep)',
   
  # Synth Effects
   
   96 : 'FX 1 (rain)', #yes (Event Horizon)
   97 : 'FX 2 (soundtrack)',
   98 : 'FX 3 (crystal)',
   99 : 'FX 4 (atmosphere)',
  100 : 'FX 5 (brightness)', #yes
  101 : 'FX 6 (goblins)', #no
  102 : 'FX 7 (echoes)',
  103 : 'FX 8 (sci-fi)', #no
  
  # Ethnic
  
  104 : 'Sitar', #yes
  105 : 'Banjo',
  106 : 'Shamisen', #no
  107 : 'Koto',
  108 : 'Kalimba', #no
  109 : 'Bagpipe',
  110 : 'Fiddle',
  111 : 'Shanai', #yes - (Saxophone)
  
  # Percussive
  
  112 : 'Tinkle Bell',
  113 : 'Agogo',
  114 : 'Steel Drums',
  115 : 'Woodblock', #no
  116 : 'Taiko Drum',
  117 : 'Melodic Tom', #yes
  118 : 'Synth Drum', #yes
  119 : 'Reverse Cymbal',
  
  # Sound effects
  
  120 : 'Guitar Fret Noise', #yes
  121 : 'Breath Noise',
  122 : 'Seashore',
  123 : 'Bird Tweet',
  124 : 'Telephone Ring',
  125 : 'Helicopter', #no
  126 : 'Applause',
  127 : 'Gunshot'
}

DRUM_SOUND_NOTES = {
    35 : "Acoustic Bass Drum",
    36 : "Bass Drum",
    37 : "Side Stick",
    38 : "Acoustic Snare",
    39 : "Hand Clap",
    40 : "Electric Snare",
    41 : "Low Floor Tom",
    42 : "Closed Hi Hat",
    43 : "High Floor Tom",
    44 : "Pedal Hi Hat",
    45 : "Low Tom",
    46 : "Open hi Hat",
    47 : "Low Mid Tom",
    48 : "Hi Mid Tom",
    49 : "Crash Cymbal 1",
    50 : "High Tom",
    51 : "Ride Cymbal 1",
    52 : "Chinese Cymbal",
    53 : "Ride Bell",
    54 : "Tambourine",
    55 : "Splash Cymbal",
    56 : "Cowbell",
    57 : "Crash Cymbal 2",
    58 : "Vibra slap",
    59 : "Ride Cymbal 2",
    60 : "Hi Bongo",
    61 : "Low Bongo",
    62 : "Mute Hi Conga",
    63 : "Open Hi Conga",
    64 : "Low Conga",
    65 : "High Timbale",
    66 : "Low Timbale",
    67 : "High Agogo",
    68 : "Low Agogo",
    69 : "Cabasa",
    70 : "Maracas",
    71 : "Short Whistle",
    72 : "Long Whistle",
    73 : "Short Guiro",
    74 : "Long Guiro",
    75 : "Claves",
    76 : "Hi Wood Block",
    77 : "Low Wood Block",
    78 : "Mute Cuica",
    79 : "Open Cuica",
    80 : "Mute Triangle",
    81 : "Open Triangle"
}

def get_gm_instrument_name(gm_program):
  if gm_program in GM_INSTRUMENTS:
    return GM_INSTRUMENTS[gm_program]
  return None