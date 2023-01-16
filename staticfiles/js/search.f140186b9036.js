let keyword = document.getElementById('base_search')
let base = document.getElementsByClassName('base')
let table_box = document.getElementsByClassName('table_box')

keyword.addEventListener('input', () => {
    for (let i = 0; i < base.length; i++) {
        if (keyword.value === base[i].innerHTML) {
            table_box[i].style.display = ''
        } else {
            table_box[i].style.display = 'none'
        }
    }
})