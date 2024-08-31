import streamlit as st
import pandas as pd
import akshare as ak
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import math

st.title("基金简易收益计算系统（Man发布，后续持续更新）")

# st.image("WechatIMG926.jpeg", width=200)
#
# st.write("## hello!!")
#
# a = 3 * 34
#
# # {"first":12,"second":45,"third":88}
# #
# # {"google":[12,12],"google":[13,13]}
#
# df = pd.DataFrame({"学号": ["01", "02", "03", "04", "05"],
#                    "班级": ["二班", "一班", "三班", "四班", "二班"],
#                    "成绩": [98, 68, 65, 87, 76]})
#
# st.dataframe(df)
#
# st.divider()
#
# st.table(df)

# currency_boc_sina_df = ak.currency_boc_sina(symbol="美元", start_date="20230101", end_date="20230201")
#
# df_exchange = pd.DataFrame(currency_boc_sina_df)
#
# st.dataframe(df_exchange)
#
#
# def create_chart1(input_data):
#     df_data = pd.DataFrame(input_data["中行汇买价"], columns=input_data["日期"])
#     df_data.set_index(input_data["日期"][0], inplace=True)
#     st.line_chart(df_data)
#
# create_chart1(df_exchange)


# 代码：970129
fund_code = st.text_input("请输入您购买的基金代码")
start_purchase_date = st.date_input("请选择您的配置该基金的日期")
finish_purchase_date = st.date_input("请选择您赎回该基金的日期，如果还没有赎回，则不选择,默认选择今天")


# 今年的天数
def days_this_year():
    now = datetime.date.today()
    current_year_func = datetime.date.today().year
    year_start = datetime.date(current_year_func, 1, 1)
    return (now - year_start).days

# 去年今天的天数
def days_last_year():
    last_year_func = datetime.date.today().year - 1
    day_of_last_year_func = datetime.date(last_year_func,datetime.date.today().month,datetime.date.today().day)
    last_year_start_func = datetime.date(last_year_func,1,1)
    return (day_of_last_year_func - last_year_start_func).days

# 两个日期相隔天数

# 同比增长函数
def year_on_year_growth(current_year_value ,last_year_value):
    year_on_year_growth_rate = (current_year_value - last_year_value)/last_year_value
    return year_on_year_growth_rate


# 调用基金接口,定义调用函数

# def check_fund_his_list(fund_code_no,start_date,finish_date):
#     fund_open_fund_info_em_df_func = ak.fund_open_fund_info_em(symbol=fund_code_no, indicator="单位净值走势")
#     df_bond_fund_func = pd.DataFrame(fund_open_fund_info_em_df_func)
#     # df_fund_dict_func = df_bond_fund_func.to_dict()
#     local_dict = 0
#     df_fund_dict_part_func = {"净值日期":{"":""},"单位净值":{"":""},"日增长率":{"":""}}
#     while df_fund_dict_func["净值日期"][local_dict] < start_date:
#         local_dict = local_dict + 1
#     while finish_date >= df_fund_dict_func["净值日期"][local_dict] >= start_date:
#         df_fund_dict_part_func["净值日期"][local_dict] = df_fund_dict_func["净值日期"][local_dict]
#         df_fund_dict_part_func["单位净值"][local_dict] = df_fund_dict_func["单位净值"][local_dict]
#         df_fund_dict_part_func["日增长率"][local_dict] = df_fund_dict_func["日增长率"][local_dict]
#         local_dict += 1
#     df_fund_part_func = pd.DataFrame(df_fund_dict_part_func)
#     return df_fund_part_func

# st.write(fund_open_fund_info_em_df[0])

# def create_chart2(input_data):
#     df_data = pd.DataFrame(input_data[])

# fund_list = ak.fund_etf_category_sina(symbol="封闭式基金")
#
# df_fund_list = pd.DataFrame(fund_list)
#
# st.dataframe(df_fund_list)

# 调用接口数据
fund_open_fund_info_em_df = ak.fund_open_fund_info_em(symbol=fund_code, indicator="单位净值走势")

# 形成接口数据的dataframe
df_bond_fund = pd.DataFrame(fund_open_fund_info_em_df)

