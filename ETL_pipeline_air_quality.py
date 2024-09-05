import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import os
import time
import schedule
import threading
import requests
import json


# Function to extract data from API
def extract_data_from_api(api_keys_path="API_keys.json", output_file_path="Data/Milan_Air_Quality.csv"):
    url = "https://air-quality.p.rapidapi.com/history/airquality"
    querystring = {"lon": "9.188", "lat": "45.464"}  # Milan coordinates

    with open(api_keys_path) as api_keys_file:
        api_keys = json.load(api_keys_file)

    response = requests.get(url, headers=api_keys, params=querystring)

    if response.status_code == 200:
        data = response.json()  
        json_output_path = "Data/Milan_Air_Quality.json"
        os.makedirs(os.path.dirname(json_output_path), exist_ok=True)
        with open(json_output_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully saved to {json_output_path}")

        df = pd.read_json(json_output_path)
        if 'data' in df.columns:
            data = pd.json_normalize(df['data'])  
            df.drop(columns='data', inplace=True)
            df = pd.concat([df, data], axis=1)  
        df.to_csv(output_file_path, index=False)

        print(f"Normalized data successfully saved to {output_file_path}")
        return df  
    else:
        print(f"Request failed with status code {response.status_code}")
        return None


# Function to clean data
def clean_data(df):

    print(f"DataFrame Shape before checking missing values: {df.shape}")
    missing_values = df.isnull().sum()
    if missing_values.any():
        print("\BE CAREFULL!! There are missing values in the following columns:")
        print(missing_values[missing_values > 0])
    else:
        print("\nNo duplicates found in this DataFrame.")

    initial_shape = df.shape
    df = df.drop_duplicates()
    final_shape = df.shape
    if initial_shape != final_shape:
        print(f"\nDuplicated rows removed. New DataFrame shape: {final_shape}")
    else:
        print("\nNo duplicates found in this DataFrame.")


    try:
        df['timestamp_local'] = pd.to_datetime(df['timestamp_local'])
        df['timestamp_utc'] = pd.to_datetime(df['timestamp_utc'])
    except Exception as e:
        print(f"\nERROR during datetime columsn conversion: {e}")
        return df

    if pd.api.types.is_datetime64_any_dtype(df['timestamp_local']) and pd.api.types.is_datetime64_any_dtype(df['timestamp_utc']):
        print("\nThe columns 'timestamp_local' and 'timestamp_utc' have been successfully converted to datetime format.")
    else:
        print("\nERROR: There was a problem converting the datetime columns.")

    for col in df.columns:
        if df[col].nunique() == 1:
            df.drop(columns=[col], inplace=True)
            print(f"\Column '{col}' dropped because with only unique value.")

    if 'datetime' in df.columns:
        df.drop(columns='datetime', inplace=True)
        print("\Column 'datetime' dropped.")
    else:
        print("\Column 'datetime' not found, not action done.")

    return df

# Function to transform data
def transform_data(df):
    df['year'] = df['timestamp_local'].dt.year
    df['month'] = df['timestamp_local'].dt.month
    df['day'] = df['timestamp_local'].dt.day
    df['hour'] = df['timestamp_local'].dt.hour

    df.set_index('timestamp_local', inplace=True)

    df['pm10_pm25_ratio'] = round(df['pm10'] / df['pm25'], 2)
    df['no2_o3_ratio'] = round(df['no2'] / df['o3'], 2)
    df['co_so2_ratio'] = round(df['co'] / df['so2'], 2)

    df = df[['aqi', 'co', 'no2', 'o3', 'pm10', 'pm25', 'so2', 'pm10_pm25_ratio', 'no2_o3_ratio', 'co_so2_ratio', 'timestamp_utc', 'ts',
           'year', 'month', 'day', 'hour']]

    return df

# Function to save df in the exisitng dataframe
def save_transformed_data(df, file_path='Data/Milan_Air_Quality_Transformed.csv'):
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path, index_col=0, parse_dates=['timestamp_local'])
        combined_df = pd.concat([existing_df, df]).drop_duplicates()
        combined_df.to_csv(file_path)
    else:
        df.to_csv(file_path)
    print(f"Data saved to {file_path}")

