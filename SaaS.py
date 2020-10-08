#######################################################################################################################
#
#                                                  SaaS Analytics
#
#######################################################################################################################

import FundamentalAnalysis as fa
import pandas as pd

tickers = [
    'DOCU', 'CRM', 'TWLO'
]
ticker = 'TWLO'
api_key = ''


# Revenue Growth
revenue = pd.DataFrame({'Date':[], 'Comp': [], 'Revenue': [], 'Rev_Growth': [], 'Rev_T4Q': []})
for t in tickers:
    rev_temp = fa.income_statement(t, api_key, period='quarter').loc['revenue', :].sort_values().reset_index()
    temp_df = pd.DataFrame(
        {
            'Date':         pd.to_datetime(rev_temp['index']),
            'Comp':         t,
            'Revenue':      rev_temp['revenue'],
            'Rev_Growth':   rev_temp['revenue'] / rev_temp['revenue'].shift(4) - 1,
            'Rev_T4Q':      rev_temp['revenue'].rolling(4).sum()
        }
    )
    quote = fa.stock_data(t, period="max", interval="1d")['close'].reset_index()
    quote = quote.rename(columns={'index': 'Date', 'close': 'Price'})
    quote['Date'] = pd.to_datetime(quote['Date'])
    temp_df = pd.merge(temp_df, quote, how='left', on='Date')
    revenue = pd.concat([revenue, temp_df])

revenue.groupby(['Date', 'Comp'])['Rev_Growth'].sum().unstack().fillna(method='ffill').plot()
