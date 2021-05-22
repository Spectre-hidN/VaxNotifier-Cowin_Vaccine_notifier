import json
import os
import subprocess
import sys
import datetime
import time


subprocess.call(['clear'])

try:
    if sys.argv[1] == '--setup':
        try:
            print("\033[38;5;46mDownloading and installing essentials...\033[0m")
            subprocess.call(['apt-get', 'update', '-y'])
            subprocess.call(['apt-get', 'upgrade', '-y'])
            subprocess.call(['pkg', 'install', 'termux-api', '-y'])
            subprocess.call(['pip', 'install', 'requests'])
            print('\033[38;5;46mProcess Done!\033[0m')
            print('\033[38;5;196mRestart Termux and run this without --setup flag\033[0m')
            sys.exit()
        except Exception as Error:
            print(f'\033[38;5;196mFATAL ERROR: \033[0m{str(Error)}')
            sys.exit(2)

except Exception as Error:
    pass

try:
    import requests
except:
    print('\033[38;5;196mFatal Error:\033[0m Requests module not found! Try running this with --setup flag to fix missing packages.')
    sys.exit(2)

default_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
                   "origin": "https://www.cowin.gov.in",
                   "referer": "https://www.cowin.gov.in/"}

def get_public_data():
    """Get the public data and return a tuple of status_code and JSON text"""

    print("Processing...")

    #Register IP on server to allow API to fetch content.
    requests.get("https://www.cowin.gov.in", headers={'User-Agent': default_headers['User-Agent']})

    url = "https://cdn-api.co-vin.in/api/v1/reports/v2/getPublicReports?state_id=&district_id=&date="
    response = requests.get(url, headers=default_headers)

    return (response.status_code, response.text)

def get_states():
    """Get States ID and return tupe of status_code and JSON text"""

    print("Getting state lists...")

    #Register IP on server to allow API to fetch content.
    requests.get("https://www.cowin.gov.in", headers={'User-Agent': default_headers['User-Agent']})

    url = 'https://cdn-api.co-vin.in/api/v2/admin/location/states'
    response = requests.get(url, headers=default_headers)

    return (response.status_code, response.text)

def get_districts(state_id):
    """Get Districts ID and return tuple of status_code and JSON text"""

    print("Getting district lists...")

    url = f'https://cdn-api.co-vin.in/api/v2/admin/location/districts/{state_id}'
    response = requests.get(url, headers=default_headers)

    return (response.status_code, response.text)

def get_centres(district_id, date, method):
    """Get centre data return tuple of status_code and JSON text"""
    if method == 'ByDistrict':
        url= f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={date}"
    elif method == 'ByPin':
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={district_id}&date={date}"
    
    try:
        response = requests.get(url, headers=default_headers)
    except:
        return (8001, '')

    return (response.status_code, response.text)

def get_approx_location(lat, long):
    return f"http://maps.google.com/?ie=UTF8&hq=&ll={lat},{long}&z=14"

def show_notifier(Doses_available, Centre_name, Vaccine_name, date):
    subprocess.call(["termux-notification", "--title", 'Vaccine Available!', '--content', f'{Doses_available} Dose(s) of {Vaccine_name} available\nat {Centre_name}\non {date}.',  '--priority',  'high', '--button1', 'Register now', '--button1-action', 'termux-open-url https://www.cowin.gov.in'])
    subprocess.call(['termux-vibrate', '-f', '-d', '500'])
    time.sleep(0.5)
    subprocess.call(['termux-vibrate', '-f', '-d', '500'])
    
    return

print("""
\033[38;5;197m █░█ ▄▀█ ▀▄▀ █▄░█ █▀█ ▀█▀ █ █▀▀ █ █▀▀ █▀█
\033[38;5;56m ▀▄▀ █▀█ █░█ █░▀█ █▄█ ░█░ █ █▀░ █ ██▄ █▀▄
            \033[38;5;21mCo\033[38;5;46mWin \033[38;5;51mVaccine \033[0mNotifier""")

