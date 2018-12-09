from bs4 import BeautifulSoup as bs
import os
import time
from pprint import pprint
def combineList(personDict,log=False):
    myList = []
    counter = 1
    for key in personDict:
        #print personDict[key][0]
        for i in personDict[key][1]:
            if i not in myList:
                if log:
                    print "Favori Adayim {:<2} {:.>20}".format(counter,i)
                    counter+=1
                myList.append(i)
    return myList

def noneFollowers(followers,combine_list,log=False):
    none_follewer = []
    for i in followers:
        if i not in combine_list:
            none_follewer.append(i)

    if log:
        print "Size,", len(none_follewer)
        print none_follewer
    return none_follewer

def getPhotoLinks(source,log=False):
    photo_row = source.find_all('div', {"class": "Nnq7C weEfm"})
    links = []
    for i in photo_row:
        photo_column = i.find_all('div', {"class": "v1Nh3"})
        for j in photo_column:
            url = j.find('a')
            links.append(str(url).split('">')[0].split('"')[1])
            if log:
                print str(url).split('">')[0].split('"')[1]
    return links

def getPersons(source,log=False):
    names = source.find_all('a', {'class': 'FPmhX'})
    if log:
        print "Names LEN :", len(names)
        print "Source TITLE :", source.title
    _name = []
    for i in names:
        name = str(i).split('" href="/')[1].split('/" title="')[0]
        _name.append(name)
        #print "NAME :", name
    return (source.title.text, _name)

def getMyFollows():
    with open('myFollows.html', 'r') as f:
        content = f.read().decode('utf8')
    #print content
    source = bs(content, 'html5lib')
    myFollows = []
    follows =source.find_all('a', {'class': '_2dbep'})
    for i in follows:
        myFollows.append(str(i).split('" href="/')[1].split('/" style="')[0])

    return myFollows
def create_NamesJSON4CombineList(index=None):
    content = None
    path = os.curdir + '/photos/'
    dir = os.listdir(path)
    names_json = {}
    file_names = []
    counter = 0
    for file in dir:
        if counter == index and index:
            break

        filename = path + file
        file_names.append(file)
        counter += 1
        with open(filename, 'r') as f:
            content = f.read().decode('utf8')

        source = bs(content, 'html5lib')

        names_json[file] = getPersons(source)
    return names_json,file_names
#Her linke ait source cekilerek verildi



def getMyListandNoneFollowers():
    index = None
    myFollows = getMyFollows()
    names_json,fileNames = create_NamesJSON4CombineList(index)
    myList = combineList(names_json)
    none_followers = noneFollowers(myFollows, myList)

    counter = 0
    print "MyList"
    for i in myList:
        print "{:<20} -> {:<3}:{:.<20}".format("Follower",counter, i)
        counter += 1

    counter = 0
    print('It seems people which below dont like you,')
    for i in none_followers:
        print "{:<20} -> {:<3}:{:.<20}".format("Person",counter, i)
        counter += 1






