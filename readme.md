compile into an executable using:

```
pyinstaller --clean --windowed --add-data "bracks.png:." kinter.py
```

`--clean` clears temp files
`--windowed` generates an application file on MacOS
`--add-data "<filepath>:."` includes a file or directory