compile into an executable using:

```
pyinstaller --clean --windowed --icon robo.icns --add-data "bracks.png:." kinter.py
```

`--clean` clears temp files
`--windowed` generates an application file on MacOS
`--icon <icon.ico or icon.icns>`
`--add-data "<filepath>:."` includes a file or directory
