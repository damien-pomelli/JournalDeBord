## Logbook generator
## Usage: python generate_logbook.py [dates] [--all FUTURE_DATE]

import os
import datetime
import argparse

template_path = "template.md"
logbook_folder_path = "/mnt/c/Users/Damien/Dropbox/PC/Documents/HEIG TB/Suivi - planif/Journal de bord" # "/mnt/c/Users/Damien/Dropbox/PC/Documents/YOTASYS/TDOA" # "/mnt/c/Users/Damien/Dropbox/PC/Documents/HEIG TB/Suivi - planif/Journal de bord" # "LogBook"

def parse_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d")

def get_week_number(date):
    return date.strftime("%U")

def get_week_day(date):
    return date.strftime("%d")

# def get_week_date(date):
#     return date.strftime("%Y-%m-%d")

def get_week_month(date):
    return date.strftime("%m")

def get_week_month_fr(date):
    month_number = int(date.strftime("%m"))
    month_names = {
        1: "Janvier",
        2: "Février",
        3: "Mars",
        4: "Avril",
        5: "Mai",
        6: "Juin",
        7: "Juillet",
        8: "Août",
        9: "Septembre",
        10: "Octobre",
        11: "Novembre",
        12: "Décembre"
    }
    return month_names[month_number], month_number

def get_week_days(date):
    start_of_week = date - datetime.timedelta(days=date.weekday())
    days = []
    months = []
    for i in range(7):
        days.append(get_week_day(start_of_week + datetime.timedelta(days=i)))
        months.append(get_week_month(start_of_week + datetime.timedelta(days=i)))
    return days, months

def get_week_year(date):
    return date.strftime("%Y")

def get_week_template():
    with open(template_path, "r") as file:
        return file.read()
    
def replace_week_template(template, week_number, week_days, week_year):
    template = template.replace("XX", week_number)
    template = template.replace("LU", week_days[0][0])
    template = template.replace("MA", week_days[0][1])
    template = template.replace("ME", week_days[0][2])
    template = template.replace("JE", week_days[0][3])
    template = template.replace("VE", week_days[0][4])
    template = template.replace("SA", week_days[0][5])
    template = template.replace("DI", week_days[0][6])
    template = template.replace("Mlu", week_days[1][0])
    template = template.replace("Mma", week_days[1][1])
    template = template.replace("Mme", week_days[1][2])
    template = template.replace("Mje", week_days[1][3])
    template = template.replace("Mve", week_days[1][4])
    template = template.replace("Msa", week_days[1][5])
    template = template.replace("Mdi", week_days[1][6])
    template = template.replace("YYYY", week_year)
    return template

def get_week_file_path(date):
    start_of_week = date - datetime.timedelta(days=date.weekday())
    week_number = get_week_number(start_of_week)
    week_month_fr, month_number = get_week_month_fr(start_of_week)
    week_year = get_week_year(start_of_week)
    week_file_name = f"Week {week_number}.md"
    week_folder_path = os.path.join(logbook_folder_path, week_year, f"{month_number:02d}_" + week_month_fr)
    week_file_path = os.path.join(week_folder_path, week_file_name)
    return week_file_path

def create_week_folder(date):
    start_of_week = date - datetime.timedelta(days=date.weekday())
    week_month_fr, month_number = get_week_month_fr(start_of_week)
    week_year = get_week_year(start_of_week)
    week_folder_path = os.path.join(logbook_folder_path, week_year, f"{month_number:02d}_" + week_month_fr)

    if not os.path.exists(week_folder_path):
        os.makedirs(week_folder_path)

def create_week_file(date):
    week_template = get_week_template()
    week_file_path = get_week_file_path(date)
    week_number = get_week_number(date)
    week_days = get_week_days(date)
    week_year = get_week_year(date)
    week_content = replace_week_template(week_template, week_number, week_days, week_year)
  
    if not os.path.exists(week_file_path):
        with open(week_file_path, "w") as file:
            file.write(week_content)

def get_mondays_between(start, end):
    current_monday = start - datetime.timedelta(days=start.weekday())
    last_monday = end - datetime.timedelta(days=end.weekday())

    mondays = []
    while current_monday <= last_monday + datetime.timedelta(weeks=1):
        mondays.append(current_monday)
        current_monday += datetime.timedelta(weeks=1)
    return mondays

def generate_logbook(date):
    create_week_folder(date)
    create_week_file(date)

def main():

    parser = argparse.ArgumentParser(description="Logbook generator")
    parser.add_argument("dates", nargs="*", help="Dates au format YYYY-MM-DD dont le logbook doit être généré")
    parser.add_argument("--all", metavar="FUTURE_DATE", help="Génère un journal de bord pour chaque semaine jusqu'à FUTURE_DATE incluse (format YYYY-MM-DD)")
    args = parser.parse_args()

    today = datetime.datetime.now()

    if args.all:
        future_date = parse_date(args.all)
        if future_date < today:
            print("❌ La date passée à --all doit se trouver dans le futur.")
            return
        weeks = get_mondays_between(today, future_date)
        for week in weeks:
            generate_logbook(week)

    elif args.dates:
        for date_str in args.dates:
            try:
                date = parse_date(date_str)
                generate_logbook(date)
            except ValueError:
                print(f"⚠️ Format de date invalide : {date_str} (attendu : YYYY-MM-DD)")
    else:
        generate_logbook(today)
    
    print("✅ Journal de bord généré avec succès.")


if __name__ == "__main__":
    main()
