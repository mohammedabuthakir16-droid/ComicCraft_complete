// ComicCraft Interactive Studio & Comic Reader Engine

document.addEventListener("DOMContentLoaded", () => {
  // 1. Interactive Ambient Particles Background
  initAmbientParticles();

  // 2. Visual Art Style Cards & Preset Synchronization
  initStyleSelector();

  // 3. Panel Count Buttons
  initPanelCountSelector();

  // 4. Magic Inspiration Wand ("Inspire Me")
  initInspireMe();

  // 5. Live Storyboard Mock Synchronization
  initLiveMockSync();

  // 6. Form Submission & Enhanced Loading Modal Progression
  initLoadingModal();

  // 7. Interactive Procedural Web Audio Sound Synthesizer
  initSoundBadges();

  // 8. Comic Reader Modes (Classic Spread vs Webtoon Flow)
  initReaderModeToggle();

  // 9. Fullscreen Cinema Mode Lightbox
  initCinemaMode();

  // 10. Share & Toast Notifications
  initShareButton();
});

/* ==========================================================================
   1. Ambient Particles Canvas (Subtle Floating Cosmic Spores)
   ========================================================================== */
function initAmbientParticles() {
  const canvas = document.getElementById("ambient-canvas");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  window.addEventListener("resize", () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  const particles = [];
  const particleCount = Math.min(38, Math.floor(width / 35));

  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      radius: Math.random() * 2.2 + 0.8,
      dx: (Math.random() - 0.5) * 0.45,
      dy: -Math.random() * 0.45 - 0.15,
      alpha: Math.random() * 0.5 + 0.25,
      color: Math.random() > 0.4 ? "59, 130, 246" : "245, 158, 11" // Blue or Amber
    });
  }

  function render() {
    ctx.clearRect(0, 0, width, height);

    for (let p of particles) {
      p.x += p.dx;
      p.y += p.dy;

      if (p.y < -10) {
        p.y = height + 10;
        p.x = Math.random() * width;
      }
      if (p.x < -10) p.x = width + 10;
      if (p.x > width + 10) p.x = -10;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${p.color}, ${p.alpha})`;
      ctx.shadowBlur = 8;
      ctx.shadowColor = `rgba(${p.color}, 0.8)`;
      ctx.fill();
    }

    requestAnimationFrame(render);
  }

  render();
}

/* ==========================================================================
   2. Visual Art Style Cards Selector
   ========================================================================== */
function initStyleSelector() {
  const cards = document.querySelectorAll(".style-card");
  const hiddenSelect = document.getElementById("art-style-select");
  const previewBadge = document.getElementById("preview-style-badge");

  if (!cards.length || !hiddenSelect) return;

  cards.forEach(card => {
    card.addEventListener("click", () => {
      const selectedStyle = card.getAttribute("data-style");
      
      // Update hidden select
      hiddenSelect.value = selectedStyle;
      hiddenSelect.dispatchEvent(new Event("change"));

      // Update card visual state
      cards.forEach(c => c.classList.remove("active"));
      card.classList.add("active");

      // Update live preview badge if present
      if (previewBadge) {
        previewBadge.innerText = selectedStyle;
      }

      // Subtle haptic / audio feedback
      playPopSound(440);
    });
  });

  // Preset Chips
  const presetChips = document.querySelectorAll(".preset-chip");
  const promptInput = document.getElementById("prompt-input");
  const charInput = document.getElementById("character-input");

  presetChips.forEach(chip => {
    chip.addEventListener("click", () => {
      presetChips.forEach(c => c.classList.remove("highlighted"));
      chip.classList.add("highlighted");

      const promptText = chip.getAttribute("data-prompt");
      const charName = chip.getAttribute("data-char");
      const styleName = chip.getAttribute("data-style");
      const panelCount = chip.getAttribute("data-panels");

      if (promptText && promptInput) promptInput.value = promptText;
      if (charName && charInput) {
        charInput.value = charName;
        charInput.dispatchEvent(new Event("input"));
      }

      if (styleName) {
        hiddenSelect.value = styleName;
        cards.forEach(c => {
          if (c.getAttribute("data-style") === styleName) {
            c.classList.add("active");
          } else {
            c.classList.remove("active");
          }
        });
        if (previewBadge) previewBadge.innerText = styleName;
      }

      if (panelCount) {
        setPanelCount(panelCount);
      }

      playPopSound(520);
    });
  });
}

/* ==========================================================================
   3. Panel Count Buttons
   ========================================================================== */
function initPanelCountSelector() {
  const panelBtns = document.querySelectorAll(".panel-btn");
  const select = document.getElementById("panel-count-select");
  const mockPanelMeta = document.getElementById("mock-panel-meta");

  if (!panelBtns.length || !select) return;

  panelBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const count = btn.getAttribute("data-count");
      setPanelCount(count);
      playPopSound(480);
    });
  });
}

function setPanelCount(count) {
  const panelBtns = document.querySelectorAll(".panel-btn");
  const select = document.getElementById("panel-count-select");
  const mockPanelMeta = document.getElementById("mock-panel-meta");

  panelBtns.forEach(b => {
    if (b.getAttribute("data-count") === count.toString()) {
      b.classList.add("active");
    } else {
      b.classList.remove("active");
    }
  });

  if (select) select.value = count;
  if (mockPanelMeta) mockPanelMeta.innerText = `Scene 1 of ${count}`;
}

/* ==========================================================================
   4. Magic Inspiration Wand ("Inspire Me")
   ========================================================================== */
function initInspireMe() {
  const btnInspire = document.getElementById("btn-inspire");
  const promptInput = document.getElementById("prompt-input");
  const charInput = document.getElementById("character-input");
  const styleSelect = document.getElementById("art-style-select");
  const styleCards = document.querySelectorAll(".style-card");
  const previewBadge = document.getElementById("preview-style-badge");

  if (!btnInspire || !promptInput) return;

  const inspirationPool = [
    {
      prompt: "A brave little fox named Hope ventures into the mystical Whispering Woods to recover the fallen Starlight Blossom before shadows consume the forest.",
      char: "Hope",
      style: "Classic Comic Book",
      panels: 4
    },
    {
      prompt: "In the rain-slicked neon alleys of Neo-Veridia, a cyber-runner uncovers a sentient rogue AI core hidden inside an ancient arcade cabinet.",
      char: "Aria Volt",
      style: "Cyberpunk Sci-Fi",
      panels: 4
    },
    {
      prompt: "A weary 1940s private investigator investigates glowing celestial footsteps that mysteriously appear every midnight across Central Park.",
      char: "Jack Vance",
      style: "Dark Graphic Novel",
      panels: 4
    },
    {
      prompt: "An exiled clockwork paladin must rekindle the sacred sun-furnace of his floating island kingdom before mechanical gargoyles breach the gates.",
      char: "Sir Kay",
      style: "Classic Comic Book",
      panels: 4
    },
    {
      prompt: "A young deep-sea cartographer discovers an ancient bioluminescent city carved into the ocean trench, guarded by singing leviathans.",
      char: "Coralia",
      style: "Watercolor Fantasy",
      panels: 4
    },
    {
      prompt: "During a solar eclipse over Tokyo, a rebellious high-school martial artist awakens the sealed spirit of a lightning dragon in his grandfather's tea shop.",
      char: "Renzo",
      style: "Manga / Anime",
      panels: 4
    },
    {
      prompt: "An interstellar postal pilot crash-lands on a desert planet where dunes shift like liquid glass, discovering an ancient message meant for Earth.",
      char: "Captain Nova",
      style: "Vintage 1950s Pulp",
      panels: 4
    }
  ];

  let lastIdx = -1;

  btnInspire.addEventListener("click", () => {
    let randIdx;
    do {
      randIdx = Math.floor(Math.random() * inspirationPool.length);
    } while (randIdx === lastIdx && inspirationPool.length > 1);
    lastIdx = randIdx;

    const idea = inspirationPool[randIdx];

    // Animate button
    btnInspire.style.transform = "rotate(15deg) scale(1.08)";
    setTimeout(() => (btnInspire.style.transform = ""), 250);

    promptInput.value = idea.prompt;
    if (charInput) {
      charInput.value = idea.char;
      charInput.dispatchEvent(new Event("input"));
    }

    if (styleSelect) {
      styleSelect.value = idea.style;
      styleCards.forEach(c => {
        if (c.getAttribute("data-style") === idea.style) {
          c.classList.add("active");
        } else {
          c.classList.remove("active");
        }
      });
      if (previewBadge) previewBadge.innerText = idea.style;
    }

    setPanelCount(idea.panels);
    playPopSound(600);
    showToast(`🪄 Inspired: "${idea.prompt.slice(0, 35)}..."`);
  });
}

/* ==========================================================================
   5. Live Storyboard Mock Synchronization
   ========================================================================== */
function initLiveMockSync() {
  const charInput = document.getElementById("character-input");
  const speakerName = document.getElementById("mock-speaker-name");

  if (charInput && speakerName) {
    charInput.addEventListener("input", () => {
      const val = charInput.value.trim();
      speakerName.innerText = val ? val.toUpperCase() : "HERO";
    });
  }
}

/* ==========================================================================
   6. Form Submission & Enhanced Loading Modal Progression
   ========================================================================== */
function initLoadingModal() {
  const form = document.getElementById("comic-create-form");
  const overlay = document.getElementById("loading-overlay");
  const stepText = document.getElementById("loading-step");
  const detailText = document.getElementById("loading-detail");
  const progressBar = document.getElementById("loading-progress-bar");

  if (!form || !overlay) return;

  const milestones = [
    {
      title: "⚡ Writing Dramatic Story Arc with Gemini...",
      detail: "Structuring realistic three-act narrative pacing, sensory worldbuilding, and authentic dialogue.",
      stepId: "step-item-1",
      pct: 25
    },
    {
      title: "🎬 Directing Cinematic Visual Panels...",
      detail: "Formulating character visual consistency, dramatic camera angles, and atmospheric lighting.",
      stepId: "step-item-2",
      pct: 55
    },
    {
      title: "💬 Inking Speech Balloons & Sound Badges...",
      detail: "Rendering dialogue pointers, narration caption cards, and impact typography.",
      stepId: "step-item-3",
      pct: 80
    },
    {
      title: "📖 Compiling Print-Ready PDF Comic Book...",
      detail: "Formatting high-resolution A4 multi-page document with cover art and headers.",
      stepId: "step-item-4",
      pct: 95
    }
  ];

  form.addEventListener("submit", () => {
    overlay.style.display = "flex";
    playPopSound(500);

    let idx = 0;
    const interval = setInterval(() => {
      idx++;
      if (idx < milestones.length) {
        const m = milestones[idx];
        if (stepText) stepText.innerText = m.title;
        if (detailText) detailText.innerText = m.detail;
        if (progressBar) progressBar.style.width = `${m.pct}%`;

        // Update checklist
        const prevItem = document.getElementById(milestones[idx - 1].stepId);
        const curItem = document.getElementById(m.stepId);
        if (prevItem) {
          prevItem.classList.remove("active");
          prevItem.classList.add("done");
        }
        if (curItem) {
          curItem.classList.add("active");
        }
      }
    }, 2800);
  });
}

/* ==========================================================================
   7. Interactive Procedural Web Audio Sound Synthesizer
   ========================================================================== */
let audioCtx = null;

function getAudioContext() {
  if (!audioCtx) {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (AudioContext) audioCtx = new AudioContext();
  }
  if (audioCtx && audioCtx.state === "suspended") {
    audioCtx.resume();
  }
  return audioCtx;
}

function playPopSound(freq = 440) {
  try {
    const ctx = getAudioContext();
    if (!ctx) return;

    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = "sine";
    osc.frequency.setValueAtTime(freq, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(freq * 0.4, ctx.currentTime + 0.12);

    gain.gain.setValueAtTime(0.18, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.12);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start();
    osc.stop(ctx.currentTime + 0.13);
  } catch (e) {
    // Audio optional
  }
}

function playComicImpactSound(effectName = "POW") {
  try {
    const ctx = getAudioContext();
    if (!ctx) return;

    const now = ctx.currentTime;

    // 1. Noise burst for punchy impact
    const bufferSize = ctx.sampleRate * 0.2;
    const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (ctx.sampleRate * 0.05));
    }

    const noise = ctx.createBufferSource();
    noise.buffer = buffer;

    const noiseFilter = ctx.createBiquadFilter();
    noiseFilter.type = "lowpass";
    noiseFilter.frequency.setValueAtTime(800, now);

    const noiseGain = ctx.createGain();
    noiseGain.gain.setValueAtTime(0.35, now);
    noiseGain.gain.exponentialRampToValueAtTime(0.01, now + 0.18);

    noise.connect(noiseFilter);
    noiseFilter.connect(noiseGain);
    noiseGain.connect(ctx.destination);
    noise.start(now);

    // 2. Punchy low-end thud
    const osc = ctx.createOscillator();
    const oscGain = ctx.createGain();

    osc.type = "triangle";
    osc.frequency.setValueAtTime(220, now);
    osc.frequency.exponentialRampToValueAtTime(45, now + 0.18);

    oscGain.gain.setValueAtTime(0.4, now);
    oscGain.gain.exponentialRampToValueAtTime(0.001, now + 0.22);

    osc.connect(oscGain);
    oscGain.connect(ctx.destination);
    osc.start(now);
    osc.stop(now + 0.23);
  } catch (e) {
    // Optional
  }
}

function initSoundBadges() {
  const soundBadges = document.querySelectorAll(".sound-badge-interactive");
  soundBadges.forEach(badge => {
    badge.addEventListener("click", e => {
      e.stopPropagation();
      const sound = badge.getAttribute("data-sound") || "POW!";
      playComicImpactSound(sound);

      // Micro-animation
      badge.style.transform = "scale(1.2) rotate(6deg)";
      setTimeout(() => {
        badge.style.transform = "";
      }, 200);

      showToast(`💥 ${sound}`);
    });
  });
}

/* ==========================================================================
   8. Comic Reader Modes (Classic Spread vs Webtoon Flow)
   ========================================================================== */
function initReaderModeToggle() {
  const toggle = document.getElementById("reader-mode-toggle");
  const wrapper = document.getElementById("panels-wrapper");
  if (!toggle || !wrapper) return;

  const buttons = toggle.querySelectorAll(".mode-btn");

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      const mode = btn.getAttribute("data-mode");
      if (mode === "cinema") return; // Handled by cinema init

      buttons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      if (mode === "webtoon") {
        wrapper.classList.remove("layout-classic");
        wrapper.classList.add("layout-webtoon");
        showToast("📜 Switched to Webtoon Continuous Scroll");
      } else {
        wrapper.classList.remove("layout-webtoon");
        wrapper.classList.add("layout-classic");
        showToast("📰 Switched to Classic Graphic Novel Spread");
      }
      playPopSound(440);
    });
  });
}

/* ==========================================================================
   9. Fullscreen Cinema Mode Lightbox
   ========================================================================== */
function initCinemaMode() {
  const btnOpen = document.getElementById("btn-open-cinema");
  const modal = document.getElementById("cinema-modal");
  const overlay = document.getElementById("cinema-overlay");
  const btnClose = document.getElementById("btn-close-cinema");
  const btnPrev = document.getElementById("btn-cinema-prev");
  const btnNext = document.getElementById("btn-cinema-next");
  const jsonEl = document.getElementById("comic-data-json");

  if (!btnOpen || !modal || !jsonEl) return;

  let comicData = null;
  try {
    comicData = JSON.parse(jsonEl.textContent);
  } catch (e) {
    return;
  }

  const panels = comicData.panels || [];
  if (!panels.length) return;

  let currentIdx = 0;

  function renderCinemaPanel(idx) {
    currentIdx = Math.max(0, Math.min(idx, panels.length - 1));
    const p = panels[currentIdx];

    const titleEl = document.getElementById("cinema-panel-title");
    const counterEl = document.getElementById("cinema-counter");
    const imgEl = document.getElementById("cinema-img");
    const soundEl = document.getElementById("cinema-sound");
    const narrationEl = document.getElementById("cinema-narration");
    const speakerEl = document.getElementById("cinema-speaker");
    const dialogueEl = document.getElementById("cinema-dialogue");
    const dotsWrap = document.getElementById("cinema-dots");

    if (titleEl) titleEl.innerText = `Panel ${p.panel_number}: ${p.panel_title || 'Scene'}`;
    if (counterEl) counterEl.innerText = `${currentIdx + 1} / ${panels.length}`;
    if (imgEl) imgEl.src = p.image_url;

    if (soundEl) {
      if (p.sound_effect) {
        soundEl.style.display = "block";
        soundEl.innerText = p.sound_effect;
      } else {
        soundEl.style.display = "none";
      }
    }

    if (narrationEl) {
      narrationEl.innerText = p.caption || "";
      narrationEl.style.display = p.caption ? "block" : "none";
    }

    if (speakerEl) speakerEl.innerText = `💬 ${p.speaker || 'HERO'}`;
    if (dialogueEl) dialogueEl.innerText = `"${p.dialogue_text || p.dialogue || ''}"`;

    // Render pagination dots
    if (dotsWrap) {
      dotsWrap.innerHTML = "";
      panels.forEach((_, i) => {
        const dot = document.createElement("div");
        dot.className = `cinema-dot ${i === currentIdx ? 'active' : ''}`;
        dot.addEventListener("click", () => renderCinemaPanel(i));
        dotsWrap.appendChild(dot);
      });
    }

    // Nav buttons disabled state
    if (btnPrev) btnPrev.disabled = currentIdx === 0;
    if (btnNext) btnNext.disabled = currentIdx === panels.length - 1;
  }

  function openCinema() {
    modal.style.display = "flex";
    document.body.style.overflow = "hidden";
    renderCinemaPanel(0);
    playPopSound(500);
  }

  function closeCinema() {
    modal.style.display = "none";
    document.body.style.overflow = "";
    playPopSound(350);
  }

  btnOpen.addEventListener("click", openCinema);
  if (btnClose) btnClose.addEventListener("click", closeCinema);
  if (overlay) overlay.addEventListener("click", closeCinema);

  if (btnPrev) {
    btnPrev.addEventListener("click", () => {
      if (currentIdx > 0) renderCinemaPanel(currentIdx - 1);
    });
  }

  if (btnNext) {
    btnNext.addEventListener("click", () => {
      if (currentIdx < panels.length - 1) renderCinemaPanel(currentIdx + 1);
    });
  }

  // Keyboard navigation
  window.addEventListener("keydown", e => {
    if (modal.style.display === "flex") {
      if (e.key === "Escape") closeCinema();
      if (e.key === "ArrowRight" && currentIdx < panels.length - 1) renderCinemaPanel(currentIdx + 1);
      if (e.key === "ArrowLeft" && currentIdx > 0) renderCinemaPanel(currentIdx - 1);
    }
  });
}

/* ==========================================================================
   10. Share & Toast Notifications
   ========================================================================== */
function initShareButton() {
  const btnShare = document.getElementById("btn-share-comic");
  if (!btnShare) return;

  btnShare.addEventListener("click", () => {
    navigator.clipboard.writeText(window.location.href).then(() => {
      showToast("🔗 Link copied to clipboard!");
      playPopSound(580);
    }).catch(() => {
      showToast("🔗 Link: " + window.location.href);
    });
  });
}

function showToast(message) {
  let toast = document.getElementById("toast-notification");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "toast-notification";
    toast.className = "toast-notification";
    document.body.appendChild(toast);
  }

  toast.innerText = message;
  toast.classList.add("show");

  clearTimeout(toast._timeout);
  toast._timeout = setTimeout(() => {
    toast.classList.remove("show");
  }, 3200);
}

/* ==========================================================================
   11. Panel Art Regeneration Engine
   ========================================================================== */
async function regeneratePanel(comicId, panelNumber) {
  const btn = document.getElementById(`btn-regen-${panelNumber}`);
  const img = document.getElementById(`panel-img-${panelNumber}`);
  if (!btn || !img) return;

  btn.classList.add("loading");
  const origHtml = btn.innerHTML;
  btn.innerHTML = `<span class="regen-icon">⏳</span> Inking...`;
  btn.disabled = true;

  try {
    const res = await fetch("/api/regenerate-panel", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ comic_id: comicId, panel_number: panelNumber })
    });

    if (res.ok) {
      const data = await res.json();
      img.src = `${data.image_url}?t=${Date.now()}`;
      showToast(`✨ Panel ${panelNumber} artwork refreshed!`);
      playPopSound(540);
    } else {
      showToast(`⚠️ Could not regenerate panel ${panelNumber}`);
    }
  } catch (err) {
    showToast(`⚠️ Error: ${err.message}`);
  } finally {
    btn.classList.remove("loading");
    btn.innerHTML = origHtml;
    btn.disabled = false;
  }
}

