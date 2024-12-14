# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['microcheck_app.py'],  # Main script
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),  # Include the assets folder
        ('Pytorch_UNet', 'Pytorch_UNet'),  # Include the Pytorch_UNet folder
        ('unet_tuning_epoch_50.pth', '.'),  # Include the model file in the root
    ],
    hiddenimports=[
        'torchvision.transforms',  # Ensure torchvision.transforms is included
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Microcheck',  # Name of the executable
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window for GUI app
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Microcheck'
)
