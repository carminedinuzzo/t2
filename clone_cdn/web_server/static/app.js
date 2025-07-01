document.getElementById('ask-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = document.getElementById('message').value;
    const resp = await fetch('/ask', {
        method: 'POST',
        body: new URLSearchParams({message}),
    });
    const data = await resp.json();
    document.getElementById('response').textContent = data.response || data.error;
});
