const parseRGBFunctionString = color => {
    let openBracket = color.indexOf("(");
    let closeBracket = color.indexOf(")");

    if (openBracket !== -1 && closeBracket !== -1)
        return (color.substring(openBracket+1, closeBracket)
            .split(",").map(item => +item));
    return null;
}

const makeRGBFunctionString = rgb => {
    return `rgba(${rgb.join(", ")})`
}

const makeRGBAFunctionString = (rgb, opacity) => {
    return `rgba(${rgb.join(", ")}, ${opacity})`
}

const isLightColor = color => {
    /**
     * Определяет является ли цвет "очень светлым" :)
     * */
    let sum = 0;
    color.forEach(item => sum+=item)
    let avg = sum / 3;
    return avg > 222;
}

const darkenLightColors = color => {
    /**
     * Делает "очень светлые" цвета темнее.
     * Принимает цвет в виде массива из трех числовых компонентов RGB.
     * */
    return color.map(item => item - 64);
}

const setTagsColors = tag => {
    let color = tag.style.color;

    let rgb = parseRGBFunctionString(color);
    let rgbBG = rgb;
    let opacity = 0.2;

    if (isLightColor(rgb)) {
        rgbBG = darkenLightColors(rgb);
        opacity = 1;
    }

    tag.style.color = makeRGBFunctionString(rgb);
    tag.style.backgroundColor = makeRGBAFunctionString(rgbBG, opacity);
}

const setTagsFilterBGColor = tag => {
    let color = tag.style.color;
    let rgb = parseRGBFunctionString(color);

    if (isLightColor(rgb))
        rgb = darkenLightColors(rgb);
    tag.style.color = makeRGBFunctionString(rgb);
}

document.addEventListener("DOMContentLoaded", event => {
    const tags = document.querySelectorAll(".tags-list-item");
    const tagsFilter = document.querySelectorAll(".tags-filter-item");

    for (let tag of tags)
        setTagsColors(tag);
    for (let tag of tagsFilter)
        setTagsFilterBGColor(tag);
})