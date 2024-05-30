import os
from typing import List

# LangChain Document loaders v.2
from langchain_community.document_loaders  import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders  import Docx2txtLoader
from langchain_community.document_loaders  import DirectoryLoader
from langchain_community.document_loaders  import WikipediaLoader
from langchain_community.document_loaders  import YoutubeLoader
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_loaders import WebBaseLoader



import requests
from bs4 import BeautifulSoup
 

'''
# LangChain Document loaders v.1
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import WikipediaLoader
from langchain.document_loaders import YoutubeLoader
'''

# Load Entire Dir
def loadDir(path, filetype='*')->List:    
    loader = DirectoryLoader(path, glob="**/*." + filetype, show_progress=True)
    docs = loader.load()
    return docs


# Load Single Files
def loadFile(file) -> List:
    if file.endswith(".pdf"):
        loader = PyPDFLoader(file)
    elif file.endswith('.docx') or file.endswith('.doc'):
        loader = Docx2txtLoader(file)
    elif file.endswith('.txt'):
        loader = TextLoader(file)
    docs = loader.load()
    return docs


# Load Wiki
def loadWiki(query, lang, n) -> List:
    loader = WikipediaLoader(query=query, lang=lang, load_max_docs=n)
    docs = loader.load()
    return docs


# Load Youtube
def loadYoutube(url, lang) -> List:
    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True, language = lang, translation = lang)
    docs = loader.load()
    return docs


# Read API
def readAPI(url, params, headers, filename):  
    import json
    import requests
    list = []
    response = requests.get(url, params=params, headers=headers).json()
    list.append(response)
    
    # save in json file        
    with open(filename, 'w') as f:
        json.dump(list,f, indent=4)

def readWebsite(urls):
    loader = AsyncHtmlLoader(urls)
    docs = loader.load()
    return docs


def readWebsite2(urls):
    loader = WebBaseLoader(urls)
    docs = loader.load()
    return docs


def loadBookURLs(urls):
    Links = []
    for url in urls:
        reqs = requests.get(url)
        #Only finds links between the list of deaths (gets the main content)
        soup = BeautifulSoup(reqs.text.split("List of deaths")[1], 'html.parser')
        urls = soup.find_all("a")
        for link in urls:
            if "#" not in link.get('href') and "http" not in link.get('href') and "File" not in link.get('href'):
                if link.get('href') not in Links:
                    Links.append(link.get('href'))
    return Links

def loadURL(url):
    Links = []
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    content = soup.find(class_="mw-body-content")
    if content is not None:
        urls = content.find_all("a")
        if urls is not None:
            for link in urls:
                if link.get('href') is not None:
                    if "#" not in link.get('href') and "http" not in link.get('href') and "File" not in link.get('href'):
                        if link.get('href') not in Links:
                            Links.append(link.get('href'))
    return Links