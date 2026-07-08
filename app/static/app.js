async function apiFetch(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    ...options,
  });
  if (!response.ok) {
    let detail = "Request failed";
    try {
      const body = await response.json();
      detail = body.detail || detail;
    } catch (e) {
      // ignore non-JSON error bodies
    }
    throw new Error(detail);
  }
  if (response.status === 204) return null;
  return response.json();
}

function setupLogout() {
  const btn = document.getElementById("logout-btn");
  if (!btn) return;
  btn.addEventListener("click", async () => {
    await apiFetch("/api/auth/logout", { method: "POST" });
    window.location.href = "/login";
  });
}

function setupLoginForm() {
  const form = document.getElementById("login-form");
  if (!form) return;
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const errorEl = document.getElementById("login-error");
    errorEl.textContent = "";
    const data = Object.fromEntries(new FormData(form).entries());
    try {
      await apiFetch("/api/auth/login", { method: "POST", body: JSON.stringify(data) });
      window.location.href = "/dashboard";
    } catch (err) {
      errorEl.textContent = err.message;
    }
  });
}

function setupSignupForm() {
  const form = document.getElementById("signup-form");
  if (!form) return;
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const errorEl = document.getElementById("signup-error");
    errorEl.textContent = "";
    const formData = new FormData(form);
    const password = formData.get("password");
    const confirm = formData.get("confirm_password");
    if (password !== confirm) {
      errorEl.textContent = "Passwords do not match";
      return;
    }
    const data = { username: formData.get("username"), password };
    try {
      await apiFetch("/api/auth/signup", { method: "POST", body: JSON.stringify(data) });
      window.location.href = "/dashboard";
    } catch (err) {
      errorEl.textContent = err.message;
    }
  });
}

function setupInsertPage() {
  const topicSelect = document.getElementById("topic-select");
  if (!topicSelect) return;

  const newTopicWrapper = document.getElementById("new-topic-wrapper");
  const newTopicInput = document.getElementById("new-topic-input");
  const recordIdInput = document.getElementById("record-id");
  const descriptionInput = document.getElementById("description-input");
  const form = document.getElementById("record-form");
  const messageEl = document.getElementById("form-message");

  function clearFormFields() {
    recordIdInput.value = "";
    descriptionInput.value = "";
    newTopicInput.value = "";
    newTopicWrapper.classList.add("hidden");
  }

  async function loadTopics(selected) {
    const topics = await apiFetch("/api/records/topics");
    topicSelect.innerHTML = '<option value="">-- Select existing topic --</option>';
    topics.forEach((topic) => {
      const opt = document.createElement("option");
      opt.value = topic;
      opt.textContent = topic;
      topicSelect.appendChild(opt);
    });
    const newOpt = document.createElement("option");
    newOpt.value = "__new__";
    newOpt.textContent = "+ New topic";
    topicSelect.appendChild(newOpt);
    topicSelect.value = selected || "";
  }

  topicSelect.addEventListener("change", async () => {
    messageEl.textContent = "";
    if (topicSelect.value === "__new__") {
      newTopicWrapper.classList.remove("hidden");
      recordIdInput.value = "";
      descriptionInput.value = "";
      return;
    }
    newTopicWrapper.classList.add("hidden");
    if (!topicSelect.value) {
      recordIdInput.value = "";
      descriptionInput.value = "";
      return;
    }
    try {
      const records = await apiFetch(`/api/records/by-topic/${encodeURIComponent(topicSelect.value)}`);
      const record = records[0];
      recordIdInput.value = record.record_id;
      descriptionInput.value = record.description ?? "";
    } catch (err) {
      messageEl.textContent = err.message;
    }
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    messageEl.textContent = "";
    const isNewTopic = topicSelect.value === "__new__";
    const topic = isNewTopic ? newTopicInput.value.trim() : topicSelect.value;
    if (!topic) {
      messageEl.textContent = "Please select or enter a topic.";
      return;
    }
    const payload = {
      topic,
      description: descriptionInput.value,
    };
    try {
      if (recordIdInput.value) {
        await apiFetch(`/api/records/${recordIdInput.value}`, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
        messageEl.textContent = "Record updated.";
      } else {
        await apiFetch("/api/records", { method: "POST", body: JSON.stringify(payload) });
        messageEl.textContent = "Record created.";
      }
      clearFormFields();
      await loadTopics(topic);
    } catch (err) {
      messageEl.textContent = err.message;
    }
  });

  loadTopics();
}

function setupDashboardPage() {
  const tableBody = document.getElementById("records-table-body");
  if (!tableBody) return;

  async function loadTable() {
    const records = await apiFetch("/api/records");
    tableBody.innerHTML = "";
    records.forEach((record) => {
      const row = document.createElement("tr");
      const topicCell = document.createElement("td");
      topicCell.textContent = record.topic;
      const descriptionCell = document.createElement("td");
      descriptionCell.textContent = record.description ?? "";
      const updatedCell = document.createElement("td");
      updatedCell.textContent = new Date(record.updated_at).toLocaleString();

      row.append(topicCell, descriptionCell, updatedCell);
      tableBody.appendChild(row);
    });
  }

  loadTable();
}

document.addEventListener("DOMContentLoaded", () => {
  setupLogout();
  setupLoginForm();
  setupSignupForm();
  setupInsertPage();
  setupDashboardPage();
});
