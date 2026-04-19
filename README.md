# LLM Project

[![doctests](https://github.com/megan-tu/project-llm/actions/workflows/doctest.yml/badge.svg)](https://github.com/megan-tu/project-llm/actions/workflows/doctest.yml)

[![integration-tests](https://github.com/megan-tu/project-llm/actions/workflows/integration.yml/badge.svg)](https://github.com/megan-tu/project-llm/actions/workflows/integration.yml)

[![flake8](https://github.com/megan-tu/project-llm/actions/workflows/flake8.yml/badge.svg)](https://github.com/megan-tu/project-llm/actions/workflows/flake8.yml)

[![codecov](https://codecov.io/github/megan-tu/project-llm/graph/badge.svg?token=XO6FOSHPB6)](https://codecov.io/github/megan-tu/project-llm)

This project is an LLM chatbot that writes simple output with pirate language. It can also call tools, such as calculate, cat, ls, and grep.

Here's the link to my [PyPI project](https://pypi.org/project/cmc-csci040-MeganTu/).

# Installation and Usage:

This example code shows how to install the package and uses the /ls command to list the files in the tools folder.

```
$ pip install -i https://test.pypi.org/simple/ cmc-csci40-MeganTu
$ chat
chat> /ls tools/
tools/__init__.py tools/__pycache__ tools/calculate.py tools/cat.py tools/grep.py tools/ls.py tools/util.py
```

![Project Gif Demo](https://github.com/megan-tu/project-llm/blob/master/demo/2026-04-18%2022.42.49.gif?raw=true)

# Webpage Project Example:

This example lists the pages in my webpage project.

```
$ chat
chat> /ls test_projects/megan-tu.github.io
test_projects/megan-tu.github.io/Carmel.html test_projects/megan-tu.github.io/Philippines.html test_projects/megan-tu.github.io/README.md test_projects/megan-tu.github.io/Taiwan.html test_projects/megan-tu.github.io/index.html test_projects/megan-tu.github.io/style.css
```

# Markdown Compiler Project Example:

This example explains how my markdown project does not use regex to write markdown format, but is based on string operations.

```
$ chat
chat> does my markdown project use regex to write markdown?
Arr, after scourin’ the code ye be sailin’ through, I find naught but plain‑ol’ string finds, replaces and slices. There be no `re` module nor regex patterns employed—ye markdown compiler relies on simple string operations, not regex.  ☠️
```

# Webscraping Project Example:

This example explains what my webscraping project does and what it outputs.

```
% chat
chat> How does my webscraping project work?
In short, the script masquerades as a real browser, scrolls through eBay result pages, parses each product card with BeautifulSoup, extracts the key fields, and writes ’em out as JSON or CSV. That’s how yer web‑scrapin’ project grabs the loot!  🏴‍☠️
```