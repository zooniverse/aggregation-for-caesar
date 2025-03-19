#!/usr/bin/env pythonw

import sys
import multiprocessing

target = None
if "__compiled__" in globals():
    target = sys.argv[0]
    multiprocessing.freeze_support()

import os
import inspect
import panoptes_aggregation

if sys.platform == 'win32':
    stack_filename = [s.filename for s in inspect.stack() if ('.exe' in s.filename)]
    if len(stack_filename) == 1:
        # when on windows make sure a copy of the calling script does not have `.exe`
        # at the end of the filename
        base_name = stack_filename[0].split('.exe')[0]
        exe = '{0}.exe'.format(base_name)
        import shutil
        if not os.path.isfile(base_name):
            shutil.copy2(exe, base_name)

try:
    import gooey
    import gooey.gui.components.console
except ImportError:
    raise ImportError('The GUI component is not installed, reinstall with `pip install -U panoptes_aggregation[gui]`')

panoptes_aggregation.scripts.pbar_override(panoptes_aggregation.scripts.pb)
panoptes_aggregation.scripts.gui_override(gooey)

current_folder = os.path.dirname(os.path.abspath(__file__))

help_items = [
    {
        'type': 'Link',
        'menuTitle': 'Documentation',
        'url': 'https://aggregation-caesar.zooniverse.org/docs'
    }
]

if "__compiled__" in globals():
    # when packaged we need to make the licenses for each dependency available
    # to view in the GUI as these .txt files will be packaged inside the executable
    if sys.platform == 'darwin':
        # due to file permission errors these can't be opened directly
        # instead provide instructions for navigating to the files
        help_items.append({
            'type': 'MessageDialog',
            'menuTitle': 'Dependencies Licenses Information',
            'message': 'The licenses for all packaged dependencies can be found inside this application.  To view these files control click the application, select "Show Package Contents", and navigate to the "Contents/Resources" folder.  A summary of each license is contained in "dependency_licenses_summary.txt" and the full license text is in "dependency_licenses_full.txt".',
            'caption': 'Dependencies Licenses'
        })
    elif sys.platform == 'win32':
        # Windows has no issue just opening the files :D
        help_items.append({
            'type': 'Link',
            'menuTitle': 'Dependencies Licenses Summary',
            'url': f'file://{current_folder}/dependency_licenses_summary.txt'
        })
        help_items.append({
            'type': 'Link',
            'menuTitle': 'Dependencies Licenses Full Text',
            'url': f'file://{current_folder}/dependency_licenses_full.txt'
        })

menu = [{
    'name': 'Help',
    'items': help_items
}]

gui = gooey.Gooey(
    program_name="Aggregate",
    default_size=(1000, 900),
    progress_regex=r"^[a-zA-Z:\s|]+ (\d+)% .+$",
    terminal_font_family="Consolas",
    navigation='TABBED',
    image_dir=gooey.local_resource_path(os.path.join(current_folder, 'icons')),
    target=target,
    menu=menu
)(panoptes_aggregation.scripts.parser_main)

if __name__ == '__main__':
    gui()
