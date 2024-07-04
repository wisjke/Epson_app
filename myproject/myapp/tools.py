import csv
import chardet
import pandas as pd


class ExcelToCsvConverter:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.csv_file = "Merch.csv"

    def convert(self):
        df = pd.read_excel(self.excel_file)
        df.to_csv(self.csv_file, index=False)

        return self.csv_file


class SaleReader:
    def __init__(self, sale_filename):
        self.sale_filename = sale_filename

    def read(self):
        encoding = self.detect_encoding(self.sale_filename)
        with open(self.sale_filename, 'r', encoding=encoding) as file:
            reader = csv.DictReader(file, delimiter=';')
            salers_dk = {}
            for line in reader:
                contact = line["ContactID"]
                task = line["taskDescription"]
                # Витягуємо завдання з taskDescription
                task_number = self.extract_task_number(task)
                if task_number:
                    task = f"Завдання {task_number}"
                    if contact not in salers_dk:
                        salers_dk[contact] = [task]
                    else:
                        salers_dk[contact].append(task)
        return salers_dk

    def extract_task_number(self, task_description):
        import re
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
            dk = {}
            for line in reader:
                err = line["ERR"]
                tel = line["tel"]
                if err in dk:
                    dk[err].append(tel)
                else:
                    dk[err] = [tel]
        return dk

    def detect_encoding(self, filename):
        with open(filename, 'rb') as file:
            raw_data = file.read(10000)
        result = chardet.detect(raw_data)
        return result['encoding']

