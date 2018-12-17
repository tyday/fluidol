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
        self.error, self.htmlInformation, self.imgInformation = self.openFluidolSealHtmlPage()
        
        if self.error == 0:
            self.name = self.htmlInformation[1].strong.extract().get_text()
            self.description =self.htmlInformation[1].get_text().strip('\n')  
            self.List1_Name = ""          
            self.List1 = self.get_List1()
            self.List2_Name = ""
            self.List2 = self.get_List2()
        else:
            self.name = 'error'
            self.description = 'error' 
            self.List1_Name = "error"          
            self.List1 = 'error'
            self.List2_Name = "error"
            self.List2 = 'error'
        
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
            imgResults = fbs.find_all(class_='product3')
            imgResults += fbs.find_all(class_='productImage')
#            docResults = fbs.find
            return 0, results, imgResults
    
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
    def get_unorganized_list(self):
        if len(self.htmlInformation)>1:
            information=[]
            for item in self.htmlInformation:
                try:
                    information.append(item.get_text().strip('\n'))
                except:
                    information.append('error')
            return information
    def get_image_list(self):
        root_url = "https://www.fluidol.com"
        return_list = []
        return_list_front = []
        if len(self.imgInformation)>1:
            for image in self.imgInformation:
                if 'productImage' in image['class']:
                    image_alt = image['alt']
                    image_src = root_url + image['src'].lstrip('.')
#                    return_list_front.append(image_alt + ',' + image_src)
                    return_list_front.append(image_alt)
                    return_list_front.append(image_src)
                else:
                    image_alt = image['alt']
                    image_src = root_url + image['src'].lstrip('.')
#                    return_list.append(image_alt + ',' + image_src)
                    return_list.append(image_alt)
                    return_list.append(image_src)
            return return_list_front + return_list
        else:
            return ['no images']
    def get_document_list(self):
        root_url = "https://www.fluidol.com"
        return_list = []
        
def create_Seal_List(initial_list):
    """ The seals are divided into category.
        But each category has a link list to its sibling seals
        This creates a complete list from the link list
        """
    root_url = "https://www.fluidol.com"
    return_list = []
    for link in initial_list:
        res = Seal(link)
        sibling_seals = res.htmlInformation[0]
        sibling_seals_list = sibling_seals.findAll('a')
        """ The first link is to the category... so we skip it """
        for i in range(1,len(sibling_seals_list)):
            tag = sibling_seals_list[i]
            tag = tag['href']
            tag = tag.lstrip('..')
            tag = root_url + tag
            return_list.append(tag)
#    print(sibling_seals)
#    print(sibling_seals_list)
#    print(return_list)
    return return_list
def add_seals_to_xlsx(seal_list):
    try:
        workbook = openpyxl.load_workbook('seal_information.xlsx')
    except:
        workbook = openpyxl.Workbook()
    sheet = workbook['Organized']
    for seal in seal_list:
        try:
            seal_info = Seal(seal)
            sheet.append([seal_info.name, seal_info.description,
                          seal_info.List1_Name, seal_info.List1, 
                          seal_info.List2_Name,seal_info.List2])
        except:
            sheet.append(['error'])
    
    workbook.save('seal_information.xlsx')
def add_unorganized_seal_info_to_xlsx(seal_list):
    try:
        workbook = openpyxl.load_workbook('seal_information.xlsx')
    except:
        workbook = openpyxl.Workbook()
    sheet = workbook['Unorganized']
    for seal in seal_list:
        try:
            seal_info = Seal(seal)
            sheet.append(seal_info.get_unorganized_list())
        except:
            sheet.append(['error'])
    
    workbook.save('seal_information.xlsx')
def add_images_to_xlsx(seal_list):
    try:
        workbook = openpyxl.load_workbook('seal_information.xlsx')
    except:
        workbook = openpyxl.Workbook()
    try:
        sheet = workbook['Images']
    except:
        sheet = workbook.create_sheet('Images')
    for seal in seal_list:
        try:
            seal_info = Seal(seal)
            sheet.append(seal_info.get_image_list
                         ())
        except:
            sheet.append(['error'])
    
    workbook.save('seal_information.xlsx')
if __name__ == "__main__":
    # Experimental seal
    seal19 = Seal("https://www.fluidol.com/cartridgeMechanical/style19.html")
    seal42 = Seal("https://www.fluidol.com/cartridgeMechanical/style42.html")
    

#         Using initial list. Create list of all seals and then fill spreadsheet with values
    initial_list = [
            "https://www.fluidol.com/cartridgeMechanical/style91.html",
            "https://www.fluidol.com/multiLipCartridge/style42.html",
            "https://www.fluidol.com/multiLipComponent/style45.html",
            "https://www.fluidol.com/componentMechanical/style10.html",
            "https://www.fluidol.com/mixer/style19.html",
            "https://www.fluidol.com/teflonLipSeal/everseal.html",
            "https://www.fluidol.com/bearingProtection/style93.html",
            "https://www.fluidol.com/braidedPacking/wedgee.html",
            "https://www.fluidol.com/lubrication/magnalube1.html",
            "https://www.fluidol.com/radialFaceLipSeal/rotaseal.html",
            ]
    extended_list = create_Seal_List(initial_list)
    extended_list = extended_list + initial_list[:]
    
#    add_seals_to_xlsx(extended_list)
    add_unorganized_seal_info_to_xlsx(extended_list)
#    add_images_to_xlsx(extended_list)