print("""
\033[38;5;197m<< Choose from below >> \033[0m
______________________
| 1. Get Public Data |
| 2. Setup notifier  |
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
\033[38;5;93mYour choice (\033[38;5;208m1\033[0m or \033[38;5;208m2\033[38;5;93m only): \033[0m""", end='')
choice = input()

if choice == '1':
    json_data = get_public_data()

    if json_data[0] != 200:
        print(f"\033[38;5;196mServer Error: {str(json_data[0])}\033[0m")
        sys.exit(json_data[0])

    parsed_json = json.loads(json_data[1])

    subprocess.call(['clear'])

    timestamp = parsed_json["timestamp"]

    print(f"\033[38;5;177mPUBLIC DATA as of {timestamp} \033[0m")
    print("\033[38;5;177m‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\033[0m")

    print()
    print("\033[38;5;36m++ Registration Data ++\033[0m")
    total_registered = parsed_json["topBlock"]["registration"]["total"]
    registered_18_45 = parsed_json["topBlock"]["registration"]["cit_18_45"]
    registered_45_plus = parsed_json["topBlock"]["registration"]["cit_45_above"]
    registered_today = parsed_json["topBlock"]["registration"]["today"]

    print(f"\033[38;5;196m+\033[0m \033[38;5;45mTotal Registration: \033[0m{str(total_registered)}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;27mRegistered age 18-45: \033[0m{str(registered_18_45)}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;48mRegistered age 45+: \033[0m{str(registered_45_plus)}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;164mToday's Registration: \033[0m{str(registered_today)}")
    print()

    print("\033[38;5;82m++ Vaccination Data ++\033[0m")
    total_vaccinated = parsed_json["topBlock"]["vaccination"]["total"]
    total_male = parsed_json["topBlock"]["vaccination"]["male"]
    total_female = parsed_json["topBlock"]["vaccination"]["female"]
    total_others = parsed_json["topBlock"]["vaccination"]["others"]
    vaccinated_with_covishield =parsed_json["topBlock"]["vaccination"]["covishield"]
    vaccinated_with_covaxin = parsed_json["topBlock"]["vaccination"]["covaxin"]
    vaccinated_today = parsed_json["topBlock"]["vaccination"]["today"]
    total_dose_1 = parsed_json["topBlock"]["vaccination"]["tot_dose_1"]
    total_dose_2 = parsed_json["topBlock"]["vaccination"]["tot_dose_2"]
    total_doses = parsed_json["topBlock"]["vaccination"]["total_doses"]
    aefi = parsed_json["topBlock"]["vaccination"]["aefi"]
    today_dose_1 = parsed_json["topBlock"]["vaccination"]["today_dose_one"]
    today_dose_2 = parsed_json["topBlock"]["vaccination"]["today_dose_two"]
    today_male = parsed_json["topBlock"]["vaccination"]["today_male"]
    today_female = parsed_json["topBlock"]["vaccination"]["today_female"]
    today_others = parsed_json["topBlock"]["vaccination"]["today_others"]
    today_aefi = parsed_json["topBlock"]["vaccination"]["today_aefi"]

    print(f"\033[38;5;196m+\033[0m \033[38;5;45mTotal Vaccinated: \033[0m{str(total_vaccinated)}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;35mTotal Male Vaccinated: \033[0m{str(total_male)}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;87mTotal Female Vaccinated: \033[0m{str(total_female)}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;41mTotal Others Vaccinated: \033[0m{str(total_others)}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;220mTotal Vaccinated with Covishield: \033[0m{str(vaccinated_with_covishield)}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;199mTotal Vaccinated with Covaxin: \033[0m{str(vaccinated_with_covaxin)}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;62mTotal Vaccinated Today: \033[0m{str(vaccinated_today)}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;9mTotal Dose-1 : \033[0m{str(total_dose_1)}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;206mTotal Dose-2 : \033[0m{str(total_dose_2)}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;155mTotal Doses served : \033[0m{str(total_doses)}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;33mAEFI : \033[0m{str(aefi)}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;47mToday's Dose-1 : \033[0m{str(today_dose_1)}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;14mToday's Dose-2 : \033[0m{str(today_dose_2)}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;200mToday's Vaccinated Male: \033[0m{str(today_male)}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;159mToday's Vaccinated Female: \033[0m{str(today_female)}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;198mToday's Vaccinated Others: \033[0m{str(today_others)}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;208mToday's AEFI: \033[0m{str(today_aefi)}")

    print()

    print("\033[38;5;197m++ Vaccination Timestamps ++\033[0m")
    for elmt in parsed_json["vaccinationDoneByTime"]:
        upperscore = (len(elmt["ts"]) + len("Timestamp ")) *  '‾'
        print(f'\033[38;5;104mTimestamp {elmt["ts"]}')
        print(f"\033[38;5;104m{upperscore}\033[0m")
        print(f'\033[38;5;93m+\033[0m \033[38;5;198mBatch: \033[0m{elmt["label"]}')
        print(f'\033[38;5;93m+\033[0m \033[38;5;198mTotal doses served: \033[0m{elmt["count"]}')
        print(f'\033[38;5;93m+\033[0m \033[38;5;198mDose-1 served: \033[0m{elmt["dose_one"]}')
        print(f'\033[38;5;93m+\033[0m \033[38;5;198mDose-2 served: \033[0m{elmt["dose_two"]}')
        print('-' * os.get_terminal_size()[0])
        print()
    
    print("\033[38;5;203m++ Vaccination Data By States ++\033[0m")
    for elmt in parsed_json["getBeneficiariesGroupBy"]:
        print(f"\033[38;5;196m+\033[0m \033[38;5;214mState Name: \033[0m{str(elmt['state_name'])}")
        print(f'\033[38;5;40m   -\033[38;5;87mID: \033[0m{str(elmt["state_id"])}')
        print(f'\033[38;5;40m   -\033[38;5;87mTotal Vaccinated: \033[0m{str(elmt["total"])}')
        print(f'\033[38;5;40m   -\033[38;5;87mPartially Vaccinated: \033[0m{str(elmt["partial_vaccinated"])}')
        print(f'\033[38;5;40m   -\033[38;5;87mFully Vaccinated: \033[0m{str(elmt["totally_vaccinated"])}')
        print(f"\033[38;5;40m   -\033[38;5;87mVaccinated Today: \033[0m{str(elmt['today'])}")
        print()
    
    print("\033[38;5;138m++ Vaccination By Age ++\033[0m")
    print(f"\033[38;5;196m+\033[0m \033[38;5;45mTotal Vaccinated: \033[0m{str(total_vaccinated)}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;153mTotal Vaccinated [18-45]: \033[0m{str(parsed_json['vaccinationByAge']['vac_18_45'])}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;154mTotal Vaccinated [45-60]: \033[0m{str(parsed_json['vaccinationByAge']['vac_45_60'])}")
    print(f"\033[38;5;196m+\033[0m \033[38;5;40mTotal Vaccinated [60+]: \033[0m{str(parsed_json['vaccinationByAge']['above_60'])}")
    
    print()
    
    print("\033[38;5;83m++ Registration Timestamps ++\033[0m")
    for elmt in parsed_json["timeWiseTodayRegReport"]:
        upperscore = (len(elmt["ts"]) + len("Timestamp ")) *  '‾'
        print(f'\033[38;5;104mTimestamp {elmt["ts"]}')
        print(f"\033[38;5;104m{upperscore}\033[0m")
        print(f'\033[38;5;93m+\033[0m \033[38;5;203mInterval: \033[0m{elmt["label"]}')
        print(f'\033[38;5;93m+\033[0m \033[38;5;203mTotal Registration: \033[0m{elmt["total"]}')
        print(f'\033[38;5;93m+\033[0m \033[38;5;203mRegistered Users [Age-18]: \033[0m{elmt["age18"]}')
        print(f'\033[38;5;93m+\033[0m \033[38;5;203mRegistered Users [Age-45]: \033[0m{elmt["age45"]}')
        print(f'\033[38;5;93m+\033[0m \033[38;5;203mRegistered Users [Age-60]: \033[0m{elmt["age60"]}')
        print(f'\033[38;5;93m+\033[0m \033[38;5;203mRegistered Users [Sex-Male]: \033[0m{elmt["male"]}')
        print(f'\033[38;5;93m+\033[0m \033[38;5;203mRegistered Users [sex-Female]: \033[0m{elmt["female"]}')
        print(f'\033[38;5;93m+\033[0m \033[38;5;203mRegistered Users [Others]: \033[0m{elmt["others"]}')
        print('-' * os.get_terminal_size()[0])
        print()
    
    print("\033[38;5;196m*\033[38;5;220mAll the above data are collected from cowin Public API.\033[0m")

