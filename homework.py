import datetime as dt

class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.today = dt.datetime.today()
        self.week_ago = self.today - dt.timedelta(7)

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        day_stats = []
        for record in self.records:
            if record.date == self.today:
                day_stats.append(record.amount)
        return sum(day_stats)

    def get_week_stats(self):
        week_stats = []
        for record in self.records:
            if self.week_ago <= record.date <= self.today:
                week_stats.append(record.amount)
        return sum(week_stats)

    def today_limit_balance(self):
        limit_today = self.limit - self.get_today_stats()
        return limit_today


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        calories_remained = self.today_limit_balance()
        if calories_remained > 0:
            message = (f'Сегодня можно съесть что-нибудь ещё, но с общей'
                       f'калорийностью не более {calories_remained} кКал')
        else:
            message = 'Хватит есть!'
        return message


class CashCalculator(Calculator):
    EURO_RATE = 79.11
    USD_RATE = 73.75
    RUB_RATE = 1

    def __init__(self, limit):
        super().__init__(limit)

    def get_today_cash_remained(self, currency='rub'):
        currencies = {'usd': ('USD', CashCalculator.USD_RATE),
                      'eur': ('Euro', CashCalculator.EURO_RATE),
                      'rub': ('руб', CashCalculator.RUB_RATE)}
        cash_remained = self.today_limit_balance()
        currency_name = currencies[currency][0]
        currency_rate = currencies[currency][1]
        cash_remained = round(cash_remained / currency_rate, 2)
        debt = abs(self.limit - cash_remained)
        if cash_remained > 0:
            return f'На сегодня осталось {cash_remained} {currency_name}'
        elif cash_remained == 0:
            return 'Денег нет, держись'
        else:
            return f'Денег нет, держись. Твой долг: {debt} {currency_name}'

class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y')


if __name__ == '__main__':
    cash_calculator = CashCalculator(1000)
    cash_calculator.add_record(Record(amount=178, comment="кофе"))
    cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
    cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))
    print(cash_calculator.get_today_cash_remained("rub"))
