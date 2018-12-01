from yametrikapy import Metrika


def yandex():
    client_id = '123456'
    client_secret = 'qwerty'
    code = '123456'

    metrika = Metrika(client_id, client_secret=client_secret, code=code)

    counters = metrika.counters().counters
    print(counters)

    counter_id = counters[0]['id']
    stat = metrika.stat_data(counter_id, 'ym:s:visits,ym:s:users', dimensions='ym:s:searchEngineName')
    print(stat.data)

    counter = metrika.add_counter('My new counter', 'my-site.com')
    print(counter.counter['id'], counter.counter['name'])

    # Output obtained data
    print(metrika.get_data())