elif choice == '2':
    subprocess.call(['clear'])
    print("""
\033[38;5;198m<<Choose from Below >>\033[0m
 _________________________________________________    
|1. Notify when vaccine available at your Pincode |
|2. Notify when vaccine available at your District|
 ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
\033[38;5;93mYour choice (\033[38;5;208m1\033[0m or \033[38;5;208m2\033[38;5;93m only): \033[0m""", end='')
    choice = input()

    if choice == '1':
        pin_code = input("\033[38;5;93mType your Pin Code: \033[0m")
        
        try:
            minimum_dose_codn = int(input("\033[38;5;93mSet minimum vaccine availability Condition [Default > 1]: \033[0m"))
        except:
            minimum_dose_codn = 1

        subprocess.call(['clear'])

        print('\033[38;5;82m++ Notifier Started! ++')
        print()

        print('\033[38;5;196m[\033[0m+\033[38;5;196m]\033[0m You will get notified when there will be any available slot at your region within next 15 Days')
        print("\033[38;5;196m[\033[0m+\033[38;5;196m]\033[0m Make sure Termux is running in the background and you have active internet connection all the time!")
        print('\033[38;5;196m[\033[0m+\033[38;5;196m]\033[0m All the data will get logged in this console so, check here if you accidently removed your notification.')

        print()

        print('\033[38;5;46mVaccination Slot logs\033[0m')
        print('\033[38;5;46m‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\033[0m')
        
        IDs = []
        IDs_reset_date_start = datetime.datetime.now().strftime("%d")
        IDs_reset_date = datetime.datetime.strptime(IDs_reset_date_start, "%d") + datetime.timedelta(days=1)
        IDs_reset_date = IDs_reset_date.strftime('%d')

        while 1:
            today = datetime.datetime.now()
            date_str = today.strftime("%d-%m-%Y")
            date_start = datetime.datetime.strptime(date_str, "%d-%m-%Y")
            for i in range(1, 16):
                check_date = date_start + datetime.timedelta(days=i)
                check_date = check_date.strftime("%d-%m-%Y")

                centre_data = get_centres(pin_code, check_date, 'ByPin')

                if centre_data[0] != 200:
                    print(f'\033[38;5;105mTimestamp {datetime.datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")}\033[0m')
                    print(f"\033[38;5;196m    Server Error: {str(centre_data[0])}\033[0m")
                    print('-' * os.get_terminal_size()[0])
                    print()
                    time.sleep(30)
                 
                else:
                    parsed_json = json.loads(centre_data[1])

                    for elmt in parsed_json['centers']:
                        for session in elmt['sessions']:
                            if session['available_capacity'] >= minimum_dose_codn:
                                if session['session_id'] not in IDs:
                                    print(f'\033[38;5;105mTimestamp {datetime.datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")}\033[0m')
                                    print('\033[38;5;83m    Vaccine Availability found!\033[0m')
                                    print(f'\033[38;5;171m       Centre Name: \033[0m{elmt["name"]}')
                                    print(f'\033[38;5;171m       Centre Address: \033[0m{elmt["address"]}')
                                    print(f'\033[38;5;171m       Time Available: \033[0m{elmt["from"]}-{elmt["to"]}')
                                    print(f'\033[38;5;171m       Fee Type: \033[0m{elmt["fee_type"]}')
                                    print(f'\033[38;5;171m       Vaccine Name: \033[38;5;46m{session["vaccine"]}\033[0m')
                                    print(f'\033[38;5;171m       Minimum Age: \033[0m{str(session["min_age_limit"])}')
                                    print(f'\033[38;5;171m       Doses Available: \033[0m{str(session["available_capacity"])}')
                                    print(f'\033[38;5;171m       Available Date: \033[0m{str(session["date"])}')
                                    slot_string = ''
                                    for slot in session['slots']:
                                        slot_string += f'[{slot}] '
                                    print(f'\033[38;5;171m       Slots Available: \033[0m{slot_string}') 
                                    print(f'\033[38;5;171m       Approx Geo Location: \033[0m{get_approx_location(str(elmt["lat"]), str(elmt["long"]))}')
                                    print('-' * os.get_terminal_size()[0])
                                    print()
                                    show_notifier(str(session["available_capacity"]), elmt["name"], session["vaccine"], session["date"])
                                    IDs.append(session['session_id'])
                
                time.sleep(7)
            
            #Reset the Ids list after a day
            if today.strftime('%d') == IDs_reset_date:
                IDs = []
                IDs_reset_date_start = datetime.datetime.now().strftime("%d")
                IDs_reset_date = datetime.datetime.strptime(IDs_reset_date_start, "%d") + datetime.timedelta(days=1)
                IDs_reset_date = IDs_reset_date.strftime('%d')



    elif choice == '2':
        state_data = get_states()
        
        if state_data[0] != 200:
            print(f"\033[38;5;196mServer Error: {str(state_data[0])}\033[0m")
            sys.exit(state_data[0])
        
        parsed_json = json.loads(state_data[1])

        subprocess.call(['clear'])

        print('\033[38;5;202mState ID  \033[0m|  \033[38;5;226mState Name\033[0m')
        print()

        for elmt in parsed_json["states"]:
            if elmt["state_id"] >= 10:
                intermediate_space = ' ' * (9 - 1)
            elif elmt["state_id"] < 10:
                intermediate_space = ' ' * (9)
            print(f'\033[38;5;202m{str(elmt["state_id"])}{intermediate_space}\033[0m|  \033[38;5;226m{elmt["state_name"]}\033[0m')

        print()
        
        state_id = input("\033[38;5;93mChoose your state ID from the above list: \033[0m")
        district_data = get_districts(state_id)

        if district_data[0] != 200:
             print(f"\033[38;5;196mServer Error: {str(district_data[0])}\033[0m")
             sys.exit(district_data[0])
        
        subprocess.call(['clear'])

        parsed_json = json.loads(district_data[1])

        print('\033[38;5;202mDistrict ID  \033[0m|  \033[38;5;226mDistrict Name\033[0m')
        print()

        for elmt in parsed_json["districts"]:
            if elmt["district_id"] >= 100:
                intermediate_space = ' ' * (12 - 2)
            elif elmt["district_id"] >= 10:
                intermediate_space = ' ' * (12 - 1)
            elif elmt["district_id"] < 10:
                intermediate_space = ' ' * (12)
            print(f'\033[38;5;202m{str(elmt["district_id"])}{intermediate_space}\033[0m|  \033[38;5;226m{elmt["district_name"]}\033[0m')

        print()
        
        District_id = input("\033[38;5;93mChoose your District ID from the above list: \033[0m")
        try:
            minimum_dose_codn = int(input("\033[38;5;93mSet minimum vaccine availability Condition [Default > 1]: \033[0m"))
        except:
            minimum_dose_codn = 1
        print("Setting up...")

        subprocess.call(['clear'])

        print('\033[38;5;82m++ Notifier Started! ++')
        print()

        print('\033[38;5;196m[\033[0m+\033[38;5;196m]\033[0m You will get notified when there will be any available slot at your region within next 15 Days')
        print("\033[38;5;196m[\033[0m+\033[38;5;196m]\033[0m Make sure Termux is running in the background and you have active internet connection all the time!")
        print('\033[38;5;196m[\033[0m+\033[38;5;196m]\033[0m All the data will get logged in this console so, check here if you accidently removed your notification.')

        print()

        print('\033[38;5;46mVaccination Slot logs\033[0m')
        print('\033[38;5;46m‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\033[0m')

        IDs = []
        IDs_reset_date_start = datetime.datetime.now().strftime("%d")
        IDs_reset_date = datetime.datetime.strptime(IDs_reset_date_start, "%d") + datetime.timedelta(days=1)
        IDs_reset_date = IDs_reset_date.strftime('%d')

        while 1:
            today = datetime.datetime.now()
            date_str = today.strftime("%d-%m-%Y")
            date_start = datetime.datetime.strptime(date_str, "%d-%m-%Y")
            for i in range(1, 16):
                check_date = date_start + datetime.timedelta(days=i)
                check_date = check_date.strftime("%d-%m-%Y")
                
                centre_data = get_centres(District_id, check_date, 'ByDistrict')

                if centre_data[0] != 200:
                    print(f'\033[38;5;105mTimestamp {datetime.datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")}\033[0m')
                    print(f"\033[38;5;196m    Server Error: {str(centre_data[0])}\033[0m")
                    print('-' * os.get_terminal_size()[0])
                    print()
                    time.sleep(30)
                
                else:
                    parsed_json = json.loads(centre_data[1])

                    for elmt in parsed_json['centers']:
                        for session in elmt['sessions']:
                            if session['available_capacity'] >= minimum_dose_codn:
                                if session['session_id'] not in IDs:
                                    print(f'\033[38;5;105mTimestamp {datetime.datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")}\033[0m')
                                    print('\033[38;5;83m    Vaccine Availability found!\033[0m')
                                    print(f'\033[38;5;171m       Centre Name: \033[0m{elmt["name"]}')
                                    print(f'\033[38;5;171m       Centre Address: \033[0m{elmt["address"]}')
                                    print(f'\033[38;5;171m       Time Available: \033[0m{elmt["from"]}-{elmt["to"]}')
                                    print(f'\033[38;5;171m       Fee Type: \033[0m{elmt["fee_type"]}')
                                    print(f'\033[38;5;171m       Vaccine Name: \033[38;5;46m{session["vaccine"]}\033[0m')
                                    print(f'\033[38;5;171m       Minimum Age: \033[0m{str(session["min_age_limit"])}')
                                    print(f'\033[38;5;171m       Doses Available: \033[0m{str(session["available_capacity"])}')
                                    print(f'\033[38;5;171m       Available Date: \033[0m{str(session["date"])}')
                                    slot_string = ''
                                    for slot in session['slots']:
                                        slot_string += f'[{slot}] '
                                    print(f'\033[38;5;171m       Slots Available: \033[0m{slot_string}') 
                                    print(f'\033[38;5;171m       Approx Geo Location: \033[0m{get_approx_location(str(elmt["lat"]), str(elmt["long"]))}')
                                    print('-' * os.get_terminal_size()[0])
                                    print()
                                    show_notifier(str(session["available_capacity"]), elmt["name"], session["vaccine"], session["date"])
                                    IDs.append(session['session_id'])
                
                time.sleep(7)

            #Reset the Ids list after a day
            if today.strftime('%d') == IDs_reset_date:
                IDs = []
                IDs_reset_date_start = datetime.datetime.now().strftime("%d")
                IDs_reset_date = datetime.datetime.strptime(IDs_reset_date_start, "%d") + datetime.timedelta(days=1)
                IDs_reset_date = IDs_reset_date.strftime('%d')

else:
    print("\033[38;5;196mInvalid Choice! Retry...\033[0m")
