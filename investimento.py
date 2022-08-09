import pandas as pd
import streamlit as st
import time
import plotly.express as px

@st.cache
def convert_df(df):
    return df.to_csv().encode("utf-8")

def investimento_retroativo(M, C, t, interest):
    """
    Input:
     M = initial amount
     C = monthly contribution
     t = time in months
     interest = annual interest in % (Ex: If interest is 13%, then interest = 13)
    Output:

     month-to-month table with accrued value, accrued interest and nominal interest
    """
    interest = interest / 100
    mensal = [M]
    juros = [0]
    inte = 0
    for i in range(t):
        M += C + (M * (interest / 12))
        mensal.append(M)

    for i, j in enumerate(mensal):
        inte += j * interest / 12
        juros.append(inte)

    try:
        real_interest = [0]
        for i in range(len(juros)):
            real_interest.append(juros[i + 1] - juros[i])
    except:
        real_interest.append(juros[-1])
        real_interest = real_interest[:-1]

    return pd.DataFrame.from_dict(
        {
            "cumulative_value": mensal,
            "cumulative_interest": juros,
            "real_interest": real_interest,
        },
        orient="index",
    ).transpose()

M = st.number_input("Initial amount", value=0, min_value=0, format="%.2d")
C = st.number_input(
    "Monthly investment (interest yield will be reinvested)", value=5000, min_value=0
)
t = st.number_input("Total time of application (in months)", value=60, min_value=0)
interest = st.number_input(
    "Annual interest rate, in % (Ex: If the annual interest rate is 13%, then, interest = 13)",
    value=13,
    min_value=0,
)

if st.button("Calculate"):

    df = investimento_retroativo(int(M), int(C), int(t), int(interest))
    df.drop(df.tail(1).index, inplace=True)
    st.dataframe(df)
    csv = convert_df(df)
    st.download_button(
        "Download csv", csv, "interest_table.csv", "text/csv", key="download-csv"
    )

    valor_total = df.cumulative_value.max()

    st.write("In the end, you will have: ", str(f"{round(valor_total,2):,.2f}"))

    fig = px.bar(
        df,
        x=df.index,
        y=df.columns,
        labels={"index": "months", "value": "amounts", "variable": "amounts"},
        title="Amount X Months investment",
    )
    st.plotly_chart(fig)

with st.sidebar:
    st.write("This app was made by Victor Sotero.")
    st.write(
        "Check out the source code on my GitHub! [link](https://github.com/50sotero/investimento)."
    )
    st.write(
        "Check out my LinkedIn profile! [link](https://www.linkedin.com/in/victor-sotero/)."
    )
    with st.spinner(""):
        time.sleep(2)
    st.success("Thanks for coming!")
