const INGREDIENT_FIELDS_PREFIX = "ingredient";
const INGREDIENT_LABEL = "Ингредиент";
const INGREDIENT_HELP_TEXT = "Выберите ингредиент";
const AMOUNT_LABEL = "Количество";
const AMOUNT_HELP_TEXT = "Введите количество";
const INGREDIENT_BTN_TEXT = "Удалить ингредиент";


const addClasses = (element, classesString) => {
    /** Добавляет элементу классы из строки classesString. Классы
     * разделены пробелами
     * */
    for (let cl of classesString.split(" "))
        element.classList.add(cl);
}

const createHtmlElement = (tag, textContent="", options={}) => {
    /** Создание HTML-элемента по тегу tag, с добавлением текстового содержимого
     * textContent.
     * options - объект, содержащий id - идентификатор, classes - строка с
     * CSS-классами, разделенными пробелами, attributes - массив атрибутов,
     * состоящий из массивов размером по 2 элемента (атрибут - значение).
     */
    let element = document.createElement(tag);
    element.textContent = textContent;
    if (options["id"])
        element.id = options["id"];
    if (options["classes"])
        addClasses(element, options["classes"]);
    if (options["attributes"])
        for (let attribute of options["attributes"])
            element.setAttribute(attribute[0], attribute[1]);
    return element;
}

const createWrap = (to_wrap, wrapClasses) => {
    /**
     * Создание обертки div с классами wrapClasses над элементом (или списком
     * элементов) to_wrap.
     * to_wrap - html-элемент или массив из html-элементов.
     * Классы передаются в виде строки, разделить - пробел.
     * */
    let wrap = document.createElement("div");
    addClasses(wrap, wrapClasses);

    if (Array.isArray(to_wrap))
        for (let element of to_wrap)
            wrap.appendChild(element);
    else
        wrap.appendChild(to_wrap);
    return wrap;
}

const addIngredientFormFields = (container) => {
    /** Добавление полей для выбора ингридиента и его количества в формсет
     * (container). */
    let totalFormsInput = document.querySelector(`#id_${INGREDIENT_FIELDS_PREFIX}-TOTAL_FORMS`);
    let maxNumFormsInput = document.querySelector(`#id_${INGREDIENT_FIELDS_PREFIX}-MAX_NUM_FORMS`);

    let index = +totalFormsInput.value;

    if (+totalFormsInput.value === +maxNumFormsInput.value) {
        $("#maxLimitError").modal({keyboard: true})
        return
    }

    // Создание элемента select для выбора ингридиентов и его подписи
    let selectLabel = createHtmlElement("div", INGREDIENT_LABEL, {"classes": "col-12 col-sm-5"});
    let select = createHtmlElement("select", "", {
        "classes": "dropdown-menu",
        "id": `id_${INGREDIENT_FIELDS_PREFIX}-${index}-ingredient`,
        "attributes": [
            ["name", `${INGREDIENT_FIELDS_PREFIX}-${index}-ingredient`],
        ]
    });
    let option = createHtmlElement("option", "---------");
    select.appendChild(option);
    let innerSelectWrap = createWrap(select, "form-control select2-custom-container");
    let selectWrap = createWrap(innerSelectWrap, "col-12 col-sm-7");
    let outerSelectWrap = createWrap([selectLabel, selectWrap],
        "form-group row my-2");
    // Создание блока с подсказкой для выбора ингредиентов
    let selectHelpText = createHtmlElement("small", INGREDIENT_HELP_TEXT, {"classes": "form-text"});
    let selectHelpTextWrap = createWrap(selectHelpText, "col-12 col-sm-7 offset-sm-5");

    // Создание элемента input для ввода количества ингридиентов и его подписи
    let inputLabel = createHtmlElement("div", AMOUNT_LABEL, {"classes": "col-5"});
    let input = createHtmlElement("input", "", {
        "classes": "form-control",
        "id": `id_${INGREDIENT_FIELDS_PREFIX}-${index}-amount`,
        "attributes": [
            ["name", `${INGREDIENT_FIELDS_PREFIX}-${index}-amount`],
            ["type", "number"],
        ]
    });
    let innerInputWrap = createWrap(input, "col-7");
    let outerInputWrap = createWrap([inputLabel, innerInputWrap],
        "form-group row my-2");

    // Создание блока с подсказкой для выбора количества ингредиента
    let inputHelpText = createHtmlElement("small", AMOUNT_HELP_TEXT, {"classes": "form-text"});
    let inputHelpTextWrap = createWrap(inputHelpText, "col-12 col-sm-7 offset-sm-5");

    // Создание кнопки удаления
    let button = createHtmlElement("a", INGREDIENT_BTN_TEXT,
        {"classes": "btn btn-light remove-ingredient-button d-block"});
    let buttonInnerWrap = createWrap(button, "col col-sm-7 offset-sm-5")
    let buttonWrap = createWrap(buttonInnerWrap, "row my-2 text-right");
    button.addEventListener("click", event => {
            event.preventDefault();
            removeIngredientFormFields(event.target)
        });

    // Общая обертка для полей выбора ингридиента, ввода его количества, кнопки
    let wrap = createWrap([outerSelectWrap, selectHelpTextWrap,
            outerInputWrap, inputHelpTextWrap, buttonWrap],
        "add-ingredient-container border my-2 p-2 border-light rounded");
    wrap.id = `container-id_${INGREDIENT_FIELDS_PREFIX}-${index}-ingredient`;

    container.appendChild(wrap);

    totalFormsInput.value = index + 1;

    return wrap;
}

