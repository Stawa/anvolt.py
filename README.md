<h1 align="center">
    anvolt.py
</h1>

<h3 align="center">
    Advanced tool with API integration and additional features
</h2>

<p align="center">
    <a href="https://codeclimate.com/github/Stawa/anvolt.py/maintainability"><img src="https://api.codeclimate.com/v1/badges/780b1926cc1affa10cf4/maintainability" /></a>
    <a href="https://stawa.gitbook.io/estraapi-documentation/"><img src ="https://img.shields.io/static/v1?label=python&message=3.10&color=informational"></a>
</p>


### <span class="emoji">✨</span> Features

Explore the vast array of features available in [anvolt.py](https://anvolt.vercel.app/api/) with this comprehensive list:

- **Roleplaying Images**
- **Quizzes / Trivia**
- **Anime Images (SFW / NSFW)**
- **Client-Side Support**
- **Ease-of-Use Codes**

### <span class="emoji">📦</span> Installation

There are two ways to install [anvolt.py](https://anvolt.vercel.app/api/), first you can use the stable release from PyPI:

```bash
$ pip install anvolt.py
```

Second you can use the development version from GitHub to get the latest features and updates:

```bash
$ pip install git+https://github.com/Stawa/anvolt.py/
```
For more information on how to use the package, check out the [documentation](https://anvolt.vercel.app/docs/)

### <span class="emoji"> 🚀 </span> Quickstart

Every function will have its own response class, for example bite function, it return `Responses` class that you can find on `anvolt.models.response`

```py
from anvolt import AnVoltClient

client = AnVoltClient() # client_id and client_secret (optional)

def example():
    bite = client.sfw.bite()
    print(bite.url) # Return str

example()
```

### <span class="emoji">🔗</span> Links

- [Documentation](https://anvolt.vercel.app/api/)
- [Homepage](https://github.com/Stawa/anvolt.py)
- [Application Programming Interface](https://anvolt.vercel.app/api/)
