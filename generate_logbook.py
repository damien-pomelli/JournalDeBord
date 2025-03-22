# Crée un journal de bord dans le dossier Logbook sous la forme
# de fichiers Mardown pour chaque semaine de l'année.
# Les fichiers sont nommés "YYYY-MM-DD.md" et sont contenus dans
# un dossier "MM" pour chaque mois de l'année.
# Les fichiers sont générés avec un template Markdown et pour
# la semaine en cours par défaut. Le lancement du script peut être suivi d'arguements
# pour spécifier une ou plusieurs semaines à générer. Le nombre XX de la semaine
# dans le template est remplacé par le numéro de la semaine dans l'année.


# A AMELIORER
# - Remplacer jours et mois car le mois peut changer en fonction du jour
# - Simplifier le code et rendre plus robuste les arguments
# - Ajouter les dossiers pour les années et un num avant le mois pour l'ordre

import os
import sys
import datetime

template_path = "template.md"
logbook_folder_path = "LogBook"

def get_week_number(date):
    return date.strftime("%U")

def get_week_day(date):
    return date.strftime("%d")

def get_week_date(date):
    return date.strftime("%Y-%m-%d")

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
    return month_names[month_number]

# Générer le numéro de tous les jours de la semaine
def get_week_days(date):
    # Ajuster la date pour qu'elle corresponde au lundi de la semaine
    start_of_week = date - datetime.timedelta(days=date.weekday())
    week_dates = []
    for i in range(7):
        week_dates.append(get_week_day(start_of_week + datetime.timedelta(days=i)))
    return week_dates

def get_week_year(date):
    return date.strftime("%Y")

def get_week_template():
    with open(template_path, "r") as file:
        return file.read()
    
# Remplacer le template par les informations de la semaine
def replace_week_template(template, week_number, week_days, week_month, week_year):
    template = template.replace("XX", week_number)
    template = template.replace("LU", week_days[0])
    template = template.replace("MA", week_days[1])
    template = template.replace("ME", week_days[2])
    template = template.replace("JE", week_days[3])
    template = template.replace("VE", week_days[4])
    template = template.replace("SA", week_days[5])
    template = template.replace("DI", week_days[6])
    template = template.replace("MM", week_month)
    template = template.replace("YYYY", week_year)
    return template

def get_week_file_path(date):
    # Récupère le chemin du fichier de la semaine
    # Le nom du fichier est "YYYY-MM-DD.md" où DD est 
    # le numéro du jour de la semaine du lundi de cette semaine
    week_number = get_week_number(date)
    week_month_fr = get_week_month_fr(date)
    week_file_name = f"Week {week_number}.md"
    week_folder_path = os.path.join(logbook_folder_path, week_month_fr)
    week_file_path = os.path.join(week_folder_path, week_file_name)
    return week_file_path

def create_week_folder(date):
    # Crée le dossier du mois si il n'existe pas
    # Le nom du dossier est le numéro du mois en français
    week_month_fr = get_week_month_fr(date)
    week_folder_path = os.path.join(logbook_folder_path, week_month_fr)
    if not os.path.exists(week_folder_path):
        os.makedirs(week_folder_path)

def create_week_file(date):
    week_template = get_week_template()
    week_file_path = get_week_file_path(date)
    week_number = get_week_number(date)
    week_day = get_week_day(date)
    week_days = get_week_days(date)
    week_month = get_week_month(date)
    week_year = get_week_year(date)
    week_content = replace_week_template(week_template, week_number, week_days, week_month, week_year)
    with open(week_file_path, "w") as file:
        file.write(week_content)

def generate_logbook():
    date = datetime.datetime.now()
    create_week_folder(date)
    create_week_file(date)
    # Lis les arguments pour générer des semaines spécifiques
    # Si l'argument -all est présent, génère toutes les semaines 
    # jusqu'à la date passée en argument
    if "-all" in sys.argv:
        if len(sys.argv) > 2:
            date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d")
        # else:
        #     date = datetime.datetime.now()
        for i in range(1, int(get_week_number(date)) + 1):
            week_date = date - datetime.timedelta(days=date.weekday()) + datetime.timedelta(weeks=i)
            create_week_folder(week_date)
            create_week_file(week_date)
    else:
        for arg in sys.argv[1:]:
            #if arg.isdigit():
            date = datetime.datetime.strptime(arg, "%Y-%m-%d")
            create_week_folder(date)
            create_week_file(date)

    # if len(sys.argv) > 1:
    #     for arg in sys.argv[1:]:
    #         date = datetime.datetime.strptime(arg, "%Y-%m-%d")
    #         create_week_folder(date)
    #         create_week_file(date)

if __name__ == "__main__":
    generate_logbook()
