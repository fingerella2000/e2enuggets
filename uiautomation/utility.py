import sys
import os
sys.path.append(os.getcwd())
from selenium import webdriver         
from PIL import Image, ImageChops, ImageDraw
import requests
import time
import lxml.html as LH
import pandas as pd
import random
import os, errno


class FileUtil():

    """read as list"""  
    def readFromFile(self, file_path):
        with open(file_path, 'r') as f:
            _lists = f.read().splitlines()
        f.closed
        return _lists

    """write list to file"""
    def writeToFile(self, input, dir_path, file_path):
        try:
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        try:
            with open(file_path, 'w') as f:
                for line in input:
                    f.write(line)
                    f.write("\n")
            f.closed
        except:
            raise("failed to write file")
        return True

class ImageComparer(object):

    def _grayOut(self, size, color):
        img = Image.new('L',size)
        dr = ImageDraw.Draw(img)
        dr.rectangle((0,0) + size, color)
        return img

    def compareImages(self, path_one, path_two, path_diff, opacity=0.85):         
        """ Compares to images and saves a diff image, if there is a difference   
        @param: path_one: The path to the first image 
        @param: path_two: The path to the second image 
        @param: diff: The path to the different image """ 
        a = Image.open(path_one)
        b = Image.open(path_two)
        diff = ImageChops.difference(a, b)
        if diff.getbbox() is None: 
            return True
        else:
            diff = diff.convert('L')
            # Hack: there is no threshold in PILL,
            # so we add the difference with itself to do
            # a poor man's thresholding of the mask: 
            #(the values for equal pixels-  0 - don't add up)
            thresholded_diff = diff
            for repeat in range(3):
                thresholded_diff  = ImageChops.add(thresholded_diff, thresholded_diff)
            size = diff.size
            mask = self._grayOut(size, int(255 * (opacity)))
            shade = self._grayOut(size, 0)
            new_diff = a.copy()
            new_diff.paste(shade, mask=mask)
            # To have the original image show partially
            # on the final result, simply put "diff" instead of thresholded_diff bellow
            new_diff.paste(b, mask=thresholded_diff)            
            new_diff.save(path_diff)
            return False

class TableCreator(object):
    
    def __init__(self, columns, cells):        
        self.columns = columns
        self.cells = cells
        self.row_title = []
        self.table = [[]]
        self.table.clear()

        x_value = ""
        y_value = ""
        table_title_index = 0
        columns = []
        for container in self.cells:
            x_new_value = container.location['x']
            y_new_value = container.location['y']
            cell_text = container.text

            """the first few loops will initialize the table title since this report has a certain number columns."""
            if table_title_index < self.columns:
                self.row_title.append(cell_text)
                table_title_index = table_title_index + 1
                continue

            table_title_index = table_title_index + 1
            """get the first cell of the table"""
            if x_new_value != x_value and y_new_value != y_value and table_title_index == self.columns + 1:
                columns.append(cell_text)            
                """the report table content is loaded column by column except the table title."""
                """continue looping the current column"""
            elif x_new_value == x_value and y_new_value != y_value:
                columns.append(cell_text)
            else:
                self.table.append(columns)
                columns = []
                columns.append(cell_text)         

            # save the old value
            x_value = x_new_value
            y_value = y_new_value   

        self.table.append(columns)

    def getHeader(self):
        return self.row_title

    def getContent(self):
        return list(zip(*self.table))

class TableWithFooterCreator(object):
    
    def __init__(self, columns, cells):        
        self.columns = columns
        self.cells = cells
        self.header = []
        self.footer = []
        self.table = [[]]
        self.table.clear()

        x_value = ""
        y_value = ""
        table_title_index = 0
        columns = []
        for container in self.cells:
            x_new_value = container.location['x']
            y_new_value = container.location['y']
            cell_text = container.text

            """the first few loops will initialize the table header since this report has a certain number columns."""
            if table_title_index < self.columns:
                self.header.append(cell_text)
                table_title_index = table_title_index + 1
                continue
            
            """the next few loops will initialize the table footer.""" 
            if table_title_index < self.columns * 2:
                self.footer.append(cell_text)
                table_title_index = table_title_index + 1
                continue

            table_title_index = table_title_index + 1
            """get the first cell of the table"""
            if x_new_value != x_value and y_new_value != y_value and table_title_index == self.columns * 2 + 1:
                columns.append(cell_text)            
                """the report table content is loaded column by column except the table title."""
                """continue looping the current column"""
            elif x_new_value == x_value and y_new_value != y_value:
                columns.append(cell_text)
            else:
                self.table.append(columns)
                columns = []
                columns.append(cell_text)         

            # save the old value
            x_value = x_new_value
            y_value = y_new_value   

        self.table.append(columns)

    def getHeader(self):
        return self.header

    def getFooter(self):
        return self.footer

    def getContent(self):
        return list(zip(*self.table))

