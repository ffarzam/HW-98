import datetime
import calendar
import time



def main(date_1,date_2):
    first_date=datetime.datetime.strptime(date_1, "%Y-%m-%d %H:%M:%S")
    second_date = datetime.datetime.strptime(date_2, "%Y-%m-%d %H:%M:%S")
    delta= second_date - first_date
    print(delta.seconds)

    year_1=first_date.year
    year_2=second_date.year
    leap_years = [year_ for year_ in range(year_1, year_2) if calendar.isleap(year_)]
    number_of_leap_year = calendar.leapdays(year_1, year_2)
    print(f"List of Leap Years: {leap_years}")
    print(f"Number of Leap Years: {number_of_leap_year}")


if __name__ == "__main__":

    f_date = input("Enter the first date like (2022-05-10 02:51:11): ")
    s_date = input("Enter the second date like (2022-05-10 02:51:11): ")
    main(f_date,s_date)