function formatDate(dt) {
    let y = dt.getFullYear();
    let m = ('00' + (dt.getMonth() + 1)).slice(-2)
    let d = ('00' + dt.getDate()).slice(-2)
    return (y + '-' + m + '-' + d)
}

function getAfterNDays(n) {
    let dt = new Date();
    dt.setDate(dt.getDate() + n);
    return formatDate(dt);
}

function alert_check() {
    let kind = document.getElementById('id_choice_kind')
    let paid_leave = document.getElementById('id_paid_leave')

    if (kind.value === '休暇希望') {
        console.log(paid_leave.value)
        let date_value = document.querySelector("#holiday_input > input[type=hidden]").value
        let date_reformat = date_value.toString()
        if (date_reformat === '') {
            alert('休暇希望日を入力してください')
            return false
        }
        for (let n = 0; n < 11; n++) {
            if (getAfterNDays(n) === date_reformat) {
                alert('休暇希望は10日前までの申請をお願いいたします')
                return false
            } else {

            }
        }
        if (paid_leave.value === '有給') {
            for (let n = 0; n < 15; n++) {
                if (getAfterNDays(n) === date_reformat) {
                    alert('有給希望は14日前までの申請をお願いいたします')
                    return false
                } else {

                }
            }
        }
    } else if (kind.value === '振替') {

        let makeup_holiday_value = document.querySelector("#makeup_holiday > input[type=hidden]").value
        let work_date_value = document.querySelector("#work_date > input[type=hidden]").value
        let kind_work_time = document.getElementById('id_work_time')

        let holiday_reformat = makeup_holiday_value.toString()
        let workdate_reformat = work_date_value.toString()

        let check_makeup_holiday = makeup_holiday_value.slice(5, -3)
        let check_date_value = work_date_value.slice(5, -3)

        if (holiday_reformat === '' || workdate_reformat === '') {
            alert('振替希望日を入力してください')
            return false
        } else if (kind_work_time.value === '') {
            alert('振替日の勤務時間を選択してください')
            return false
        }

        for (let n = 0; n < 11; n++) {
            if (getAfterNDays(n) === holiday_reformat || getAfterNDays(n) === workdate_reformat) {
                alert('振替希望は10日前までの申請をお願いいたします')
                return false
            } else {

            }
        }

        if (check_makeup_holiday === check_date_value) {
            return true;
        } else {
            alert('振替は同月内での申請をお願いいたします')
            work_date_value.value = '';
            work_date_value.value = '';
            return false;
        }

    }
}
