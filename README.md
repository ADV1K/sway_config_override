# Sway Configuration Override Implementation

## Running It on sample config
```shell
$ python3 sway_config.py config
```

## File Structure
```
 .
├──  config.d
│  ├──  global
│  │  ├──  10_font
│  │  └──  20_colors
│  └──  local
│     └──  10_font
├──  config           --> sample config
└──  sway_config.py   --> main program
```


## Task Description
sway is a replacement for the popular i3 windows manager in Linux. We care a lot about it because a very successful project from GSoC '22 integrated it in Regolith linux, a ubuntu based distribution that we love.

A configuration option that sway has (and i3 as well) is to include partial configuration files from directories, like this:

File: /etc/regolith/sway/config

```
###############################################################################
# sway Config Partials
###############################################################################

# Include any regolith sway partials
include /usr/share/regolith/sway/config.d/*

# Include any user sway partials
include $HOME/.config/regolith2/sway/config.d/*
```

Note that it first imports the global configuration, then the user configuration, which often overlaps. We want to add a new directive called include_one that would work like this:

```
include_one $HOME/.config/regolith2/sway/config.d/* /usr/share/regolith/sway/config.d/*
```

Note that both directories are passed to the same include_one. It would include all the files in the first directory and then from the second directory it would only import the files that weren't import before. So if the first directory contains a file called for example, "70_bar" then such file would be skipped when processing the second directory.

