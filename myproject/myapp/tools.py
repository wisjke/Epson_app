import csv
import chardet
import pandas as pd
import re

class ExcelToCsvConverter:
    def __init__(self, excel_file):
        self.excel_file = "Merch.csv"
        self.excel_file_path = excel_file

    def convert(self):
        df = pd.read_excel(self.excel_file_path)
        df.to_csv(self.excel_file, index=False)
        return self.excel_file

class SalersReader:
    def __init__(self, sale_filename):
        self.sale_filename = sale_filename

    def read(self):
        encoding = self.detect_encoding(self.sale_filename)
        with open(self.sale_filename, 'r', encoding=encoding) as file:
            reader = csv.DictReader(file, delimiter=';')
            salers = {}
            for line in reader:
                contact = line["ContactID"]
                task = line["taskDescription"]
                task_number = self.extract_task_number(task)
                if task_number:
                    task = f"Завдання {task_number}"
                    if contact not in salers:
                        salers[contact] = [task]
                    else:
                        salers[contact].append(task)
        return salers

    def extract_task_number(self, task_description):
        match = re.search(r'Завдання (\d+)', task_description)
        if match:
            return match.group(1)
        return None

    def detect_encoding(self, filename):
        with open(filename, 'rb') as file:
            raw_data = file.read(10000)
        result = chardet.detect(raw_data)
        return result['encoding']

class MerchReader:
    def __init__(self, merch_filename):
        converter = ExcelToCsvConverter(merch_filename)
        merch_filename = converter.convert()
        self.merch_filename = merch_filename

    def read(self):
        encoding = self.detect_encoding(self.merch_filename)
        with open(self.merch_filename, 'r', encoding=encoding) as file:
            reader = csv.DictReader(file, delimiter=',')
            merchs = {}
            for line in reader:
                err = line["ERR"]
                tel = line["tel"]
                city = line["city"]
                if err not in merchs:
                    merchs[err] = {'phones': [tel], 'city': city}
                else:
                    merchs[err]['phones'].append(tel)
        return merchs

    def detect_encoding(self, filename):
        with open(filename, 'rb') as file:
            raw_data = file.read(10000)
        result = chardet.detect(raw_data)
        return result['encoding']
