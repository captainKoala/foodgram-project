USERS_URL = "/api/users/"
USERS_ME_URL = USERS_URL + "me/"
USERS_SET_PASSWORD_URL = USERS_URL + "set_password/"
TAGS_LIST_URL = "/api/tags/"
RECIPES_URL = "/api/recipes/"

USER_DATA_1 = {
    "username": "test_user_1",
    "first_name": "Test",
    "last_name": "User",
    "email": "test_user@ex.com",
    "password": "passwordPhrase_1234",
}
USER_DATA_2 = {
    "username": "test_user_2",
    "first_name": "Second",
    "last_name": "User",
    "email": "test_user_2@ex.com",
    "password": "very_strong_Password_1234",
}

TAG_DATA_1 = {
    "name": "tag1",
    "color": "#ffaacc",
    "slug": "tag1"
}
TAG_DATA_2 = {
    "name": "tag2",
    "color": "#1199FF",
    "slug": "tag2"
}

INGREDIENT_DATA_1 = {
    "name": "first ingredient",
    "measurement_unit": "unit 1"
}
INGREDIENT_DATA_2 = {
    "name": "second ingredient",
    "measurement_unit": "unit 2"
}
INGREDIENT_DATA_3 = {
    "name": "second ingredient",
    "measurement_unit": "unit 2"
}

RECIPE_DATA_1 = {
    "ingredients": [
        {
            "id": 1,
            "amount": 250,
        },
        {
            "id": 2,
            "amount": 300,
        }
    ],
    "tags": [1, 2],
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABiey"
             "waAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACk"
             "lEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
    "name": "First recipe",
    "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis "
            "ullamcorper mattis ligula sit amet ullamcorper. Curabitur non "
            "ultricies diam.",
    "cooking_time": 15,
}
