compile into an executable using:

```
pyinstaller --clean --windowed --icon serpent.icns --add-data "serpent.png:." --noconfirm --name SerpentSerialTool serpent.py
```
or 
```
pyinstaller SerpentSerialTool.spec
```

`--clean` clears temp files
`--windowed` generates an application file on MacOS
`--icon <icon.ico or icon.icns>`
`--add-data "<filepath>:."` includes a file or directory