const changeIngredientIndex = (currentIndex, newIndex) => {
    const container = document.querySelector(
        `#container-id_${INGREDIENT_FIELDS_PREFIX}-${currentIndex}-ingredient`);
    container.id = `container-id_${INGREDIENT_FIELDS_PREFIX}-${newIndex}-ingredient`;

    const select = container.querySelector(
        `#id_${INGREDIENT_FIELDS_PREFIX}-${currentIndex}-ingredient`);
    select.id = `id_${INGREDIENT_FIELDS_PREFIX}-${newIndex}-ingredient`;
    select.setAttribute("name", `${INGREDIENT_FIELDS_PREFIX}-${newIndex}-ingredient`)
    select.setAttribute("data-select2-id",
        `select2-data-id_${INGREDIENT_FIELDS_PREFIX}-${newIndex}-ingredient`);


    const select2span = container.querySelector(".select2-selection");
    select2span.setAttribute("aria-labelledby",
        `select2-id_${INGREDIENT_FIELDS_PREFIX}-${newIndex}-ingredient-container`);
    select2span.setAttribute("aria-controls",
        `select2-id_${INGREDIENT_FIELDS_PREFIX}-${newIndex}-ingredient-container`)

    const select2innerSpan = select2span.querySelector(
        `#select2-id_${INGREDIENT_FIELDS_PREFIX}-${currentIndex}-ingredient-container`);
    select2innerSpan.id = `select2-id_${INGREDIENT_FIELDS_PREFIX}-${newIndex}-ingredient-container`;

    container.querySelector(`input[name=${INGREDIENT_FIELDS_PREFIX}-${newIndex}-amount]`)
}

const removeIngredientFormFields = (removeBtn) => {
    let totalFormsInput = document.querySelector(`#id_${INGREDIENT_FIELDS_PREFIX}-TOTAL_FORMS`);
    let minNumFormsInput = document.querySelector(`#id_${INGREDIENT_FIELDS_PREFIX}-MIN_NUM_FORMS`);

    if (+totalFormsInput.value <= +minNumFormsInput.value) {
        $("#minLimitError").modal({keyboard: true});
        return;
    }

    const container = removeBtn.closest(".add-ingredient-container");
    let index = +container.id.replace("container-id_ingredient-", "").replace("-ingredient", "");
    container.remove();
    for (let i = index + 1; i <= +totalFormsInput.value; i++)
        changeIngredientIndex(i, i - 1);

    console.log("totalFormsInput.value:", totalFormsInput.value);
    totalFormsInput.value = +totalFormsInput.value - 1;
}

const addSelect2 = elements => {
    /** Добавление к элементам elements элемента поиска по списку из select2. **/
    elements.select2({
        language: "ru",
        ajax: {
            url: "/ingredients/",
            dataType: "json",
            processResults: function(data) {
                return {
                    results: $.map(data, function (item) {
                        return {id: item.id, text: item.name}
                    })
                }
            }
        },
        minimumInputLength: 2
    });
}

document.addEventListener("DOMContentLoaded", event => {
    const formset = document.querySelector("#ingredients-formset");
    const addIngredientBtn = document.querySelector("#add-ingredient-button");
    const removeIngredientBtns = document.querySelectorAll(
        ".remove-ingredient-button");

    addIngredientBtn.addEventListener("click", event => {
        event.preventDefault();
        let selectContainer = addIngredientFormFields(formset);
        let select = $(selectContainer).find("select");
        addSelect2(select);
    });

    for (let btn of removeIngredientBtns)
        btn.addEventListener("click", event => {
            event.preventDefault();
            removeIngredientFormFields(event.target)
        })

    // Добавление выпадающего меню с поиском на выбор ингредиентов
    addSelect2($("#ingredients-formset select"));
})