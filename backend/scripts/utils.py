import csv

from api.models import Ingredient


def import_ingredients(csv_file):
    """
    Импорт списка ингредиентов из CSV-файла (разделитель - запятая).
    В CSV-файле должны быть два столбца с данными (без заголовков):
    наименование ингредиента, единица измерения.
    """
    with open(csv_file) as f:
        reader = csv.reader(f)
        for row in reader:
            new_ingredient = Ingredient(
                name=row[0],
                measurement_unit=row[1],
            )
            new_ingredient.save()
