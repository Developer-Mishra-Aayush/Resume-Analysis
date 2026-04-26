console.log("Script started loading");
const API = "http://localhost:8000/api";
let currentEmail = "";
let resendTmr = null;

// ─── Router ───────────────────────────────────────────
function showScreen(id) {
  document
    .querySelectorAll(".screen")
    .forEach((s) => s.classList.remove("active"));
  const el = document.getElementById("screen-" + id);
  if (el) el.classList.add("active");
}

// ─── Candidate pages ──────────────────────────────────
function cNav(btn, id) {
  if (btn) {
    document
      .querySelectorAll("#cand-sidebar .nav-link")
      .forEach((l) => l.classList.remove("active"));
    btn.classList.add("active");
  } else {
    document.querySelectorAll("#cand-sidebar .nav-link").forEach((l) => {
      if (
        l.getAttribute("onclick") &&
        l.getAttribute("onclick").includes("'" + id + "'")
      )
        l.classList.add("active");
    });
  }
  document
    .querySelectorAll(".cpage")
    .forEach((p) => (p.style.display = "none"));
  const pg = document.getElementById(id);
  if (pg) pg.style.display = "flex";
}

// ─── HR pages ─────────────────────────────────────────
function hNav(btn, id) {
  if (btn) {
    document
      .querySelectorAll("#hr-sidebar .nav-link")
      .forEach((l) => l.classList.remove("active"));
    btn.classList.add("active");
  }
  document
    .querySelectorAll(".hrpage")
    .forEach((p) => (p.style.display = "none"));
  const pg = document.getElementById(id);
  if (pg) pg.style.display = "flex";
}

// ─── Auth ─────────────────────────────────────────────
function sendOTP() {
  console.log("sendOTP called");
  const email = document.getElementById("login-email").value.trim();
  const name = document.getElementById("login-name").value.trim();
  console.log("Email:", email);
  if (!email) {
    showAlert("login-alert", "error", "Enter your email.");
    return;
  }
  const btn = document.getElementById("send-otp-btn");
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Sending...';

  setTimeout(() => {
    try {
      currentEmail = email;
      document.getElementById("otp-hint").textContent =
        `Sent a 6-digit code to ${email}`;
      showScreen("otp");
      startResendTimer();
      document.querySelectorAll(".otp-box")[0].focus();
    } catch (e) {
      console.error("Error:", e);
      showAlert("login-alert", "error", "Failed. Check your email.");
    } finally {
      btn.disabled = false;
      btn.innerHTML = "Send OTP →";
    }
  }, 1000);
}

async function verifyOTP() {
  const otp = Array.from(document.querySelectorAll(".otp-box"))
    .map((b) => b.value)
    .join("");
  if (otp.length < 6) {
    showAlert("otp-alert", "error", "Enter all 6 digits.");
    return;
  }
  const btn = document.getElementById("verify-btn");
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Verifying...';
  try {
    // REAL: const res=await fetch(`${API}/auth/verify-otp/`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:currentEmail,otp})})
    // const data=await res.json();if(!res.ok)throw new Error(data.error||'Invalid OTP')
    // localStorage.setItem('access_token',data.tokens.access);localStorage.setItem('refresh_token',data.tokens.refresh);
    // if(data.role==='hr'){showScreen('hr')}else{showScreen('candidate')}
    await sleep(900);
    clearInterval(resendTmr);
    const role = otp === "111111" ? "hr" : "candidate";
    if (role === "hr") showScreen("hr");
    else showScreen("candidate");
  } catch (e) {
    showAlert("otp-alert", "error", e.message || "Invalid OTP.");
  } finally {
    btn.disabled = false;
    btn.innerHTML = "Verify & Login";
  }
}

function resendOTP() {
  document.querySelectorAll(".otp-box").forEach((b) => (b.value = ""));
  document.querySelectorAll(".otp-box")[0].focus();
  startResendTimer();
  showAlert("otp-alert", "success", "New OTP sent!");
}

