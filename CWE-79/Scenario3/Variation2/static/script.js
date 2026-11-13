async function loadComments() {
    const response = await fetch("/api/comments");
    const comments = await response.json();
    const container = document.getElementById("comments");

    //TO DO: Display all comments inside the container, each comment has "name" and "message"
}
loadComments();