from selenium import webdriver         
from PIL import Image, ImageChops, ImageDraw


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