# Streamlit Dashboard Template for MIC Forecasting (%R, Median, P90)

# ⚠️ NOTE: This code must be run locally in a Streamlit-supported environment.
# Streamlit is not available in restricted environments like this one.

try:
    import streamlit as st
    import pandas as pd
    import plotly.express as px

    st.set_page_config(page_title="MIC Forecasting Dashboard", layout="wide")
    st.title("🧪 MIC Forecasting Dashboard (Region-wise)")

    # Sidebar - Upload and filters
    st.sidebar.header("Upload & Filter Options")
    file = st.sidebar.file_uploader("Upload Forecast Summary CSV", type="csv")

    if file is not None:
        df = pd.read_csv(file)

        # Auto-detect available drug-bug combos and parameters
        available_regions = df['Region'].unique().tolist() if 'Region' in df.columns else []
        available_variables = [col for col in df.columns if col not in ['Year', 'Region']]

        # Dropdown selectors
        selected_regions = st.sidebar.multiselect("Select WHO Regions", available_regions, default=available_regions)
        selected_variables = st.sidebar.multiselect("Select Parameters to Plot", available_variables, default=['%R'])

        # Filtered data
        df_filtered = df[df['Region'].isin(selected_regions)]

        # Layout: show plots side by side for each variable
        for var in selected_variables:
            st.subheader(f"📈 Forecast: {var} by Region")
            fig = px.line(df_filtered, x='Year', y=var, color='Region', markers=True,
                          labels={'value': var, 'Year': 'Year'},
                          title=f"{var} Forecast Across Regions")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.markdown("### 📥 Download Filtered Data")
        st.dataframe(df_filtered)
        st.download_button("Download CSV", df_filtered.to_csv(index=False), file_name="filtered_forecast_data.csv")

    else:
        st.info("👈 Please upload a region-wise forecast CSV to begin.")

    # Footer
    st.markdown("---")
    st.markdown("Built as a template for multi-drug-bug MIC forecasting. Future-ready for Age, Specimen, Ward filters.")

except ModuleNotFoundError:
    print("❌ This code requires the 'streamlit' module. Please run it locally with Streamlit installed.")
    print("You can install it using: pip install streamlit")
