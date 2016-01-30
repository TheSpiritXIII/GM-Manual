GM-Manual
=========
`GM-Manual` is a small Python module that maps keywords to online `GameMaker: Studio` documentation URLs licensed with the MIT license. Additionally, it comes with a small self-contained IRC client that utilizes the functions, licensed with GPL3.

Usage
-----
Just include `gm_manual.py` and then import it with `import gm_manual`.

Finally, basic usage is outlined below:
```
manual = gm_manual.ManualIndex.load() # Load the manual from YYG's website.
manual.insert("some_function", "www.example.com", "Description") # Example of adding custom function.
manual.find("draw_sprite", 0) # Show description and URL of first instance of requested function or 'Not found'.
```
