document.addEventListener('DOMContentLoaded', () => {
    
    // Page switcher logic framework
    function navigateTo(targetPageId) {
        document.querySelectorAll('.app-section').forEach(page => {
            page.classList.remove('active-page');
        });
        const targetPage = document.getElementById(targetPageId);
        if (targetPage) {
            targetPage.classList.add('active-page');
        }
        window.scrollTo(0, 0);
    }

    // Start assessment button listener logic
    const startBtn = document.getElementById('start-btn');
    if (startBtn) {
        startBtn.addEventListener('click', () => {
            navigateTo('assessment-page-view');
        });
    }

    // Reset button evaluation matrices handler
    const resetBtn = document.getElementById('reset-btn');
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            const form = document.getElementById('career-form');
            if (form) form.reset();
            navigateTo('assessment-page-view');
        });
    }

    // Form Pipeline inference handler 
    const careerForm = document.getElementById('career-form');
    if (careerForm) {
        careerForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            const formContent = document.getElementById('form-content-area');
            const loaderArea = document.getElementById('form-loader-area');

            const payload = {
                education: document.getElementById('education').value,
                specialization: document.getElementById('specialization').value,
                skills: document.getElementById('skills').value,
                interests: document.getElementById('interests').value
            };

            formContent.style.display = 'none';
            loaderArea.style.display = 'block';

            const categoryOutput = document.getElementById('category-output');
            const predictionsList = document.getElementById('predictions-list');
            const careerDescription = document.getElementById('career-description');
            const resultIcon = document.getElementById('result-icon');
            const resultHeading = document.getElementById('result-heading');

            try {
                const response = await fetch('http://127.0.0.1:5000/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                if (!response.ok) throw new Error('Model inference failure');

                const data = await response.json();

                resultIcon.textContent = "🎯";
                resultHeading.textContent = "Optimal Vector Matched";
                categoryOutput.textContent = data.category;

                predictionsList.innerHTML = '';
                data.predictions.forEach((pred, index) => {
                    const card = document.createElement('div');
                    card.className = 'prediction-card';
                    card.innerHTML = `
                        <span class="prediction-rank">#${index + 1}</span>
                        <span class="prediction-title">${pred.title}</span>
                        <span class="prediction-confidence">${pred.confidence}%</span>
                    `;
                    predictionsList.appendChild(card);
                });

                careerDescription.textContent = `Based on your profile, the model's top match is ${data.predictions[0].title}, with ${data.predictions[0].confidence}% confidence within the ${data.category} field.`;

            } catch (error) {
                console.error("System connection error:", error);
                resultIcon.textContent = "⚠️";
                resultHeading.textContent = "Inference Pipeline Failed";
                predictionsList.innerHTML = '';
                careerDescription.textContent = "Failed to receive a response from the backend machine learning model. Please make sure your Python Flask server is active locally on http://127.0.0.1:5000.";
            
            } finally {
                formContent.style.display = 'block';
                loaderArea.style.display = 'none';
                navigateTo('result-page-view');
            }
        });
    }
})