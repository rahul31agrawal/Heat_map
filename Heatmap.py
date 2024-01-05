import streamlit as st

import pandas as pd
import os 
import warnings

import seaborn as sns

warnings.filterwarnings('ignore')
st.set_page_config(page_title="Davis Prices Analytics!!!", page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: Prices EDA")
st.markdown('<style>div.block-container{padding-top:1rem;} </style>',unsafe_allow_html=True)

df = pd.read_excel("6 month davis pricesheets excluded exchange.xlsx")
df['assesment_frequency'] = df['assesment_frequency'].replace(['weekly', 'monthly', 'daily'], ['Weekly', 'Monthly', 'Daily'])
filtered_df = df[df['assesment_frequency'].isin(['Monthly', 'Bi-weekly', 'Daily', 'Weekly'])]
df = filtered_df

col1, col2 = st.columns((2))

st.sidebar.header("Choose your filter: ")
# Create for Category

default_dpc_values = ['DPC406', 'DPC1030','DPC1018','DPC1007','DPC1715','DPC1040','DPC1600','DPC2063',]

dpc = st.sidebar.multiselect("Select DPC's", df["dpc_number"].unique(),default=default_dpc_values)

if not dpc:
    df2 = df.copy()
   

else:
    df2 = df[df["dpc_number"].isin(dpc)]





# Assuming your DataFrame is named 'df' and the date column is named 'date_column'
df2['formatted_date'] = pd.to_datetime(df2['startDate']).dt.strftime("%b'%y")

df2 = df2.pivot_table(index=['dpc_number','dpc_website_name','parent_category','assesment_frequency'], columns=['formatted_date'], values='new_price_value', aggfunc='mean')



# Check if df2 is empty
if df2.empty:
    st.warning("No data available for the selected filters.")
else:
    # Sort the columns by converting 'formatted_date' to datetime
    df2.columns = pd.to_datetime(df2.columns, format="%b'%y")
    df2 = df2.sort_index(axis=1)

    # Convert columns back to the original format ("%b'%y")
    df2.columns = df2.columns.strftime("%b'%y")

    first_column_name = df2.columns[5]

    # Extract the column names
    columns_to_format = df2.columns[0:6]

    # CODE1
    # Function to apply color gradient to each row
    def row_gradient(row):
        # Set the number of color shades
        num_shades = 12

        # Check if the row contains NaN values
        if row.isna().any():
          return [f'background-color: rgb(255, 255, 255)'] * len(row)

        # Create a color palette with the desired number of shades
        palette = sns.color_palette("RdYlGn", n_colors=num_shades)

        # Calculate the mid value for colormap scaling
        mid = (row.max() + row.min()) / 2

        # Check if the range is zero
        if row.max() == row.min():
            # If the range is zero, assign a default color (e.g., white)
            return [f'background-color: rgb(255, 255, 255)'] * len(row)

        # Map each value in the row to a corresponding color in the palette
        colors = [
            palette[int((num_shades - 1) * (value - row.min()) / (row.max() - row.min()))]
            for value in row
        ]

        # Convert colors to RGB format
        rgb_colors = [
            f'rgb({int(255 * color[0])}, {int(255 * color[1])}, {int(255 * color[2])})'
            for color in colors
        ]

        return [f'background-color: {rgb}' for rgb in rgb_colors]

    # Apply the styling function to each row
    s = df2.style.apply(lambda row: row_gradient(row), axis=1)

    # Display the styled DataFrame
    st.dataframe(s.format({columns_to_format[0]: '{:,.2f}',columns_to_format[1]: '{:,.2f}',columns_to_format[2]: '{:,.2f}',columns_to_format[3]: '{:,.2f}',columns_to_format[4]: '{:,.2f}',columns_to_format[5]: '{:,.2f}'}))
