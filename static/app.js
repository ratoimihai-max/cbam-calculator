const form = document.querySelector("#cbam-form");
const tipProdus = document.querySelector("#tip_produs");
const grosimePanouField = document.querySelector("#grosime-panou-field");
const grosimeTablaField = document.querySelector("#grosime-tabla-field");
const grosimePanou = document.querySelector("#grosime_panou_mm");
const grosimeTabla = document.querySelector("#grosime_tabla_mm");
const panelSheetFields = document.querySelectorAll(".panel-sheet-field");
const tipPanou = document.querySelector("#tip_panou");
const grosimeTablaExterior = document.querySelector("#grosime_tabla_exterior_mm");
const grosimeTablaInterior = document.querySelector("#grosime_tabla_interior_mm");
const tara = document.querySelector("#tara");
const codNC = document.querySelector("#cod_NC");
const errorBox = document.querySelector("#error");
const defaultValuesBody = document.querySelector("#default-values-body");
const countrySearch = document.querySelector("#country-search");

let coduriImplicite = {};
let valoriDefaultTari = [];
let valoriDirecteTari = [];

function formatNumber(value, digits = 3) {
  return new Intl.NumberFormat("ro-RO", {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  }).format(value);
}

function setOptions(select, values, formatter = (value) => value) {
  select.innerHTML = "";
  values.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = formatter(value);
    select.append(option);
  });
}

function updateProductFields() {
  const isPanel = tipProdus.value === "panou_sandwich";
  grosimePanouField.classList.toggle("hidden", !isPanel);
  grosimeTablaField.classList.toggle("hidden", isPanel);
  panelSheetFields.forEach((field) => field.classList.toggle("hidden", !isPanel));
  grosimePanou.disabled = !isPanel;
  grosimeTabla.disabled = isPanel;
  tipPanou.disabled = !isPanel;
  grosimeTablaExterior.disabled = !isPanel;
  grosimeTablaInterior.disabled = !isPanel;

  const defaultCode = coduriImplicite[tipProdus.value];
  if (defaultCode) {
    codNC.value = defaultCode;
  }
}

function collectPayload() {
  return {
    tip_produs: tipProdus.value,
    tip_panou: tipPanou.disabled ? "" : tipPanou.value,
    grosime_panou_mm: grosimePanou.disabled ? "" : grosimePanou.value,
    grosime_tabla_mm: grosimeTabla.disabled ? "" : grosimeTabla.value,
    grosime_tabla_exterior_mm: grosimeTablaExterior.disabled ? "" : grosimeTablaExterior.value,
    grosime_tabla_interior_mm: grosimeTablaInterior.disabled ? "" : grosimeTablaInterior.value,
    suprafata_m2: document.querySelector("#suprafata_m2").value,
    tara: tara.value,
    cod_NC: codNC.value,
    anul: document.querySelector("#anul").value || "2026",
    pret_ETS: document.querySelector("#pret_ETS").value,
    taxa_carbon_origine: document.querySelector("#taxa_carbon_origine").value || 0,
  };
}

function showError(message) {
  errorBox.textContent = message;
  errorBox.classList.remove("hidden");
}

function clearError() {
  errorBox.textContent = "";
  errorBox.classList.add("hidden");
}

function renderResult(data) {
  document.querySelector("#greutate_kg_m2").textContent = formatNumber(data.greutate_kg_m2);
  document.querySelector("#greutate_tone").textContent = formatNumber(data.greutate_tone);
  document.querySelector("#valoare_implicita").textContent = formatNumber(data.valoare_implicita);
  document.querySelector("#sursa_valoare_implicita").textContent =
    data.sursa_valoare_implicita === "specifica_tarii"
      ? "tCO2/t produs, valoare specifica tarii"
      : "tCO2/t produs, default pe cod NC";
  document.querySelector("#emisii_tco2").textContent = formatNumber(data.emisii_tco2);
  document.querySelector("#cost_cbam_eur").textContent = formatNumber(data.cost_cbam_eur, 2);
  document.querySelector("#cost_cbam_eur_m2").textContent = formatNumber(data.cost_cbam_eur_m2, 2);
}

function sourceLabel(row) {
  const sources = Object.values(row.surse);
  return sources.includes("specifica_tarii") ? "specifica tarii" : "default cod NC";
}

function renderDefaultValuesTable(filter = "") {
  const normalizedFilter = filter.trim().toLowerCase();
  const rows = valoriDefaultTari.filter((row) =>
    row.tara.toLowerCase().includes(normalizedFilter)
  );

  defaultValuesBody.innerHTML = "";
  rows.forEach((row) => {
    const directRow = valoriDirecteTari.find((item) => item.tara === row.tara);
    const tr = document.createElement("tr");
    const taraCell = document.createElement("td");
    const direct7210Cell = document.createElement("td");
    const direct7308Cell = document.createElement("td");
    const markup7210Cell = document.createElement("td");
    const markup7308Cell = document.createElement("td");
    const sourceCell = document.createElement("td");

    taraCell.textContent = row.tara;
    direct7210Cell.textContent = formatNumber(directRow.valori["7210"]);
    direct7308Cell.textContent = formatNumber(directRow.valori["7308"]);
    markup7210Cell.textContent = formatNumber(row.valori["7210"]);
    markup7308Cell.textContent = formatNumber(row.valori["7308"]);
    sourceCell.textContent = sourceLabel(row);

    tr.append(taraCell, direct7210Cell, direct7308Cell, markup7210Cell, markup7308Cell, sourceCell);
    defaultValuesBody.append(tr);
  });
}

async function calculate() {
  clearError();
  const response = await fetch("/api/calculate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(collectPayload()),
  });

  const data = await response.json();
  if (!response.ok) {
    showError(data.error || "Calculul nu a reusit.");
    return;
  }

  renderResult(data);
}

async function init() {
  const response = await fetch("/api/options");
  const options = await response.json();
  coduriImplicite = options.coduri_implicite;
  valoriDefaultTari = options.valori_default_tari;
  valoriDirecteTari = options.valori_directe_tari;

  setOptions(grosimePanou, options.grosimi_panou, (value) => `${value} mm`);
  setOptions(tara, options.tari);
  setOptions(codNC, options.coduri_nc);
  renderDefaultValuesTable();

  grosimePanou.value = "60";
  updateProductFields();
  await calculate();
}

tipProdus.addEventListener("change", () => {
  updateProductFields();
  calculate();
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  calculate();
});

form.addEventListener("input", () => {
  clearTimeout(window.calculateTimer);
  window.calculateTimer = setTimeout(calculate, 250);
});

countrySearch.addEventListener("input", () => renderDefaultValuesTable(countrySearch.value));

init().catch((error) => showError(error.message));
