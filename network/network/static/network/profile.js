document.addEventListener('DOMContentLoaded', 
function() {
    document.querySelector('#follow').onclick = follow;
})

function follow() {

    // Get follow button and number of followers using queryselector
    let foll = document.querySelector('#follow');
    let followersnum = document.querySelector('#followersnum');

    // On clicking the follow button, change 'follow' to 'unfollow' or vice versa
    // Increase or decrease number of followers
    // Call fput function
    if (foll.innerHTML === 'Follow') {
        foll.innerHTML = 'Unfollow';
        followersnum.innerHTML++;
        fput(true);
    } else {
        foll.innerHTML = 'Follow';
        followersnum.innerHTML--;
        fput(false);
    }
}

function fput(data) {

    // Send put request to required path with either true or false
    let username = document.querySelector('#username').innerHTML;
    fetch(`/user/${username}`, {
        headers: {
            'X-CSRFToken': csrf_token
        },
        method: 'PUT',
        body: JSON.stringify({
            follow: data
        })
    });
}