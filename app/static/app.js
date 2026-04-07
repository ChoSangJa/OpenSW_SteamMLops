document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const steamIdInput = document.getElementById('steamIdInput');
    const loading = document.getElementById('loading');
    const resultArea = document.getElementById('resultArea');

    // UI Elements
    const playstyleResult = document.getElementById('playstyleResult');
    const playtimeResult = document.getElementById('playtimeResult');
    const gameCountResult = document.getElementById('gameCountResult');
    const topGamesList = document.getElementById('topGamesList');
    const recommendationsList = document.getElementById('recommendationsList');

    analyzeBtn.addEventListener('click', async () => {
        const steamId = steamIdInput.value.trim();
        if (!steamId) {
            alert('Steam ID를 입력해주세요.');
            return;
        }

        if (!/^\d{17}$/.test(steamId)) {
            alert('유효한 17자리 Steam64 ID를 입력해주세요.');
            return;
        }

        // Show loading, hide result
        loading.classList.remove('hidden');
        resultArea.classList.add('hidden');
        console.log(`Starting analysis for Steam ID: ${steamId}...`);

        try {
            const response = await fetch(`/api/v1/analyze/${steamId}`);
            console.log(`API response received with status: ${response.status}`);
            const data = await response.json();

            if (!response.ok) {
                // Hide loading before showing alert to avoid user confusion
                loading.classList.add('hidden');
                throw new Error(data.detail || '분석 중 오류가 발생했습니다.');
            }

            renderResults(data);
            loading.classList.add('hidden'); // Hide after success
        } catch (error) {
            loading.classList.add('hidden'); // Hide on error
            alert(error.message);
        }
    });

    function renderResults(data) {
        playstyleResult.textContent = data.playstyle;
        playtimeResult.textContent = data.total_playtime_hours.toLocaleString();
        gameCountResult.textContent = data.total_games_owned.toLocaleString();

        // Clear and render top games
        topGamesList.innerHTML = '';
        if (data.top_games && data.top_games.length > 0) {
            data.top_games.forEach(game => {
                const li = document.createElement('li');
                li.className = 'game-item';
                li.innerHTML = `
                    <span class="game-name">${game.name}</span>
                    <span class="game-time">${game.playtime_hours.toLocaleString()} 시간</span>
                `;
                topGamesList.appendChild(li);
            });
        } else {
            topGamesList.innerHTML = '<li class="hint">플레이 데이터가 있는 게임이 없습니다.</li>';
        }

        // Clear and render recommendations
        recommendationsList.innerHTML = '';
        if (data.recommendations && data.recommendations.length > 0) {
            data.recommendations.forEach(rec => {
                const div = document.createElement('div');
                div.className = 'rec-item';
                div.innerHTML = `
                    <span class="rec-name">${rec.name}</span>
                    <p class="rec-reason">${rec.reason}</p>
                `;
                recommendationsList.appendChild(div);
            });
        }

        // Show result area
        resultArea.classList.remove('hidden');
        resultArea.scrollIntoView({ behavior: 'smooth' });
    }

    // Allow Enter key to trigger search
    steamIdInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            analyzeBtn.click();
        }
    });
});
