# repo-filter

This is a git filtering script for [automuteus](https://github.com/AutoMuteUs-Portable/automuteus) and [galactus](https://github.com/AutoMuteUs-Portable/galactus)

# Usage
1. Clone this repository
2. Run `pip install .` to install the command
3. Run `repo-filter --help` to see the command usage

# Notes
This is built for my personal use. It uses dill(alternative to pickle) to dump and load filter classes. There is potential threat of being arbitrary code execution. So, please use this at your own risk.