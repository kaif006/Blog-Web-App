

document.querySelectorAll('.like-btn').forEach(button => {
    const postId = button.dataset.id;

    // Fetch initial like status and count
    fetch(`/blog/like-status/${postId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.liked) {
                button.innerHTML = '❤️ Liked';
            } else {
                button.innerHTML = '🤍 Like';
            }
            button.nextElementSibling.innerText = `${data.likes_count} like${data.likes_count === 1 ? '' : 's'}`;
        });

    button.addEventListener('click', () => {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        fetch(`/blog/like/${postId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.liked) {
                button.innerHTML = '❤️ Liked';
            } else {
                button.innerHTML = '🤍 Like';
            }
            button.nextElementSibling.innerText = `${data.likes_count} like${data.likes_count === 1 ? '' : 's'}`;
        });
    });
});
