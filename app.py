import pandas as pd
import streamlit as st
import re

st.title("HEY!")

data = pd.read_csv('raw_data/Food Ingredients and Recipe Dataset with Image Name Mapping.csv')
data.drop(columns='Unnamed: 0', inplace=True)

def get_ingredient_list(the_string):
    return str(the_string)[1:-1].split('\', \'')

def recepie_filter(df, recepies):
    if len(recepies) == 0:
        return st.write('Select a recepie')

    else:
        if len(recepies) == 1:
            df_filt = df[df['Title'].apply(lambda x:
                recepies[0] in x)]
            return df_filt
        if len(recepies) == 2:
            df_filt = df[df['Title'].apply(lambda x:
                recepies[0] in x or
                recepies[1] in x)]
            return df_filt
        if len(recepies) == 3:
            df_filt = df[df['Title'].apply(lambda x:
                recepies[0] in x or
                recepies[1] in x or
                recepies[2] in x)]
            return df_filt


data['Extra_Clean_Ingredients'] = data['Cleaned_Ingredients'].apply(get_ingredient_list)

empty_list = [None] * len(data.index)
data['tuple_ing_list'] = empty_list

pattern = re.compile(r'^\D*(\d+\.*\d*)\s*(.*)$')

for i in range(len(data)):
    ing_list = []
    for item in data.iloc[i]['Extra_Clean_Ingredients']:
        match = pattern.match(item)
        if match:
            quant = match.group(1)
            ingre = match.group(2).strip()
            ing_list.append((ingre,quant))
        else:
            ing_list.append((item, 0))

    data.at[i, 'tuple_ing_list'] = ing_list

selected_meals = st.multiselect('Pick a meal', data['Title'],
               placeholder='Pick a meal', max_selections=3)


if selected_meals:
    title = selected_meals

    df1 = data[data['Title'].isin(title)]['tuple_ing_list']

    length = len(df1)

    if length == 1:
        st.subheader(f"Shopping list for {length} recepies")
        st.write(pd.DataFrame(data[data['Title'].isin(title)]['tuple_ing_list'].to_list()[0],
                     columns=['Ingredients', 'Quntity'])[['Quntity', 'Ingredients']])

    if length == 2:
        st.subheader(f"Shopping list for {length} recepies")
        dd1 = pd.DataFrame(data[data['Title'].isin(title)]['tuple_ing_list'].to_list()[0],
                     columns=['Ingredients', 'Quntity'])[['Quntity', 'Ingredients']]
        dd2 = pd.DataFrame(data[data['Title'].isin(title)]['tuple_ing_list'].to_list()[1],
                     columns=['Ingredients', 'Quntity'])[['Quntity', 'Ingredients']]

        merg = pd.concat([dd1, dd2])
        st.write(merg)

    if length == 3:
        st.subheader(f"Shopping list for {length} recepies")
        dd1 = pd.DataFrame(data[data['Title'].isin(title)]['tuple_ing_list'].to_list()[0],
                     columns=['Ingredients', 'Quntity'])[['Quntity', 'Ingredients']]
        dd2 = pd.DataFrame(data[data['Title'].isin(title)]['tuple_ing_list'].to_list()[1],
                     columns=['Ingredients', 'Quntity'])[['Quntity', 'Ingredients']]
        dd3 = pd.DataFrame(data[data['Title'].isin(title)]['tuple_ing_list'].to_list()[2],
                     columns=['Ingredients', 'Quntity'])[['Quntity', 'Ingredients']]

        merg = pd.concat([dd1, dd2, dd3])

        st.write(merg)
