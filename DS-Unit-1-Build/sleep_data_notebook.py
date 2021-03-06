# -*- coding: utf-8 -*-
"""Sleep Data notebook.ipynb

Automatically generated by Colaboratory.

Original file is located at
https://colab.research.google.com/drive/1bG0QlMhdhw_3MY-sey6ncWhkpGedILzx
"""

import pandas as pd
import numpy as np
from datetime import datetime
from scipy import stats
from scipy.stats.distributions import chi2
import matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from IPython.display import IFrame

sc_sleep_data = pd.read_csv('/content/sleepdata.csv', delimiter=';')
sc_sleep_data.head(419)

sc_sleep_data.isnull().any()

sc_sleep_data.isnull().sum()

# Dropping the 'Heart rate' column

sc_sleep_data = sc_sleep_data.drop(columns=['Heart rate',
                                            'Wake up',
                                            'Sleep Notes'])
sc_sleep_data.head()

# converting percentages to floats

sc_sleep_data['Sleep quality'] = sc_sleep_data['Sleep quality'].str.rstrip('%').astype('float') / 100
sc_sleep_data['Sleep quality'].head()

sc_sleep_data.info()

# Looking to create a column of days
sc_sleep_data['Start'].describe()

# # Test to find day of the week
# copy_1_date = pd.Timestamp(sc_sleep_data['Start'][0])

# copy_1_date.dayofweek

sc_sleep_data['Weekday'] = pd.to_datetime(sc_sleep_data['End'],
                                          infer_datetime_format=True)

sc_sleep_data['Weekday'] = sc_sleep_data['Weekday'].apply(lambda time: time.dayofweek)
sc_sleep_data.head()

# some_column = np.array(sc_sleep_data['Time in bed'], dtype=np.datetime64)
# print(some_column)

sc_sleep_data['Start'] = np.array(sc_sleep_data['Start'],
                                  dtype=np.datetime64)

sc_sleep_data['End'] = np.array(sc_sleep_data['End'],
                                dtype=np.datetime64)
sc_sleep_data.info()


# for i in sc_sleep_data['Time in bed']:
#   sc_sleep_data['Time in bed'] = datetime.strptime(i, '%H:%M').time()
# sc_sleep_data['Time in bed']

# Formatting 'Time in bed' into date time format with a today's time stamp
# will then remove date, and leave hours and min

sc_sleep_data['Time in bed'] = pd.to_datetime(sc_sleep_data['Time in bed'],
                                              infer_datetime_format=True)

sc_sleep_data['Time in bed'] = np.array(sc_sleep_data['Time in bed'],
                                        dtype=np.datetime64)
sc_sleep_data['Time in bed'].head()

# It took so long to finally acheive this single code of line.  But i finally
# got the column 'Time in bed' into time format

sc_sleep_data['Time in bed'] = sc_sleep_data['Time in bed'].dt.time
sc_sleep_data

# Creating a column containg the dates, and then creating a column cointaning
# time to bed, and time to rise

sc_sleep_data['Date'] = sc_sleep_data['Start'].dt.date
sc_sleep_data['Date']

# replacing ints in 'Weekday' column with days of the week using a dictionary

d = {0: 'Monday',
     1: 'Tuesday',
     2: 'Wednesday',
     3: 'Thursday',
     4: 'Friday',
     5: 'Saturday',
     6: 'Sunday'}

sc_sleep_data['Weekday categories'] = sc_sleep_data['Weekday'].map(d)
sc_sleep_data.head()

# we need categorical variable to do a Chi**2 test


cut_points = [0, .30, .60, 1]

label_names = ['0% - 30%',
               '31% - 60%',
               '>60%']

sc_sleep_data['Sleep Quality Categories'] = pd.cut(sc_sleep_data['Sleep quality'],
                                                   cut_points,
                                                   labels=label_names)

# New Dataframe excluding the 'Wake up' and 'Sleep Notes' column

new_df = sc_sleep_data[['Start',
                        'End',
                        'Sleep quality',
                        'Time in bed',
                       'Activity (steps)',
                        'Weekday',
                        'Date',
                        'Sleep Quality Categories',
                        'Weekday categories']]

new_df.head(419)

new_df['Start'] = new_df['Start'].dt.time
new_df['End'] = new_df['End'].dt.time

new_df['Date'] = pd.DataFrame(new_df['Date'].drop_duplicates(keep='first'))
new_df['Date']

