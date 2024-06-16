import json

# Charger les données depuis db.json
with open('db.json', 'r') as file:
    data = json.load(file)

# Supprimer l'entrée de ContentType avec app_label "app" et model "message"
data = [item for item in data if not (item.get('model') == 'contenttypes.contenttype' and 
                                      item.get('pk') == 4 and 
                                      item.get('fields', {}).get('app_label') == 'app' and 
                                      item.get('fields', {}).get('model') == 'logentry')]

# Enregistrer les modifications dans le fichier db.json
with open('db.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Entrée en double supprimée avec succès dans db.json.")


"""import json

# Chargement des données depuis le fichier db.json
with open('db.json', 'r') as file:
    data = json.load(file)

# Liste pour stocker les IDs déjà rencontrés
permission_ids = set()
content_type_ids = set()

# Liste pour stocker les éléments à conserver
cleaned_data = []

# Parcours des données pour supprimer les doublons
for item in data:
    if item['model'] == 'auth.permission':
        permission_id = item['pk']
        # Vérification si l'ID de permission est déjà rencontré
        if permission_id not in permission_ids:
            permission_ids.add(permission_id)
            cleaned_data.append(item)
    elif item['model'] == 'contenttypes.contenttype':
        content_type_id = item['pk']
        # Vérification si l'ID de type de contenu est déjà rencontré
        if content_type_id not in content_type_ids:
            content_type_ids.add(content_type_id)
            cleaned_data.append(item)
    else:
        cleaned_data.append(item)

# Enregistrement des données nettoyées dans le fichier db_cleaned.json
with open('db_cleaned.json', 'w') as file:
    json.dump(cleaned_data, file, indent=4)

print("Doublons supprimés avec succès. Les données nettoyées ont été enregistrées dans db_cleaned.json.")
"""
