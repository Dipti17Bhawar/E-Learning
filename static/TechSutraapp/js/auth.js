// Global Utility Functions
function logout() {
    localStorage.removeItem("username");
    window.location.href = "/";
}

function goToDashboard() {
    if (localStorage.getItem("username")) {
        window.location.href = "/dashboard/";
    } else {
        window.location.href = "/login/";
    }
}

function loginUser(event) {
    event.preventDefault();
    const usernameInput = document.getElementById("username").value;
    localStorage.setItem("username", usernameInput);
    window.location.href = "/dashboard/";
}

function registerUser(event) {
    event.preventDefault();
    const usernameInput = document.getElementById("reg-username").value;
    localStorage.setItem("username", usernameInput);
    window.location.href = "/dashboard/";
}

function clearSelection(listId) {
    const items = document.getElementById(listId).querySelectorAll('p');
    items.forEach(item => item.classList.remove('selected'));
}

function selectBranch(branch, element) {
    localStorage.setItem("branch", branch);
    clearSelection('branchList');
    element.classList.add('selected');
}

function selectSemester(semester, element) {
    localStorage.setItem("semester", semester);
    clearSelection('semesterList');
    element.classList.add('selected');
}

function selectSubject(subject, element) {
    localStorage.setItem("subject", subject);
    clearSelection('subjectList');
    element.classList.add('selected');
    setTimeout(() => {
        window.location.href = "/resources/";
    }, 300);
}

function goBack() {
    window.history.back();
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function viewFile(type) {
    const subject = localStorage.getItem("subject");
    const filePath = `/static/notes/${subject}/${type}.pdf`;
    window.open("/view/?file=" + encodeURIComponent(filePath), "_blank");
}

function downloadFile(type) {
    const subject = localStorage.getItem("subject");
    const filePath = `/static/notes/${subject}/${type}.pdf`;
    window.open(filePath, "_blank");
}

let reviews = JSON.parse(localStorage.getItem("reviews")) || [];

function displayReviews() {
    const reviewList = document.getElementById("reviewList");
    if (!reviewList) return;
    reviewList.innerHTML = "";
    const subject = localStorage.getItem("subject");
    const subjectReviews = reviews.filter(r => r.subject === subject);

    if (subjectReviews.length === 0) {
        reviewList.innerHTML = "<p>No reviews yet. Be the first to review!</p>";
        return;
    }

    subjectReviews.forEach(r => {
        const div = document.createElement("div");
        div.classList.add("review-card");
        div.innerHTML = `
            <strong>${r.username}</strong> (${r.date})<br>
            Rating: ${"⭐".repeat(r.rating)}<br>
            <p>${r.text}</p>
        `;
        reviewList.appendChild(div);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const path = window.location.pathname;

    // Home Page specific
    const exploreBtn = document.getElementById("exploreBtn");
    if (exploreBtn) {
        exploreBtn.onclick = () => window.location.href = "/dashboard/";
    }

    // Dashboard Page specific
    if (path === "/dashboard/") {
        const username = "{{ request.user.username }}"; // Not accessible in static file, will override in HTML below
    }

    // Resources Page specific
    if (path === "/resources/") {
        const subject = localStorage.getItem("subject");
        if (!subject) {
            alert("No subject selected! Redirecting to dashboard.");
            window.location.href = "/dashboard/";
        } else {
            const subjectTitle = document.getElementById("subjectTitle");
            if (subjectTitle) {
                subjectTitle.innerText = subject + " Resources";
            }

            const resourceTypes = ["notes", "syllabus", "qp"];
            const resourceCards = document.getElementById("resourceCards");
            if (resourceCards) {
                resourceTypes.forEach(type => {
                    const card = document.createElement("div");
                    card.classList.add("card");

                    const title = document.createElement("h3");
                    title.innerText = capitalize(type);
                    card.appendChild(title);

                    const viewBtn = document.createElement("button");
                    viewBtn.innerText = "View";
                    viewBtn.onclick = () => viewFile(type);
                    card.appendChild(viewBtn);

                    const downloadBtn = document.createElement("button");
                    downloadBtn.innerText = "Download";
                    downloadBtn.onclick = () => downloadFile(type);
                    card.appendChild(downloadBtn);

                    resourceCards.appendChild(card);
                });
            }

            displayReviews();

            const reviewForm = document.getElementById("reviewForm");
            if (reviewForm) {
                reviewForm.addEventListener("submit", function(e) {
                    e.preventDefault();
                    const reviewText = document.getElementById("reviewText").value.trim();
                    const rating = document.getElementById("rating").value;

                    // Grab the natively authenticated username injected into the DOM by Django
                    const userElement = document.getElementById("server-username");
                    const currentUsername = userElement ? userElement.innerText.trim() : "Anonymous";

                    if (!reviewText || !rating) return;

                    const review = {
                        username: currentUsername,
                        subject: subject,
                        text: reviewText,
                        rating: rating,
                        date: new Date().toLocaleString()
                    };

                    reviews.push(review);
                    localStorage.setItem("reviews", JSON.stringify(reviews));
                    displayReviews();
                    reviewForm.reset();
                });
            }
        }
    }

    // View Page specific
    if (path === "/view/") {
        const urlParams = new URLSearchParams(window.location.search);
        let file = urlParams.get("file");
        const pdfViewer = document.getElementById('pdfViewer');

        if (pdfViewer && file) {
            pdfViewer.src = file;
        } else if (pdfViewer) {
            console.log("No file specified");
        }
    }
});