# looking at the element type in the column 'Date'

type(new_df['Date'][0])

# Changing 'Time in bed' column values to floats

# print((float(new_df['Time in bed'][0].minute)/60) + (float(new_df['Time in bed'][0].hour)))

# running a for loop to change the hour and minute values in the 'Time in bed'
# column into float types for analysis

df = []
for i in new_df['Time in bed']:
    df.append(round((float(i.minute)/60) + (float(i.hour)), 2))

new_df['Time in bed'] = np.array(df)
new_df['Time in bed']

# print(new_df.info())
# print(new_df.isnull().any())
# print(new_df.describe())
new_df['Weekday'].value_counts()

# Creating a contingency table of observed values from
# 'Weekday' and 'Sleep Quality Categories' columns

new_df['Weekday categories'].value_counts()

observed = pd.crosstab(new_df['Weekday categories'],
                       new_df['Sleep Quality Categories'])

observed

# Null Hypothesis: There will be no difference in quality of sleep based on
# day of the week
# Alt Hypothesis:  There is a difference in quality of sleep based on day of the
# week.

# A p-value result of  <.05 allows us to reject the Null Hypothesis; implying
# that there is independence, and therefore the quality of sleep is affected by
# day of the week

chi_squared, p_value, dof, expected = stats.chi2_contingency(observed)

print(f'Chi-Squared: {chi_squared}', '\n')
print(f'P-value: {p_value}', '\n')
print(f'Degrees of Freedom: {dof}', '\n')
print('Expected: \n', np.array(expected))


print('P-value from chi^2 statistic:', chi2.sf(chi_squared, 12))

# Taking counts for plotting

Friday = observed.iloc[0][0:].values
Monday = observed.iloc[1][0:].values
Saturday = observed.iloc[2][0:].values
Sunday = observed.iloc[3][0:].values
Thursday = observed.iloc[4][0:].values
Tuesday = observed.iloc[5][0:].values
Wednesday = observed.iloc[5][0:].values


labels = ['0% - 30%', '31% - 60%', '>61%']
Friday = observed.iloc[0][0:].values
Monday = observed.iloc[1][0:].values
Saturday = observed.iloc[2][0:].values
Sunday = observed.iloc[3][0:].values
Thursday = observed.iloc[4][0:].values
Tuesday = observed.iloc[5][0:].values
Wednesday = observed.iloc[5][0:].values

x = np.arange(len(labels))  # the label locations
width = 0.08  # the width of the bars

fig, ax = plt.subplots(figsize=(13, 5))
rects1 = ax.bar(x - width*3.002,
                Monday,
                .1,
                label='Monday',
                color='black',
                alpha=.8)
rects2 = ax.bar(x - width*1.7,
                Tuesday,
                .1,
                label='Tuesday',
                color='black',
                alpha=.5)
rects3 = ax.bar(x - width*.39,
                Wednesday,
                .1,
                label='Wednesday',
                color='black',
                alpha=.2)
rects4 = ax.bar(x + width*.96,
                Thursday,
                .1,
                label='Thursday',
                color='black',
                alpha=.1)
rects5 = ax.bar(x + width*2.31,
                Friday,
                .1,
                label='Friday',
                color='red',
                alpha=.1)
rects6 = ax.bar(x + width*3.665,
                Saturday,
                .1,
                label='Saturday',
                color='red',
                alpha=.3)
rects7 = ax.bar(x + width*5,
                Sunday,
                .1,
                label='Sunday',
                color='red',
                alpha=.6)


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Sleep Quality Affected by Day of the Week',
             size=25,
             y=1.05)

ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
ax.set_ylim(0, 55)


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center',
                    va='bottom',
                    size=12)


autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
autolabel(rects4)
autolabel(rects5)
autolabel(rects6)
autolabel(rects7)


# consider doing a dist plot or scatter plot with the given parameters as anext
# step also, look into a violoin plot; plotly for the following

fig.tight_layout()
plt.xlabel('Quality of Sleep', size=15)
plt.ylabel('Counts', size=15)
plt.show()

data = px.data.gapminder()

# new_df = px.data.data(new_df)
sleep_quality_hist = px.histogram(new_df,
                                  x='Sleep quality',
                                  #  histnorm='percent',
                                  histnorm='probability density',
                                  #  nbins=0,
                                  #  range_x=(0, .3)),
                                  # marginal='rug',
                                  nbins=47,
                                  title='Sleep Quality Distribtion',
                                  labels={'Sleep quality': 'Sleep Quality Distribution'})

