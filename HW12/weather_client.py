from actions import *


def start_client() -> None:
    while True:
        print()
        choice = input("1) sign up\n"
                       "2) sign in\n"
                       "3) Exit\n"
                       "-----> ")
        print()

        if choice == "1":
            try:
                user = sign_in()
                send_user(user)
                print("You've registered successfully!")
            except Exception as e:
                print(e)

        elif choice == "2":
            username = input("username")
            password = input("password")

            if is_logged_in(username, password):
                while True:
                    do_what = input("What do you want to do?\n"
                                    "1) Get Weather Information\n"
                                    "2)Exit\n"
                                    "-----> ")

                    if do_what == "1":
                        get_weather_info(username)

                    elif do_what == "2":
                        break

        elif choice == "3":
            break


if __name__ == "__main__":
    start_client()

    # Langarūd
