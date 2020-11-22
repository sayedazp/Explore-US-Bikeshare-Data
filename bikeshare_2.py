import time
import pandas as pd
import numpy as np
import os
#changing directory to the working file path !
os.chdir(os.path.dirname(os.path.abspath(__file__)))

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
print('Hello! Let\'s explore some US bikeshare data!')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    #get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Would you like to see data for Chicago, New York city, or Washington? ----> ").lower()
        if city in list(CITY_DATA.keys()):
            break
        else:
            print("sorry that's not a valid input")  

    # get user input for month (all, january, february, ... , june)
    while True:
        q1 = input("for a specific month enter : 'M' for all months enter : 'all'----> ").capitalize()
        if q1 == "m".capitalize():
            month = input("Which month - January, February, March, April, May, june?----> ").capitalize() 
            months = ["January", "February", "March", "April", "May","June"]
            if month in months:
                break
            else:
                print("sorry that's not a valid input")
        elif q1 == "all".capitalize():
            month = "all"
            break
        else:
            print("please enter a valid value")

    # # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        q2 = input("for a specific DAY enter : 'D' for all days enter : 'all'----> ").capitalize()
        if q2 == "d".capitalize():
            day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday,Saturday, or Sunday?").capitalize() 
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday","Saturday" , "Sunday"]
            if day in days:
                break
            else:
                print("sorry that's not a valid input")
        elif q2 == "all".capitalize():
            day = "all"
            break
        else:
            print("please enter a valid value")

    print('-'*40)
    return city, month, day

#my_data = get_filters()
#(city,month,day) = my_data  
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df =  df[df['day'] == day.title()]
    return df

#df = load_data(city,month,day)
# city, month, day = get_filters()
# df = load_data(city, month, day)
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == "all":
        popular_month = df['month'].mode()[0]
        print(f"the most popular month is ---> {popular_month}")

    # display the most common day of week
    if day == "all":
        popular_day = df['day'].mode()[0]
        print(f"the most popular day is ---> {popular_day}")

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(f"the most popular hour is ----> {popular_hour}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#time_stats(df)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_ststation = df['Start Station'].mode()[0]
    print(f"the most commonly used start station is ---> {popular_ststation}")

    # display most commonly used end station
    popular_enstation = df['End Station'].mode()[0]
    print(f"the most commonly used end station is ---> {popular_enstation}")

    # display most frequent combination of start station and end station trip
    df['combination'] =df['Start Station'] + " and " + df['End Station']
    the_most_comb = df['combination'].mode()[0]
    print(f"the most frequent combination of start station and end station trip is ----> {the_most_comb} ")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#station_stats(df)
def seconds_converter(time):
    """"Converts seconds into days , hours , minutes and seconds"""
    days_time = time // (24 * 3600)
    time %= (24 * 3600)
    hours_time = time // 3600
    time %= 3600
    minutes_time = time // 60
    time %= 60
    seconds_time = time
    return days_time,hours_time,minutes_time,seconds_time
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total_time = sum(df['Trip Duration'])
    print(f"total time travelled is ---> {seconds_converter(total_time)[0]} days and {seconds_converter(total_time)[1]} hours and {seconds_converter(total_time)[2]} minutes and {seconds_converter(total_time)[3]} seconds")
    
    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print(f"mean travelling time is ---> {mean_travel} seconds which means: \n{seconds_converter(mean_travel)[0]} days and {seconds_converter(mean_travel)[1]} hours and {seconds_converter(mean_travel)[2]} minutes and {seconds_converter(mean_travel)[3]} seconds ")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#trip_duration_stats(df)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    try:
        number_of_user_types = len(df['User Type'].unique())
        for i in range(number_of_user_types):
            type_user = df['User Type'].unique()[i]
            print(f"number of {type_user} is {df[df['User Type'] == type_user]['User Type'].count()} ") 
    except:
        print("No Data available to show !")    
    if city != "washington":
        # Display counts of gender
        try:
            genderdf = df.dropna(subset = ["Gender"])
            number_of_user_gender = len(genderdf['Gender'].unique())
            for i in range(number_of_user_gender):
                gender = genderdf['Gender'].unique()[i]
                print(f"number of {gender} is {genderdf[genderdf['Gender'] == gender]['Gender'].count()} ")
        except:
            print("No Data available to show !")
        # Display earliest, most recent, and most common year of birth
        #Deleting NaN values
        try:
            yeardf = df.dropna(subset = ["Birth Year"])
            earliest_year = int(yeardf['Birth Year'].max())
            recent_year = int(yeardf['Birth Year'].min())
            popular_year = int(yeardf['Birth Year'].mode()[0])
            print(f"the earliest year is ---> {earliest_year}\nthe most recent year is ---> {recent_year}\nthe most popular year is ---> {popular_year}")
        except:
            print("No Data available to show !")
    else:
        print(30*"*")
        print("\n>>> counts of genders and earliest, most recent, and most common year of birth are not available for washington sorry ! <<<\n")
        print(30*"*")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(city):
    """displays the raw data table depending on the chosing city 5 rows a time
    Args : 
        (str) city : city name    
    """
    i = 5
    try:
        while True:
            if i ==5:
                qu = input("would you like to see the raw data ? [yes] or [no]---> " ).lower().strip()
                if qu == "yes":
                    ndt = pd.read_csv(CITY_DATA[city])
                    print(ndt[:i])
                    i += 5
                elif qu == "no":
                    break
                else:
                    print("there is no valid input !")
                    continue
            elif i > 5:
                qu2 = input("would you like to see more data ? [yes] or [no]---> ").lower().strip()
                if qu2 == "yes":
                    ndt = pd.read_csv(CITY_DATA[city])
                    print(ndt[:i])
                    i += 5
                elif qu2 =="no":
                    break
                else:
                    print("there is no valid input")
                    continue
            else:
                break
    except:
        print("Error happened you have already showed the full data")

            

        

def main():
    while True:

        global city , month, day
        city, month, day = get_filters()
        question = input(f"your choices are {city} as a city and {month} as a month and {day} as a day continue [yes] or [no] ----> ").lower().strip()
        if question == "yes":
            print("continued")
            print("*"*50)
            df = load_data(city, month, day)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_raw_data(city)  
            while True:
                breaking = 0
                restart = input('\nWould you like to restart? Enter yes or no.\n').strip()
                if restart.lower() == 'no':
                    breaking = 1
                    break
                elif restart.lower() == 'yes':
                    break
                else:
                    print("please insert yes or no")
            if breaking == 1:
                break
        elif question == "no":
            restart = input('\nWould you like to restart? Enter yes or no.\n').strip()
            if restart.lower() != 'yes':
                break          
            continue
        else:
            print("please insert yes or no")

       
            

if __name__ == "__main__":
	main()
