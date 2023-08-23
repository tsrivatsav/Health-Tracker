import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

### Read in the data ###

## Data is manually entered into excel spreadsheet with columns of:
## Date, Calories in, Distance Ran (miles), Time Ran (mins), Bench 5RM (lbs)
## Squat 5RM (lbs), Pull ups (max set), Daily Meditation, Body Weight (lbs)
df = pd.read_excel('Health Tracker.xlsx', parse_dates=['Date'])
# print("a")
# print(df)

### Preprocessing ###

## Firstly let's impute all missing values appropriately
## In this case if a value is missing, it's probably because I had a bad day 
## The values below are my guesses for a typical bad day
## Also let's assume that if I filled in distance ran then I also filled in time ran

df['Calories in'] = df['Calories in'].fillna(2500)
df['Distance Ran (miles)'] = df['Distance Ran (miles)'].fillna(0)
df['Time Ran (mins)'] = df['Time Ran (mins)'].fillna(0)
df['Bench 5RM (lbs)'] = df['Bench 5RM (lbs)'].fillna(0)
df['Squat 5RM (lbs)'] = df['Squat 5RM (lbs)'].fillna(0)
df['Pull ups (max set)'] = df['Pull ups (max set)'].fillna(0)
df['Daily Meditation'] = df['Daily Meditation'].fillna(0)
## assume that body weight doesnt change from day to day
df['Body Weight (lbs)'] = df['Body Weight (lbs)'].fillna(method='ffill')

# print("b")
# print(df)

### Diet/Weight Gain ###

## let's visualize calories in
# df.plot(x='Date', y='Calories in', kind='line')
# plt.show()
## let's normalize calories in to between -1 and 1 so that we can compare it with other metrics later
df['Norm Calories in'] = (df['Calories in'] - df['Calories in'].mean()) / (df['Calories in'].max() - df['Calories in'].min())

## Let's visualize body weight
# df.plot(x='Date', y='Body Weight (lbs)', kind='line')
# plt.show()
## let's normalize body weight
df['Norm Body Weight (lbs)'] = (df['Body Weight (lbs)'] - df['Body Weight (lbs)'].mean()) / (df['Body Weight (lbs)'].max() - df['Body Weight (lbs)'].min())

## There's 3500 calories in a lb -- so we can estimate my TDEE (Total Daily Energy Expenditure) based on calories in and body weight changes
## Any repeated miscalculations for calories in will be accounted for by the TDEE calculation 
## If I'm eating less in reality than I think, then the TDEE value that I use will also be lesser than its true value and so it'll balance out

## let's calculate the average calories in per day
daily_avg_cals = df['Calories in'].mean()
# print("c")
# print(daily_avg_cals)

## let's calculate the average change in body weight per day
df['Change in body weight from previous day'] = df['Body Weight (lbs)'] - df['Body Weight (lbs)'].shift(1)
# print("d")
# print(df['Change in body weight from previous day'])
daily_avg_weight_change = df['Change in body weight from previous day'].mean()
# print("e")
# print(daily_avg_weight_change)

## Finally, let's calculate the TDEE
## TDEE = Avg Calories in per day - (Avg Change in body weight per day)*3500
tdee = daily_avg_cals - daily_avg_weight_change * 3500
# print("f")
# My TDEE is 3408 based on this calculation
# print(tdee)

### Running ###

## let's visualize distance ran
# df.plot(x='Date', y='Distance Ran (miles)', kind='line')
# plt.show()
## let's normalize distance ran
df['Norm Distance Ran (miles)'] = (df['Distance Ran (miles)'] - df['Distance Ran (miles)'].mean()) / (df['Distance Ran (miles)'].max() - df['Distance Ran (miles)'].min())

## let's visualize time ran
# df.plot(x='Date', y='Time Ran (mins)', kind='line')
# plt.show()
## let's normalize time ran
df['Norm Time Ran (mins)'] = (df['Time Ran (mins)'] - df['Time Ran (mins)'].mean()) / (df['Time Ran (mins)'].max() - df['Time Ran (mins)'].min())

## let's calculate my mile pace by dividing distance ran by time ran
df['Mile Pace (mins/mile)'] = df[df['Time Ran (mins)'] != 0]['Time Ran (mins)'] / df['Distance Ran (miles)']
## and let's impute missing values using ffill
df['Mile Pace (mins/mile)'] = df['Mile Pace (mins/mile)'].fillna(method='ffill')

## let's visualize my mile pace
# df.plot(x='Date', y='Mile Pace (mins/mile)', kind='line')
# plt.show()
## let's normalize my mile pace
df['Norm Mile Pace (mins/mile)'] = (df['Mile Pace (mins/mile)'] - df['Mile Pace (mins/mile)'].mean()) / (df['Mile Pace (mins/mile)'].max() - df['Mile Pace (mins/mile)'].min())

# ### Strength ###

# ## let's visualize Bench 5RM (lbs)
# df.plot(x='Date', y='Bench 5RM (lbs)', kind='line')
# # plt.show()
# ## let's normalize Bench 5RM (lbs)
# df['Norm Bench 5RM (lbs)'] = (df['Bench 5RM (lbs)'] - df['Bench 5RM (lbs)'].mean()) / (df['Bench 5RM (lbs)'].max() - df['Bench 5RM (lbs)'].min())

# ## let's visualize Squat 5RM (lbs)
# df.plot(x='Date', y='Squat 5RM (lbs)', kind='line')
# # plt.show()
# ## let's normalize Squat 5RM (lbs)
# df['Norm Squat 5RM (lbs)'] = (df['Squat 5RM (lbs)'] - df['Squat 5RM (lbs)'].mean()) / (df['Squat 5RM (lbs)'].max() - df['Squat 5RM (lbs)'].min())

# ## let's visualize Pull ups (max set)
# df.plot(x='Date', y='Pull ups (max set)', kind='line')
# # plt.show()
# ## let's normalize Pull ups (max set)
# df['Norm Pull Ups (max set)'] = (df['Pull ups (max set)'] - df['Pull ups (max set)'].mean()) / (df['Pull ups (max set)'].max() - df['Pull ups (max set)'].min())

# ### Meditation ###

# ## let's visualize Daily Meditation
# df.plot(x='Date', y='Daily Meditation', kind='line')
# # plt.show()
# ## let's normalize Daily Meditation
# df['Norm Daily Meditation'] = (df['Daily Meditation'] - df['Daily Meditation'].mean()) / (df['Daily Meditation'].max() - df['Daily Meditation'].min())
