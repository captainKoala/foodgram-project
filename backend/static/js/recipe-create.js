const INGREDIENT_FIELDS_PREFIX = "ingredient";


const addClasses = (element, classesString) => {
    /** Добавляет элементу классы из строки classesString. Классы
     * разделены пробелами
     * */
    for (let cl of classesString.split(" "))
        element.classList.add(cl);
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

const createSelect = (selectClasses, selectId, selectName) => {
    /** Создает элемент select с классами selectClasses,
     * идентификатором selectId, и атрибутом name - selectName.
     * Классы передаются в виде строки, разделить - пробел.
     * **/
    let select = document.createElement("select");
    addClasses(select, selectClasses);

    select.id = selectId;
    select.setAttribute("name", selectName);
    let option = document.createElement("option");
    option.textContent = "---------";
    select.appendChild(option);

    return select;
}

const createInput = (inputType, inputClasses, inputName, inputId) => {
    /** Создает input с типом inputType, классами inputClasses,
     * атрибутом name - inputName и идентификатором inputId.
     * Классы передаются в виде строки, разделить - пробел.
     * */
    let input = document.createElement("input");
    addClasses(input, inputClasses);
    input.id = inputId;
    input.setAttribute("name", inputName);

    return input;
}

const createLabelDiv = (text, classes) => {
    let labelWrap = document.createElement("div");
    addClasses(labelWrap, classes);
    labelWrap.textContent = text;
    return labelWrap;
}

const createSelectDiv = (classes, innerWrapClasses, selectClasses,
                         selectName, selectId) => {
    let select = createSelect(selectClasses, selectId, selectName);
    let innerWrap = createWrap(select, innerWrapClasses);
    return createWrap(innerWrap, classes);
}

const createInputDiv = (inputType, classes, inputClasses, inputName, inputId) => {
    let input = createInput(inputType, inputClasses, inputName, inputId);
    return createWrap(input, classes);
}

const addIngredientFormFields = (container) => {
    /** Добавление полей для выбора ингридиента и его количества в формсет
     * (container). */
    let totalFormsInput = document.querySelector(`#id_${INGREDIENT_FIELDS_PREFIX}-TOTAL_FORMS`);
    let maxNumFormsInput = document.querySelector(`#id_${INGREDIENT_FIELDS_PREFIX}-MAX_NUM_FORMS`);

    let index = +totalFormsInput.value;

    if (+totalFormsInput.value === +maxNumFormsInput.value) {
        alert("Добавлено максимальное количество ингредиентов!");
        return
    }

    // Создание элемента select для выбора ингридиентов и его подписи
    let selectLabel = createLabelDiv("Ингредиент", "col-5");
    let select = createSelectDiv("col-7", "form-control",
        "dropdown-menu", `${INGREDIENT_FIELDS_PREFIX}-${index}-ingredient`,
        `id_${INGREDIENT_FIELDS_PREFIX}-${index}-ingredient`);
    let outerSelectWrap = createWrap([selectLabel, select],
        "form-group row my-2");
    // Создание элемента input для ввода количества ингридиентов и его подписи
    let inputLabel = createLabelDiv("Количество", "col-5");
    let input = createInputDiv("number", "col-7", "form-control",
        `${INGREDIENT_FIELDS_PREFIX}-${index}-amount`,
        `id_${INGREDIENT_FIELDS_PREFIX}-${index}-amount`);
    let outerInputWrap = createWrap([inputLabel, input],
        "form-group row my-2");
    // Создание кнопки удаления
    let button = document.createElement("a");
    button.textContent="Удалить ингредиент";
    addClasses(button, "btn btn-light remove-ingredient-button")
    let buttonWrap = createWrap(button, "my-2 text-right");
    // Общая обертка для полей выбора ингридиента, ввода его количества, кнопки
    let wrap = createWrap([outerSelectWrap, outerInputWrap, buttonWrap],
        "add-ingredient-container border my-2 p-2 border-light-rounded");
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
    select.id = `#id_${INGREDIENT_FIELDS_PREFIX}-${newIndex}-ingredient`;
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
        alert(`Должно быть не менее ${+totalFormsInput.value} ингридиентов.`);
        return;
    }

    const container = removeBtn.closest(".add-ingredient-container");
    let index = +container.id.replace("container-id_ingredient-", "").replace("-ingredient", "");
    container.remove();
    for (let i = index + 1; i < +totalFormsInput.value; i++)
        changeIngredientIndex(i, i - 1);

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