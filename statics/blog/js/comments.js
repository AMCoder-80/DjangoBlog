function test(id, state, values) {
    let elem = document.getElementById(id + state[0]);
    console.log(elem.innerText);
    console.log(elem.innerHTML);
}

function voting(id, state, user) {
    let clicked = document.getElementById(id + state[0]);
    let other = document.getElementById(id + state[1]);

    let icons = {
        '-like': '<i class="fa fa-thumbs-up"></i>',
        '-dislike': '<i class="fa fa-thumbs-down"></i>',
    }

    if (clicked.classList.contains('active')) {
        let req = new XMLHttpRequest();

        req.onload = function () {
            if (this.status === 200 && this.responseText === 'True') {
                clicked.classList.remove('active');
                clicked.innerHTML = icons[state[0]] + " " + (parseInt(clicked.innerText, 10) - 1)
            }
        }
        req.open('GET',
            '/toggle-like/?state=' + state[0] + '&operation=sub&user=' + user + '&pk=' + id, true);
        req.send();
    } else if (other.classList.contains('active')) {
        let req = new XMLHttpRequest();

        req.onload = function () {
            if (this.status === 200 && this.responseText === 'True') {
                other.classList.remove('active');
                clicked.classList.add('active');
                other.innerHTML = icons[state[1]] + " " + (parseInt(other.innerText, 10) - 1)
                clicked.innerHTML = icons[state[0]] + " " + (parseInt(clicked.innerText, 10) + 1)
            }
        }
        req.open('GET',
            '/toggle-like/?state=' + state[0] + '&operation=double&user=' + user + '&pk=' + id, true);
        req.send();
    } else {
        let req = new XMLHttpRequest();

        req.onload = function () {
            if (this.status === 200 && this.responseText === 'True') {
                clicked.classList.add('active');
                clicked.innerHTML = icons[state[0]] + " " + (parseInt(clicked.innerText, 10) + 1)
            }
        }
        req.open('GET',
            '/toggle-like/?state=' + state[0] + '&operation=add&user=' + user + '&pk=' + id, true);
        req.send();
    }
}

function reply(pk) {
    let parent = document.getElementById('id_parent').getElementsByTagName('option');

    for (let i = 0; i < parent.length; i++) {
        parent[i].selected = parent[i].value === pk.toString();
    }
}

function del(pk){
    let delete_req = new XMLHttpRequest();
    delete_req.onload = function (){
        if(this.responseText === 'OK' && this.status === 200){
            window.location.reload();
        }
    }
    delete_req.open('GET', '/delete-comment/?pk='+pk, true);
    delete_req.send();
}