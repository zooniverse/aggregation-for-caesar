# -*- mode: python ; coding: utf-8 -*-
"""
Example build.spec file

This hits most of the major notes required for
building a stand alone version of your Gooey application.
"""


import os
import gooey

from PyInstaller.building.api import EXE, PYZ, COLLECT
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.datastruct import Tree
from PyInstaller.building.osx import BUNDLE

gooey_root = os.path.dirname(gooey.__file__)
gooey_languages = Tree(os.path.join(gooey_root, 'languages'), prefix = 'gooey/languages')
gooey_images = Tree(os.path.join(gooey_root, 'images'), prefix = 'gooey/images')

block_cipher = None

a = Analysis(
    ['panoptes_aggregation/scripts/gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        (os.path.join('panoptes_aggregation', 'scripts', 'icons', '*'), 'icons')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0
)
pyz = PYZ(a.pure)

options = [('u', None, 'OPTION'), ('X utf8', None, 'OPTION')]

exe = EXE(
    pyz,
    a.scripts,
    # a.binaries,
    # a.datas,
    options,
    gooey_languages,
    gooey_images,
    exclude_binaries=True,
    # exclude_binaries=False,
    name='panoptes_aggregation_gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=True,
    argv_emulation=False,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join('panoptes_aggregation', 'scripts', 'icons', 'program_icon.ico')
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='panoptes_aggregation_gui',
)

# info_plist = {'addition_prop': 'additional_value'}
app = BUNDLE(
    # exe,
    coll,
    name='panoptes_aggregation_gui.app',
    bundle_identifier=None,
    icon=os.path.join('panoptes_aggregation', 'scripts', 'icons', 'program_icon.ico')
    # info_plist=info_plist
)