class TableWithGroupedHeaderCreator(object):
    
    def __init__(self, columns, grouped_header_dic, cells):        
        self.columns = columns
        self.grouped_header_dic = grouped_header_dic

        self.cells = cells
        self.row_title = [[]]
        self.row_title.clear()
        self.table = [[]]
        self.table.clear()

        x_value = ""
        y_value = ""
        table_title_index = 0
        columns = []
        for container in self.cells:
            x_new_value = container.location['x']
            y_new_value = container.location['y']
            cell_text = container.text
            is_grouped_header_set = 0
            """the first few loops will initialize the table title since this report has a certain number columns."""
            if table_title_index < self.columns + len(self.grouped_header_dic.keys()):    
                headers = []   
                headers.append(cell_text)                  
                # loop the group header dictionary
                for key, value in self.grouped_header_dic.items():
                    if table_title_index in value:
                        self.row_title[key].append(cell_text)
                        is_grouped_header_set = 1
                        break
                if is_grouped_header_set == 0:
                    self.row_title.append(headers)

                table_title_index = table_title_index + 1
                continue

            """then start loop the data table content"""
            table_title_index = table_title_index + 1
            """get the first cell of the table"""
            if x_new_value != x_value and y_new_value != y_value and table_title_index == self.columns + len(self.grouped_header_dic.keys()) + 1:
                columns.append(cell_text)            
                """the report table content is loaded column by column except the table title."""
                """continue looping the current column"""
            elif x_new_value == x_value and y_new_value != y_value:
                columns.append(cell_text)
            else:
                self.table.append(columns)
                columns = []
                columns.append(cell_text)         

            # save the old value
            x_value = x_new_value
            y_value = y_new_value   

        self.table.append(columns)

    def getHeader(self):
        return self.row_title

    def getContent(self):
        return list(zip(*self.table))

class UserAgentUtil(object):
    file_util = FileUtil()
    def getRandomUA(self, file_path):
        _uer_agents = self.file_util.readFromFile(file_path)
        return random.choice(_uer_agents)

    def collectAndSave(self, dir_path, file_path):
        _result = self.collect()
        self.file_util.writeToFile(_result, dir_path, file_path)


    """collect a number of pages of chrome user agent string from https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/"""
    def collect(self):
        _user_agent_list = []
        url = 'https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/'
        for page in range(5):
            response = requests.get(url + str(page+1))
            html = response.content
            dfs = pd.read_html(html)
            _user_agent_list.extend(dfs[0]['User agent'].values.tolist()) 
            time.sleep(10)
            # for df in pd.read_html(html):
            #     _user_agent_list.append(df['User agent'].values.tolist())             
        return _user_agent_list

class ProxyUtil(object):
    file_util = FileUtil()

    def getRandomProxy(self, file_path):
        _proxies = self.file_util.readFromFile(file_path)
        return random.choice(_proxies)

    def collectAndSave(self, dir_path, file_path):
        _result = self.collect()
        self.file_util.writeToFile(_result, dir_path, file_path)


    """collect a number of proxies from view-source:https://free-proxy-list.net/#list"""
    def collect(self):
        _proxy_list = []        
        with open("resources/proxies.html", 'r') as f:
            _file_data = f.read()
            dfs = pd.read_html(_file_data)
            _ip_addresses = dfs[0]['IP Address'].dropna().values.tolist()
            _ports = dfs[0]['Port'].dropna().values.tolist()
            # _anonymity = dfs[0]['Anonymity'].dropna().values.tolist()
            for (i,p) in zip(_ip_addresses, _ports):
                _proxy_list.append(str(i) + ":" +str(p))
        f.closed          
        return _proxy_list

    
# if __name__ == '__main__':
    # uau = UserAgentUtil()
    # uau.collectAndSave("resources/", "resources/useragents.txt")
    # print(uau.getRandomUA("resources/useragents.txt"))
    # proxy = ProxyUtil()
    # proxy.collectAndSave("resources/", "resources/proxies.txt")
    # print(proxy.getRandomProxy("resources/proxies.txt"))