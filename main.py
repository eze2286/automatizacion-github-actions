import os
import requests
import pandas as pd
import pygsheets
from datetime import datetime
from pytz import timezone



secrets_dir = os.path.join(os.environ['GITHUB_WORKSPACE'], '.github', 'secrets')
path = os.path.join(secrets_dir, 'PATH_AUTH')
sheet_id = '1Xv8HHezgx6bBiS70_mhAZSolXvDWtII6uAdU1dTDzmo'
gc = pygsheets.authorize(service_account_file = "secreto.json")
gsheet_1 = gc.open_by_key("1Xv8HHezgx6bBiS70_mhAZSolXvDWtII6uAdU1dTDzmo")




url = 'https://api.bluelytics.com.ar/v2/latest'
api_result = requests.get(url)

api_response = api_result.json()
dolar_blue_last_price_sell = (api_response["blue"]["value_sell"])
dolar_blue_last_price_buy = (api_response["blue"]["value_buy"])
time_now = datetime.now(timezone("America/Argentina/Buenos_Aires")).strftime('%Y-%m-%d %H:%M')

output = [dolar_blue_last_price_sell, dolar_blue_last_price_buy, time_now]
df = pd.DataFrame([output], columns = ["Venta", "Compra", "Fecha"])

ws_1 = gsheet_1.worksheet()
sheet_df = ws_1.get_as_df()

if sheet_df.empty:
    ws_1.set_dataframe(df,
                     (1,1))
else:
    df = pd.concat([sheet_df, df], 
                   ignore_index=True)
    ws_1.set_dataframe(df,
                     (1,1))
