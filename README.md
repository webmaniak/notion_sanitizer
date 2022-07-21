# Notion export sanitizer

## Introduction

Notion is a great tool for taking notes, organizing them and creating all sorts of small databases. It's handy for many uses. However its export mechanism, although generous with both Markdown+CSV and HTML export options, is kind of crappy. When you export your notes, their files are named by the page's name and a long ID which may be useful if you named many things similarly.

However, this is by no mean useful when importing those notes in another app. It's probably more confusing than helping, actually.

This project aims at sanitizing names of pages and the inner links by parsing everything in your export and removing all IDs.

## Requirements

You need Python 3.7+ installed, and you need to have an exported zip file containing Markdown and CSV files ready.

## How to run it

Clone it from this repository:

```shell
git clone https://github.com/webmaniak/notion_sanitizer.git
```

Install the requirements using `pip` and `venv`:

```shell
python -m venv venv
source venv/bin/activate
pip install wheel
pip install -r requirements.txt
```

Then copy and paste your exported zip in the project's root folder and name it `Export.zip`. Run the following command:

```shell
python notion_sanitizer.py
```

Your output should be in `data/`.

## Known limitations

The following limitations currently need your attention:

* The script only works when you put your exported ZIP file in the project's root, and name it `Export.zip`
* The script only works for Markdown+CSV exports
* The script doesn't handle well duplicates; you'll see errors in the console

I may (or may not) fix them later. Feel free to fork or submit pull requests if you feel like it.
