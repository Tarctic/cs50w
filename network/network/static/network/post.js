document.addEventListener('DOMContentLoaded', function() {

  load_posts();
});

function load_posts() {
  
  // Collecting all posts from index.html
  const posts = JSON.parse(document.getElementById('posts').textContent);
  posts.forEach(post => {
    console.log(post.id);
    const e = document.createElement('post');

    // Send get request to get information about likes for all posts
    fetch(`http://127.0.0.1:8000/likes/${post.id}`)
    .then(response => response.json())
    .then(like_content => {

      // Html, css content for images (if image exists)
      if (post.img) {
        var img = `<img src="${post.img}" class="mx-auto d-block" alt="Image could not be loaded" width="400"></img>`;
      } else {
        var img = '';
      }

      // Adding 'hidden' attribute to edit button tag if user is not logged in
      const userstate = JSON.parse(document.getElementById('userstate').textContent);
      if (userstate == post.poster) {
        var hide_edit = '';
      } else {
        var hide_edit = 'hidden';
      }

      // Html, css content for each post
      e.innerHTML = `
      <div class="card">
        <span class="card-top">
          <strong><a class="poster" href="http://127.0.0.1:8000/user/${post.poster}">${post.poster}</a></strong>
          <button ${hide_edit} id="edit-${post.id}" class="edit"><i class="far fa-edit text"></i></button>
        </span>
        <hr>
        <div class="card-body" id="body-${post.id}"><p class="card-text" id="text-${post.id}">${post.content}</p></div>
        ${img}
        <p class="creation">${post.creation}</p>
        <span class="like">
          <span id="like-${post.id}" class="${like_content.mylike}"></span>
          <span id="count-${post.id}"> ${like_content.likenum}</span>
        </span>
      </div>
      <br>`;
      document.querySelector('#post_page').append(e);

      // Like button function
      let like_button = document.querySelector(`#like-${post.id}`);
      like_button.addEventListener('click', function() {
        const userstate = JSON.parse(document.getElementById('userstate').textContent);

        // When like button is clicked, if user is logged in, carry out function. Else, redirect to login page.
        if (userstate != 'anonymous') {
          like(post.id);
        } else {
          location.href = 'http://127.0.0.1:8000/login';
        }
      });

      // Edit button function
      let edit_button = document.querySelector(`#edit-${post.id}`);
      edit_button.addEventListener('click', function() {
        edit(post.id, post.poster, post.content);
      });

      
    });
  });
}

function edit(id, poster, content) {

  // Disable edit button
  var edit = document.querySelector(`#edit-${id}`);
  edit.disabled = true;

  // Replace body of post with textarea (and previous content in the textarea) and 'Save' button
  document.getElementById(`body-${id}`).innerHTML =`<textarea id="textarea-${id}" class="submit-textarea" maxlength="5000" cols="65" rows="7">${content}</textarea>
  <button id="submit-${id}" class="submit">Save</button>`;

  // On click of save button, change post content to what user has saved and call put() function
  var submit = document.querySelector(`#submit-${id}`);
  submit.addEventListener('click', function() {

    var content = document.getElementById(`textarea-${id}`).value;
    document.getElementById(`body-${id}`).innerHTML = `<p class="card-text" id="text-${id}">${content}</p>`;

    edit.disabled = false;

    const userstate = JSON.parse(document.getElementById('userstate').textContent);
    if (userstate == poster) {
      put(id, 'edit', content);
    } else {
      location.href = 'http://127.0.0.1:8000/logout';
    }
  })
}

function like(id) {

  // Get the like button and number of likes using queryselector
    let button = document.querySelector(`#like-${id}`);
    let count = document.querySelector(`#count-${id}`);

  // Change icon class (bootstrap) to show that the post has been liked or unliked
  // Increase or decrease number of likes
    if (button.classList.contains('fas')) {
        button.classList.remove('fas');
        button.classList.add('far');
        count.innerHTML --;
        put(id, 'likes', false);
    } else {
        button.classList.remove('far');
        button.classList.add('fas');
        count.innerHTML ++;
        put(id, 'likes', true);
    }
}


// Send put request with the data to the specified path
function put(id, where, data) {
    fetch(`/${where}/${id}`, {
      headers: {
        'X-CSRFToken': csrf_token
      },
      method: 'PUT',
      body: JSON.stringify({
        data: data
      })
    });
}
