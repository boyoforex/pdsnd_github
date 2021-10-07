#Import needed python modules
import time
import pandas as pd
import numpy as np

# Create a dictionary with the name of city and corresponding data file
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Creat lists of expected user inputs
city_list = ['new york city', 'chicago', 'washington']
month_list = ['all','january', 'february', 'march', 'april', 'may', 'june']
day_list = ['all','sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

#Create list of 12-hour human-friendly time hour
hours = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"]

#Function to get user input to filter data
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # Ensure the user wants to run the program
    
    city = input("Please input the city of interest: Type either New York City or Chicago or Washington: \n").lower().strip()
    while(city not in city_list):
        print("Sorry, the input is not recognized. Only New York City or Chicago or Washington is acceptable.")
        city = input("Please input the city of interest: Type either New York City or Chicago or Washington: \n").lower().strip()
    if city in city_list:
        print("You just told me you're interested in {} city, if not restart program.".format(city))
    # get user input for month (all, january, february, ... , june) 
    month = input("We have data for January, February, March, April, May and June. Please type specific month of interest or 'all' for entire dataset: \n").lower().strip()
    while(month not in month_list):
        print("Wrong Input, Please check spelling and acceptable options and try again.")
        month = input("We have data for January, February, March, April, May and June. Please type specific month of interest or 'all' for entire dataset: \n").lower().strip()
    if month in month_list:
        print("You just told me you're interested in {}, if not restart program.".format(month))
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Are you interested in a particular day? If so, type either Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type all for entire dataset: \n").lower().strip()
    while(day not in day_list):
        print("Wrong Input, Please check spelling and acceptable options and try again.")
        day = input("Are you interested in a particular day? If so, type either Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type all for entire dataset: \n").lower().strip()
    if day in day_list:
        print("You just told me you're interested in {}, if not restart program.".format(day))
    #print('-'*40)


    return city, month, day

#Function to filter database based on user preference
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
    # load user-specified data file into a dataframe, remove "NaN" and convert time to pandas datetime
    df = pd.read_csv(CITY_DATA[city])
    df.dropna(inplace=True)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # create new columns for month, hour, day of week
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    # Apply user-specified month and day filter to the dataframe
    if month != 'all':
        month = month_list.index(month)
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df

#Function to convert computed time to user-friendly output
def seconds2str(time_seconds):
    """
    Function to transform large time value in seconds to corresponding weeks, days, hours, minutes and seconds.

    Args:
        (int) time_seconds - large seconds value to convert
    Returns:
        (str) sec_str - number of weeks(wk), days(dy), hours(hr), minutes(min), and seconds(sec) in input time_seconds
    """

    min, sec = divmod(time_seconds, 60)
    hr, min = divmod(min, 60)
    dy, hr = divmod(hr, 24)
    wk, dy = divmod(dy, 7)
    
    sec_str = ''
    if wk > 0:
        sec_str += '{} weeks, '.format(wk)
    if dy > 0:
        sec_str += '{} days, '.format(dy)
    if hr > 0:
        sec_str += '{} hours, '.format(hr)
    if min > 0:
        sec_str += '{} minutes, '.format(min)
    if time_seconds > 59:
        sec_str += '{} seconds'.format(sec)
    return sec_str

#Function to calculate descriptive statistics for user-selected data
def cal_stats(df,city, month, day):
    start_time = time.time()
    """Displays statistics on the most frequent times of travel."""

    print('+'*40)
    print('\n HERE IS THE SUMMARY OF YOUR INPUT CRITERIA.......STARTING STAT CALCULATION\n')
    print('+'*40)
    print("You are interest in {} city for {} month and {} day\n".format(city,month,day))
    print("There are {} trips and you are using {:.2f} per cent of the city data based on criteria\n".format(len(df),((len(df)/len(pd.read_csv(CITY_DATA[city])))*100) ))
    print("There are {} start stations and {} end stations in the filtered data".format(len(df['Start Station'].unique()), len(df['End Station'].unique())))

    print('+'*40)
    print('\n CALCULATING THE MOST FREQUENT TIMES OF TRAVEL BASED ON YOUR INPUT CRITERIA\n')
    print('+'*40)
    
    # display the most common month
    month_mode = df['month'].apply(lambda x: month_list[x]).mode()[0]
    print("The most common month for biking is: {}".format(month_mode))

    # display the most common day of week
    day_mode = df['day_of_week'].apply(lambda x: day_list[x]).mode()[0]
    print("The most common day of the week for biking is: {}".format(day_mode))

    # display the most common start hour
    hour_mode = df['hour'].apply(lambda x: hours[x]).mode()[0]
    print("The most common hour for biking is: {}".format(str(hour_mode)))

    print('+'*40)
    print('\n CALCULATING THE MOST POPULAR STATIONS AND TRIPS BASED ON YOUR INPUT CRITERIA\n')
    print('+'*40)

    # display most commonly used start station
    begin_station_mode = df['Start Station'].mode()[0]
    begin_percent=df['Start Station'].value_counts()[begin_station_mode]
    print("Most of the trip begins at station {} for a total of {} times".format(begin_station_mode ,begin_percent))

    # display most commonly used end station
    end_station_mode = df['End Station'].mode()[0]
    end_percent=df['End Station'].value_counts()[end_station_mode]
    print("Most of the trip ends at station {} for a total of {} times".format(end_station_mode ,end_percent))

    # display most frequent combination of start station and end station trip
    station_combination = (df['Start Station'] + "-" + df['End Station']).mode()[0]
    grp_combination = df.groupby(['Start Station', 'End Station'])
    percent_combination = grp_combination['Trip Duration'].count().max()
    print("Most of the trips are from the station at {} to the station at {}. A total of {} trips".format(str(station_combination.split("-")[0]), str(station_combination.split("-")[1]),percent_combination))
    
    print('+'*40)
    print('\n CALCULATING TRIP DURATION BASED ON YOUR INPUT CRITERIA\n')
    print('+'*40)

    # display total travel time
    total_traveltime = int(df['Trip Duration'].sum())   
    print("The total travel time is: {}".format(seconds2str(total_traveltime)))

    # display mean travel time
    mean_traveltime = int(df['Trip Duration'].mean())
    print("The mean travel time is: {}".format(seconds2str(mean_traveltime)))

    print('+'*40)
    print('\n CALCULATING USER STATISTICS BASED ON YOUR INPUT CRITERIA\n')
    print('+'*40)
    
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("The number of unique user types is:")
    for i in range(len(user_types)):
        val = user_types[i]
        user_type = user_types.index[i]
        print('    {0:21}'.format((user_type + ':')), val)
    
    print('-'*40)
    #print('\n')
    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print("The number of user gender is:")
        for i in range(len(gender)):
            val = gender[i]
            genders = gender.index[i]
            print('    {0:21}'.format((genders + ':')), val)
    else:
        print("We're sorry, the database doesn't contain information about the gender of bikers")
    print('-'*40)
    #print('\n')
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("The earliest year of birth is: {}".format(int(df['Birth Year'].min())))
        print("The most recent year of birth is: {}".format(int(df['Birth Year'].max())))
        print("The most common ear of birth is: {}".format(int(df['Birth Year'].mode())))
    else:
        print("We're sorry, the database doesn't contain information about the year of birth of bikers")

    print('+'*40)
    print('\nTHIS IS THE END OF THE STATISTICS BASED ON YOUR INPUT CRITERIA.THAT MUST BE A LOT OF INFORMATION!\n')
    print("\nThe entire computation took %s seconds." % (time.time() - start_time))
    print('+'*40)

#Function to manage raw data request and output
def display_rawdata(df):
    '''This function finds out if the user wants to view the raw data and if so, it displays it five lines per time.
    After displaying five lines, the user is asked if they would like to view the next five lines until they say no or the end is reached.
    
    Args:
        df: selected city dataframe
    Returns:
        five lines of the dataframe 
    '''
    # iterate from 0 to the maximum number of rows in steps of 5
    for i in range(0, len(df), 5):
        answer = input("\nWould you like to view row {} to {} of {} in the trip data you selected? Type yes or no \n".format(i+1,i+5,len(df))).lower()
        if answer != 'yes':
            break
        print(df.iloc[i:i+5])
        print('-'*40)
        if i < len(df) and i+5 > len(df):
            print("This is the last row of data, thanks for viewing!")
        
        if i > len(df):
            print("END OF DATA REACHED!")
            print('-'*40)
            break



#Main part of the program
def main():
    # Ensure the user wants to run the program
    priint('\nHello! Trust you\'re doing great today.')
#Looking for ways to make the output impressive. This is python ASCII ART inspiration from https://asciiart.website/index.php?art=transportation/bicycles
    asci_image = '''
    
                                 $"   *.      *bike*
              d$$$$$$$P"                  $    J
                  ^$.                     4r  "
                  d"b                    .db
                 P   $                  e" $
        ..ec.. ."     *.              zP   $.zec..
    .^        3*b.     *.           .P" .@"4F      "4
  ."         d"  ^b.    *c        .$"  d"   $         %
 /          P      $.    "c      d"   @     3r         3
4        .eE........$r===e$$$$eeP    J       *..        b
$       $$$$$       $   4$$$$$$$     F       d$$$.      4
$       $$$$$       $   4$$$$$$$     L       *$$$"      4
4      Udacity  """3P ===$$$$$$"     3      Udacity     P
 *                 $       """        b                J
  ".             .P                    %.             @
    %.         z*"                      ^%.        .r"
       "*==*""                             ^"*==*""   Ojo21'
    
    '''
    print(asci_image)
    print('This program explore bikeshare data for chicago, new york city and washington in United States')
    go_ahead = input("Is this your intented purpose? If so type yes to continue or no to quit: \n").lower()
    while(go_ahead not in ['yes','no']):
        print("Sorry, I didn't catch that. Try again, type yes or no")
    while(go_ahead=='no'):
        print("Thanks for your time, Bye for now")
        break
    while (go_ahead=='yes'):
        city, month, day = get_filters()
        if city=='' or month=='' or day=='':
            print("We're sorry, empty city, month or day. Please check")
            break
        df = load_data(city, month, day)
        if len(df) > 0:
            cal_stats(df,city, month, day)
            display_rawdata(df)
        else:
            print("We're sorry, there is no data based on your input criteria")
            break

        restart = input('\nWould you like to rerun the program? Enter yes or no.\n').lower()
        while(restart not in ['yes','no']):
            print("Wrong Input, Please check spelling and type either yes or no")
            restart = input('\nWould you like to rerun the program? Enter yes or no.\n').lower()
        if restart == 'no':
            print("Thanks for your time, Bye for now!")
            break


if __name__ == "__main__":
	main()
