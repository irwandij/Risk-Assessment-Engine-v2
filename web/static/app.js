(() => {
  const state = {
    selectedType: null,
    config: null,
    stepIndex: 0,
    values: {},
    lastResponse: null,
    validationScope: "step",
  };

  const els = {
    typeSelector: document.getElementById("typeSelector"),
    wizardSection: document.getElementById("wizardSection"),
    resultSection: document.getElementById("resultSection"),
    errorBanner: document.getElementById("errorBanner"),
    wizardTitle: document.getElementById("wizardTitle"),
    wizardDescription: document.getElementById("wizardDescription"),
    stepList: document.getElementById("stepList"),
    stepMeta: document.getElementById("stepMeta"),
    fieldContainer: document.getElementById("fieldContainer"),
    validationList: document.getElementById("validationList"),
    progressBar: document.getElementById("progressBar"),
    prevBtn: document.getElementById("prevBtn"),
    nextBtn: document.getElementById("nextBtn"),
    submitBtn: document.getElementById("submitBtn"),
    wizardForm: document.getElementById("wizardForm"),
    changeTypeBtn: document.getElementById("changeTypeBtn"),
    decisionText: document.getElementById("decisionText"),
    scoreText: document.getElementById("scoreText"),
    riskText: document.getElementById("riskText"),
    resultHeadline: document.getElementById("resultHeadline"),
    triggerList: document.getElementById("triggerList"),
    concernList: document.getElementById("concernList"),
    parameterTableWrap: document.getElementById("parameterTableWrap"),
    downloadJsonBtn: document.getElementById("downloadJsonBtn"),
    downloadMdBtn: document.getElementById("downloadMdBtn"),
    newAssessmentBtn: document.getElementById("newAssessmentBtn"),
  };

  function sanitizePath(path) {
    return `field_${path.replace(/[^a-zA-Z0-9]+/g, "_")}`;
  }

  function showError(message) {
    els.errorBanner.textContent = message;
    els.errorBanner.classList.remove("hidden");
  }

  function clearError() {
    els.errorBanner.textContent = "";
    els.errorBanner.classList.add("hidden");
  }

  function resetFlow() {
    state.selectedType = null;
    state.config = null;
    state.stepIndex = 0;
    state.values = {};
    state.lastResponse = null;
    state.validationScope = "step";

    els.typeSelector.classList.remove("hidden");
    els.wizardSection.classList.add("hidden");
    els.resultSection.classList.add("hidden");
    clearError();

    document.querySelectorAll(".type-card").forEach((card) => {
      card.classList.remove("active");
    });
  }

  function getAllFields() {
    if (!state.config) return [];
    return state.config.steps.flatMap((step) => step.fields);
  }

  function valueForField(field) {
    if (Object.prototype.hasOwnProperty.call(state.values, field.path)) {
      return state.values[field.path];
    }
    return field.default;
  }

  function isMissing(field, value) {
    if (!field.required) return false;
    if (field.type === "boolean") return value !== true && value !== false;
    if (field.type === "number") return value === null || value === undefined || value === "" || Number.isNaN(value);
    if (field.type === "list_text") return !Array.isArray(value) || value.length === 0;
    return value === null || value === undefined || String(value).trim() === "";
  }

  function collectMissing(scope = "step") {
    const candidates = scope === "all" ? state.config.steps : [state.config.steps[state.stepIndex]];
    const missing = [];

    candidates.forEach((step) => {
      step.fields.forEach((field) => {
        const value = valueForField(field);
        if (isMissing(field, value)) {
          missing.push({
            path: field.path,
            label: field.label,
            stepId: step.id,
            stepTitle: step.title,
          });
        }
      });
    });

    return missing;
  }

  function parseRawValue(field, rawValue) {
    if (field.type === "number") {
      if (rawValue === "" || rawValue === null || rawValue === undefined) return null;
      const num = field.number_mode === "int" ? parseInt(rawValue, 10) : Number(rawValue);
      return Number.isNaN(num) ? null : num;
    }

    if (field.type === "list_text") {
      if (!rawValue) return [];
      return String(rawValue)
        .split("\n")
        .map((line) => line.trim())
        .filter(Boolean);
    }

    if (field.type === "boolean") return rawValue;

    return rawValue;
  }

  function setNested(target, path, value) {
    const parts = path.split(".");
    let cursor = target;
    parts.forEach((part, idx) => {
      if (idx === parts.length - 1) {
        cursor[part] = value;
      } else {
        if (!cursor[part] || typeof cursor[part] !== "object") {
          cursor[part] = {};
        }
        cursor = cursor[part];
      }
    });
  }

  function buildPayload() {
    const payload = {};
    getAllFields().forEach((field) => {
      const value = parseRawValue(field, valueForField(field));
      if (value === null || value === undefined || value === "") return;
      setNested(payload, field.path, value);
    });
    return payload;
  }

  function updateProgress() {
    const total = state.config.steps.length;
    const current = state.stepIndex + 1;
    const percent = Math.round((current / total) * 100);
    els.progressBar.style.width = `${percent}%`;
  }

  function renderStepRail() {
    els.stepList.innerHTML = "";
    const allMissing = collectMissing("all");

    state.config.steps.forEach((step, idx) => {
      const li = document.createElement("li");
      li.className = "step-item";
      if (idx === state.stepIndex) li.classList.add("active");
      if (idx < state.stepIndex) li.classList.add("done");

      const missingInStep = allMissing.filter((m) => m.stepId === step.id).length;
      li.textContent = `${idx + 1}. ${step.title}${missingInStep ? ` (${missingInStep} missing)` : ""}`;
      els.stepList.appendChild(li);
    });
  }

  function renderValidationSummary() {
    const missing = collectMissing(state.validationScope);
    els.validationList.innerHTML = "";

    if (missing.length === 0) {
      const li = document.createElement("li");
      li.textContent = "No required fields missing in current scope.";
      li.style.color = "#0f766e";
      els.validationList.appendChild(li);
      return missing;
    }

    missing.forEach((item) => {
      const li = document.createElement("li");
      li.textContent = `${item.stepTitle}: ${item.label}`;
      els.validationList.appendChild(li);
    });

    return missing;
  }

  function clearInvalidStyles() {
    document.querySelectorAll(".field-card.invalid").forEach((node) => node.classList.remove("invalid"));
  }

  function highlightInvalidPaths(paths) {
    clearInvalidStyles();
    paths.forEach((path) => {
      const node = document.getElementById(sanitizePath(path));
      if (node) node.classList.add("invalid");
    });

    if (paths.length > 0) {
      const first = document.getElementById(sanitizePath(paths[0]));
      if (first) first.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }

  function onFieldChange(field, rawValue) {
    state.values[field.path] = rawValue;
    const fieldNode = document.getElementById(sanitizePath(field.path));
    if (fieldNode) fieldNode.classList.remove("invalid");

    renderStepRail();
    renderValidationSummary();
  }

  function makeInput(field) {
    const wrap = document.createElement("div");
    wrap.className = "field-card";
    wrap.id = sanitizePath(field.path);

    const label = document.createElement("label");
    label.textContent = field.label;
    if (field.required) {
      const star = document.createElement("span");
      star.className = "required";
      star.textContent = "*";
      label.appendChild(star);
    }
    wrap.appendChild(label);

    const value = valueForField(field);

    if (field.type === "boolean") {
      const group = document.createElement("div");
      group.className = "boolean-group";

      const yes = document.createElement("button");
      yes.type = "button";
      yes.className = `toggle-btn ${value === true ? "active true" : ""}`;
      yes.textContent = "Yes";
      yes.addEventListener("click", () => {
        onFieldChange(field, true);
        renderCurrentStep();
      });

      const no = document.createElement("button");
      no.type = "button";
      no.className = `toggle-btn ${value === false ? "active false" : ""}`;
      no.textContent = "No";
      no.addEventListener("click", () => {
        onFieldChange(field, false);
        renderCurrentStep();
      });

      group.appendChild(yes);
      group.appendChild(no);
      wrap.appendChild(group);
    } else {
      const input = field.type === "textarea" || field.type === "list_text"
        ? document.createElement("textarea")
        : document.createElement("input");

      if (input.tagName === "INPUT") {
        input.type = field.type === "number" ? "number" : field.type === "date" ? "date" : "text";
        if (field.number_mode === "float") input.step = "0.01";
        if (field.number_mode === "int") input.step = "1";
      }

      input.value = value ?? "";
      input.addEventListener("input", (event) => {
        onFieldChange(field, event.target.value);
      });
      wrap.appendChild(input);
    }

    if (field.help) {
      const help = document.createElement("p");
      help.className = "field-help";
      help.textContent = field.help;
      wrap.appendChild(help);
    }

    return wrap;
  }

  function renderCurrentStep() {
    const step = state.config.steps[state.stepIndex];
    els.stepMeta.innerHTML = `
      <h3>${step.title}</h3>
      <p>${step.description || "Provide the required analyst findings for this section."}</p>
    `;

    els.fieldContainer.innerHTML = "";
    step.fields.forEach((field) => {
      els.fieldContainer.appendChild(makeInput(field));
    });

    els.prevBtn.disabled = state.stepIndex === 0;
    const lastStep = state.stepIndex === state.config.steps.length - 1;
    els.nextBtn.classList.toggle("hidden", lastStep);
    els.submitBtn.classList.toggle("hidden", !lastStep);

    updateProgress();
    renderStepRail();
    renderValidationSummary();
  }

  function validateCurrentStep() {
    state.validationScope = "step";
    const missing = collectMissing("step");
    renderValidationSummary();
    highlightInvalidPaths(missing.map((item) => item.path));
    return missing.length === 0;
  }

  function validateAllSteps() {
    state.validationScope = "all";
    const missing = collectMissing("all");
    renderValidationSummary();
    highlightInvalidPaths(missing.map((item) => item.path));

    if (missing.length > 0) {
      const first = missing[0];
      const stepIdx = state.config.steps.findIndex((step) => step.id === first.stepId);
      if (stepIdx >= 0 && stepIdx !== state.stepIndex) {
        state.stepIndex = stepIdx;
        renderCurrentStep();
        highlightInvalidPaths([first.path]);
      }
      return false;
    }

    return true;
  }

  function renderResult(response) {
    const result = response.result;
    const decisionResult = result.decision_result || {};

    els.resultHeadline.textContent = `${result.merchant_name} • ${result.classification?.assessment_type_display || state.config.title}`;
    els.decisionText.textContent = decisionResult.decision || "-";
    const max = state.config.max_score || 100;
    els.scoreText.textContent = `${result.total_score}/${max}`;
    els.riskText.textContent = decisionResult.risk_level || "-";

    const triggers = decisionResult.auto_reject_triggers || [];
    const concerns = result.concerns || [];

    els.triggerList.innerHTML = "";
    if (triggers.length === 0) {
      const li = document.createElement("li");
      li.textContent = "No auto-reject trigger activated.";
      els.triggerList.appendChild(li);
    } else {
      triggers.forEach((trigger) => {
        const li = document.createElement("li");
        li.textContent = `${trigger.code}: ${trigger.reason}`;
        els.triggerList.appendChild(li);
      });
    }

    els.concernList.innerHTML = "";
    if (concerns.length === 0) {
      const li = document.createElement("li");
      li.textContent = "No major concern surfaced.";
      els.concernList.appendChild(li);
    } else {
      concerns.slice(0, 6).forEach((concern) => {
        const li = document.createElement("li");
        li.textContent = concern;
        els.concernList.appendChild(li);
      });
    }

    const scores = Object.entries(result.parameter_scores || {});
    let table = "<table><thead><tr><th>Parameter</th><th>Score</th><th>Rating</th><th>Top Gap</th></tr></thead><tbody>";
    scores.forEach(([key, val]) => {
      const topGap = (val.gaps && val.gaps.length > 0) ? val.gaps[0] : "-";
      table += `<tr><td>${key} • ${val.parameter_name}</td><td>${val.score}/${val.max_score}</td><td>${val.rating}</td><td>${topGap}</td></tr>`;
    });
    table += "</tbody></table>";
    els.parameterTableWrap.innerHTML = table;

    state.lastResponse = response;
    els.wizardSection.classList.add("hidden");
    els.resultSection.classList.remove("hidden");
    clearError();
  }

  function downloadBlob(content, filename, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = filename;
    anchor.click();
    URL.revokeObjectURL(url);
  }

  async function runAssessment() {
    const payload = buildPayload();

    try {
      const response = await fetch(`/api/assess/${state.selectedType}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (response.status === 422) {
        const data = await response.json();
        const details = data.details || [];
        const paths = details.map((d) => d.path).filter(Boolean);
        highlightInvalidPaths(paths);
        if (paths.length > 0) {
          showError(`Validation failed: ${details[0].message}`);
        } else {
          showError("Validation failed. Please review required fields.");
        }
        return;
      }

      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        showError(data.message || "Assessment request failed.");
        return;
      }

      const data = await response.json();
      renderResult(data);
    } catch (error) {
      showError("Unable to connect to assessment service.");
    }
  }

  async function loadType(typeId) {
    clearError();
    state.selectedType = typeId;
    state.stepIndex = 0;
    state.values = {};
    state.lastResponse = null;
    state.validationScope = "step";

    document.querySelectorAll(".type-card").forEach((card) => {
      card.classList.toggle("active", card.dataset.type === typeId);
    });

    try {
      const response = await fetch(`/api/form-config/${typeId}`);
      if (!response.ok) {
        throw new Error(`Unable to load config for ${typeId}`);
      }
      state.config = await response.json();
      els.wizardTitle.textContent = state.config.title;
      els.wizardDescription.textContent = state.config.description;
      els.typeSelector.classList.add("hidden");
      els.resultSection.classList.add("hidden");
      els.wizardSection.classList.remove("hidden");
      renderCurrentStep();
    } catch (error) {
      showError("Failed to load assessment form configuration.");
    }
  }

  function bindEvents() {
    document.querySelectorAll(".type-card").forEach((card) => {
      card.addEventListener("click", () => loadType(card.dataset.type));
    });

    els.prevBtn.addEventListener("click", () => {
      if (state.stepIndex === 0) return;
      state.stepIndex -= 1;
      state.validationScope = "step";
      renderCurrentStep();
    });

    els.nextBtn.addEventListener("click", () => {
      if (!validateCurrentStep()) return;
      state.stepIndex += 1;
      state.validationScope = "step";
      renderCurrentStep();
    });

    els.wizardForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (!validateAllSteps()) return;
      await runAssessment();
    });

    els.changeTypeBtn.addEventListener("click", () => {
      resetFlow();
    });

    els.newAssessmentBtn.addEventListener("click", () => {
      resetFlow();
    });

    els.downloadJsonBtn.addEventListener("click", () => {
      if (!state.lastResponse) return;
      downloadBlob(
        JSON.stringify(state.lastResponse.result, null, 2),
        state.lastResponse.download.json_filename,
        "application/json"
      );
    });

    els.downloadMdBtn.addEventListener("click", () => {
      if (!state.lastResponse) return;
      downloadBlob(
        state.lastResponse.report_markdown,
        state.lastResponse.download.markdown_filename,
        "text/markdown"
      );
    });
  }

  bindEvents();
})();
