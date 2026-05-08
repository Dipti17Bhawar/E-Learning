// Dark mode toggle
function toggleMode() {
    document.body.classList.toggle("light");
}
const API = window.location.origin;

// SEMESTERS
document.getElementById("department").addEventListener("change", function() {
    fetch(`${API}/api/sem/${this.value}`)
    .then(res => res.json())
    .then(data => {
        let sem = document.getElementById("semester");
        sem.innerHTML = "";
        data.forEach(s => {
            sem.innerHTML += `<option value="${s.id}">Sem ${s.number}</option>`;
        });
    });
});

// SUBJECTS
document.getElementById("semester").addEventListener("change", function() {
    fetch(`${API}/api/sub/${this.value}`)
    .then(res => res.json())
    .then(data => {
        let sub = document.getElementById("subject");
        sub.innerHTML = "";
        data.forEach(s => {
            sub.innerHTML += `<option value="${s.id}">${s.name}</option>`;
        });
    });
});

// NOTES
document.getElementById("subject").addEventListener("change", function() {
    fetch(`${API}/api/notes/${this.value}`)
    .then(res => res.json())
    .then(data => {
        let notes = document.getElementById("notes");
        notes.innerHTML = "";

        data.forEach(n => {
            notes.innerHTML += `
                <div class="card glass">
                    <h3>${n.title}</h3>
                    <a href="/media/${n.file}" target="_blank">📄 View PDF</a>
                </div>
            `;
        });
    });
});