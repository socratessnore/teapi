from datetime import datetime
from openpyxl import load_workbook


class DataHandler:
    def __init__(self, inputfile):
        self.date = None
        self.kwh = None
        self.temperature = None

        self.inputfile = inputfile

    @staticmethod
    def to_isoformat(date_string):
        date_object = datetime.strptime(date_string, "%d.%m.%Y")
        return date_object.isoformat()

    def read_excel_file(self):
        # Getdata from second sheet that contains more data
        # including daily kWh and average temperature (Celsius)
        sheet_id = 1

        # First four rows are title information
        data_row = 5

        workbook = load_workbook(filename=self.inputfile, data_only=True)

        worksheet = workbook.worksheets[sheet_id]

        row = worksheet[data_row]

        self.date = self.to_isoformat(row[0].value)
        self.kwh = row[1].value
        self.temperature = row[2].value

    def write_results_to_file(self, filename):
        file = open(filename, "w+")
        file.write("{}|{}|{}".format(self.date, self.kwh, self.temperature))
        file.close()
        return filename
