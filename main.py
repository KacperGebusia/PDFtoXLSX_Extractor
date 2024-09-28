import re
from pdfminer.high_level import extract_pages, extract_text
import pandas as pd

text = extract_text('data/invoices/f-vat_2011.pdf')
# print(text)

invoice_number = re.search(r'Faktura VAT nr ([\w\s\d]+)', text).group(1).strip()
issue_date = re.search(r'Data wystawienia:\s*(\d{4}-\d{2}-\d{2})', text).group(1).strip()
sale_date = re.search(r'Data sprzedaży:\s*(\d{4}-\d{2}-\d{2})', text).group(1).strip()

print(invoice_number)
print(issue_date)
print(sale_date)


import tabula

tables = tabula.read_pdf('data/invoices/f-vat_2011.pdf', pages="all")
#print(tables)
df = tables[0]
df = df[df.lp >= 1]
print(df)

df['Numer faktury'] = invoice_number
df['Data wystawienia'] = issue_date
df['Data sprzedaży'] = sale_date

df.to_excel('data/results/faktura_baza_danych.xlsx', index=False, engine='openpyxl')