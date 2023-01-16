let kind = document.getElementById('id_choice_kind')
let behind_time = document.getElementById('id_behind_work')
let behind_exit = document.getElementById('id_behind_exit')
let change_input = document.getElementsByClassName('change_input')
let holiday_input = document.getElementById('holiday_input')
let switch_display = document.getElementsByClassName('switch_display')
let current = document.getElementById('current')
let apply = document.getElementById('apply')


kind.addEventListener('change', () => {
    if (kind.value === '遅刻') {
        for (let i = 0; i < change_input.length; i++) {
            change_input[i].style.height = 'auto'
            change_input[i].style.marginBottom = '1%'
            change_input[i].style.textAlign = 'left'
            change_input[i].style.display = 'flex'
            change_input[i].style.paddingTop = '8px'
            change_input[i].style.paddingBottom = '8px'
            change_input[i].style.borderBottom = '0.5px solid #bdbdbd'
            behind_time.required = 'required'
            behind_exit.required = 'required'
        }
    } else if (kind.value === '振替' || kind.value === '振替 希望') {
        let text_delete = document.getElementById('id_date')
        let paid_leave = document.getElementById('paid_leave')
        let id_paid_leave = document.getElementById('id_paid_leave')
        let value_delete = document.querySelector("#holiday_input > input[type=hidden]")
        text_delete.value = ''
        value_delete.value = ''
        id_paid_leave.value = ''
        for (let i = 0; i < change_input.length; i++) {
            change_input[i].style.height = 'auto'
            change_input[i].style.marginBottom = '1%'
            change_input[i].style.textAlign = 'left'
            change_input[i].style.display = 'flex'
            change_input[i].style.paddingTop = '8px'
            change_input[i].style.paddingBottom = '8px'
            change_input[i].style.borderBottom = '0.5px solid #bdbdbd'
            holiday_input.style.display = 'none'
            paid_leave.style.display = 'none'
        }
    } else if (kind.value === '休暇希望' || kind.value === '休暇 希望') {
        let holiday_delete = document.querySelector("#makeup_holiday > input[type=hidden]")
        let holiday_text_delete = document.getElementById('id_holiday_date')
        let workday_delete = document.querySelector("#work_date > input[type=hidden]")
        let workday_text_delete = document.getElementById('id_work_date')
        let worktime_delete = document.getElementById('id_work_time')
        let paid_leave = document.getElementById('paid_leave')
        holiday_text_delete.value = ''
        workday_text_delete.value = ''
        holiday_delete.value = ''
        workday_delete.value = ''
        worktime_delete.value = ''
        holiday_input.style.display = 'flex'
        paid_leave.style.display = 'flex'
        for (let i = 0; i < change_input.length; i++) {
            change_input[i].style.display = 'none'
        }
    } else if (kind.value === '欠勤') {
        for (let i = 0; i < change_input.length; i++) {
            change_input[i].style.display = 'none'
            behind_time.required = false
            behind_exit.required = false
        }
    } else if (kind.value === 'リフレッシュ休暇') {
        let holiday_delete = document.querySelector("#makeup_holiday > input[type=hidden]")
        let holiday_text_delete = document.getElementById('id_early_date')
        let workday_text_delete = document.getElementById('id_early_work')
        holiday_text_delete.value = ''
        workday_text_delete.value = ''
        holiday_delete.value = ''
        holiday_input.style.display = 'flex'
        for (let i = 0; i < change_input.length; i++) {
            change_input[i].style.display = 'none'
        }
    } else if (kind.value === '時短') {
        let value_delete = document.querySelector("#holiday_input > input[type=hidden]")
        value_delete.value = ''
        for (let i = 0; i < change_input.length; i++) {
            change_input[i].style.height = 'auto'
            change_input[i].style.marginBottom = '1%'
            change_input[i].style.textAlign = 'left'
            change_input[i].style.display = 'flex'
            change_input[i].style.paddingTop = '8px'
            change_input[i].style.paddingBottom = '8px'
            change_input[i].style.borderBottom = '0.5px solid #bdbdbd'
            holiday_input.style.display = 'none'
        }
    } else if (kind.value === '') {
        for (let i = 0; i < switch_display.length; i++) {
            switch_display[i].style.setProperty('display', 'none', 'important')
        }
    } else if (kind.value === '変更無し') {
        apply.style.setProperty('display', 'none', 'important')
        current.style.setProperty('display', 'block', 'important')
    } else if (kind.value === '変更希望') {
        current.style.setProperty('display', 'none', 'important')
        apply.style.setProperty('display', 'block', 'important')
    }
})
