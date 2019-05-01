# -*- coding: utf-8 -*-
import re
import json
import requests
from bs4 import BeautifulSoup

def getIssuesInThePage(response):
    """
    Recebe o response da página.\n
    Retorna uma Lista de String contendo todas as issues da página.
    """
    bs = BeautifulSoup(response.text, "html.parser")
    issueList = bs.find_all("a", {"data-hovercard-type":"issue"})
    return issueList

def issuesTagAvaliation(issueTextString, tagsList):
    """
    Recebe uma String contendo o texto da Issue e uma Lista de String contendo as categorias.\n
    Retorna True se a Issue possui umas das categorias e False caso contrário.
    """
    issueTextString = issueTextString.get_text().lower()
    issueTextString = issueTextString.replace('[', '')
    issueTextString = issueTextString.replace(']', '')

    for tag in tagsList:
        tag = tag.lower()
        if(re.search(tag, issueTextString) != None): 
            return True
    return False

if __name__ == "__main__":
    jsonPages = json.load(open('urls.json'))

    for page in jsonPages['site']:
        response = requests.get(page['link'])
        issueList = getIssuesInThePage(response)
        validIssue = []

        for issue in issueList:
            tagValidation = issuesTagAvaliation(issue, page['tags'])
            if(tagValidation == True):
                validIssue.append(issue.get_text())