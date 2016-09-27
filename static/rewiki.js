
var PREFIX = "/";

var simplemde;

function get_page() {
    return window.location.hash.substr(1);
}

function set_title(title) {
    document.getElementById("title").setAttribute("value", title);
}

function submitEditor() {
    fetch(PREFIX + 'content/' + get_page(), {
        method: 'post',
        body: JSON.stringify({
            content: simplemde.value()
        }),
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    }).then(function(response) {
        console.log(response.statusCode + " " + response.statusText);
        document.getElementById("status").innerHTML = "<p>OK</p>";
        document.getElementById("status").style.display = "block";
    }).catch(function(err) {
        console.error("Got error, " + err);
    })
}


function loading () {
    simplemde = new SimpleMDE({ element: document.getElementById("editor") });
    var path = get_page();
    if (path !== null) {
        set_title(path);
        fetch(PREFIX + 'content/' + path + '/_content', {
            method: 'get'
        }).then(function (response) {
            response.text().then(function (content) {
                console.log("foo");
                console.log(content);
                simplemde.value(content);
            }, function (err) {
                console.log("error: " + err);
            })
        }).catch(function (err) {
            console.error("Got error," + err);
        });

    }
}

window.onload = loading;