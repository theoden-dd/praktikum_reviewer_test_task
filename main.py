import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        # Здесь был бы полезен докстринг.
        # 1. Очень удобно по сигнатуре функции понимать типы данных.
        #    Т.к. здесь не используются аннотации типов, можно указать типы
        #    данных в док-стринге.
        # 2. У параметра `date` сразу 2 неочевидных момента.
        # 2.1. Если параметр не передать, подставится текущая дата.
        # 2.2. Дата ожидается в строго заданном формате.
        # Докстринг - идеальное место, чтобы описать подобные нюансы входов
        # и выходов функции.
        self.amount = amount
        self.date = (
            # Зачем разрывать if not date на 3 разных строки?
            # Эта конструкция хорошо бьется переводом строки перед else и перед
            # if, например.
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        # Здесь бы пригодился докстринг про то, что это за `limit`?
        # Вдруг он на год или неделю. Читая именно эту часть кода - это неясно.
        self.limit = limit
        self.records = []

    def add_record(self, record):
        # Здесь также аннотация типов или докстринг могли прояснить природу
        # аргумента `record`.
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Переменная цикла Record должна начинаться со строчной буквы согласно
        # ПЕП8.
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                # Здесь можно использовать оператор увеличения +=,
                # как это сделано ниже.
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        # Заметь, здесь переменная цикла названа по ПЕП8, в отличие от случая
        # выше.
        for record in self.records:
            if (
                # Так расчет дат производится дважды.
                # Лучше или вынести выражение в переменную,
                # или использовать запись вида 0 <= x < 7.
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Комментарий к этому методу - полпути к докстрингу, отлично!
    # Как мы уже заметили выше, там же можно указать возвращаемый тип данных.
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Однобуквенная переменная.
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Продолжение строки через обратный слэш.
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # Лишний else (guard block!).
        else:
            # Скобки вокруг литерала - лишние.
            # А вот пробел после return - нелишний.
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                # Константы класса не нужно передавать в метод
                                # таким образом.
                                # К ним можно обратиться через self.
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # У переменной чаще всего должно быть ровно одно назначение.
        # И оно должно быть отражено в ее имени.
        # Здесь тип валюты скорее в переменной `currency`, а в currency_type,
        # как мы видим ниже, записывается человеко-читаемое название валюты.
        # Его мы в итоге и возвращаем в строке.
        # Поэтому хорошим именем, например, может быть `currency_title`.
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            # Заметь, что здесь назначение переменной немного размывается.
            # До этого мы хранили в ней остаток в рублях, а теперь - в валюте.
            # Так изредка можно делать, чтобы не плодить слишком уж много
            # переменных, но следует быть очень осторожными!
            cash_remained /= USD_RATE
            currency_type = 'USD'
        # Назначение переменной `currency_type` - другое, поэтому проверять
        # ее значение здесь и в следующей ветке - некорректно.
        # Надежнее проверять currency, которая хранит именно тип валюты.
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Зачем здесь это сравнение с единицей?
            cash_remained == 1.00
            currency_type = 'руб'
        # Если здесь сделать отступ в пустую строку, мы визуально отделим
        # расчет валюты от логики вывода. Это повысит читаемость.
        if cash_remained > 0:
            return (
                # Вызов функции в ф-строке. Решается форматом `{x:.2}`.
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        # Следующие 2 элифа могут быть ифами (guard block!).
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # Продолжение строки через обратный слэш.
            # Для единообразия лучше использовать ф-строки, раз уж они
            # применены в других местах.
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Эту реализацию можно удалить. Если не переопределять этот метод, и так
    # будет вызван метод предка даже при обращении к экземпляру потомка.
    def get_week_stats(self):
        super().get_week_stats()
