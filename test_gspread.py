import pprint
from sheets.spreadsheet import get_client

pp = pprint.PrettyPrinter()

scopes = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

client = get_client(scopes)

worksheet = client.open('Results - TG').sheet1
values = worksheet.get_all_values()
# print(values)
pp.pprint(values)

worksheet.update_acell('B1', 'Bingo!')

cell_list = worksheet.range('A1:A7')
cell_values = [1,2,3,4,5,6,7]

for i, val in enumerate(cell_values):  #gives us a tuple of an index and value
    cell_list[i].value = val    #use the index on cell_list and the val from cell_values

worksheet.update_cells(cell_list)
