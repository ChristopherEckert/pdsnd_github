import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#global variable definitions
Cities = ['chicago', 'new york city', 'washington']
Months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
Days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which city would you like to see data for? (Chicago, New York City , or Washington) \n> ')
        city = city.lower()
        if city in Cities:
            break
        else:
            print('I am sorry, that is not a valid input for which we have data. Please make a valid entry.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month would you like data for? (January, February, March, April, May, June, or ALL) \n> ')
        month = month.lower()
        if month in Months:
            break
        else:
            print('I am sorry, that is not a valid input for which we have data. Please make a valid entry.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('What day of the week would you like data for? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or ALL) \n> ')
        day = day.lower()
        if day in Days:
            break
        else:
            print('I am sorry, that is not a valid input for which we have data. Please make a valid entry.')

    print('\nYou chose:  City - ', city, ', Month - ', month, ', Day - ', day)


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

    # Practice problem 3 used as reference

    start_time = time.time()
    # load data file to dataframe
    df = pd.read_csv(CITY_DATA[city])
    print('\nFile', CITY_DATA[city], 'Read!')

    # convert start time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], infer_datetime_format=True)

    # extract month and day of week to new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    #filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = Months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    print('\nLoading the data took %s seconds.' % f'{(time.time() - start_time):.2f}')
    print('-'*40)

    return df


def time_stats(df):
    """
    Displays statistics on the most common times of travel.
    """

    print('\nCalculating The Most common Times of Bike Usage...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most common Month is :', Months[common_month-1])

    # display the most common day of week
    common_week_day = df['day_of_week'].mode()[0]
#    print('\n', common_week_day, '\n')
    print('Most common Day is :', common_week_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print('Most common Start Hour is :', common_start_hour)


    print('\nThis took %s seconds.' % f'{(time.time() - start_time):.2f}')
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_stat = df['Start Station'].mode()[0]
    count_start = df[df["Start Station"] == most_common_start_stat].count()[0]
    print('Most Commonly used Start Station is :', most_common_start_stat, ' :: with ', count_start, 'trip starts.')
 
    # display most commonly used end station
    most_common_end_stat = df['End Station'].mode()[0]
    count_end = df[df["End Station"] == most_common_end_stat].count()[0]
    print('Most Commonly used End Station is :', most_common_end_stat, ' :: with ', count_end, 'trip ends.')

    # display most common combination of start station and end station trip
    df['Route'] = df['End Station'] + ' to ' + df['Start Station']
    common_route = df['Route'].mode()[0]
    count_route = df[df['Route'] == common_route].count()[0]
    print('Most common Route is : ', common_route, ' :: with ', count_route, 'trips.')

    print('\nThis took %s seconds.' % f'{(time.time() - start_time):.2f}')
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total Travel Time : ', f' {total_time/60/60:.2f}',  'hours.')

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Mean Travel Time : ', f' {mean_time/60:.2f}', 'minutes.').__format__

    print('\nThis took %s seconds.' % f'{(time.time() - start_time):.2f}')
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_frame()
    print(user_types)

    # Display counts of gender
    while True:
        if 'Gender' in df.columns or 'Birth Year' in df.columns:
            gender_types = df['Gender'].value_counts().to_frame()
            print('\n', gender_types)
            # Display earliest, most recent, and most common year of birth
            birth_year = df['Birth Year']
            # the most common birth year
            common_year = birth_year.mode()[0]
            print('\nThe most common birth year is:', f'{common_year:.0f}')
            # the most recent birth year
            most_recent = birth_year.max()
            print('The most recent birth year is:', f'{most_recent:.0f}')
            # the most earliest birth year
            earliest_year = birth_year.min()
            print('The earliest birth year is:', f'{earliest_year:.0f}')
            break
        else:
            print('User gender and age data is not available for this location.')
            break

    print('\nThis took %s seconds.' % f'{(time.time() - start_time):.2f}')
    print('-'*40)


def display_raw_data(df):

    """
    Displays raw data var_step rows at a time until the user chooses to stop, or end of file is reached.
    """
    var_step = 10
    start_time = time.time()
#    df = pd.read_csv(CITY_DATA[city])
    print('\nRaw data will be displayed {} lines at a time.\n'.format(var_step))
    
    step = 0
    print(df.iloc[step:step + var_step])
    step += var_step
    max_step = df['Start Time'].count()
    while True:
         if step >= max_step:
             break
         else:
            more_data = input(
                'Would you like to see {} more rows of data? Enter \033[4mY\033[0mes or \033[4mN\033[0mo.\n'.format(var_step))[:1].lower()
            match more_data:
                case 'y':
                    print(df.iloc[step:step + var_step])
                    step += var_step
                case 'n':
                    print('\nNo further data will be displayed.')
                    break
                case other:
                    print('Incorrect input, please try again.')
        
    print('\nYou spent %s seconds reviewing this data.' % f'{(time.time() - start_time):.2f}')
    print('-'*40)

def main():
    restart_flag = True
    while restart_flag:
        city, month, day = get_filters()
        # defined a default for testing, comment above 
#        city = 'washington'
#        month = 'all'
#        day = 'all'
        df = load_data(city, month, day)
        
        more_data_flag = True
        while more_data_flag:
            print('\nWhat type of data would you like to see? (enter the corresponding number:) \n> ')
            selection = input('1. Time statistics\n2. Station statistics\n3. Trip duration statistics\n4. User statistics\n5. raw data\n')

            # system calls function to run selected data
            match selection:
                case '1':
                    time_stats(df)
                case '2':
                    station_stats(df)
                case '3':
                    trip_duration_stats(df)
                case '4':
                    user_stats(df)
                case '5':
                    display_raw_data(df)
                case other:
                    print('\nThat was an invalid selection.')    
            
            # ask user if they want to choose another data type
            while more_data_flag:
                more_data = input('\nWould you like to see additional data? Enter \033[4mY\033[0mes or \033[4mN\033[0mo.\n')[:1].lower()
                match more_data:
                    case 'y':
                        break
                    case 'n':
                        more_data_flag = False
                    case other:
                        print('Incorrect input, please try again.')
                        
        # see if the user wants to start over from the beginning
        while restart_flag:
            restart = input('\nWould you like to restart with new selections? Enter \033[4mY\033[0mes or \033[4mN\033[0mo.\n')[:1].lower()
            match restart:
                case 'y':
                    break
                case 'n':
                    print('\nThank you for using our software! Have a great day!!!\n')
                    restart_flag = False
                case other:
                    print('Incorrect input, please try again.')

if __name__ == "__main__":
	main()
