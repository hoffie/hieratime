# hieratime
hieratime is a python-based hierarchical time tracker with a simple vim integration.

## Prerequisites
vim with python support

## Platforms
Until now, hieratime has only been tested on Linux; in theory it should run on other go-supported systems as well.

## Installation
- clone this repository
- copy the contents of [vimrc](vimrc) to your ~/.vimrc config file
- adapt the path to your hieratime clone in your .vimrc

## Usage
1. Start by opening [example.hieratime](example.hieratime) in a new vim instance.
2. Navigate to the *Work* entry and expand it using `zA` (all vim folding commands should work).
3. Navigate to *Examining hieratime* and start a clock by hitting `Ctrl + H` `Ctrl + I` (**h**ieratime clock-**i**n).
4. After you are done with your hieratime tests, stop the clock again using `Ctrl + H` `Ctrl + O` (**h**ieratime clock-**o**ut). In order to remember what you have done, you can add some quick notes directly after the CLOCK lines using standard vim commands (such as `o` for inserting a new line after the CLOCK entry).
5. If you manually edit any timestamps you can re-calculate all durations and fix formatting by typing `Ctrl + H` `Ctrl + H`.

## Notes
- Be sure that your own file also has the .hieratime extension as the keyboard shortcuts are bound to the extension.
- Expect this extension to be rather slow with larger files. Although no concrete tests have been done yet, the parsing is currently not really optimized and each modification requires the whole file to be re-parsed.
- The file format and the working principle are heavily inspired by emacs orgmode's time tracking. However, this project does not try to compete with of orgmode. orgmode is way more powerful and this project is just a very basic time tracking tool.
- If you are using this in production, it is recommended to place the file under versioning with git or similar tools.
- The file format is pretty flexible and any parsing problems should be automatically detected without destroying any data. However, nothing is perfect...
- The mentioned basic features certainly do not provide any magic. However, extracting data from .hieratime files in order to import them into time tracking systems or generate reporting tables should be pretty easy using the python API.

## License
hieratime is distributed under the [MIT license](LICENSE.MIT)

## Author
This project was initially created by Christian Hoffmann ([@hoffie](https://github.com/hoffie)).