# st.dataframe(df_bond_fund)

# 设置用户选择的数据的dataframe
df_bond_fund_chosen = df_bond_fund[(df_bond_fund["净值日期"] >= start_purchase_date) &
                                   (df_bond_fund["净值日期"] <= finish_purchase_date)]

st.dataframe(df_bond_fund_chosen)

# st购买净值曲线图
st.bar_chart(df_bond_fund_chosen, x="净值日期", y="日增长率",x_label="日期")
# st.line_chart(df_bond_fund_chosen, x="净值日期", y="单位净值",x_label="日期", y_label="当日净值")

# plt绘制的曲线图
# fig, ax = sns.lineplot(x="净值日期",y="日增长率")
# ax.plot(df_bond_fund_chosen)
# st.pyplot(fig)

# 今年和去年
current_year = datetime.date.today().year
last_year = datetime.date.today().year - 1

# 今年和去年的1月1日
year_start_date = datetime.date(current_year, 1, 1)
last_year_start_date = datetime.date(last_year, 1, 1)

# 去年的今天
today_of_last_year = datetime.date(last_year,datetime.date.today().month,datetime.date.today().day)

# 今年和去年的同一时间净值dataframe
df_bond_fund_current_year = df_bond_fund[df_bond_fund["净值日期"] >= year_start_date]
df_bond_fund_last_year = df_bond_fund[(df_bond_fund["净值日期"] >= last_year_start_date) &
                                      (df_bond_fund["净值日期"] <= today_of_last_year)]

#

# 今年和去年和总的收益
current_earn_value = df_bond_fund_current_year.iloc[-1, 1] - df_bond_fund_current_year.iloc[0, 1]
last_earn_value = df_bond_fund_last_year.iloc[-1, 1] - df_bond_fund_last_year.iloc[0, 1]
total_earn_value = df_bond_fund_chosen.iloc[-1,1] - df_bond_fund_chosen.iloc[0, 1]

# 年化收益率 = [（投资内收益 / 本金）/ 投资天数] *365 ×100%
fund_current_year_rate = ((current_earn_value/df_bond_fund_current_year.iloc[0, 1])/days_this_year())*365*100
fund_last_year_rate = ((last_earn_value/df_bond_fund_last_year.iloc[0, 1])/days_last_year())*365*100

# 计算整体的收益年化率
fund_total_year_rate = ((total_earn_value/df_bond_fund_chosen.iloc[0, 1])/(finish_purchase_date-start_purchase_date).days)*365*100
# 收益同比增长率

earn_value_year_on_year_growth = year_on_year_growth(current_earn_value,last_earn_value)

#计算整体的收益年化率


# st.write(fund_current_year_rate)

# st.write(df_bond_fund_current_year.loc[0, "单位净值"])

# fund_increase_rate =

# st.dataframe(df_bond_fund_current_year)

# st.write(current_year)


# 显示结果
st.write(f"今年该基金的年化收益率为：{fund_current_year_rate:.2f}%")
st.write(f"去年该基金同一时段的年化收益率为：{fund_last_year_rate:.2f}%")
st.write(f"您购买的该基金整体年化收益率为：{fund_total_year_rate:.2f}%")
st.write(f"该基金的收益同比增长为：{earn_value_year_on_year_growth:.2f}%")

# #打印字典
# st.write(df_fund_dict)

# 打印dataframe
# df_fund = st.dataframe(df_bond_fund)
#
# df_fund_list = check_fund_his_list(fund_code,start_purchase_date,finish_purchase_date)
# st.dataframe(df_fund_list)

# df_fund_dict_part_func1 = {"净值日期":{"":""},"单位净值":{"":""},"日增长率":{"":""}}
# df_fund_dict_part_func1["净值日期"] = df_fund_dict["净值日期"]
# df_fund_dict_part_func1["单位净值"] = df_fund_dict["单位净值"]
# df_fund_dict_part_func1["日增长率"] = df_fund_dict["日增长率"]
#
# st.write(df_fund_dict_part_func1)
# st.write(df_fund_dict["净值日期"])

# sns.lineplot(data = df_bond_fund_chosen,x="净值日期",y="单位净值")
