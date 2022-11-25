from typing import Union

import pandas.core.groupby
import yaml
from util import parser
from util import silenter
from dataflow import ruler
from util import evaluator
from util import processor
from dataflow import expresser
from influxdb_client import InfluxDBClient

cnf: dict = yaml.full_load(open("../alerty/template.yaml"))
Alerty: dict = {}

# 基本配置
service = cnf.pop("service", ["unknown"])
active_duration = cnf.pop("for", 3600)
asleep_duration = cnf.pop("sleep", 10.0)
calm_recover = cnf.pop("recover", -1)
action = cnf.pop("action", [])
silenter = silenter.Silenter(cnf.pop("silent", []))

# database
database = cnf.pop("database", {})
flux = database.pop("flux", "")
flux_cli = InfluxDBClient(**database)

# data
resultset_cnf = cnf.pop("resultset", {})
data: Union[pandas.core.groupby.GroupBy, pandas.DataFrame]

data = flux_cli.query_api().\
    query_data_frame(flux).\
    drop(columns=resultset_cnf.pop("drop", None))
groupby_cols = resultset_cnf.pop("groupby", None)
data = data.groupby(by=groupby_cols) if groupby_cols is not None else (("default", data),)


print(data)  # 此处data会由于groupby的设置与否而确定为不同的类型，无groupby则为DataFrame，有groupby则为GroupBy


# rule
ruleset = cnf.pop("rule", {})
ruleset = {name: ruler.Ruler("template", name, rule) for name, rule in ruleset.items()}
[print(f"{rule}") for rule in ruleset.values()]


# alerts
alertset = cnf.pop("alert", {})


def result_handler(rule):
    if rule in ("|", "&"):
        return rule
    else:
        return tuple(ruleset.get(rule, lambda x: False)(group[1]) for group in data)


for k, v in alertset.items():
    trigger = parser.infix2postfix(v.get("trigger", ""))
    if trigger is not None:
        resultlist = tuple(map(result_handler, trigger))

        print("resultlist", resultlist)
        print("result:", evaluator.eval_boolean_sequential_postfix(resultlist))





