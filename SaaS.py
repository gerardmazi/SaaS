###########################################################################################################
#
#                                           SaaS Analytics
#
###########################################################################################################

import FundamentalAnalysis as fa
import pandas as pd

ticker = 'DOCU'
api_key = ''

# Price to Sales
ps = fa.financial_ratios(ticker, api_key, period='quarter').loc['priceToSalesRatio', :].sort_values()
ps.plot()

revenue = pd.DataFrame(
    {
        'revenue': fa.income_statement(ticker, api_key, period="quarter").loc['revenue', :].sort_values()
    }
)
revenue['growth'] = revenue / revenue.shift(4) - 1
revenue.revenue.plot(kind='bar')
revenue.growth.plot()