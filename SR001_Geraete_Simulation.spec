# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/Users/roze/Documents/Python Projekte/Seminarraum_001_Mediensteuerung/SR001_Geraete_Simulation.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/roze/Documents/Python Projekte/Seminarraum_001_Mediensteuerung/Universität_Heidelberg.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SR001_Geraete_Simulation',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\roze\\Documents\\Python Projekte\\Seminarraum_001_Mediensteuerung\\Universität_Heidelberg.ico'],
)
