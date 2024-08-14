#
#
#
import pandas as pd
import plotly.express as px
import pytz

def Peking2BkkTZ( datetime_str ):
    peking_tz = pytz.timezone('Asia/Shanghai')
    bangkok_tz = pytz.timezone('Asia/Bangkok')
    peking_time = peking_tz.localize(datetime_str)
    bangkok_time = peking_time.astimezone(bangkok_tz)
    return pd.to_datetime( bangkok_time.strftime('%Y-%m-%d %H:%M:%S') )

vdm_log = "VDM data by Wang/VDM data by Wang/TH0813_1Sec.txt"
HDR = ['yyyymmdd','hhmmss',  'T01X_mm', 'T01Y_mm', 'T02X_mm', 'T02Y_mm', 
                             'T03X_mm', 'T03Y_mm', 'T04X_mm', 'T04Y_mm' ]
df = pd.read_csv( vdm_log, skiprows=1,  header=None,names=HDR, sep=r'\s+')

df['dt'] = pd.to_datetime( df['yyyymmdd'] + ' ' + df['hhmmss']  )
#def MakeBangkokTZ(row):
#    return Peking2BkkTZ( row["dt"] )
df['BKK_TZ'] = df['dt'].apply( lambda x : Peking2BkkTZ(x)  )
df_ = df[~df.isin([999.0000]).any(axis=1)]
for tg in ['T01','T02','T03', 'T04']:
    print(  df_[[ f'{tg}X_mm', f'{tg}Y_mm' ]].describe() )
#import pdb; pdb.set_trace()
#############################################################################
fig = px.line(df_, x='dt', y=['T01X_mm', 'T01Y_mm', 'T02X_mm', 'T02Y_mm', 
                             'T03X_mm', 'T03Y_mm', 'T04X_mm', 'T04Y_mm'],
              labels={'value': 'Measurement (mm)', 'dt': 'Time'},
              title='Interactive Time Series Plot')
fig.show()
