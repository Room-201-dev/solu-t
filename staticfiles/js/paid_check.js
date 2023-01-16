window.addEventListener('load', () => {
    let table_box = document.getElementsByClassName('table_box')
    let paid_leave = document.getElementsByClassName('paid_leave')
    for (let i = 0; i < paid_leave.length; i++) {
        if (paid_leave[i].innerHTML === '有給') {
            let child_table = table_box[i].childElementCount
            table_box[i].style.backgroundColor = '#587D9F'
            for (let n = 0; n < child_table; n ++) {
                table_box[i].children[n].style.color = '#fff'
            }
        }
    }
})
