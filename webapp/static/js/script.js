// Stockage local des données
let exoplanets = JSON.parse(localStorage.getItem('exoplanets')) || [];

// Fonction pour changer d'onglet
function switchTab(tab) {
    // Mise à jour des boutons d'onglets
    const tabs = document.querySelectorAll('.tab-button');
    tabs.forEach(t => {
        t.classList.remove('text-purple-600', 'border-purple-600', 'bg-purple-50');
        t.classList.add('text-gray-500', 'border-transparent');
    });
    
    const activeTab = document.getElementById(`tab-${tab}`);
    activeTab.classList.remove('text-gray-500', 'border-transparent');
    activeTab.classList.add('text-purple-600', 'border-purple-600', 'bg-purple-50');
    
    // Mise à jour du contenu
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(c => {
        c.classList.remove('block');
        c.classList.add('hidden');
    });
    
    const activeContent = document.getElementById(`content-${tab}`);
    activeContent.classList.remove('hidden');
    activeContent.classList.add('block');
}

// Initialisation au chargement
window.addEventListener('load', function() {
    displayExoplanets();
});

document.getElementById('exoplanetForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Récupération des valeurs du formulaire
    const formData = {
        id: Date.now(),
        koi_period: parseFloat(document.getElementById('koi_period').value),
        koi_duration: parseFloat(document.getElementById('koi_duration').value),
        koi_depth: parseFloat(document.getElementById('koi_depth').value),
        koi_impact: parseFloat(document.getElementById('koi_impact').value),
        koi_srad: parseFloat(document.getElementById('koi_srad').value),
        koi_slogg: parseFloat(document.getElementById('koi_slogg').value),
        koi_steff: parseFloat(document.getElementById('koi_steff').value),
        createdAt: new Date().toISOString()
    };

    // Ajout aux données
    exoplanets.push(formData);
    localStorage.setItem('exoplanets', JSON.stringify(exoplanets));
    
    // Réinitialisation du formulaire
    this.reset();
    
    // Affichage des données
    displayExoplanets();
    
    // Retour à l'onglet des données
    switchTab('data');
    
    // Notification de succès
    showNotification('✅ Exoplanète enregistrée avec succès !');
});

// Affichage des exoplanètes
function displayExoplanets() {
    const dataGrid = document.getElementById('dataGrid');
    const emptyState = document.getElementById('emptyState');
    const planetCount = document.getElementById('planetCount');
    
    planetCount.textContent = `${exoplanets.length} planète(s)`;
    
    if (exoplanets.length === 0) {
        emptyState.classList.remove('hidden');
        dataGrid.classList.add('hidden');
        return;
    }
    
    emptyState.classList.add('hidden');
    dataGrid.classList.remove('hidden');
    
    dataGrid.innerHTML = exoplanets.map((planet, index) => `
        <div class="bg-gradient-to-br from-purple-50 to-indigo-50 rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden border-2 border-purple-200 hover:border-purple-400">
            <div class="bg-gradient-to-r from-purple-600 to-indigo-700 text-white p-4">
                <div class="flex justify-between items-center">
                    <h3 class="text-xl font-bold">🪐 Exoplanète #${exoplanets.length - index}</h3>
                    <button onclick="deleteExoplanet(${planet.id})" class="text-white hover:text-red-300 transition-colors" title="Supprimer">
                        🗑️
                    </button>
                </div>
                <p class="text-sm opacity-80 mt-1">${new Date(planet.createdAt).toLocaleString('fr-FR')}</p>
            </div>
            
            <div class="p-4 space-y-2 text-sm">
                <div class="flex justify-between py-2 border-b border-purple-200">
                    <span class="font-semibold text-gray-600">Période Orbitale:</span>
                    <span class="text-purple-700 font-medium">${planet.koi_period.toFixed(2)} j</span>
                </div>
                <div class="flex justify-between py-2 border-b border-purple-200">
                    <span class="font-semibold text-gray-600">Durée du Transit:</span>
                    <span class="text-purple-700 font-medium">${planet.koi_duration.toFixed(2)} h</span>
                </div>
                <div class="flex justify-between py-2 border-b border-purple-200">
                    <span class="font-semibold text-gray-600">Profondeur Transit:</span>
                    <span class="text-purple-700 font-medium">${planet.koi_depth.toFixed(2)} ppm</span>
                </div>
                <div class="flex justify-between py-2 border-b border-purple-200">
                    <span class="font-semibold text-gray-600">Paramètre Impact:</span>
                    <span class="text-purple-700 font-medium">${planet.koi_impact.toFixed(2)}</span>
                </div>
                <div class="flex justify-between py-2 border-b border-purple-200">
                    <span class="font-semibold text-gray-600">Rayon Stellaire:</span>
                    <span class="text-purple-700 font-medium">${planet.koi_srad.toFixed(2)} R☉</span>
                </div>
                <div class="flex justify-between py-2 border-b border-purple-200">
                    <span class="font-semibold text-gray-600">Gravité Surface:</span>
                    <span class="text-purple-700 font-medium">${planet.koi_slogg.toFixed(2)} log(g)</span>
                </div>
                <div class="flex justify-between py-2">
                    <span class="font-semibold text-gray-600">Température:</span>
                    <span class="text-purple-700 font-medium">${planet.koi_steff.toFixed(0)} K</span>
                </div>
            </div>
            
            <div class="bg-purple-100 p-3 flex justify-center">
                <button onclick="analyzeExoplanet(${planet.id})" class="px-4 py-2 bg-gradient-to-r from-purple-600 to-indigo-700 text-white rounded-lg font-semibold hover:shadow-lg transition-all text-sm">
                    🚀 Analyser
                </button>
            </div>
        </div>
    `).join('');
}

// Supprimer une exoplanète
function deleteExoplanet(id) {
    if (confirm('Êtes-vous sûr de vouloir supprimer cette exoplanète ?')) {
        exoplanets = exoplanets.filter(p => p.id !== id);
        localStorage.setItem('exoplanets', JSON.stringify(exoplanets));
        displayExoplanets();
        showNotification('🗑️ Exoplanète supprimée');
    }
}

// Analyser une exoplanète
function analyzeExoplanet(id) {
    const planet = exoplanets.find(p => p.id === id);
    if (planet) {
        // Redirection vers la page de détail
        window.location.href = `detail.html?id=${id}`;
    }
}

// Notification
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'fixed top-5 right-5 bg-green-500 text-white px-6 py-4 rounded-xl shadow-2xl z-50 transition-all duration-300';
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateY(-20px)';
        notification.style.transition = 'all 0.3s';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Validation en temps réel pour le paramètre d'impact
document.getElementById('koi_impact').addEventListener('input', function(e) {
    const value = parseFloat(e.target.value);
    if (value < 0 || value > 1) {
        e.target.setCustomValidity('Le paramètre d\'impact doit être entre 0 et 1');
    } else {
        e.target.setCustomValidity('');
    }
});


