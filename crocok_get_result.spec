# -*- mode: python -*-

block_cipher = None


a = Analysis(['crocok_get_result.py'],
             pathex=['C:\\Users\\ASenkovskiy\\PycharmProjects\\CrocokGetResult'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas + [("key.pem", ".\\key.pem", "DATA"), ("croc.jpg", ".\\croc.jpg", "DATA")],
          name='crocok_get_result.exe',
          debug=False,
          strip=False,
          upx=True,
          console=False , 
		  icon='crocicon.ico'
		  )
