# LLM Project

[![doctests](https://github.com/megan-tu/project-llm/actions/workflows/doctest.yml/badge.svg?branch=features)](https://github.com/megan-tu/project-llm/actions/workflows/doctest.yml) [![integration-tests](https://github.com/megan-tu/project-llm/actions/workflows/integration.yml/badge.svg?branch=features)](https://github.com/megan-tu/project-llm/actions/workflows/integration.yml) [![flake8](https://github.com/megan-tu/project-llm/actions/workflows/flake8.yml/badge.svg?branch=features)](https://github.com/megan-tu/project-llm/actions/workflows/flake8.yml) [![codecov](https://codecov.io/github/megan-tu/project-llm/graph/badge.svg?token=XO6FOSHPB6)](https://codecov.io/github/megan-tu/project-llm) [![Publish Python distribution to PyPI](https://github.com/megan-tu/project-llm/actions/workflows/publish-to-pypi.yaml/badge.svg)](https://github.com/megan-tu/project-llm/actions/workflows/publish-to-pypi.yaml)

This project is an LLM chatbot that writes simple output with pirate language. It can also call tools, such as calculate, cat, ls, and grep.

Here's the link to my [PyPI project](https://pypi.org/project/cmc-csci40-MeganTu/).

## Installation and Usage:

This example code shows how to install the package, uses the /ls command to list the files in the tools folder, and demonstrates how the chatbot works in multiple rounds.

```
$ pip install -i https://test.pypi.org/simple/ cmc-csci40-MeganTu
$ chat
chat> /ls tools/
tools/__init__.py tools/__pycache__ tools/calculate.py tools/cat.py tools/doctest.py tools/grep.py tools/ls.py tools/rm.py tools/util.py tools/write_file.py tools/write_files.py
chat> My name is Bob
Ahoy, Bob! Ye be sailin’ these digital seas with a fine name. May the wind be ever at yer back, matey!
chat> I'm 23 years old.
Aye, a spry 23 summers on the deck, Bob! May yer voyages be full o’ treasure and good rum!
chat> What's my name?
Yer name be Bob, matey!
chat> How old am I?
Ye be 23 years o’ age, matey!
```

![Project Gif Demo](https://github.com/megan-tu/project-llm/blob/master/demo/2026-04-18%2022.42.49.gif?raw=true)

## More Examples

This example lists the pages in my webpage project.

```
$ cd megan-tu.github.io
$ chat
chat> /ls test_projects/megan-tu.github.io
test_projects/megan-tu.github.io/Carmel.html test_projects/megan-tu.github.io/Philippines.html test_projects/megan-tu.github.io/README.md test_projects/megan-tu.github.io/Taiwan.html test_projects/megan-tu.github.io/index.html test_projects/megan-tu.github.io/style.css
```

This example explains how my markdown project does not use regex to write markdown format, but is based on string operations.

```
$ cd test_projects/markdown-project
$ chat
chat> does my markdown project use regex to write markdown?
Arr, after scourin’ the code ye be sailin’ through, I find naught but plain‑ol’ string finds, replaces and slices. There be no `re` module nor regex patterns employed—ye markdown compiler relies on simple string operations, not regex.  ☠️
```

This example explains what my webscraping project does and what it outputs.

```
$ cd test_projects/project-webscraping
$ chat
chat> How does my webscraping project work?
In short, the script masquerades as a real browser, scrolls through eBay result pages, parses each product card with BeautifulSoup, extracts the key fields, and writes ’em out as JSON or CSV. That’s how yer web‑scrapin’ project grabs the loot!  🏴‍☠️
```

This example demonstrates how the chatbot can create or delete files when asked, and the changes are automatically added and committed to the git repo.

```
$ ls
__pycache__           file2.txt
example1.py             test1.txt
example2.py             Trump_tweets_graph.png
file1.py
$ git log --oneline
6390af6 (HEAD -> features, origin/features) ls
$ chat
chat> write_file('test_examples/example_3.py', 'x = "hello world"', 'example_3')
Arrr, file be written, matey!
chat> ^D
$ ls test_examples
__pycache__           file1.py
example_3.py            file2.txt
example1.py             test1.txt
example2.py             Trump_tweets_graph.png
$ git log --oneline
671af4e (HEAD -> features) [docchat] example_3
$ chat
chat> can you remove 'test_examples/example_3.py'
File 'test_examples/example_3.py' has been removed.
chat> ^D
$ ls test_examples
__pycache__           example1.py             example2.py             file1.py                file2.txt               test1.txt               Trump_tweets_graph.png
```