function startResendTimer() {
  let t = 60;
  const btn = document.getElementById("resend-btn");
  const el = document.getElementById("resend-timer");
  btn.disabled = true;
  clearInterval(resendTmr);
  resendTmr = setInterval(() => {
    t--;
    el.textContent = t;
    if (t <= 0) {
      clearInterval(resendTmr);
      btn.disabled = false;
      btn.textContent = "Resend code";
    }
  }, 1000);
}

function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  document.querySelectorAll(".otp-box").forEach((b) => (b.value = ""));
  showScreen("login");
}

// ─── OTP keyboard ─────────────────────────────────────
const otpBoxes = document.querySelectorAll(".otp-box");
if (otpBoxes.length > 0) {
  otpBoxes.forEach((box, i, all) => {
    box.addEventListener("input", () => {
      if (box.value && i < all.length - 1) all[i + 1].focus();
      if (box.value.length > 1) box.value = box.value.slice(-1);
    });
    box.addEventListener("keydown", (e) => {
      if (e.key === "Backspace" && !box.value && i > 0) all[i - 1].focus();
      if (e.key === "Enter") verifyOTP();
    });
  });
}

// ─── File upload ──────────────────────────────────────
function fileSelected(inp) {
  const f = inp.files[0];
  if (!f) return;
  if (f.size > 5 * 1024 * 1024) {
    showAlert("upload-alert", "error", "File too large. Max 5MB.");
    return;
  }
  if (!f.name.toLowerCase().endsWith(".pdf")) {
    showAlert("upload-alert", "error", "PDF files only.");
    return;
  }
  document.getElementById("file-name").textContent = f.name;
  document.getElementById("file-size").textContent =
    ` (${(f.size / 1024).toFixed(0)} KB)`;
  document.getElementById("file-info").style.display = "flex";
  document.getElementById("upload-zone").style.display = "none";
}
function clearFile() {
  document.getElementById("file-input").value = "";
  document.getElementById("file-info").style.display = "none";
  document.getElementById("upload-zone").style.display = "block";
}
function dragOver(e) {
  e.preventDefault();
  document.getElementById("upload-zone").classList.add("dragover");
}
function dragLeave() {
  document.getElementById("upload-zone").classList.remove("dragover");
}
function dropFile(e) {
  e.preventDefault();
  dragLeave();
  const f = e.dataTransfer.files[0];
  if (!f) return;
  const dt = new DataTransfer();
  dt.items.add(f);
  const inp = document.getElementById("file-input");
  inp.files = dt.files;
  fileSelected(inp);
}

// ─── Analysis ─────────────────────────────────────────
async function startAnalysis() {
  const jd = document.getElementById("jd-select").value;
  const file = document.getElementById("file-input").files[0];
  if (!file) {
    showAlert("upload-alert", "error", "Upload a PDF first.");
    return;
  }
  if (!jd) {
    showAlert("upload-alert", "error", "Select a Job Description.");
    return;
  }
  document.getElementById("analyze-btn").disabled = true;
  document.getElementById("analyzing-state").style.display = "block";
  // REAL: FormData upload → POST analyze → poll
  await sleep(3000);
  document.getElementById("analyzing-state").style.display = "none";
  document.getElementById("analyze-btn").disabled = false;
  cNav(null, "c-result");
}

