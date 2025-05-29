import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load data
base_dir = os.path.dirname(__file__)
csv_path = os.path.join(base_dir, "cleared_data.csv")
all_df = pd.read_csv(csv_path)

# Membentuk kolom tanggal
all_df['date'] = pd.to_datetime(all_df[['year', 'month', 'day']])
all_df['year'] = all_df['date'].dt.year

st.set_page_config(layout="wide")
st.title("🌏 Dashboard Kualitas Udara Beijing (2013–2017)")

# ============================
# 1. Tren PM2.5 Tahunan
# ============================
st.header("📈 Tren PM2.5 Tahunan (Per Stasiun)")

with st.expander("ℹ️ Apa itu PM2.5?"):
    st.markdown("""
    **PM2.5** adalah partikel polusi udara yang berukuran lebih kecil dari 2.5 mikrometer.
    
    Karena ukurannya yang sangat kecil (sekitar 30 kali lebih kecil dari diameter rambut manusia), PM2.5 dapat masuk jauh ke dalam paru-paru dan bahkan ke dalam aliran darah.

    ❗ Konsentrasi tinggi PM2.5 berisiko menyebabkan gangguan kesehatan seperti:
    - Asma dan penyakit paru
    - Penyakit jantung
    - Gangguan pernapasan

    Oleh karena itu, pemantauan **PM2.5** penting untuk mengetahui tingkat kualitas udara.
    """)

stations = all_df['station'].unique().tolist()
selected_stations = st.multiselect("Pilih stasiun untuk dianalisis:", stations, default=stations)

yearly_trend = all_df.groupby(['year', 'station'])[['PM2.5']].mean().reset_index()
filtered_trend = yearly_trend[yearly_trend['station'].isin(selected_stations)]

fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.lineplot(data=filtered_trend, x='year', y='PM2.5', hue='station', marker='o', ax=ax1)
ax1.set_title('Tren Rata-rata PM2.5 per Tahun')
ax1.set_ylabel('Rata-rata PM2.5')
ax1.set_xlabel('Tahun')
ax1.grid(True)
st.pyplot(fig1)

# ============================
# 2. Stasiun Tertinggi & Terendah PM2.5
# ============================
st.header("🏭 Stasiun dengan PM2.5 Tertinggi dan Terendah")

available_years = sorted(all_df['year'].unique())
selected_year = st.selectbox("Pilih tahun:", available_years)

filtered_year_df = all_df[all_df['year'] == selected_year]
station_mean_pm25 = filtered_year_df.groupby('station')['PM2.5'].mean().sort_values(ascending=False)

col1, col2 = st.columns(2)
with col1:
    st.subheader(f"🔴 5 Stasiun Tertinggi (PM2.5) di {selected_year}")
    st.write(station_mean_pm25.head(5))
with col2:
    st.subheader(f"🟢 5 Stasiun Terendah (PM2.5) di {selected_year}")
    st.write(station_mean_pm25.tail(5))

fig2, ax2 = plt.subplots(figsize=(12, 6))
station_mean_pm25.plot(kind='bar', color='salmon', ax=ax2)
ax2.set_title(f'Rata-rata PM2.5 per Stasiun di Tahun {selected_year}')
ax2.set_ylabel('PM2.5')
ax2.set_xlabel('Stasiun')
ax2.set_xticklabels(station_mean_pm25.index, rotation=45)
ax2.grid(True)
plt.tight_layout()
st.pyplot(fig2)

# ============================
# 3. Perbandingan Musim
# ============================
st.header("❄️☀️ Perbandingan Polusi: Musim Dingin vs Musim Panas")

# Menentukan musim berdasarkan bulan
def assign_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Other'

all_df['season'] = all_df['month'].apply(assign_season)

# Pilihan polutan untuk dibandingkan
available_pollutants = ['PM2.5', 'PM10', 'CO', 'SO2', 'NO2']
selected_pollutants = st.multiselect("Pilih polutan untuk dibandingkan antar musim:", available_pollutants, default=available_pollutants)

seasonal_data = all_df[all_df['season'].isin(['Winter', 'Summer'])]

seasonal_mean = seasonal_data.groupby('season')[selected_pollutants].mean()

st.subheader("📊 Rata-rata Konsentrasi Polutan")
st.dataframe(seasonal_mean)

fig3, ax3 = plt.subplots(figsize=(10, 5))
seasonal_mean.T.plot(kind='bar', ax=ax3)
ax3.set_title('Perbandingan Konsentrasi Polutan antara Musim Dingin dan Musim Panas')
ax3.set_ylabel('Rata-rata Konsentrasi')
ax3.set_xlabel('Jenis Polutan')
ax3.grid(True)
plt.tight_layout()
st.pyplot(fig3)
