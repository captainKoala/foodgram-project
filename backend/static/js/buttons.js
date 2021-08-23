function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const makeFetch = async (request, options)  => {
    return fetch(request, options)
        .then(async response => {
            if (response.status === 201)
                return response.json();
            if (response.status === 204)
                return {"detail": "Запись удалена."}
            if (!response.ok)
                response = `${response.status} ${response.statusText}`
                return {"error": response}
        })
        .catch(error => console.log("Error: " + error))
}

const toggleButtonsHandler = (currentBtn, url) => {
    /**
     * Делает запрос к серверу на изменение состояния кнопки
     * и переключает кнопки на странице.
     * Например, кнопка Подписаться/Отписаться
     * */
    const csrftoken = getCookie('csrftoken');
    const request = new Request(
        url, {headers: {"X-CSRFToken": csrftoken}});

    const options = currentBtn.dataset.is_selected === "true" ?
        {method: "DELETE", mode: "same-origin"} :
        {method: "GET", mode: "same-origin"};

    makeFetch(request, options)
        .then(response => {
            if (response["error"])
                console.log(response["error"])
            else
                for (let elem of currentBtn.parentElement.children)
                {
                    elem.classList.toggle("d-none");
                    elem.classList.toggle("d-block");
                }
        })
        .catch()
}

const updateCounter = (selector, diff) => {
    const countSpans = document.querySelectorAll(selector);
    for (let span of countSpans) {
        let count = +span.textContent + diff;
        span.textContent = count;
        if (count === 0)
            span.classList.add("d-none");
        else
            span.classList.remove("d-none");
    }
}

const shoppingCartHandler = (event) => {
    /**
     * Нажатие кнопки добавить/удалить из списка покупок.
     * */
    event.preventDefault();

    const currentBtn = event.target.closest("a");

    let diff = currentBtn.dataset.is_selected === "true" ? -1 : 1;
    updateCounter(".shopping-cart-count", diff);

    const recipeID = currentBtn.dataset.recipeid;
    const url = `/recipes/${recipeID}/shopping_cart/`;

    toggleButtonsHandler(currentBtn, url);
}

const favoritesHandler = event => {
    /**
     * Нажатие кнопки добавть/удалить из избранного.
     * */
    event.preventDefault();

    const currentBtn = event.target.closest("a");

    let diff = currentBtn.dataset.is_selected === "true" ? -1 : 1;
    updateCounter(".favorites-count", diff);

    const recipeID = currentBtn.dataset.recipeid;
    const url = `/recipes/${recipeID}/favorite/`;

    toggleButtonsHandler(currentBtn, url);
}

const followAuthorHandler = event => {
    /**
     * Нажатие кнопки подписаться/отписаться от автора.
     * */
    event.preventDefault();

    const currentBtn = event.target.closest("a");
    const authorID = currentBtn.dataset.authorid;
    const url = `/users/${authorID}/subscribe/`

    toggleButtonsHandler(currentBtn, url);
}

document.addEventListener("DOMContentLoaded", event => {
    /**
     * Добавление слушателей событий нажатия на все кнопки избранного и подписок.
     * */
    const favoriteButtons = document.querySelectorAll(".in-favorite");
    const shoppingCartButtons = document.querySelectorAll(".btn-shopping-cart");
    const followAuthorButtons = document.querySelectorAll(".btn-follow-author")


    for (let btn of favoriteButtons)
        btn.addEventListener("click", favoritesHandler);
    for (let btn of shoppingCartButtons)
        btn.addEventListener("click", shoppingCartHandler);
    for (let btn of followAuthorButtons)
        btn.addEventListener("click", followAuthorHandler);
})
