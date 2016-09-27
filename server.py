#!/usr/bin/env python
# encoding: utf-8


from librewiki.app import app
from librewiki import routes


if __name__ == "__main__":
    app.run('localhost', 8080)