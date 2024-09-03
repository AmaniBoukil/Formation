from datetime import datetime

# Exemple de chaînes de date/heure
time_str1 = '2024-07-03 18:50:13'
time_str2 = '2024-07-03 18:51:24'

# Convertir les chaînes en objets datetime
time1 = datetime.strptime(time_str1, '%Y-%m-%d %H:%M:%S')
time2 = datetime.strptime(time_str2, '%Y-%m-%d %H:%M:%S')

# Comparer les instants datetime
if time1 < time2:
    print(f"{time_str1} est antérieur à {time_str2}")
elif time1 > time2:
    print(f"{time_str1} est postérieur à {time_str2}")
else:
    print(f"{time_str1} et {time_str2} sont identiques")

# Calculer la différence entre deux instants datetime
time_difference = time2 - time1
print(f"Différence de temps : {time_difference}")