# Bar plot: average time asleep,


avg_tbed = go.Figure()

avg_tbed.add_trace(go.Box(y=new_df['Time in bed'],
                          name='Time Asleep',
                          marker_color='royalblue',
                          boxmean='sd',
                          boxpoints='all',  # represent mean and STD
                          notched=True,), )
avg_tbed.update_layout(title_text='Time Asleep (h) Statistics')


timbd_v_qual = px.bar(new_df,
                      x='Sleep quality',
                      y='Time in bed',
                      hover_data=['Sleep quality'],
                      color='Sleep quality',
                      labels={'Time in bed': 'Time Asleep (h)',
                              'Sleep quality': 'Quality of Sleep'},
                      height=400,
                      title='Sample Distribution: Sleep Quality and Time Asleep as it Relates to Activity')

act_v_qual = px.bar(new_df,
                    x='Sleep quality',
                    y='Activity (steps)',
                    hover_data=['Sleep quality', 'Time in bed'],
                    color='Time in bed',
                    labels={'Sleep quality': 'Quality of Sleep Distribution',
                            'Activity (steps)': 'Activity (steps)'},
                    height=400,
                    title='Sample Distribution: Sleep Quality as it Relates to Time Asleep')


# data = px.data.ne
qual_v_wkdy = px.box(new_df,
                     x='Weekday categories',
                     y='Sleep quality',
                     #  range_y=(0, .4),
                     points='suspectedoutliers',
                     category_orders={'Weekday categories':
                                      ['Monday', 'Tuesday', 'Wednesday',
                                       'Thursday', 'Friday', 'Saturday',
                                       'Sunday']},
                     notched=True,
                     title='Sleep Quality Throughout the Week',
                     labels={'Weekday categories': 'Day of the Week'})


sleep_quality_hist.show()
avg_tbed.show()
qual_v_wkdy.show()
timbd_v_qual.show()
act_v_qual.show()


IFrame(src="https://dash-simple-apps.plotly.host/dash-boxplot/code",
       width="100%",
       height=500,
       frameBorder="0")

# data = px.data.ne
qual_v_wkdy = px.box(new_df,
                     x='Weekday categories',
                     y='Sleep quality',
                     #  range_y=(0, .4),
                     points='suspectedoutliers',
                     category_orders={'Weekday categories':
                                      ['Monday', 'Tuesday', 'Wednesday',
                                       'Thursday', 'Friday', 'Saturday',
                                       'Sunday']},
                     notched=True)
qual_v_wkdy.show()

new_df.head()

new_df.head()

new_df['Start by hour'] = pd.to_datetime(sc_sleep_data['Start'],
                                         infer_datetime_format=True)

new_df['Start by hour'] = np.array(new_df['Start by hour'],
                                   dtype=np.datetime64)

new_df['Start by hour'] = new_df['Start by hour'].dt.hour

new_df['End by hour'] = pd.to_datetime(sc_sleep_data['End'],
                                       infer_datetime_format=True)

new_df['End by hour'] = np.array(new_df['End by hour'],
                                 dtype=np.datetime64)

new_df['End by hour'] = new_df['End by hour'].dt.hour

new_df['Start by week'] = pd.to_datetime(sc_sleep_data['Start'],
                                         infer_datetime_format=True)

new_df['Start by week'] = np.array(new_df['Start by week'],
                                   dtype=np.datetime64)

new_df['Start by week'] = new_df['Start by week'].dt.week

new_df.head()

new_df['Start by hour'].value_counts()

# Scatter plot of the time i go to sleep/wake


# import plotly.express as px
# # iris = px.data.new_df() # iris is a pandas DataFrame
# fig = px.scatter(new_df, x='Start by hour', y='Sleep quality')
# fig.show()


tbed_v_bedt = px.scatter(new_df,
                         x='Start by hour',
                         y='Time in bed',
                         color='Sleep quality',
                         hover_data=['Sleep quality'],
                         size='Sleep quality',
                         title='Sleep Quality Affected by Bed Time',
                         labels={'Start by hour': 'Bed Time',
                                 'Time in bed': 'Time Asleep (hrs)'},)

