# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Jukebox application
Builds standalone executables for Linux and Windows
"""

import os
import sys
from pathlib import Path

block_cipher = None

# Get the base directory
base_dir = Path('.').resolve()
src_dir = base_dir / 'src'
static_dir = src_dir / 'server' / 'static'

# Collect all data files
datas = [
    (str(static_dir), 'src/server/static'),
    (str(base_dir / 'env.example'), '.'),
    (str(base_dir / 'README.md'), '.'),
]

# Add template files if they exist
templates_dir = src_dir / 'server' / 'templates'
if templates_dir.exists():
    datas.append((str(templates_dir), 'src/server/templates'))

# Hidden imports for dynamic imports
hiddenimports = [
    'flask',
    'flask_cors',
    'dotenv',
    'selenium',
    'mercadopago',
    'requests',
    'jsonschema',
    'pydantic',
    'cryptography',
    'src.db',
    'src.db.models',
    'src.hardware',
    'src.hardware.bill_acceptor',
    'src.payments',
    'src.payments.base_gateway',
    'src.payments.mercadopago_gateway',
    'src.youtube',
    'src.youtube.youtube_player',
    'src.youtube.idle_music_manager',
    'src.server.config',
]

# Conditionally add RPi.GPIO for Raspberry Pi builds
# This will fail on non-Raspberry Pi systems, which is expected
try:
    import RPi.GPIO
    hiddenimports.append('RPi.GPIO')
except:
    pass

a = Analysis(
    ['src/server/app.py'],
    pathex=[str(base_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='jukebox',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
