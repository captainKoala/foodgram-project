const LINKS_PER_PAGINATOR = 5;

const createPaginatorItem = (pageNumber, isActive=false, isDisabled=false,
                             itemText="", url="", params="") => {
    /**
     * Создает элемент паджинатора li со ссылкой.
     * Возвращает соответствующий HTML-элемент.
     */
    console.log(params)
    let li = document.createElement("li");
    let a = document.createElement("a");

    li.classList.add("page-item");
    if (isActive)
        li.classList.add("active");

    if (isDisabled)
        li.classList.add("disabled");

    a.classList.add("page-link");
    a.href = url ? url : `?page=${pageNumber}&${params}`;
    a.textContent = itemText ? itemText : pageNumber;

    li.appendChild(a);
    return li;
}

document.addEventListener("DOMContentLoaded", event => {
    const paginator = document.querySelector(".pagination");

    if (paginator)
    {
        const numPages = +paginator.dataset.numPages;
        const currentPage = +paginator.dataset.currentPage;
        let params = paginator.dataset.params;

        if (!numPages || !currentPage)
            return;

        if (numPages > LINKS_PER_PAGINATOR)
            paginator.appendChild(createPaginatorItem(1, false,
                currentPage === 1, "<<", "", params));
        paginator.appendChild(createPaginatorItem(currentPage - 1, false,
            currentPage === 1, "<", "", params));

        let startPageNumber = currentPage - Math.floor(LINKS_PER_PAGINATOR/2);
        let endPageNumber = currentPage + Math.floor((LINKS_PER_PAGINATOR-1)/2);

        if (startPageNumber < 1) {
            endPageNumber += 1 - startPageNumber;
            startPageNumber = 1;
        }
        if (endPageNumber > numPages)
            endPageNumber = numPages;

        while (endPageNumber - startPageNumber + 1 < LINKS_PER_PAGINATOR && startPageNumber > 1)
            startPageNumber--;

        for (let i = startPageNumber; i <= endPageNumber; i++) {
            paginator.appendChild(
                createPaginatorItem(i, i === currentPage, false, false,
                    i === currentPage ? "#" : "", params));
        }

        paginator.appendChild(
            createPaginatorItem(currentPage + 1, false,
                currentPage === numPages, ">", "", params));
        if (numPages > LINKS_PER_PAGINATOR)
            paginator.appendChild(
                createPaginatorItem(numPages, false,
                    currentPage === numPages, ">>", "", params));
    }
})
