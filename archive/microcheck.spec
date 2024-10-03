# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['microcheck.py'],
             pathex=[r'C:\Users\Dell\Desktop\school\Microcheck'],
             binaries=[
                 (r'C:\Users\Dell\Desktop\school\Microcheck\myenv\Lib\site-packages\torch\lib\fbgemm.dll', 'torch/lib'),
                 (r'C:\Users\Dell\Desktop\school\Microcheck\myenv\Lib\site-packages\torch\lib\*.dll', 'torch/lib')
             ],
             datas=[
                 (r'C:\Users\Dell\Desktop\school\Microcheck\assets', 'assets'),
                 (r'C:\Users\Dell\Desktop\school\Microcheck\yolo_microplastic.pt', 'yolo_microplastic.pt')
             ],
             hiddenimports=['torch', 'ultralytics'],
             hookspath=[r'C:\Users\DELL\Desktop\school\Microcheck\hook-torch.py'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='microcheck',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='microcheck')
