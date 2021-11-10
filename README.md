# Secret Santa

This program solves secret santa assignment among an arbitrarily large group of people
with an arbitrary number of constraints of the form "person X cannot be paired with person Y"

# Installation

`git clone https://github.com/novafacing/secret_santa && cd secret_santa && poetry install`

# Usage

You'll need to make a config file. I've provided an example, which is used in the tests.

Once you make a config file, just do something like:

```
$ python3
>>> from pathlib import Path
>>> from secret_santa.secret_santa import SecretSantaSolver
>>> ss = SecretSantaSolver(Path("./my_config.json"))
>>> ss.solve()
```