# Function to visualize and save plots
def create_and_save_visualizations(df, feature_to_viz = 'aqi', scatter_x = 'pm10', scatter_y = 'pm25'):
    # Histogram with Mean and Standard Deviation
    column = feature_to_viz
    mean_value = df[column].mean()
    std_value = df[column].std()

    fig_histogram = px.histogram(df, x=column, nbins=50, title=f'Distribution of {column.capitalize()} with Mean and STD')
    fig_histogram.add_vline(x=mean_value, line_dash="dash", line_color="green", annotation_text="Mean")
    fig_histogram.add_vline(x=mean_value + std_value, line_dash="dash", line_color="red", annotation_text="+1 STD")
    fig_histogram.add_vline(x=mean_value - std_value, line_dash="dash", line_color="red", annotation_text="-1 STD")
    fig_histogram.write_image(f'Images/Air_Quality/{feature_to_viz}_histogram.png')  
    fig_histogram.write_html(f'Images/Air_Quality/{feature_to_viz}_histogram.html')  

    # Box Plot
    fig_box = px.box(df, x=column, title=f'Box Plot of {column.capitalize()} by Category')
    fig_box.write_image('Images/Air_Quality/aqi_box_plot.png')  
    fig_box.write_html('Images/Air_Quality/aqi_box_plot.html')  

    # Correlation Matrix Heatmap
    correlation_matrix = df.corr()
    fig_heatmap = px.imshow(round(correlation_matrix, 2), title='Correlation Matrix Heatmap', color_continuous_scale='Magma',
                           aspect='auto', text_auto=True)
    fig_heatmap.write_image('Images/Air_Quality/correlation_matrix_heatmap.png') 
    fig_heatmap.write_html('Images/Air_Quality/correlation_matrix_heatmap.html')  

    # Time Series Plot
    fig_time_series = px.area(df, x='timestamp_local', y=feature_to_viz, title=f'Time Series of {feature_to_viz} with Rangeslider')
    fig_time_series.update_xaxes(minor=dict(ticks="inside", showgrid=True))
    fig_time_series.update_xaxes(rangeslider_visible=True)
    fig_time_series.write_image(f'Images/Air_Quality/time_series_{feature_to_viz}_plot.png')  
    fig_time_series.write_html(f'Images/Air_Quality/time_series_{feature_to_viz}_plot.html') 

    # Scatter Plot with Regression Line
    fig_scatter = px.scatter(df, x=scatter_x, y=scatter_y, title='Scatter Plot with Regression Line')
    fig_scatter.write_image(f'Images/Air_Quality/scatter_plot_{scatter_x}_vs_{scatter_y}.png')  
    fig_scatter.write_html(f'Images/Air_Quality/scatter_plot_{scatter_x}_vs_{scatter_y}.html')  

    # Distribution Plot with KDE and Histogram
    df_numeric = df.select_dtypes(include='number')
    features = df_numeric.columns

    fig = go.Figure()
    for feature in features:
        hist_data = [df[feature]]
        group_labels = [feature]
        distplot = ff.create_distplot(hist_data, group_labels, show_hist=True, show_rug=False)
        for trace in distplot.data:
            trace.visible = (feature == features[0]) 
            fig.add_trace(trace)

    dropdown_buttons = [
        dict(
            label=feature,
            method='update',
            args=[{'visible': [i // 2 == j for i in range(len(features) * 2)]}]
        )
        for j, feature in enumerate(features)
    ]

    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=dropdown_buttons,
                x=0.17,
                y=1.15,
                xanchor='right',
                yanchor='top'
            )
        ],
        title='Distribution and KDE of Selected Feature',
        xaxis_title='Feature Values',
        yaxis_title='Density',
        showlegend=True
    )
    fig.write_image('Images/Air_Quality/distribution_kde_plot.png')  
    fig.write_html('Images/Air_Quality/distribution_kde_plot.html') 

    print("All visualizations have been created and saved successfully.")

# Main ETL pipeline
def etl_process():
    df = extract_data_from_api()

    df = clean_data(df)

    df = transform_data(df)

    save_transformed_data(df)

    create_and_save_visualizations(df)

    print("ETL process completed successfully.")

# Plan execution every 24 hours
schedule.every(24).hours.do(etl_process)

# Execute pipeline continously with interruption options
def run_scheduler():
    while not stop_thread:  
        schedule.run_pending()
        time.sleep(1)

stop_thread = False 
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()
while True:
    user_input = input("Digit 'exit' to interrupt the pipeline: ").strip().lower()
    if user_input == 'exit':
        stop_thread = True 
        scheduler_thread.join() 
        print("Pipeline correctly interrupted.")
        break