tbed_v_wkup = px.scatter(new_df,
                         x='End by hour',
                         y='Time in bed',
                         color='Sleep quality',
                         hover_data=['Sleep quality'],
                         size='Sleep quality',
                         title='Sleep Quality Affected by Wake-up Time',
                         labels={'End by hour': 'Wake-up Time',
                                 'Time in bed': 'Time Asleep (hrs)'})


wkup_v_bedt = px.scatter(new_df,
                         x='Start by hour',
                         y='End by hour',
                         color='Sleep quality',
                         hover_data=['Sleep quality', 'Time in bed'],
                         range_x=(-1, 10),
                         range_y=(0, 15),
                         size='Sleep quality',
                         title='Early to Bed Late to Rise = Better Sleep',
                         labels={'End by hour': 'Wake-up Time',
                                 'Start by hour': 'Bed Time'})

tbed_v_bedt.show()
tbed_v_wkup.show()
wkup_v_bedt.show()

weather_df = pd.read_csv('/content/1950768.csv')
weather_df

weather_df = weather_df.dropna()
weather_df

weather_df = pd.DataFrame(weather_df.drop(columns='STATION'))
weather_df

weather_df['DATE'] = weather_df['DATE'].drop_duplicates(keep='first')
weather_df.shape

weather_df = weather_df.dropna()
print(weather_df.shape)
weather_df.head(3)

weather_df.columns = ['Date', 'AvgWnd', 'TAvg']

weather_df['Date'] = weather_df['Date'].astype(str)

print(weather_df.head(3))

weather_df.shape

new_df['Date'] = new_df['Date'].astype(str)

left = new_df
right = weather_df

concat_df = pd.merge(new_df,
                     weather_df,
                     on='Date',
                     how='inner')
concat_df

concat_df['Sleep Quality Categories'].isna().sum()

concat_df = concat_df.dropna()
print(concat_df.shape)
print(concat_df.isnull().any())
concat_df.head(3)

# concat_df['Date'] = concat_df['Date'].drop_duplicates(keep='first')
# concat_df['Date'] = concat_df['Date'].dropna()
# print(concat_df.shape)
# concat_df.head(4)


slp_qual_v_dt = px.scatter(concat_df,
                           x='Date',
                           y='TAvg',
                           color='Sleep quality',
                           size='Time in bed',
                           hover_data=['Sleep quality'],
                           labels={'Date': 'Time of Year',
                                   'TAvg': 'Average T (F)'},
                           title='Sleep Affected by Temperature')

# comp_grph = px.scatter(concat_df,
#                        x='Date',
#                        y='TAvg',
#                        color='Sleep quality',
#                        size='Time in bed',
#                        hover_data=['Sleep quality'],
#                        labels={'Date': 'Time of Year',
#                                 'TAvg': 'Average T (F)'})

time_v_temp = px.scatter(concat_df,
                         x='Date',
                         y='TAvg',
                         color='TAvg',
                         size='TAvg',
                         hover_data=['Sleep quality'],
                         labels={'Date': 'Time of Year',
                                 'TAvg': 'Average T (F)'},
                         title='Temperature Through the Year')

slp_qual_v_wnd = px.scatter(concat_df,
                            x='Date',
                            y='AvgWnd',
                            color='Sleep quality',
                            size='Time in bed',
                            hover_data=['Sleep quality'],
                            labels={'Date': 'Time of Year',
                                    'AvgWnd': 'Average Wind Speed (m/s)'},
                            title='Sleep Affected by Wind Speeds')

time_v_wnd = px.scatter(concat_df,
                        x='Date',
                        y='AvgWnd',
                        color='AvgWnd',
                        size='AvgWnd',
                        hover_data=['Sleep quality'],
                        labels={'Date': 'Time of Year',
                                'AvgWnd': 'Average Wind Speed (m/s)'},
                        title='Wind Speeds Through the Year')

slp_qual_v_time_in_bed = px.scatter(concat_df,
                                    x='Time in bed',
                                    y='Sleep quality',
                                    color='Sleep quality',
                                    size='Time in bed',
                                    hover_data=['Sleep quality'],
                                    labels={'Time in bed': 'Time Asleep (h)'},
                                    title='Sleep Quality Affected by Time Asleep')

# comp_grph.show()
time_v_temp.show()
time_v_wnd.show()
slp_qual_v_wnd.show()
slp_qual_v_dt.show()
slp_qual_v_time_in_bed.show()
