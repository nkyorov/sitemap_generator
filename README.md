# Sitemap Generator Tool

> Based on single threaded web crawler. The general behaviour can be described as neutral/polite. Sitemap is created in both XML file format, as well as plotted as a graph. Developed as part of the degree specification for BSc Computer Science with Distributed Systems, University of Leeds 2019.
## Table of Contents 

> If you're `README` has a lot of info, section headers might be nice.

- [Manual Installation](#manual_installation)
- [Automatic Installation](#automatic_installation)



---

## Manual Installation
Make sure that tkinter is installed on your operating system.

```shell
$ sudo apt-get install python3-tk
```

Set up virtual environment

```shell
$ python3 -m venv [virtualenv_name]
```
Once in the folder virtualenv_name, the virtual environment must be started.

```shell
$ python3 -m source bin/activate
```

All external packages must be installed. We have included a file called requirements.txt with
all containing all packages to speed up the process.

```shell
$ pip3 install -r requirements.txt
```

## Automatic installation

Run the basic script that sets up the virtual environment and installs required packages

```shell
$ sh setup.sh
```






