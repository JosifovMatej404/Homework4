class CompanyData:
    def __init__(self,date,last_trade_price,max_price,min_price,avg_price,percent_change,volume,turnover_best_denars,total_turnover_denars):
        self.date = date
        self.last_trade_price = last_trade_price
        self.max = max_price
        self.min = min_price
        self.avg_price = avg_price
        self.percent_change = percent_change
        self.volume = volume
        self.turnover_best_denars = turnover_best_denars
        self.total_turnover_denars = total_turnover_denars