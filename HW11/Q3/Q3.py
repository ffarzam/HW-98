from datetime import datetime, timedelta
import calendar
import jdatetime
import pytz


def check_date(f_date, s_date):
    if f_date > s_date:
        temp = f_date
        f_date = s_date
        s_date = temp

    return f_date, s_date


def is_daylight_saving(date_):
    timezone = pytz.timezone('Asia/Tehran')
    date_ = timezone.localize(datetime.strptime(date_, '%Y-%m-%d'))
    if date_.dst() != timedelta(0):
        return True
    else:
        return False


def difference_in_day(f_date, s_date):
    diff = s_date - f_date
    print("\033[0;31m" f"Difference of {f_date} and {s_date}: {diff.days} Days" "\033[0m")


def leap_year_count(f_date, s_date):
    year_1 = f_date.year
    year_2 = s_date.year
    leap_years = [year_ for year_ in range(year_1, year_2) if calendar.isleap(year_)]
    number_of_leap_year = calendar.leapdays(year_1, year_2)
    print("\033[0;34m" f"List of Leap Years: {leap_years}" "\033[0m")
    print("\033[0;34m" f"Number of Leap Years: {number_of_leap_year}" "\033[0m")


def DST_changes(f_date, s_date):
    count_dst = 0
    for i in range(int((s_date - f_date).days)):
        new_date = f_date + timedelta(1)
        if is_daylight_saving(new_date.date().strftime("%Y-%m-%d")) != is_daylight_saving(f_date.date().strftime("%Y-%m-%d")):
            count_dst += 1
        f_date = new_date
    print("\033[0;35m" "count of DST changes", count_dst, "\033[0m")


def show_solar_year(*args):
    for i in args:
        date_in_hijri = jdatetime.date.fromgregorian(day=i.day,
                                                     month=i.month,
                                                     year=i.year)
        print(
            "\033[0;32m" f"Converting {i.date()} to {date_in_hijri.strftime('%Y-%m-%d')} Solar Hijri" "\033[0;m")


def main(date_1, date_2):
    first_date = datetime.strptime(date_1, "%Y-%m-%d %H:%M:%S")
    second_date = datetime.strptime(date_2, "%Y-%m-%d %H:%M:%S")

    first_date, second_date = check_date(first_date, second_date)

    difference_in_day(first_date, second_date)

    leap_year_count(first_date, second_date)

    DST_changes(first_date, second_date)

    show_solar_year(first_date, second_date)


if __name__ == "__main__":
    date1 = input("Enter the first date like (2022-05-10 02:51:11): ")
    date2 = input("Enter the second date like (2022-05-10 02:51:11): ")
    main(date1, date2)
