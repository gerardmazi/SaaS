###########################################################################################################
#
#                                           SaaS Analytics
#
###########################################################################################################

import FundamentalAnalysis as fa
import pandas as pd

tickers = [
    'DOCU', 'CRM'
]
ticker = 'DOCU'
api_key = ''

# Price to Sales
ps = fa.financial_ratios(tickers, api_key, period='quarter').loc['priceToSalesRatio', :].sort_values()
ps.plot()

# Revenue Growth
revenue = pd.DataFrame(
    {
        'revenue': fa.income_statement(ticker, api_key, period="quarter").loc['revenue', :].sort_values().reset_index()['index']
    }
).reset_index()
revenue['growth'] = revenue / revenue.shift(4) - 1
revenue.revenue.plot(kind='bar')
revenue.growth.plot()

revenue = pd.DataFrame({'Date':[], 'Comp': [], 'Revenue': [], 'Rev_Growth': []})
for t in tickers:
    rev_temp = fa.income_statement(t, api_key, period='quarter').loc['revenue', :].sort_values().reset_index()
    temp_df = pd.DataFrame(
        {
            'Date':         rev_temp['index'],
            'Comp':         t,
            'Revenue':      rev_temp['revenue'],
            'Rev_Growth':   rev_temp['revenue'] / rev_temp['revenue'].shift(4) - 1
        }
    )
    revenue = pd.concat([revenue, temp_df])

revenue.groupby(['Date', 'Comp'])['Rev_Growth'].sum().unstack().plot()