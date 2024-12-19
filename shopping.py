import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Wczytaj dane
@st.cache_data
def load_data():
    return pd.read_csv('shopping_trends.csv')

data = load_data()

# Ustawienia strony
st.title("Shopping Trends Dashboard")
st.sidebar.title("Opcje analizy")

# Filtry
age_filter = st.sidebar.slider("Wiek klienta", int(data["Age"].min()), int(data["Age"].max()), (18, 70))
price_filter = st.sidebar.slider("Cena", int(data["Purchase Amount (USD)"].min()), int(data["Purchase Amount (USD)"].max()), (0, 100))
gender_filter = st.sidebar.multiselect("Płeć", data["Gender"].unique(), data["Gender"].unique())
category_filter = st.sidebar.multiselect("Kategorie produktów", data["Category"].unique(), data["Category"].unique())
name_filter = st.sidebar.multiselect("Nazwa produktów", data["Item Purchased"].unique(), data["Item Purchased"].unique())

# Filtruj dane
filtered_data = data[(data["Age"] >= age_filter[0]) & 
                     (data["Age"] <= age_filter[1]) & 
                     (data["Purchase Amount (USD)"] >= price_filter[0]) & 
                     (data["Purchase Amount (USD)"] <= price_filter[1]) & 
                     (data["Gender"].isin(gender_filter)) & 
                     (data["Category"].isin(category_filter)) &
                     (data["Item Purchased"].isin(name_filter))]

# Wyświetlanie danych
st.write("### Filtrowane dane", filtered_data)

# Wykresy
st.write("## Analiza wizualna")

# Wykres 1: Zakupy wg kategorii
st.write("### Liczba zakupów wg kategorii")
category_counts = filtered_data["Category"].value_counts()
fig, ax = plt.subplots()
category_counts.plot(kind="bar", ax=ax)
ax.set_xlabel("Kategoria")
ax.set_ylabel("Liczba zakupów")
st.pyplot(fig)

# Wykres 2: Średnia kwota zakupów wg sezonu
st.write("### Średnia kwota zakupów wg sezonu")
season_mean = filtered_data.groupby("Season")["Purchase Amount (USD)"].mean()
fig, ax = plt.subplots()
season_mean.plot(kind="bar", ax=ax)
ax.set_xlabel("Sezon")
ax.set_ylabel("Średnia kwota zakupów (USD)")
st.pyplot(fig)

# Wykres 3: Liczba klientów wg wieku
st.write("### Liczba klientów wg wieku")
fig, ax = plt.subplots()
filtered_data["Age"].hist(bins=20, ax=ax)
ax.set_xlabel("Wiek")
ax.set_ylabel("Liczba klientów")
st.pyplot(fig)

# Wykres 4: Liczba zakupów wg nazwy produktu
st.write("### Liczba kupionych prodkutów według nazwy")
counts_names = filtered_data["Item Purchased"].value_counts()
st.write(counts_names)
fig, ax = plt.subplots()
def make_autopct(counts_names):
    def my_autopct(pct):
        total = sum(counts_names)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct
counts_names.plot(kind="pie", autopct=make_autopct(counts_names))
st.pyplot(fig)

# Wykres 5: Liczba zakupów według płci:
st.write("### Liczba kupionych prodkutów według płci")

counts_genders = filtered_data["Gender"].value_counts()
fig, ax = plt.subplots()
counts_genders.plot(kind="pie", autopct='%1.1f%%')
st.pyplot(fig)

# Wykres 6: Ceny zakupów według płci
st.write("### Ceny zakupów według płci")

male_data = filtered_data[ (filtered_data["Gender"].str.contains("Male"))]
female_data = filtered_data[ (filtered_data["Gender"].str.contains("Female"))]
avg_male = sum(male_data["Purchase Amount (USD)"]) / len(male_data["Purchase Amount (USD)"])
st.write("Średnia cena zakupów dla mężczyzn:", avg_male)

avg_famele = sum(female_data["Purchase Amount (USD)"]) / len(female_data["Purchase Amount (USD)"])
st.write("Średnia cena zakupów dla kobiet:", avg_famele)

y = np.array([avg_male,avg_famele])
x = np.array(["mężczyzna","kobieta"])
bar_colors = ['tab:red', 'tab:blue']

fix, ax.bar(x,y,color=bar_colors)


st.pyplot(fig)
