"""
    Verison: 1.0
    Date: 03.07.2019
"""

import time
import datetime
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    
    check = False
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while check != True:
        
        city = input('\nPlease enter the city name you want to check the data for.\n')
        
        if city.lower() in ['washington', 'new york city', 'chicago']:
            print('You selected the city: ' + city)
            check = True
        else:
            print('The city name was not correct.')
    
        
    check = False
    # get user input for month (all, january, february, ... , june)
    while check != True:

        month = input('\nPlease enter the month you want to check the data for.\n')
        
        if month.lower() in ['all','january', 'february', 'march', 'april', 'may', 'june',
                             'july', 'august', 'september', 'october', 'november', 'december']:
            print('You selected the month: ' + month)
            check = True
        else:
            print('The month was not correct.')
            

    check = False
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while check != True:

        day = input('\nPlease enter the day you want to check the data for.\n')
        
        if day.lower() in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                             'saturday', 'sunday']:
            print('You selected the weekday: ' + day)
            check = True
        else:
            print('The month was not correct.')


    print('-'*40)
    return city, month, day


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
    # get the respective filename
    file = "{}.csv".format(city)
    
    # read in the current data
    df = pd.read_csv(file)
    
    df = add_hour(df)
    df = add_weekday(df)
    df = add_month(df)
    df = add_start_end_station_combination(df)
    
    df = filter_dataframe(df, month, day)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df.month.value_counts().sort_values(ascending=False)
    print("{} is the most common month with a count of {}".format(most_common_month.index[0], most_common_month[0]))


    # display the most common day of week
    most_common_day = df.day_of_week.value_counts().sort_values(ascending=False)
    print("{} is the most common day with a count of {}".format(most_common_day.index[0], most_common_day[0]))


    # display the most common start hour
    most_common_hour = df.hour.value_counts().sort_values(ascending=False)
    print("{} is the most common day with a count of {}".format(most_common_hour.index[0], most_common_hour[0]))   

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df['Start Station'].value_counts().sort_values(ascending=False)
    print("{} is the most common start station with a count of {}".format(most_common_start.index[0], most_common_start[0]))  

    # display most commonly used end 
    most_common_end = df['End Station'].value_counts().sort_values(ascending=False)
    print("{} is the most common end station with a count of {}".format(most_common_end.index[0], most_common_end[0]))  

    # display most frequent combination of start station and end station trip
    most_common_combo = df['start_end_combination'].value_counts().sort_values(ascending=False)
    print("{} is the most common start-end station combination with a count of {}".format(most_common_combo.index[0], most_common_combo[0]))  

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = str(datetime.timedelta(seconds=int(df['Trip Duration'].sum())))
    print('The total travel time is {}'.format(total_travel_time))

    # display mean travel time
    avg_travel_time = str(datetime.timedelta(seconds=int(df['Trip Duration'].mean())))
    print('The total travel time is {}'.format(avg_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nWe have following user types and its count:\n')
    print(user_types)

    # Display counts of gender
    if 'gender' in df:
        gender = df['Gender'].value_counts()
        print('\nWe have following gender distribution:\n')
        print(gender)
    else:
        print('We do not have information about the gender.')

    # Display earliest, most recent, and most common year of birth
    if 'birth year' in df:
        min_birth_year = df['Birth Year'].min()
        max_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].value_counts().sort_values(ascending=False)
        print('\nThe earliest birth year is: {}\n'.format(min_birth_year))
        print('\nThe most recent birth year is: {}\n'.format(max_birth_year))
        print('\nThe most common birth year is: {}\n'.format(most_common_birth_year.index[0]))
    else:
        print('We do not have information about the birth year.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def add_weekday(df):
    """
    @param: DataFrame which contains timestamps
    @returns: DataFrame which contains additional column with day of week
    """    
    df['dates'] = pd.to_datetime(df['Start Time'])
    df['day_of_week'] = df['dates'].dt.day_name().str.lower()
    
    return df
    
    
def add_month(df):
    """
    @param: DataFrame which contains timestamps
    @returns: DataFrame which contains additional column with month
    """    
    df['dates'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['dates'].dt.month_name().str.lower()
    
    return df
    

def add_hour(df):
    """
    @param: DataFrame which contains timestamps
    @returns: DataFrame which contains additional column with hour only   
    """
    df['dates'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['dates'].dt.hour
    
    return df
 
    
def add_start_end_station_combination(df):
    """
    @param: DataFrame which contains start and end station
    @returns: DataFrame which contains additional column with combined stations
    """
    df['start_end_combination'] = list(zip(df['Start Station'], df['End Station']))
    
    return df


def filter_dataframe(df, month, day):
    """
    @params: DataFrame, Month (string), day (String)
    @returns: filtered dataframe by time if not selected all
    """
    
    if month != 'all':
        df = df[df.month == month]
    
    if day != 'all':
        df = df[df.day_of_week == day]
        
    return df

def display_data(df):
    """

    :param df: DataFrame containing the filtered data
    :return: -
    """

    i = 0
    check = False
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while check != True:

        if i == 0:
            check = input('\nDo you want to see top 5 rows of the data.\n')
        else:
            check = input('\nDo you want to see 5 more?\n')

        if check.lower() == 'yes':
            print(df.iloc[i*5:(i+1)*5])
            i = i + 1
        elif check.lower() == 'no':
            check = True
        else:
            print('Please type yes or no.')
        


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
