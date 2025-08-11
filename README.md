# HealthKart Influencer Campaign Dashboard

## 🚀 Project Overview

This dashboard is an open-source tool built to track, analyze, and visualize the performance of influencer marketing campaigns across various platforms (Instagram, YouTube, etc.). It allows for real-time monitoring of key metrics like ROI and Incremental ROAS, and provides actionable insights into influencer and campaign performance.

## 🛠️ Setup and Installation

1.  **Clone the repository (if applicable):**
    `git clone <your-repo-url>`
    `cd <your-repo-name>`

2.  **Install Dependencies:**
    This project requires Python and a few libraries. You can install them using pip:
    `pip install pandas streamlit plotly numpy faker`

3.  **Generate Simulated Data:**
    Since no real data was provided, a data simulation script (`generate_data.py` or the `datasets.ipynb` notebook) is used to create realistic data. Run the script to create the necessary CSV files:
    `python generate_data.py` if using a `.py` file

4.  **Run the Dashboard:**
    Once the CSV files are generated, you can start the Streamlit application:
    `streamlit run dashboard.py`

    This command will launch the dashboard in your web browser.

## 📝 Assumptions for Data Modeling

To make the simulated data as realistic as possible, the following assumptions were made:

* **Campaigns:** We assume campaigns run for approximately three months, and influencers are either paid per post or per order.
* **Payouts:** An influencer's payout rate is assumed to be proportional to their follower count. Larger influencers command higher fees per post.
* **Revenue:** Revenue generated is assumed to be influenced by an influencer's reach and engagement. Larger influencers drive higher sales volumes.
* **Incremental ROAS:** The "organic baseline revenue" is defined as the revenue generated from non-influencer sources within the `tracking_data` dataset. This is used to calculate the incremental revenue from influencer campaigns.

## ✨ Dashboard Features

* ** Dashboard Link: ** https://healthkart-influencer-campaign-dashboard.streamlit.app/
* **Interactive Filters:** Filter data by influencer category, social media platform, and date range.
* **Key Performance Indicators (KPIs):** Displays total revenue, total payouts, ROI, and Incremental ROAS.
* **Performance Visualizations:** Includes charts to show revenue trends over time, and performance breakdowns by platform and influencer category.
* **Influencer Leaderboard:** Identifies and ranks top-performing and under-performing influencers by ROI.
* **Automated Report Generation:** A button generates a detailed, easy-to-read text report summarizing key insights.
* **Download Functionality:** Allows for the export of data and the generated report.

## 🧑‍💻 About the Author

**Siddharth R Bhardwaj**

I am a data analyst with a passion for building insightful dashboards and tools. This project was developed as an intern assignment for HealthKart.

* **LinkedIn:** https://www.linkedin.com/in/siddharth-r-bhardwaj24082/
* **GitHub:** https://github.com/bsid24082/
* **Email:** siddharth.bhardwaj24082@gmail.com
