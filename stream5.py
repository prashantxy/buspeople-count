import streamlit as st
import pandas as pd

# Load datasets
@st.cache
def load_data():
    bus_stops = pd.read_csv('test1/bus.csv')
    routes = pd.read_csv('test1/bus.csv')
    return bus_stops, routes

# Function to calculate emissions
def calculate_emissions(distance, fuel_consumption, emissions_factor):
    return distance * fuel_consumption * emissions_factor / 1000  # in kg CO2

def main():
    st.title('Carbon Emission Tracking for Bus Routes')

    # Load data
    bus, routes = load_data()

    st.sidebar.header('Select Route')
    route_id = st.sidebar.selectbox('Choose a Route ID:', routes['Route ID'].unique())
    
    # Get route details
    route = routes[routes['Route ID'] == route_id].iloc[0]
    distance = route['Distance (km)']
    fuel_consumption = route['Fuel Consumption (L/km)']
    emissions_factor = route['Emissions Factor (g CO2/L)']

    st.write(f"Route ID: {route_id}")
    st.write(f"Start Bus Stop ID: {route['Start Bus Stop ID']}")
    st.write(f"End Bus Stop ID: {route['End Bus Stop ID']}")
    st.write(f"Distance: {distance} km")
    st.write(f"Fuel Consumption: {fuel_consumption} L/km")
    st.write(f"Emissions Factor: {emissions_factor} g CO2/L")

    # Calculate emissions
    emissions = calculate_emissions(distance, fuel_consumption, emissions_factor)
    st.write(f"Estimated Carbon Emissions for this Route: {emissions:.2f} kg CO2")

    # Optionally, plot data or additional visualizations
    st.bar_chart({'Emissions (kg CO2)': [emissions]})

if __name__ == "__main__":
    main()
