# Mediawiki downloader

This python script scans website for pages and downloads them. Notice: it will not download media files like photos, videos and so on.

Download directory: script execution directory.

It indexes all pages and creates a file "num2name.txt" where you can get original page name for each number of xml-document (see below).
After this it downloads all pages in XML format with all history. Names look like "0.xml", "1.xml", ....

Tested on Linux where it works. Should be work on Mac or Windows too.

# Requirements

* Obviously, python

* BeautifulSoup4

```bash
         pip install bs4
```

# Usage

```bash
python mediawiki_downloader.py "url"
```

URL should be like in example below (with 'http://' or 'https://' at beginning).

Example:

```bash
python mediawiki_downloader.py "http://wiki.example.com"
```
