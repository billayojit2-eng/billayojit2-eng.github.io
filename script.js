// ---------------- PROGRESS ----------------
function updateProgress(subject) {
    const boxes = document.querySelectorAll(
        `input[data-subject="${subject}"]`
    );

    const checked = Array.from(boxes).filter(b => b.checked).length;
    const total = boxes.length;

    const percent = total === 0 ? 0 : Math.round((checked / total) * 100);

    document.getElementById(`${subject}-progress`).innerText =
        `Progress: ${percent}%`;

    document.getElementById(`${subject}-bar`).value = percent;
}


// ---------------- EXAM PLANNER (localStorage) ----------------
function saveExam() {
    ["physics", "chemistry", "biology"].forEach(sub => {
        localStorage.setItem(
            sub + "-date",
            document.getElementById(sub + "-date").value
        );
        localStorage.setItem(
            sub + "-rev",
            document.getElementById(sub + "-rev").checked
        );
    });
}

function loadExamDates() {
    ["physics", "chemistry", "biology"].forEach(sub => {
        document.getElementById(sub + "-date").value =
            localStorage.getItem(sub + "-date") || "";
        document.getElementById(sub + "-rev").checked =
            localStorage.getItem(sub + "-rev") === "true";
    });
}


// ---------------- LOAD LESSONS FROM SQL ----------------
function loadLessonsFromSQL() {
    fetch("http://127.0.0.1:5000/lessons")
        .then(res => res.json())
        .then(lessons => {
            lessons.forEach(lesson => {
                const subject = lesson.subject.toLowerCase();
                const ul = document.getElementById(subject + "-list");
                if (!ul) return;

                const key = subject + "-" + lesson.id;
const checked = localStorage.getItem(key) === "true";

const li = document.createElement("li");
li.innerHTML = `
  <input type="checkbox"
         data-subject="${subject}"
         onchange="saveCheckbox(this, ${lesson.id})">
  ${lesson.chapter} – ${lesson.difficulty} – ${lesson.pages} pages
`;


                ul.appendChild(li);
            });

            updateProgress("physics");
            updateProgress("chemistry");
            updateProgress("biology");
        });
}


// ---------------- PAGE LOAD ----------------
window.onload = function () {
    loadExamDates();
    loadLessonsFromSQL();
};
function saveCheckbox(box) {
    const key = box.dataset.key;
    localStorage.setItem(key, box.checked);
    updateProgress(box.dataset.subject);
}
function saveCheckbox(box, lessonId) {
    fetch("http://127.0.0.1:5000/save-progress", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            lesson_id: lessonId,
            completed: box.checked
        })
    }).then(() => {
        updateProgress(box.dataset.subject);
    });
}
