import os
from PyInstaller.utils.hooks import get_package_paths

block_cipher = None

_, llama_cpp_pkg_path = get_package_paths('llama_cpp')

llama_dll_path = os.path.join(llama_cpp_pkg_path, 'lib', 'llama.dll')

a = Analysis(
    ['Nexus.py'],
    pathex=[],
    binaries=[
        (llama_dll_path, 'llama_cpp/lib')
    ],
    datas=[
        ('cmd.ico', '.'),
        (os.path.join(llama_cpp_pkg_path, 'lib'), 'llama_cpp/lib')
    ],
    hiddenimports=['llama_cpp', 'art', 'pyperclip', 'tqdm'],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NexusAI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='cmd.ico',
)
