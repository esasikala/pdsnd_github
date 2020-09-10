import time
import datetime
import pandas as pd
import numpy as np
import os

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = [*CITY_DATA]

def on_press(key):
    print('{0} pressed'.format(key))

def on_release(key):
    print('{0} release'.format(key))
    if key == Key.esc:
        # Stop listener
        return False

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    days =  ['all', 'monday','tuesday','wednesday','thursday','friday','saturday','sunday']

    correct_user_input = 'n'
    city = input("Enter city name: " + "\n")

    while correct_user_input == 'n':
        if city.lower() in cities:
            correct_user_input = 'y'
        else:
            city = input("You entered an invalid city name. Enter city name: " + "\n")

    # TO DO: get user input for month (all, january, february, ... , june)
    correct_user_input = 'n'
    month = input("Enter month name [e.g. february] or 'all' for all months: " + "\n")

    while correct_user_input == 'n':
        if month.lower() in months:
            correct_user_input = 'y'
        else:
            month = input("You entered an invalid month. Enter month name [e.g. february] or 'all' for all months: " + "\n")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter day of week [e.g. monday] or 'all' for all days: " + "\n")
    correct_user_input = 'n'

    while correct_user_input == 'n':
        if day.lower() in days:
            correct_user_input = 'y'
        else:
            day = input("You entered an invalid day of the week. Enter day of the week [e.g. monday] or 'all' for all days: " + "\n")

    print('-'*40)
    city = city.lower()
    month = month.lower()

    return(city, month, day)


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['start_month'] = pd.to_datetime(df['Start Time']).dt.strftime('%B')
    df['start_day'] = pd.to_datetime(df['Start Time']).dt.strftime('%A')
    #df['end_month'] = pd.to_datetime(df['End Time']).dt.strftime('%B')
    #df['end_day'] = pd.to_datetime(df['End Time']).dt.strftime('%A')

    #print(city_df.dtypes)
    if month != 'all' and day != 'all':
        is_month_date = ( df['start_month'] == month.title() ) &  (df['start_day'] == day.title() )
        df = df[is_month_date]

    elif month != 'all' and day == 'all':
        is_month_date = ( df['start_month'] == month.title() )
        df = df[is_month_date]
    elif month == 'all' and day != 'all'    :
        is_month_date = (df['start_day'] == day.title())
        df = df[is_month_date]

    sample_data = input('\nDo you want to view sample data? Enter yes or no. \n')

    while sample_data != 'yes' and sample_data != 'no':
        sample_data = input('\nInvalid entry. Enter yes or no. \n')

    if sample_data == 'yes':
        row_num = len(df.index)

        while True:
            try:
                row_cnt = int(input('\nEnter number of lines to view at one time. \n'))
            except ValueError:
                print('\nInvalid entry. Enter an integer.')
                continue
            else:
                if row_cnt > row_num:
                    print('\nInvalid entry. You entered a number greater than rows available.')
                    continue
                else:
                    break

        row_start = 0
        row_end = row_start + row_cnt

    while sample_data == 'yes' and row_end <= row_num:
        os.system("cls")
        new_df = pd.DataFrame(df[row_start:row_end])
        print(new_df)
        print('-'*40)
        is_continue = input("Press 'c' to continue or 'q' to quit. " + "\n")

        while is_continue != 'q' and is_continue != 'c':
            is_continue = input("Invalid entry. Press 'c' to continue or 'q' to quit. " + "\n")

        if is_continue == 'q':
            print("you chose to quit viewing sample data.")
            row_end = row_num + 1
            sample_data == 'no'
            break
        else:
            row_start += row_cnt
            row_end += row_cnt
            if row_end > row_num and row_start < row_num:
                row_end -= row_end - row_num
            elif row_end > row_num:
                print('you have reached the end of data')
                sample_data == 'no'
                break

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('Most common month: ', df['start_month'].mode().iloc[0])

    # TO DO: display the most common day of week
    print('Most common day of week: ', df['start_day'].mode().iloc[0])

    # TO DO: display the most common start hour
    df['start_hour'] = pd.to_datetime(df['Start Time']).dt.strftime('%H')
    print('Most common start hour [ 24 hour format]: ', df['start_hour'].mode().iloc[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('Most commonly used start station: ', df['Start Station'].mode().iloc[0])

    # TO DO: display most commonly used end station
    print('Most commonly used End station: ', df['End Station'].mode().iloc[0])

    # TO DO: display most frequent combination of start station and end station trip
    df['start_end_station'] = df['Start Station'] + " " + df['End Station']
    print('Most frequent combination of start and end station trip: ', df['start_end_station'].mode().iloc[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time: ', df['Trip Duration'].sum() )

    # TO DO: display mean travel time
    print('Mean travel time: ', df['Trip Duration'].mean() )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if 'Gender' not in df:
        #df = df.reindex(columns = np.append( df.columns.values, ['Gender'])
        df['Gender'] = None

    if 'User Type' not in df:
        df['User Type'] = None

    df['Gender'].fillna('No Gender available', inplace = True)
    df['User Type'].fillna('No User Type available', inplace = True)

    # TO DO: Display counts of user types
    #print(df[['User Type']].count())
    print(df.groupby('User Type').agg({'User Type': ['count']}))

    # TO DO: Display counts of gender
    #print(df.groupby(['Gender']).count())
    print(df.groupby('Gender').agg({'Gender': ['count']}))

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df:
        print('\nBirth year values are not available.\n')
    else:
        df['Birth Year_der'] = pd.to_datetime(df['Birth Year'])
        print('\n')
        print("Earliest year of birth: ", int( df['Birth Year'].min() ))
        print("Most recent year of birth: ", int( df['Birth Year'].max() ))
        print("Most common year of birth: ", int( df['Birth Year'].mode().iloc[0] ))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
