import sys
import requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

if len(sys.argv) != 2:
    if len(sys.argv) > 0: pname = sys.argv[0]
    else: pname = "mediawiki_downloader.py"
    print('usage: python ' + pname + ' "url"')
    print('example: \'python ' + pname + ' "http://wiki.example.com"\'')
    exit(0)

baseSite = sys.argv[1]

links = []
titles = []

namespacesEnded = False
namespace = 0
while not namespacesEnded:
    print('[namespace: ' + str(namespace) + ']: links searcher started')
    notFirstRun = 0
    while True:
        allPagesLink = baseSite + '/index.php?setlang=en&title=' + quote_plus('Special:AllPages') + '&namespace=' + str(namespace) + '&from='
        if notFirstRun == 1: allPagesLink += quote_plus(titles[-1])
        allPages = requests.get(allPagesLink)
        if bytes('does not have namespace',encoding='utf8') in allPages.content:
            namespacesEnded = True
            break
        table = BeautifulSoup(allPages.content, 'lxml').select_one("table.mw-allpages-table-chunk")
        if not table:
            print('[namespace: ' + str(namespace) + ']: got an error (most likely it\'s just ending of namespace)')
            break
        if len(table.select("a")) <= 1: break
        print('[namespace: ' + str(namespace) + ']: got +' + str(len(table.select("a"))) + ' links')
        anythingNew = False
        for e in table.select("a")[notFirstRun:]:
            if e.attrs['title'] not in titles:
                anythingNew = True
                links.append(e.attrs['href'])
                titles.append(e.attrs['title'])
        if notFirstRun == 0: notFirstRun = 1
        if not anythingNew: break
    print('[namespace: ' + str(namespace) + ']: links searcher finished')
    namespace += 1

f = open('num2name.txt','w')
for i in range(len(titles)):
    f.write(str(i) + ' ' + titles[i])
f.close()

print('Created an array of names in file "num2name.txt".')

print('Download started...')

for i in range(len(titles)):
    page = requests.get(baseSite + '/index.php?title=Special:Export&action=submit&history=1&pages=' + quote_plus(titles[i]))
    f = open(str(i)+'.xml','wb')
    f.write(page.content)
    f.close()
    if i % 10 == 0:
        print('Progress [' + str(i+1) + '/' + str(len(titles)) + ']')

print('Download finished. Thanks for using this tool!')
