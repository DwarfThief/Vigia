# -*- coding: utf-8 -*-
import re
import json
import requests
import datetime
from bs4 import BeautifulSoup

def getIssuesInThePage(response):
    """
    Recebe o response da página.\n
    Retorna uma Lista de String contendo todas as issues da página.
    """
    bs = BeautifulSoup(response.text, "html.parser")
    issueList = bs.find_all("a", {"data-hovercard-type":"issue"})
    return issueList

def getIssuesDate(response):
    """
    Recebe o response da página.\n
    Retorna uma Lista de String contendo todas as datas das issues da página.
    """
    bs = BeautifulSoup(response.text, "html.parser")
    issueDateList = bs.find_all("relative-time")
    return issueDateList

def compareDates(issueDate, todayDate):
    """
    Recebe objeto Date contendo a data da Issue e um objeto todayDate contendo o data da máquina.\n
    Retorna True se a diferença entre as datas forem menores ou iguas a 7 dias, retorna False caso contrário.
    """
    if(issueDate.year - todayDate.year == 0 and issueDate.month - todayDate.month == 0 and issueDate.day - todayDate.day <= 7):
        return True
    return False

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
        issueDateList = getIssuesDate(response)
        validIssue = []

        for i in range(0,len(issueDateList)):
            tempoDaIssueString = issueDateList[i].get_text()
            tempoDaIssueString = datetime.datetime.strptime(tempoDaIssueString, '%b %d, %Y').date()

            if(compareDates(tempoDaIssueString, datetime.date.today()) == False):
                print(issueList[i].getText())
                break
            elif(issuesTagAvaliation(issueList[i], page['tags']) == True):
                validIssue.append(issueList[i].get_text())
        print(validIssue)