"use strict";

document.addEventListener("DOMContentLoaded", e => {
    let tagLinks = document.querySelectorAll(".tags-filter-item");

    const clickTagFilter = event => {
        let currentLink = event.target.closest("a");
        let params = [];

        if (currentLink.dataset.isselected === "true")
            currentLink.dataset.isselected = "false"
        else
            currentLink.dataset.isselected = "true";

        for (let link of tagLinks) {
            if (link.dataset.isselected === "true")
                params.push("tags=" + link.dataset.slug);
        }
        if (params.length === 0)
            params.push("tags=__none__")
        else if (params.length === tagLinks.length)
            params = [];
        if (params)
            currentLink.href = "?" + params.join("&");
    }

    for (let link of tagLinks)
        link.addEventListener("click", clickTagFilter);
})
