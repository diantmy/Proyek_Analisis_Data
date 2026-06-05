# E-Commerce Data Analysis Dashboard

## Project Overview

Proyek ini merupakan analisis data menggunakan E-Commerce Public Dataset. Analisis dilakukan untuk memahami performa penjualan, tren transaksi pelanggan, tingkat kepuasan pelanggan, serta segmentasi pelanggan menggunakan metode RFM Analysis.

## Business Questions

1. Kategori produk apa yang menghasilkan total revenue tertinggi selama periode September 2016 hingga Oktober 2018?

2. Bagaimana tren jumlah transaksi pelanggan per bulan selama periode September 2016 hingga Oktober 2018?

3. Bagaimana tingkat kepuasan pelanggan pada setiap kategori produk berdasarkan skor ulasan (review score) selama periode September 2016 hingga Oktober 2018?

## Project Structure

```text
submission/
│
├── dashboard/
│   ├── main_data.csv
│   └── dashboard.py
│
├── data/
│
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Setup Environment

```bash
pip install -r requirements.txt
```

## Run Streamlit Dashboard

```bash
streamlit run dashboard/dashboard.py
```

## Dashboard Features

* KPI Total Revenue
* KPI Total Orders
* KPI Total Customers
* Top Product Categories by Revenue
* Monthly Orders Trend
* Customer Satisfaction Analysis
* RFM Customer Segmentation
