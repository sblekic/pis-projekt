import pdfkit


import json
import requests

path_wkhtmltopdf = r'C:\App\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# pdfkit.from_url("http://127.0.0.1:5000/narudzbenice",
#                 "out.pdf", configuration=config)


pdfkit.from_url('http://127.0.0.1:5000/namirnice',
                'test.pdf', configuration=config)
