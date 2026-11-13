async function loadComments() {
    const response = await fetch("/api/comments");
    const comments = await response.json();
    const container = document.getElementById("comments");

    comments.forEach(comment => {
        const div = document.createElement("div");

        div.innerHTML = `
            <p>${comment.name}</p>
            <p>${comment.message}</p>
        `;
        container.appendChild(div);
    });
}
loadComments();