const sectionTitle = document.getElementById("section-title");
const questionList = document.getElementById("question-list");
const answerTitle = document.getElementById("answer-title");
const answerBody = document.getElementById("answer-body");
const searchInput = document.getElementById("search-input");

const sections = {
  IELTS: "IELTS",
  SAT: "SAT",
  UNIVERSITIES: "Universities",
};

const sectionButtons = {
  IELTS: document.getElementById("btn-ielts"),
  SAT: document.getElementById("btn-sat"),
  UNIVERSITIES: document.getElementById("btn-universities"),
  Resources: document.getElementById("btn-resources"),
};

function createQuestionItem(item) {
  const wrapper = document.createElement("button");
  wrapper.className = "list-item";
  wrapper.textContent = item.question_en || item.question_uz;
  wrapper.addEventListener("click", () => loadAnswer(item.id));
  return wrapper;
}

function showQuestionList(title, items) {
  sectionTitle.textContent = title;
  questionList.innerHTML = "";

  if (!items.length) {
    questionList.innerHTML =
      "<p>No items found. Try another section or search keyword.</p>";
    answerTitle.textContent = "Answer Preview";
    answerBody.textContent =
      "Select a question to display its full answer here.";
    return;
  }

  items.forEach((item) => questionList.appendChild(createQuestionItem(item)));
}

async function loadSection(section) {
  const response = await fetch(
    `/api/questions?section=${encodeURIComponent(section)}`,
  );
  const data = await response.json();
  showQuestionList(`${section} Questions`, data.questions);
}

async function loadAnswer(id) {
  const response = await fetch(`/api/question?id=${encodeURIComponent(id)}`);
  const data = await response.json();
  if (data.error) {
    answerTitle.textContent = "Error";
    answerBody.textContent = data.error;
    return;
  }

  answerTitle.textContent = data.question_en || data.question_uz;
  answerBody.textContent = data.answer_en || data.answer_uz;
}

async function searchQuestions() {
  const query = searchInput.value.trim();
  if (!query) return;

  const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
  const data = await response.json();
  showQuestionList(`Search results for: ${query}`, data.results);
}

async function loadResources() {
  const response = await fetch(`/api/resources`);
  const data = await response.json();
  showQuestionList("University Resources", data.resources);
  answerTitle.textContent = "Resource Guide";
  answerBody.textContent =
    "Select a resource card to view a detailed answer and university guidance.";
}

sectionButtons.IELTS.addEventListener("click", () => loadSection("IELTS"));
sectionButtons.SAT.addEventListener("click", () => loadSection("SAT"));
sectionButtons.UNIVERSITIES.addEventListener("click", () =>
  loadSection("UNIVERSITIES"),
);
sectionButtons.Resources.addEventListener("click", loadResources);

searchInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    searchQuestions();
  }
});

document
  .getElementById("btn-search")
  .addEventListener("click", searchQuestions);

loadSection("IELTS");
