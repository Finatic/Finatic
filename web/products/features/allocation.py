import pandas as pd
import numpy as np
import json

class Allocation:

    def __init__(self, data_path:str, df_inp, tickers) -> None:
        super().__init__()
        self.data_path = data_path
        self.net_now_value = np.sum(df_inp['now_value'])
        self.df_listed = pd.read_csv('products/static_product/fundamentals.csv', index_col='Ticker')
        self.df_listed.index = self.df_listed.index.astype(str) + '.NS'
        self.df_inp = df_inp.join(self.df_listed[self.df_listed.index.isin(tickers)])

    def company_wise_allocation(self):
        group_company = self.df_inp.groupby(['Ticker']).agg('sum')['now_value']
        company_pie_values = group_company.to_list()
        company_pie_names = group_company.index.tolist()
        return json.dumps({'1': company_pie_values, '2': company_pie_names})
    
    def cap_wise_allocation(self):
        group_cap = self.df_inp.groupby(['Cap']).agg('sum')['now_value']
        cap_pie_values = group_cap.to_list()
        cap_pie_names = group_cap.index.tolist()
        return json.dumps({'1': cap_pie_values, '2': cap_pie_names})
    
    def sector_wise_allocation(self):
        group_sector = self.df_inp.groupby(['Sector']).agg('sum')['now_value']
        sector_pie_values = group_sector.tolist()
        sector_pie_names = group_sector.index.tolist()
        return json.dumps({'1': sector_pie_values, '2': sector_pie_names})
    
    def industry_wise_allocation(self):
        group_industry = self.df_inp.groupby(['Industry']).agg('sum')['now_value']
        industry_pie_values = group_industry.tolist()
        industry_pie_names = group_industry.index.tolist()
        return json.dumps({'1': industry_pie_values, '2': industry_pie_names})
    
    def asset_fundamentals(self):
        weighted_pe = np.sum(self.df_inp["Price to Earnings Ratio (TTM)"] * self.df_inp['now_value'] / self.net_now_value)
        weighted_beta = np.sum(self.df_inp["1-Year Beta"] * self.df_inp['now_value'] / self.net_now_value)
        list_pe = self.df_inp[['Cap', 'Industry', '1-Year Beta', 'Price to Earnings Ratio (TTM)', 'Basic EPS (TTM)']].copy()
        list_pe.index = list_pe.index.str.replace('.NS', "")
        pelist = list_pe.reset_index().to_numpy().tolist()
        return weighted_pe, weighted_beta, {'1': pelist}