#!/usr/bin/env pythonw

import gooey
from gui_overrides import gui_override, pbar_override
from aggregation_parser import main, pbe, pbr
import os

pbar_override(pbe)
pbar_override(pbr)
gui_override(gooey)

current_folder = os.path.dirname(os.path.abspath(__file__))

gui = gooey.Gooey(
    program_name="Aggregate",
    default_size=(1000, 1150),
    progress_regex=r"^[a-zA-Z:\s|]+ (\d+)% .+$",
    terminal_font_family="Consolas",
    navigation='TABBED',
    image_dir=os.path.join(current_folder, 'icons')
)(main)

if __name__ == '__main__':
    gui()
