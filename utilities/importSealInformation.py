"""
Created on Sun Dec  9 05:59:49 2018

@author: tyrda
"""

import bs4, openpyxl, requests, sys
from tkinter import Tk


class Seal:
    """A seal object from fluidol.com
    
        Attributes:
                href = reference to the html file location
    """
    def __init__(self, href=""):
        self.href = href
        self.error, self.htmlInformation = self.openFluidolSealHtmlPage()
        
        if self.error == 0:
            self.name = self.htmlInformation[1].strong.extract().get_text()
            self.description =self.htmlInformation[1].get_text().strip('\n')  
            self.List1_Name = ""          
            self.List1 = self.get_List1()
            self.List2_Name = ""
            self.List2 = self.get_List2()
        
    def openFluidolSealHtmlPage(self):
        """Opens an html file and searches for seal information
            first looks for href location from class
            then from a command line location
            finally from clipboard
            
            returns:
                errorcode, htmlInformation
        """
        if len(self.href) > 0:
            address = self.href
        elif len(sys.argv) > 1:
            address = ' '.join(sys.argv[1:])
        else:
            address = Tk().clipboard_get()
        
        sealPage = requests.get(address)
        sealPage.encoding = 'utf-8'
        if sealPage.status_code != 200:
            print('Could not find web page')
            return 1 , "Could not find web page"
        else:
            fbs = bs4.BeautifulSoup(sealPage.text,"html.parser")
#            fbs = bs4.BeautifulSoup(sealPage.text,"lxml")
            results = fbs.find_all(class_='mainText')
#            print(results[0])
            return 0, results
    
    def getAttributesList(self, bs4ElementTag):
        """ Converts fluidol Features/benefits list into a list item
        """
        featureList = bs4ElementTag.get_text().split('\n')
        returnList = []
        for item in featureList:
            if len(item) > 0:
                returnList.append(item)
        return returnList
    def get_List1(self):
        """ Feature List should exist as the 3rd element
            self.htmlInformation[3]
        """
        if len(self.htmlInformation) >= 4:
            self.List1_Name = self.htmlInformation[2].get_text().strip('\n')
            return ",".join(self.getAttributesList(self.htmlInformation[3]))
        else:
            self.List1_Name = "None"
            return "None"
    def get_List2(self):
        """ Benefits List should exist as the 5th element
            self.htmlInformation[5]
        """
        if len(self.htmlInformation) == 6:
            self.List2_Name =  self.htmlInformation[4].get_text().strip('\n')
            return ",".join(self.getAttributesList(self.htmlInformation[5]))
        else:
            self.List2_Name = "None"
            return "None"
        
if __name__ == "__main__":
    a = Seal("https://www.fluidol.com/cartridgeMechanical/style42.html")
    b = Seal("https://www.fluidol.com/cartridgeMechanical/style44.html")
    try:
        workbook = openpyxl.load_workbook('example.xlsx')
    except:
        workbook = openpyxl.Workbook()
    sheet = workbook['Sheet']
    sheet.append([a.name,a.description,a.List1_Name,a.List1,a.List2_Name,a.List2])
    sheet.append([b.name,b.description,b.List1_Name,b.List1,b.List2_Name,b.List2])
    workbook.save('example.xlsx')
    
