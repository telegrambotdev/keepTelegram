# keepTelegram

[![Language](https://img.shields.io/badge/language-python-brightgreen?style=flat-square)](https://www.python.org/)

Hello everyone! This is the repository of my bot in Telegram **"keepTelegram"**.

## Table of contents

- [Table of contents](#table-of-contents)
- [Motivation](#motivation)
- [Build status](#build-status)
- [Badges](#badges)
- [Code style](#code-style)
- [Screenshots](#screenshots)
- [Tech/framework used](#techframework-used)
- [Features](#features)
- [Installation](#installation)
- [Fast usage](#fast-usage)
- [Tests](#tests)
- [Contribute](#contribute)
- [Credits](#credits)
- [License](#license)

## Motivation

In fact, I don't remember why I wanted to do this project. But the idea of a [Google Keep](https://keep.google.com/) clone in the Telegram is interesting, so I started working. Unfortunately, bots do not currently have the ability to send pending messages, so it is not possible to make reminders (at least on free hosting).

## Build status

Here you can see build status of [continuous integration](https://en.wikipedia.org/wiki/Continuous_integration)/[continuous deployment](https://en.wikipedia.org/wiki/Continuous_deployment):

![Test Code](https://github.com/mezgoodle/keepTelegram/workflows/Test%20Code/badge.svg)

## Badges

Other badges

[![Theme](https://img.shields.io/badge/Theme-Bot-brightgreen?style=flat-square)](https://uk.wikipedia.org/wiki/%D0%A0%D0%BE%D0%B1%D0%BE%D1%82_(%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%B0))
[![Platform](https://img.shields.io/badge/Platform-Telegram-brightgreen?style=flat-square)](https://telegram.org/)

## Code style

I'm using [Codacy](https://www.codacy.com/) to automate my code quality.

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/9ad5c7e70f0d4484bffaf07965543539)](https://www.codacy.com/gh/mezgoodle/keepTelegram/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mezgoodle/keepTelegram&amp;utm_campaign=Badge_Grade)

## Screenshots

- Start of the work

![Screenshot 1](https://raw.githubusercontent.com/mezgoodle/images/master/keepTelegram1.png)

- Get all notes

![Screenshot 2](https://raw.githubusercontent.com/mezgoodle/images/master/keepTelegram2.png)

- Templates

![Screenshot 3](https://raw.githubusercontent.com/mezgoodle/images/master/keepTelegram3.png)

- Show the statistic

![Screenshot 4](https://raw.githubusercontent.com/mezgoodle/images/master/keepTelegram4.png)


## Tech/framework used

**Built with**

- [Python](https://electron.atom.io)
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [unittest](https://docs.python.org/3/library/unittest.html)

## Features

With my bot you can **make** notes and **get** statistic of all time.

## Installation

1. Clone this repository

```bash
git clone https://github.com/mezgoodle/keepTelegram.git
```

2. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages.

```bash
pip install -r requirements.txt
```

3. Rename `.env_sample` to `.env` and fill the variables like:

```bash
TELEGRAM_TOKEN = <YOUR_TELEGRAM_TOKEN>
DB_PATH=<YOUR_PATH_TO_DB>
```

4. Type in terminal:

```bash
python main.py
```

## Fast usage

Just open the [bot](t.me/tgkeepBot) in _Telegram_ and start your work with it.

## Tests

I tried _Python unittest_ for the first time instead of [_pytest_](https://docs.pytest.org/en/stable/) and I like it. I give you the [link](https://github.com/mezgoodle/keepTelegram/actions?query=workflow%3A%22Test+Code%22) to [GitHub Actions](https://github.com/features/actions), where you can see all my tests.

## Contribute

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Also look at the [CONTRIBUTING.md](https://github.com/mezgoodle/keepTelegram/blob/master/CONTRIBUTING.md).

## Credits

Links to any resources which inspired you to build this project:

- [Example with sqlite3](https://python-scripts.com/sqlite)

## License

MIT © [mezgoodle](https://github.com/mezgoodle)
