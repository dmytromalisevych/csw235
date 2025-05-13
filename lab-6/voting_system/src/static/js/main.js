document.addEventListener('DOMContentLoaded', function() {
    fetchActivePolls();

    document.body.addEventListener('click', function(e) {
        if (e.target.matches('.poll-option')) {
            handleVote(e.target);
        }
    });
});

async function fetchActivePolls() {
    try {
        const response = await fetch('/polls/active');
        const polls = await response.json();
        displayPolls(polls);
    } catch (error) {
        console.error('Error fetching polls:', error);
    }
}

function displayPolls(polls) {
    const container = document.getElementById('active-polls');
    container.innerHTML = polls.map(poll => `
        <div class="poll-card card mb-3" data-poll-id="${poll.id}">
            <div class="card-body">
                <h5 class="card-title">${poll.title}</h5>
                <p class="card-text">${poll.description}</p>
                <div class="poll-options">
                    ${poll.options.map(option => `
                        <div class="poll-option" data-option-id="${option.id}">
                            ${option.text}
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `).join('');
}

async function handleVote(optionElement) {
    const pollId = optionElement.closest('.poll-card').dataset.pollId;
    const optionId = optionElement.dataset.optionId;

    try {
        const response = await fetch('/polls/vote', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                poll_id: pollId,
                option_id: optionId
            })
        });

        if (response.ok) {
            fetchActivePolls();
        }
    } catch (error) {
        console.error('Error submitting vote:', error);
    }
}