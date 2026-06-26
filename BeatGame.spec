# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['PolisosFifow.py'],
    pathex=[],
    binaries=[],
    datas=[('Acuraccy_FromBeatGame.ttf', '.'), ('menu photo.jpg', '.'), ('MenuMusik.mp3', '.'), ('navedenie svuk.mp3', '.'), ('PressSound.mp3', '.'), ('Score_fromBeatGame.ttf', '.'), ('SetButton.mp3', '.'), ('Sick_fromBeatGame.ttf', '.'), ('start_game.ttf', '.'), ('UnSetButton.mp3', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='BeatGame',
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
)
