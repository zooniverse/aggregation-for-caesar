#!/usr/bin/env pythonw

import os
import panoptes_aggregation

try:
    import gooey
except ImportError:
    raise ImportError('The GUI component is not installed, reinstall with `pip install -U panoptes_aggregation[gui]`')

panoptes_aggregation.scripts.pbar_override(panoptes_aggregation.scripts.pbe)
panoptes_aggregation.scripts.pbar_override(panoptes_aggregation.scripts.pbr)
panoptes_aggregation.scripts.gui_override(gooey)

current_folder = os.path.dirname(os.path.abspath(__file__))

gui = gooey.Gooey(
    program_name="Aggregate",
    default_size=(1000, 1150),
    progress_regex=r"^[a-zA-Z:\s|]+ (\d+)% .+$",
    terminal_font_family="Consolas",
    navigation='TABBED',
    image_dir=os.path.join(current_folder, 'icons')
)(panoptes_aggregation.scripts.parser_main)

if __name__ == '__main__':
    gui()
