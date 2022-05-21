document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => location.reload());
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email('','',''));


  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(rec, sub, body) {

  console.log('working')
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-data').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = rec;
  document.querySelector('#compose-subject').value = sub;
  document.querySelector('#compose-body').value = body;

  document.querySelector('#compose-form').onsubmit = (event) => {
    event.preventDefault()
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients : document.querySelector('#compose-recipients').value,
        subject : document.querySelector('#compose-subject').value,
        body : document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then((result) => {
      console.log(result);
      if (result['message'] == 'Email sent successfully.') {
        load_mailbox('sent');
        return false;
      }
    }); 
  }
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-data').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);
    document.querySelectorAll(".email").forEach(e => e.remove());
    
    // ... do something else with emails ...
    emails.forEach(obj => {
      console.log(obj.id);
      const e = document.createElement('button');
      e.classList.add(`read-${obj.read}`, "email");
      e.innerHTML = `<span class="leftalign">${obj.sender}</span><span class="centeralign">${obj.subject}</span><span class="rightalign">${obj.timestamp}</span>`;
      e.addEventListener('click', function() {
        console.log('This element has been clicked!');
        read(obj.id, true);
        fetch(`emails/${obj.id}`)
        .then(response => response.json())
        .then(email_content => email_data(email_content, mailbox));
        });
      document.querySelector('#emails-view').append(e);
    })
  });
}


  
function email_data(email, mailbox) {

  console.log(mailbox)

  arch = document.querySelector('#archive');
  harch = document.querySelector('#archive-hover');
  unarch = document.querySelector('#unarchive');
  hunarch = document.querySelector('#unarchive-hover');
  reply = document.querySelector('#reply');

  if (mailbox=='archive') {
    arch.style.display = 'none';
    harch.style.display = 'none';
    
    ua = document.querySelector('#unarchive')
    ua.addEventListener('click', function() {
      archive(email.id, false);
      location.reload();
    })
  } else if (mailbox=='inbox') {
    unarch.style.display = 'none';
    hunarch.style.display = 'none';

    a = document.querySelector('#archive')
    a.addEventListener('click', function() {
      archive(email.id, true);
      location.reload();
    })
  } else if (mailbox=='sent') {
    arch.style.display = 'none';
    harch.style.display = 'none';
    unarch.style.display = 'none';
    hunarch.style.display = 'none';
    reply.style.display = 'none';
  }

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-data').style.display = 'block';


  document.querySelector('#email-subject').innerHTML = `${email.subject}`;
  document.querySelector('#email-sender').innerHTML = `From: <<strong>${email.sender}</strong>>`;
  document.querySelector('#email-recipients').innerHTML = `To:   <<strong>${email.recipients}</strong>>`;
  document.querySelector('#email-timestamp').innerHTML = `${email.timestamp}`;
  document.querySelector('#email-body').innerHTML = `${email.body}`;
  
  ur = document.querySelector('#mark-unread')
  ur.addEventListener('click', function() {
    read(email.id, false);
    location.reload();
  });

  del = document.querySelector('#delete');
  del.addEventListener('click', function() {
    delete_email(email.id);
    location.reload();
  });

  if (mailbox != 'sent') {
    reply.addEventListener('click', function() {
      sub = `Re: ${email.subject}`
      body = `Re: On ${email.timestamp} ${email.sender} wrote: ${email.body} \n Reply: \n`
      compose_email(email.sender, sub, body);
    });
  }

}

function read(id, reader) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: reader
    })
  })
}

function archive(id, arch) {
  fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: arch
        }),
      })
}

function delete_email(id) {
  fetch(`/emails/${id}`, {
        method: 'DELETE',
  })
  .then(res => res.text())
  .then(res => console.log(res))
}
