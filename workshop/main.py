import pandas as pd
import streamlit as st
import plotly.express as px


st.title("ข้อมูลการเลี้ยงเป็ดไข่")
st.header("ในประเทศไทย")
st.write("นี่คือจำนวนการเลี้ยงเป็ดไข่ทั้งหมดของประเทศไทย")

df = pd.read_csv("../datasets/1642645053.csv", encoding="tis-620")
provinces = df["สถานที่เลี้ยงสัตว์ จังหวัด"].unique()
#st.write(provinces)

option = st.selectbox(
        "which provinces?",
        provinces
)

st.write(df[    df["สถานที่เลี้ยงสัตว์ จังหวัด"] == option  ])

provinces_df = pd.read_csv("https://raw.githubusercontent.com/dataengineercafe/thailand-province-latitude-longitude/refs/heads/main/provinces.csv")
joined = pd.merge(df, provinces_df, how="left", left_on="สถานที่เลี้ยงสัตว์ จังหวัด", right_on="province_name")
   

selected_df = joined[["สถานที่เลี้ยงสัตว์ จังหวัด", "province_lat", "province_lon", "โคเนื้อ พื้นเมือง เพศผู้ (ตัว)"]]
cleaned = selected_df.dropna()
cleaned["โคเนื้อ พื้นเมือง เพศผู้ (ตัว)"] = cleaned[cleaned["โคเนื้อ พื้นเมือง เพศผู้ (ตัว)"] != "1,480"]["โคเนื้อ พื้นเมือง เพศผู้ (ตัว)"].astype(int)

grouped_df = cleaned.groupby("สถานที่เลี้ยงสัตว์ จังหวัด")["โคเนื้อ พื้นเมือง เพศผู้ (ตัว)"].sum().reset_index()
joined_df = pd.merge(grouped_df, provinces_df, how="left", left_on="สถานที่เลี้ยงสัตว์ จังหวัด", right_on="province_name")
st.write(joined_df)

joined_df = joined_df.rename(columns={"โคเนื้อ พื้นเมือง เพศผู้ (ตัว)": "amount"})

st.map(joined_df, latitude="province_lat", longitude="province_lon", size="amount")