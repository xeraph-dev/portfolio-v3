#!/usr/bin/env python

from html import unescape
from os import getcwd, path
import sys
from typing import TypedDict
import yaml
import requests
from bs4 import BeautifulSoup, Tag

url: str = "https://marketplace.visualstudio.com/items?itemName="
exts_url = "https://raw.githubusercontent.com/adrianrl99/dotfiles/main/scripts/vscode-extensions/vscode-extensions.yml"
imports: str = """\
---
import CardList from '~/components/CardList.astro'
import Section from '~/components/Section.astro'
import VSCExtension from '~/components/VSCExtension.astro'
import Layout from '~/layouts/Layout.astro'
---\n
"""


class Ext(TypedDict):
    Theme: list[str]
    General: list[str]
    Markdown: list[str]
    Git: list[str]
    Shell: list[str]
    Web: list[str]
    Python: list[str]
    Rust: list[str]
    Haskell: list[str]


try:
    ext: Ext = yaml.safe_load(requests.get(exts_url).text)

    layout = Tag(name="Layout")
    layout["title"] = "Vscode Extensions | Adrian Lopez Portfolio"

    h1 = Tag(name="h1")
    h1["class"] = "container p-2 text-center text-3xl px-4 py-2"
    h1.append("Visual Studio Code extensions")
    layout.append(h1)

    img = Tag(name="img")
    img["class"] = "container p-2 flex rounded-2xl"
    img["src"] = "https://raw.githubusercontent.com/adrianrl99/dotfiles/main/screenshots/vscode.png"
    img["alt"] = "vscode screenshot"
    layout.append(img)

    for k, v in ext.items():
        section = Tag(name="Section")
        section["id"] = k.lower()
        section["title"] = k
        section["className"] = "py-10"

        list = Tag(name="CardList")
        list["size"] = 5

        for i in v:
            li = Tag(name="li")
            vscext = Tag(name="VSCExtension")

            ext_url: str = f"{url}{i}"
            r = requests.get(ext_url)
            soup = BeautifulSoup(r.content, "html.parser")

            title: str = soup.find("span", {"class": "ux-item-name"}).text
            description: str = soup.find("div", {"class": "ux-item-shortdesc"}).text
            image: str = soup.find("img", {"class": "image-display"}).get(key="src")

            vscext["title"] = title
            vscext["description"] = description
            vscext["image"] = image
            vscext["url"] = ext_url

            li.append(vscext)
            list.append(li)

        section.append(list)
        layout.append(section)

        res = imports + layout.prettify(formatter="html5")
        res = unescape(res)

        with open(
            path.join(getcwd(), "src", "pages", "vscode-extensions.astro"), "w"
        ) as f:
            f.write(res)

except KeyboardInterrupt:
    sys.exit(1)
