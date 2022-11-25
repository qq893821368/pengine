import modulefinder

Alerty = {

}


def df_test():
    from influxdb_client import InfluxDBClient
    from dataflow import expresser
    import yaml
    import pandas

    cnf = yaml.full_load(open("../alerty/template.yaml"))
    db = cnf['database']
    rs = cnf['resultset']
    cli = InfluxDBClient(db['url'], db['token'])
    qapi = cli.query_api()
    data = qapi.query_data_frame(db['flux'], org=db['org'])
    data = data.drop(columns=rs['drop'])
    groupby = rs['groupby'] or ['host']

    expr = "First(3,Last(5,Round(Square($avg),2))) == 0.02"

    for title, content in data.groupby(by=groupby):
        content: pandas.DataFrame
        ruler = expresser.Expression(expr)
        print(ruler)
        print(ruler.match(content))
        input()


def stack_test():
    from util import parser
    from util import evaluator
    content = "(loss_rate>0 & (time_in_day | time_not_in_midnight)) | (ttl>5 & ttl<4)"
    content = "True | False & False | True"
    expr = parser.infix2postfix(content)
    expr = [bool(e) if e not in ('&', '|') else e for e in expr]
    print(evaluator.eval_boolean_postfix(expr))
    # print(expr)


def signal_test():
    # !/usr/bin/env python
    # -*- coding: utf-8 -*-
    import signal
    import time

    def signal_handler(signum, frame):
        print('Received signal: ', signum)

    while True:
        signal.signal(signal.SIGHUP, signal_handler)  # 1
        signal.signal(signal.SIGINT, signal_handler)  # 2
        signal.signal(signal.SIGQUIT, signal_handler)  # 3
        signal.signal(signal.SIGALRM, signal_handler)  # 14
        signal.signal(signal.SIGTERM, signal_handler)  # 15
        signal.signal(signal.SIGCONT, signal_handler)  # 18
        while True:
            print('waiting')
            time.sleep(1)


def parse_test():
    from util import parser
    lexpr = "Round(Mdev($avg), 2)"
    print(parser.parse_rule_lexpr(lexpr))


def op_test():
    from util import processor

    with open("test.func") as f:
        func = processor.Process(f.read(), {"Alerty": Alerty})
        print(Alerty)
        func()
        print(Alerty)
        print("func:", func())
        print(Alerty)


op_test()
