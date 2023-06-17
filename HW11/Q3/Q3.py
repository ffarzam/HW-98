import datetime



def main(date_1,date_2):
    first_date=datetime.datetime.strptime(date_1, "%Y-%m-%d %H:%M:%S")
    second_date = datetime.datetime.strptime(date_2, "%Y-%m-%d %H:%M:%S")
    delta= second_date - first_date
    print(delta.seconds)

if __name__ == "__main__":

    f_date = input("Enter the first date like (2022-05-10 02:51:11): ")
    s_date = input("Enter the second date like (2022-05-10 02:51:11): ")
    main(f_date,s_date)