function delete_quote(quote_id) {
    if (!window.confirm(`Delete ${quote_id}?`)) {
        return;
    }

    let url = `${window.location.protocol}//${window.location.hostname}:${window.location.port}/api/delete/${quote_id}`;
    let request = new XMLHttpRequest();
    request.open('POST', url, true);
    request.onload = function () {
        if (request.status >= 200 && request.status < 400) {
            let data = JSON.parse(request.response);
            if (data.ok) {
                window.location.reload();
            }
        } else {
            console.log('server error');
        }
    };
    request.send();
}
