import pandas as pd
import matplotlib.pyplot as plt
import boto3

def download_currency(val="USD"):
    s3 = boto3.client('s3')
    with open(f'b_{val}.csv', 'wb') as f:
        s3.download_fileobj('oliferbucket', f'{val}.csv', f)

download_currency()
download_currency("EUR")

fig, ax = plt.subplots(1, 1)

def set_graf(val="USD", color="black"):
    df = pd.read_csv(f'b_{val}.csv')
    df['exchangedate'] = pd.to_datetime(df['exchangedate'], format='%d.%m.%Y')
    df = df.sort_values(by='exchangedate').set_index('exchangedate')
    df.plot(y='rate', color=f'{color}', ax=ax, label=f'{val}')

set_graf()
set_graf("EUR", "blue")

ax.set_title('UAH exchange rate for 2021 year')
ax.set_xlabel('')
ax.legend()

plt.savefig("graf.png")
s3 = boto3.client('s3')
with open("graf.png", "rb") as f:
    s3.upload_fileobj(f, "oliferbucket", "graf.png")

plt.show()
