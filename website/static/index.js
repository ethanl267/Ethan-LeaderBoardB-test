function deleteNote(noteId){
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId })
    })
    .then((_res) => {
        window.location.href = '/';
    })
}

function deleteTeam(teamId){
    fetch('/delete-team', {
        method: 'POST',
        body: JSON.stringify({ teamId: teamId })
    })
    .then((_res) => {
        window.location.href = '/my-team';
    })
}

function joinTeam(teamId){
    fetch('/join-team', {
        method: 'POST',
        body: JSON.stringify({ teamId: teamId })
    }) 
    .then((_res) => {
        window.location.href = '/my-team';
    })
}


function leaveTeam(){
    fetch('/leave-team',{
        method: 'GET'
    })
    .then((_res) => {
        window.location.href = '/my-team';
    })
}


function showWork(user){
    alert(user);
}