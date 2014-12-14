import pandas as pd
import pandasql
from ggplot import *
from datetime import datetime

def plot_weather_data(turnstile_weather):  
    df = turnstile_weather[['DATEn', 'ENTRIESn_hourly', 'rain']]
    df.is_copy = False

    # get the weekday as a string
    f = lambda x: datetime.strptime(x, "%Y-%m-%d").strftime('%A') 

    df['weekday'] = df['DATEn'].apply(f)


    plot = ggplot(aes(x='ENTRIESn_hourly', color='rain'), data = df) \
            + geom_density() \
            + xlim(0,5000) \
            + facet_wrap('weekday')
            

    return plot


if __name__ == "__main__":
    
    input_filename = "turnstile_data_master_with_weather.csv"
    image = "plot.png"

    turnstile_weather = pd.read_csv(input_filename)
    turnstile_weather['datetime'] = turnstile_weather['DATEn'] + ' ' + turnstile_weather['TIMEn']
    gg =  plot_weather_data(turnstile_weather)
    ggsave(image, gg)
