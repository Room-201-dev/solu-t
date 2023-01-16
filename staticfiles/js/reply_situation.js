window.addEventListener('load', () => {
    let reply = document.getElementsByClassName('reply_situation')
    let reply_box = document.getElementsByClassName('reply_box')
    for (let i = 0; i < reply.length; i++) {
        if (reply[i].innerHTML === '返信待ち') {
            reply[i].style.backgroundColor = '#d50707'
        }
        else if(reply[i].innerHTML === '解決済み') {
            reply[i].style.backgroundColor = '#fff'
            reply[i].style.color = '#587D9F'
            reply_box[i].style.backgroundColor = '#587D9F'
            reply_box[i].style.color = '#fff'
        }
    }
})