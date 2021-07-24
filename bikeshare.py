import time
import pandas as pd
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

HINT = "Hint: it is enough to write the first couple of characters, and case-insensitive answer is also accepted."

QUESTION_DATA = {
    "city":        {"question": "Please select a city from the following list:", 
                    "values":   ["Chicago", "New York City", "Washington"]},
    "month":       {"question": "Please select a month from the following list:", 
                    "values":   ["All", "January", "February", "March", "April", "May", "June"]},
    "day_of_week": {"question": "Please select a day of week from the following list:", 
                    "values":   ["All", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]},
}


def print_separator():
    """
    Print a separator line
    """
    print('-'*40, "\n")

    
def ask_and_check(question_type):
    """
    Ask user to select an option and check if it is correct
    
    Returns: the selected option
    """
    print(QUESTION_DATA[question_type]["question"])
    print(', '.join(QUESTION_DATA[question_type]["values"]), '\n')
    
    answer = input()
    found_option = [option for option in QUESTION_DATA[question_type]["values"] if option.lower().startswith(answer.lower())]
    while len(found_option) != 1:
        if len(found_option) == 0:
            print("Invlid option, please select one of the followings:")
        elif len(found_option) > 1:
            print("Cannot identify unambigously your choice, there are too many matching items. Please try it again.")

        print(', '.join(QUESTION_DATA[question_type]["values"]), '\n')
        answer = input()
        found_option = [option for option in QUESTION_DATA[question_type]["values"] if option.lower().startswith(answer.lower())]
    
    print_separator()
    return found_option[0]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print(HINT)
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ask_and_check("city")

    # TO DO: get user input for month (all, january, february, ... , june)
    month = ask_and_check("month")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ask_and_check("day_of_week")
    
    print_separator()
    print(f'You selected the followings: city: {city}, month: {month}, day: {day}')
    print_separator()

    return city, month, day


def filter_month(df, month):
    """
    Filter by month if applicable
    Param: df: pandas data frame
    Param: month: string
    
    Returns: the filtered data frame
    """
    df['month'] = df['Start Time'].dt.month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    if month in months:        
        month = months.index(month) + 1
        df = df[df['month'] == month]
    return df


def filter_day(df, day):
    """
    Filter by day if applicable
    Param: df: pandas data frame
    Param: month: string
    
    Returns: the filtered data frame
    """
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")
    if day.lower() != "all":
        df = df[df['day_of_week'] == day.title()]
    return df


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
    df = pd.read_csv(CITY_DATA[city.lower()])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df = filter_month(df, month)
    
    df = filter_day(df, day)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month
    print('Most common month:', df['month'].mode()[0])


    # TO DO: display the most common day of week
    print('Most common day of week:', df['day_of_week'].mode()[0])


    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('Most common start hour:', df['hour'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print_separator()


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('Most commonly used start station: ', df['Start Station'].mode()[0], ", Count: " , df['Start Station'].value_counts().max())


    # TO DO: display most commonly used end station
    print('Most commonly used end station: ', df['End Station'].mode()[0], ", Count: " , df['End Station'].value_counts().max())


    # TO DO: display most frequent combination of start station and end station trip
    df['Start End'] = df['Start Station'] + " --> " + df["End Station"]
    print('Most frequent combination of start station and end station trip: ' ,df['Start End'].mode()[0], ", Count: " , 
          df['Start End'].value_counts().max())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print_separator()


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    
    # TO DO: display total travel time
    trip_sum = df['Trip Duration'].sum()
    print(f'Total travel time: {trip_sum} seconds, that is {str(datetime.timedelta(seconds=trip_sum.item()))}')


    # TO DO: display mean travel time
    trip_mean = df['Trip Duration'].mean()
    print(f'Mean travel time: {trip_mean:.2f} seconds')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print_separator()


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Counts of user types')
    print(df['User Type'].value_counts(), "\n")

    # TO DO: Display counts of gender
    if "Gender" in df.columns:
        print('Counts of gender:')
        print(df['Gender'].value_counts())
    else:
        print("Gender information is not available.")
    
    print()

    # TO DO: Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        print('Earliest year of birth: ', df['Birth Year'].min())
        print('Most recent year of birth: ', df['Birth Year'].max())
        print('Most commont year of birth: ', df['Birth Year'].mode()[0])
    else:
        print("Birth of year is not available.", "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_separator()
    

def display_raw_data(city):
    """
    Display the raw data by five rows for the specified city.
    After displaying the 5 rows, the user can decide to continue or to interrupt the displaying.
    """
    answer = input(f'If you like to display the raw data of {city}, plaese type yes or y: ')
    if answer.lower() not in ('yes', 'y'):
        return
    raw_df = pd.read_csv(CITY_DATA[city.lower()])
    raw_df.rename(columns = { 'Unnamed: 0' : "<No column name>"}, inplace=True)
    for i in range(1, raw_df.size+1):
        print(raw_df.iloc[i-1])
        print_separator()
        if (i % 5) == 0:
            answer = input('If you like to continue displaying the raw data, please type yes or y: ')
            if answer.lower() not in ('yes', 'y') :
                break
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
