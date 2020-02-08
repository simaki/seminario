# Seminario

[![version](https://img.shields.io/pypi/v/seminario.svg)](https://pypi.org/project/seminario/)
[![Build Status](https://travis-ci.org/simaki/seminario.svg?branch=master)](https://travis-ci.com/simaki/seminario)
[![codecov](https://codecov.io/gh/simaki/seminario/branch/master/graph/badge.svg)](https://codecov.io/gh/simaki/seminario)
[![LICENSE](https://img.shields.io/github/license/simaki/seminario)](LICENSE)

Python package for seminar organization.

## Installation

```sh
$ pip install seminario
```

## Requirement

- [wkhtmltopdf](https://wkhtmltopdf.org/)

## How to use

1. Copy [sample](sample/) directory.
2. Edit [`config.yml`](sample/data/config.yml) as you like.
3. Replace [`database.csv`](sample/data/database.csv) with your own one.
4. That's it!  Now you can add seminars and make posters by running `main.py`:

```sh
$ python main.py
```
