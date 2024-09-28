import re
from pdfminer.high_level import extract_pages, extract_text
import pandas as pd

pd.set_option('display.width', None)

pdf_path = 'data/invoices/f-vat_2011.pdf'
result_path = 'data/results/faktura_baza_danych.xlsx'

text = extract_text(pdf_path)
# print(text)

invoice_number = re.search(r'Faktura VAT nr ([\w\s\d]+)', text).group(1).strip()
issue_date = re.search(r'Data wystawienia:\s*(\d{4}-\d{2}-\d{2})', text).group(1).strip()
sale_date = re.search(r'Data sprzedaży:\s*(\d{4}-\d{2}-\d{2})', text).group(1).strip()

# print(invoice_number)
# print(issue_date)
# print(sale_date)


import tabula

tables = tabula.read_pdf(pdf_path, pages="all")
#print(tables)
df = tables[0]
df = df[df.lp >= 1].copy()
# print(df)

df['Numer faktury'] = invoice_number
df['Data wystawienia'] = issue_date
df['Data sprzedaży'] = sale_date

df.to_excel(result_path, index=False, engine='openpyxl')

with pd.ExcelWriter('data/results/all.xlsx', engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
    df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row, sheet_name='Sheet1')

print("Dane z faktury zapisano do pliku ", result_path)
print(df)