// ─── Chat ─────────────────────────────────────────────
const chatReplies = {
  why: "Your 82 reflects matching 8 of 12 required skills. Docker, Kubernetes, AWS, and GraphQL are missing — each costs roughly 4–5 points. Your Python + Django + PostgreSQL core is strong.",
  add: 'The highest-impact add is **Docker**. Even a single Dockerfile in a project counts. Mention: "Dockerized Django app for local dev and deployment" in any project.',
  improve:
    'Quantify everything. "Built a REST API" → "Built a REST API handling 500+ daily requests with 99.9% uptime." Add any numbers: users, speed improvement, scale.',
  gap: "Docker is the most important gap — it's listed as required, not nice-to-have. After Docker, focus on basic AWS (EC2, S3) — both are quickly learnable and high-value.",
};
async function sendChat() {
  const inp = document.getElementById("chat-inp");
  const msg = inp.value.trim();
  if (!msg) return;
  addBubble(msg, "user");
  inp.value = "";
  document.getElementById("chat-starters").style.display = "none";
  const btn = document.getElementById("chat-send");
  btn.disabled = true;
  btn.textContent = "...";
  addBubble("Thinking...", "assistant", "typing-bbl");
  // REAL: await apiFetch(`/resumes/analysis/{id}/chat/`,{method:'POST',body:JSON.stringify({message:msg})})
  await sleep(1300);
  document.getElementById("typing-bbl")?.remove();
  const k = msg.toLowerCase().includes("why")
    ? "why"
    : msg.toLowerCase().includes("add") || msg.toLowerCase().includes("skill")
      ? "add"
      : msg.toLowerCase().includes("improv")
        ? "improve"
        : "gap";
  addBubble(chatReplies[k], "assistant");
  btn.disabled = false;
  btn.textContent = "Send";
}
function chatStarter(m) {
  document.getElementById("chat-inp").value = m;
  sendChat();
}
function addBubble(t, r, id) {
  const w = document.getElementById("chat-msgs");
  const d = document.createElement("div");
  d.className = "chat-bubble " + r;
  d.textContent = t;
  if (id) d.id = id;
  w.appendChild(d);
  w.scrollTop = w.scrollHeight;
}
function chatKey(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendChat();
  }
}

// ─── Notifications ────────────────────────────────────
function toggleNotif() {
  const dd = document.getElementById("notif-dd");
  dd.classList.toggle("open");
  document.getElementById("notif-count").style.display = "none";
}
document.addEventListener("click", (e) => {
  if (!e.target.closest(".notif-btn") && !e.target.closest(".notif-dd")) {
    document.getElementById("notif-dd")?.classList.remove("open");
  }
});

// ─── HR actions ───────────────────────────────────────
function toggleJDForm() {
  const f = document.getElementById("jd-form");
  f.style.display = f.style.display === "none" ? "block" : "none";
}
function saveJD() {
  alert(
    "✅ JD saved!\n\nREAL: POST /api/jobs/ with title, description, required_skills, experience_level",
  );
  toggleJDForm();
}
function toggleJD(cb, name) {
  const badge = cb.nextElementSibling;
  if (cb.checked) {
    badge.className = "badge badge-green";
    badge.textContent = "Active";
    alert(
      `✅ "${name}" is now Active.\n\nREAL: PATCH /api/jobs/{id}/ {is_active:true}\nThis triggers the JD Alert signal → emails all verified candidates!`,
    );
  } else {
    badge.className = "badge badge-gray";
    badge.textContent = "Inactive";
  }
}
function dlCSV() {
  alert("📥 Downloading CSV...\n\nREAL: GET /api/hr/dashboard/?format=csv");
}
function dlPDF() {
  alert(
    "📄 Downloading PDF Report...\n\nREAL: GET /api/analysis/{id}/report.pdf/",
  );
}
function copyLink() {
  navigator.clipboard
    ?.writeText(window.location.href + "analysis/share/abc123")
    .catch(() => {});
  alert("🔗 Share link copied!\n\nREAL: returns URL with unique analysis slug");
}
function filterDash() {
  console.log("REAL: GET /api/hr/dashboard/?jd_id=&min_score=");
}

// ─── Helpers ──────────────────────────────────────────
function showAlert(cid, type, msg) {
  const c = document.getElementById(cid);
  if (!c) return;
  c.style.display = "flex";
  c.className = "alert alert-" + type;
  c.innerHTML = `<span>${type === "error" ? "❌" : type === "success" ? "✅" : "ℹ️"}</span><span>${msg}</span>`;
  setTimeout(() => (c.style.display = "none"), 4000);
}
function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}
async function apiFetch(ep, opts = {}) {
  const t = localStorage.getItem("access_token");
  const headers = { "Content-Type": "application/json" };
  if (t) headers["Authorization"] = "Bearer " + t;
  if (opts.headers) Object.assign(headers, opts.headers);
  const res = await fetch(API + ep, { ...opts, headers });
  if (res.status === 401) logout();
  return res;
}
