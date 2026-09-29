// ComicCraft Interactive Studio & Comic Reader Engine

document.addEventListener("DOMContentLoaded", () => {
  // 1. Interactive Ambient Particles Background
  initAmbientParticles();

  // 2. Visual Art Style Cards & Preset Synchronization
  initStyleSelector();

  // 3. Panel Count Buttons
  initPanelCountSelector();

  // 4. Magic Inspiration Wand ("Inspire Me") & Supercharge Polish
  initInspireMe();
  initSuperchargePrompt();
  initCharacterArchetypes();

  // 5. Live Storyboard Mock Synchronization
  initLiveMockSync();

  // 6. Form Submission & Enhanced Loading Modal Progression
  initLoadingModal();

  // 7. Interactive Procedural Web Audio Sound Synthesizer & Soundboard
  initSoundBadges();
  initComicSoundboard();
  initStorySparks();

  // 8. Comic Reader Modes (Classic Spread vs Webtoon Flow)
  initReaderModeToggle();

  // 9. Fullscreen Cinema Mode Lightbox
  initCinemaMode();

  // 10. Voice Narrator, Shaders, Script Editor & Strip Export
  initVoiceNarrator();
  initComicShaders();
  initScriptEditor();
  initStripExport();

  // 11. API Key Configuration Modal
  initApiKeyModal();

  // 12. Share & Toast Notifications
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
   5. Enhanced Live Storyboard Multi-Scene Engine & Fullscreen Toggle
   ========================================================================== */
function initLiveMockSync() {
  // 1. Show/Hide Toggle Button
  const btnToggle = document.getElementById("btn-toggle-storyboard");
  const studioGrid = document.querySelector(".studio-grid");
  const toggleText = document.getElementById("toggle-text");
  const toggleIcon = document.getElementById("toggle-icon");

  if (btnToggle && studioGrid) {
    btnToggle.addEventListener("click", () => {
      const isCollapsed = studioGrid.classList.toggle("preview-collapsed");
      if (isCollapsed) {
        if (toggleText) toggleText.innerText = "Show Storyboard";
        if (toggleIcon) toggleIcon.innerText = "📐";
        btnToggle.style.background = "#eff6ff";
        showToast("🖥️ Wide Workspace: Storyboard Hidden");
      } else {
        if (toggleText) toggleText.innerText = "Hide Storyboard";
        if (toggleIcon) toggleIcon.innerText = "👁️";
        btnToggle.style.background = "";
        showToast("👁️ Storyboard Preview Restored");
      }
      playPopSound(500);
    });
  }

  // 2. Multi-Scene Storyboard Elements
  const sceneElements = {
    tabs: document.querySelectorAll(".scene-tab-btn"),
    btnPrev: document.getElementById("btn-scene-prev"),
    btnNext: document.getElementById("btn-scene-next"),
    panelTitle: document.getElementById("mock-panel-title"),
    panelMeta: document.getElementById("mock-panel-meta"),
    artImg: document.getElementById("mock-art-image"),
    soundBadge: document.getElementById("mock-sound-badge"),
    cameraShot: document.getElementById("mock-camera-shot"),
    narrationText: document.getElementById("mock-narration-text"),
    speakerName: document.getElementById("mock-speaker-name"),
    dialogueText: document.getElementById("mock-dialogue-text"),
    charInput: document.getElementById("character-input"),
    promptInput: document.getElementById("prompt-input")
  };

  const sceneTemplates = {
    1: {
      title: "Panel 1: The Inciting Hook",
      shot: "ESTABLISHING WIDE SHOT",
      sound: "RUSTLE...",
      image: "/static/images/hope_fox.jpg",
      narration: "Elders called it madness. But when the starlight blossoms began to wither, courage wasn't a choice—it was a necessity.",
      dialogue: "The elders warned that no one returns from the Gloom... but I can feel the trees weeping."
    },
    2: {
      title: "Panel 2: The Rising Tension",
      shot: "DUTCH ANGLE / MEDIUM TENSION",
      sound: "WHOOSH!",
      image: "/static/images/hero_forest_bg.jpg",
      narration: "Every whisper of the wind carried forgotten warnings. Shadows stretched along the mossy stone arches like reaching claws.",
      dialogue: "Steady now. Fear is just mist—it only blinds you if you stop moving forward!"
    },
    3: {
      title: "Panel 3: The Climax Splash",
      shot: "DYNAMIC LOW-ANGLE SPLASH",
      sound: "KABOOM!",
      image: "/static/images/landscape_bg.jpg",
      narration: "A blinding arc of celestial radiance tore through the canopy, illuminating the sacred blossom atop the obsidian monolith.",
      dialogue: "There you are! Stand down, shadows—this light belongs to the stars!"
    },
    4: {
      title: "Panel 4: The Poignant Resolution",
      shot: "EMOTIONAL CLOSE-UP / WIDE HORIZON",
      sound: "CHIRP...",
      image: "/static/images/hope_fox.jpg",
      narration: "The dawn crept quietly through the branches, bathing the restored forest in warm, golden tranquility.",
      dialogue: "It's over. The grove breathes again. Tomorrow will come after all."
    }
  };

  let currentSceneIdx = 1;

  function renderScene(sceneNum) {
    currentSceneIdx = sceneNum;
    const data = sceneTemplates[sceneNum];
    if (!data) return;

    // Update active tab
    sceneElements.tabs.forEach(tab => {
      if (tab.getAttribute("data-scene") === sceneNum.toString()) {
        tab.classList.add("active");
      } else {
        tab.classList.remove("active");
      }
    });

    const charName = sceneElements.charInput ? sceneElements.charInput.value.trim() : "HERO";
    const displayName = charName ? charName.toUpperCase() : "HERO";

    if (sceneElements.panelTitle) sceneElements.panelTitle.innerText = data.title;
    if (sceneElements.panelMeta) sceneElements.panelMeta.innerText = `Scene ${sceneNum} of 4`;
    if (sceneElements.cameraShot) sceneElements.cameraShot.innerText = data.shot;
    if (sceneElements.soundBadge) sceneElements.soundBadge.innerText = data.sound;
    if (sceneElements.artImg) sceneElements.artImg.src = data.image;
    if (sceneElements.narrationText) sceneElements.narrationText.innerText = `"${data.narration}"`;
    if (sceneElements.speakerName) sceneElements.speakerName.innerText = displayName;
    if (sceneElements.dialogueText) sceneElements.dialogueText.innerText = `"${data.dialogue}"`;

    // Tactile sound
    playPopSound(420 + sceneNum * 60);
  }

  // Bind tabs
  sceneElements.tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      const num = parseInt(tab.getAttribute("data-scene"), 10) || 1;
      renderScene(num);
    });
  });

  // Bind prev/next
  if (sceneElements.btnPrev) {
    sceneElements.btnPrev.addEventListener("click", () => {
      const prev = currentSceneIdx > 1 ? currentSceneIdx - 1 : 4;
      renderScene(prev);
    });
  }
  if (sceneElements.btnNext) {
    sceneElements.btnNext.addEventListener("click", () => {
      const next = currentSceneIdx < 4 ? currentSceneIdx + 1 : 1;
      renderScene(next);
    });
  }

  // Dynamic character input update
  if (sceneElements.charInput) {
    sceneElements.charInput.addEventListener("input", () => {
      const val = sceneElements.charInput.value.trim();
      if (sceneElements.speakerName) {
        sceneElements.speakerName.innerText = val ? val.toUpperCase() : "HERO";
      }
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
   7b. Onomatopoeia Comic Soundboard & Visual Burst Particles
   ========================================================================== */
function initComicSoundboard() {
  const soundBtns = document.querySelectorAll(".sfx-blast-btn");
  if (!soundBtns.length) return;

  soundBtns.forEach(btn => {
    btn.addEventListener("click", (e) => {
      const sfxText = btn.getAttribute("data-sfx") || "POW!";
      const soundType = btn.getAttribute("data-sound") || "punch";

      // 1. Synthesize Audio
      playProceduralSfx(soundType);

      // 2. Spawn Floating Visual Comic Burst
      spawnComicBurst(e.clientX, e.clientY, sfxText);

      // 3. Tactile Feedback
      btn.style.transform = "scale(0.92) translate(2px, 2px)";
      setTimeout(() => {
        btn.style.transform = "";
      }, 150);

      showToast(`💥 SFX: ${sfxText}`);
    });
  });
}

function spawnComicBurst(x, y, text) {
  const burst = document.createElement("div");
  burst.className = "comic-burst-bubble";
  burst.textContent = text;
  burst.style.left = `${x}px`;
  burst.style.top = `${y}px`;

  document.body.appendChild(burst);

  setTimeout(() => {
    burst.remove();
  }, 800);
}

function playProceduralSfx(type) {
  try {
    const ctx = getAudioContext();
    if (!ctx) return;
    const now = ctx.currentTime;

    if (type === "punch" || type === "boom") {
      playComicImpactSound(type === "boom" ? "BOOM" : "POW");
    } else if (type === "laser") {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "sawtooth";
      osc.frequency.setValueAtTime(1100, now);
      osc.frequency.exponentialRampToValueAtTime(120, now + 0.16);

      gain.gain.setValueAtTime(0.3, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.16);

      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.17);
    } else if (type === "whoosh") {
      const bufferSize = ctx.sampleRate * 0.25;
      const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = (Math.random() * 2 - 1);
      }
      const noise = ctx.createBufferSource();
      noise.buffer = buffer;

      const filter = ctx.createBiquadFilter();
      filter.type = "bandpass";
      filter.frequency.setValueAtTime(300, now);
      filter.frequency.linearRampToValueAtTime(1600, now + 0.12);
      filter.frequency.linearRampToValueAtTime(250, now + 0.25);

      const gain = ctx.createGain();
      gain.gain.setValueAtTime(0.01, now);
      gain.gain.linearRampToValueAtTime(0.35, now + 0.1);
      gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);

      noise.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);
      noise.start(now);
    } else if (type === "electric") {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "square";
      osc.frequency.setValueAtTime(80, now);
      osc.frequency.setValueAtTime(120, now + 0.05);
      osc.frequency.setValueAtTime(65, now + 0.1);

      gain.gain.setValueAtTime(0.25, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.2);

      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.21);
    } else if (type === "sparkle") {
      const notes = [659.25, 880, 1174.66, 1760];
      notes.forEach((freq, idx) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(freq, now + idx * 0.04);
        gain.gain.setValueAtTime(0.18, now + idx * 0.04);
        gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.04 + 0.18);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now + idx * 0.04);
        osc.stop(now + idx * 0.04 + 0.19);
      });
    }
  } catch (e) {
    // Audio optional
  }
}

/* ==========================================================================
   7c. Interactive Comic Story Sparks (Premise Roulette)
   ========================================================================== */
function initStorySparks() {
  const btnRoll = document.getElementById("btn-roll-sparks");
  const btnApply = document.getElementById("btn-apply-sparks");
  const heroEl = document.getElementById("spark-hero-text");
  const questEl = document.getElementById("spark-quest-text");
  const twistEl = document.getElementById("spark-twist-text");
  const promptInput = document.getElementById("prompt-input");
  const charInput = document.getElementById("character-input");
  const artSelect = document.getElementById("art-style-select");
  const styleCards = document.querySelectorAll(".style-card");
  const previewBadge = document.getElementById("preview-style-badge");

  if (!btnRoll || !heroEl || !questEl || !twistEl) return;

  const sparkHeroes = [
    { name: "Hope", label: "🦊 Hope (Spirited Fox)", style: "Classic Comic Book", intro: "A brave little fox named Hope" },
    { name: "Jack Vance", label: "🕵️ Jack Vance (Noir P.I.)", style: "Dark Graphic Novel", intro: "Cynical detective Jack Vance" },
    { name: "Aria Volt", label: "⚡ Aria Volt (Netrunner)", style: "Cyberpunk Sci-Fi", intro: "Renegade netrunner Aria Volt" },
    { name: "Sir Kay", label: "⚔️ Sir Kay (Clockwork Knight)", style: "Classic Comic Book", intro: "A noble clockwork knight named Sir Kay" },
    { name: "Dr. Luna", label: "🔭 Dr. Luna (Cosmic Astronomer)", style: "Watercolor Fantasy", intro: "Deep-space astrophysicist Dr. Luna" },
    { name: "Kaelen", label: "🗡️ Kaelen (Blade Mystic)", style: "Manga / Anime", intro: "Exiled blade prodigy Kaelen" },
    { name: "Pip", label: "🐉 Pip (Star Dragon)", style: "Watercolor Fantasy", intro: "Curious star-drake hatchling Pip" },
    { name: "Baron Von Zinc", label: "🎩 Baron Von Zinc (Airship Alchemist)", style: "Vintage 1950s Pulp", intro: "Eccentric aerial inventor Baron Von Zinc" }
  ];

  const sparkQuests = [
    "ventures into the mystical Whispering Woods to recover the fallen Starlight Blossom",
    "infiltrates a high-orbit megacity to liberate an ancient celestial AI core",
    "investigates eerie luminescent footprints leading through rainy New York alleyways",
    "races across an exploding asteroid belt to save a dormant cosmic leviathan",
    "defends the last reservoir of pure magic from swarming mechanical shadow-beasts",
    "embarks on a forbidden deep-sea descent to chart a sunken Atlantean metropolis",
    "tracks a reality-warping glitch causing temporal echoes across Victorian London"
  ];

  const sparkTwists = [
    "only to discover the trees whisper forgotten secrets that rewrite the laws of gravity.",
    "realizing the stolen artifact is sentient and has chosen them as its protector.",
    "when time begins moving backwards with each tick of the city clocktower.",
    "uncovering that the monstrous shadow-beasts were originally created to protect humanity.",
    "discovering their reflection in mirrors is broadcasting messages from a parallel timeline.",
    "when the night sky abruptly reorganizes itself into a giant celestial map."
  ];

  let currentSpark = {
    hero: sparkHeroes[0],
    quest: sparkQuests[0],
    twist: sparkTwists[0]
  };

  btnRoll.addEventListener("click", () => {
    btnRoll.classList.add("rolling");
    playPopSound(580);

    // Rapid shuffle animation
    let shuffleCount = 0;
    const interval = setInterval(() => {
      const randHero = sparkHeroes[Math.floor(Math.random() * sparkHeroes.length)];
      const randQuest = sparkQuests[Math.floor(Math.random() * sparkQuests.length)];
      const randTwist = sparkTwists[Math.floor(Math.random() * sparkTwists.length)];

      heroEl.textContent = randHero.label;
      questEl.textContent = randQuest;
      twistEl.textContent = randTwist;

      shuffleCount++;
      if (shuffleCount >= 5) {
        clearInterval(interval);
        btnRoll.classList.remove("rolling");

        currentSpark.hero = randHero;
        currentSpark.quest = randQuest;
        currentSpark.twist = randTwist;

        playProceduralSfx("sparkle");
        showToast("🎲 Rolled New Story Sparks!");
      }
    }, 60);
  });

  if (btnApply) {
    btnApply.addEventListener("click", () => {
      const fullPrompt = `${currentSpark.hero.intro} ${currentSpark.quest}, ${currentSpark.twist}`;

      if (promptInput) {
        promptInput.value = fullPrompt;
        promptInput.focus();
      }

      if (charInput) {
        charInput.value = currentSpark.hero.name;
        charInput.dispatchEvent(new Event("input"));
      }

      if (artSelect && currentSpark.hero.style) {
        artSelect.value = currentSpark.hero.style;
        styleCards.forEach(c => {
          if (c.getAttribute("data-style") === currentSpark.hero.style) {
            c.classList.add("active");
          } else {
            c.classList.remove("active");
          }
        });
        if (previewBadge) previewBadge.innerText = currentSpark.hero.style;
      }

      playProceduralSfx("laser");
      showToast(`⚡ Story Loaded: ${currentSpark.hero.name}'s Adventure!`);
    });
  }
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

/* ==========================================================================
   12. AI Prompt Supercharger & Character Archetypes
   ========================================================================== */
function initSuperchargePrompt() {
  const btn = document.getElementById("btn-supercharge");
  const promptInput = document.getElementById("prompt-input");
  const charInput = document.getElementById("character-input");
  const styleSelect = document.getElementById("art-style-select");
  if (!btn || !promptInput) return;

  btn.addEventListener("click", async () => {
    const rawPrompt = promptInput.value.trim();
    if (!rawPrompt) {
      showToast("💡 Please enter a short story idea first!");
      promptInput.focus();
      return;
    }

    const origHtml = btn.innerHTML;
    btn.innerHTML = `<span class="sparkle-rot">✨</span> Polishing...`;
    btn.disabled = true;

    try {
      const res = await fetch("/api/enhance-prompt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt: rawPrompt,
          character_name: charInput ? charInput.value.trim() : "Hero",
          art_style: styleSelect ? styleSelect.value : "Classic Comic Book"
        })
      });

      if (res.ok) {
        const data = await res.json();
        const enhanced = data.enhanced_prompt;
        // Animated typewriter insertion
        promptInput.value = "";
        let i = 0;
        const timer = setInterval(() => {
          if (i < enhanced.length) {
            promptInput.value += enhanced.charAt(i);
            i++;
          } else {
            clearInterval(timer);
            promptInput.dispatchEvent(new Event("input"));
            showToast("✨ Story premise elevated with cinematic atmosphere!");
            playPopSound(620);
          }
        }, 12);
      } else {
        showToast("⚠️ Could not polish prompt at this time.");
      }
    } catch (err) {
      showToast("⚠️ Error: " + err.message);
    } finally {
      btn.innerHTML = origHtml;
      btn.disabled = false;
    }
  });
}

function initCharacterArchetypes() {
  const charButtons = document.querySelectorAll(".char-tag-btn");
  const charInput = document.getElementById("character-input");
  if (!charButtons.length || !charInput) return;

  charButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const name = btn.dataset.charName;
      const styleName = btn.dataset.charStyle;
      charInput.value = name;
      charInput.dispatchEvent(new Event("input"));

      // Sync with style button
      const styleCard = document.querySelector(`.style-choice-card[data-style="${styleName}"]`);
      if (styleCard) {
        styleCard.click();
      }

      showToast(`Selected protagonist: ${name}`);
      playPopSound(520);
    });
  });
}

/* ==========================================================================
   13. Voice Narrator (Web Speech API)
   ========================================================================== */
let narrationController = {
  isSpeaking: false,
  currentIndex: 0,
  speechQueue: [],
  activeUtterance: null
};

function initVoiceNarrator() {
  const playBtn = document.getElementById("btn-narrate-play");
  const stopBtn = document.getElementById("btn-narrate-stop");
  const statusText = document.getElementById("narrator-status");
  if (!playBtn) return;

  if (!("speechSynthesis" in window)) {
    if (statusText) statusText.innerText = "Voice speech not supported in this browser.";
    playBtn.disabled = true;
    return;
  }

  playBtn.addEventListener("click", () => {
    if (narrationController.isSpeaking) {
      stopNarration();
    } else {
      startNarration();
    }
  });

  if (stopBtn) {
    stopBtn.addEventListener("click", () => {
      stopNarration();
    });
  }
}

function startNarration() {
  const playBtn = document.getElementById("btn-narrate-play");
  const icon = document.getElementById("narrate-play-icon");
  const label = document.getElementById("narrate-play-text");

  const dataScript = document.getElementById("comic-data-json");
  let comic = null;
  if (dataScript) {
    try { comic = JSON.parse(dataScript.textContent); } catch (e) {}
  }

  if (!comic) return;

  window.speechSynthesis.cancel();
  narrationController.speechQueue = [];
  narrationController.currentIndex = 0;
  narrationController.isSpeaking = true;

  if (playBtn) playBtn.classList.add("speaking");
  if (icon) icon.innerText = "⏸";
  if (label) label.innerText = "Pause Story";

  // Step 0: Title & Prologue
  if (comic.title) {
    narrationController.speechQueue.push({
      text: comic.title + (comic.synopsis ? ". " + comic.synopsis : ""),
      panelNumber: null,
      desc: "Title & Prologue"
    });
  }

  // Step 1..N: Each panel
  (comic.panels || []).forEach(p => {
    let panelScript = `Panel ${p.panel_number}: ${p.panel_title}. `;
    if (p.caption) panelScript += `Narration: ${p.caption}. `;
    if (p.dialogue_text) panelScript += `${p.speaker || "Hero"} says: "${p.dialogue_text}". `;
    if (p.sound_effect) panelScript += `${p.sound_effect}! `;

    narrationController.speechQueue.push({
      text: panelScript,
      panelNumber: p.panel_number,
      desc: `Panel ${p.panel_number}: ${p.panel_title}`
    });
  });

  speakNextQueueItem();
}

function speakNextQueueItem() {
  if (!narrationController.isSpeaking) return;

  if (narrationController.currentIndex >= narrationController.speechQueue.length) {
    stopNarration();
    showToast("🏁 Story narration complete!");
    return;
  }

  const item = narrationController.speechQueue[narrationController.currentIndex];
  const statusText = document.getElementById("narrator-status");
  if (statusText) statusText.innerText = `Narrating: ${item.desc}`;

  // Highlight active panel in viewer
  document.querySelectorAll(".panel-display-item").forEach(el => el.classList.remove("active-narrating-panel"));
  if (item.panelNumber) {
    const activeCard = document.getElementById(`panel-card-${item.panelNumber}`);
    if (activeCard) {
      activeCard.classList.add("active-narrating-panel");
      activeCard.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }

  const utterance = new SpeechSynthesisUtterance(item.text);
  utterance.rate = 0.98;
  utterance.pitch = 1.0;

  const voices = window.speechSynthesis.getVoices();
  const englishVoice = voices.find(v => v.lang.startsWith("en") && !v.name.includes("Bad") && !v.name.includes("Whisper"));
  if (englishVoice) utterance.voice = englishVoice;

  utterance.onend = () => {
    narrationController.currentIndex++;
    speakNextQueueItem();
  };

  utterance.onerror = () => {
    narrationController.currentIndex++;
    speakNextQueueItem();
  };

  narrationController.activeUtterance = utterance;
  window.speechSynthesis.speak(utterance);
}

function stopNarration() {
  window.speechSynthesis.cancel();
  narrationController.isSpeaking = false;
  narrationController.currentIndex = 0;
  narrationController.activeUtterance = null;

  const playBtn = document.getElementById("btn-narrate-play");
  const icon = document.getElementById("narrate-play-icon");
  const label = document.getElementById("narrate-play-text");
  const statusText = document.getElementById("narrator-status");

  if (playBtn) playBtn.classList.remove("speaking");
  if (icon) icon.innerText = "▶";
  if (label) label.innerText = "Narrate Story";
  if (statusText) statusText.innerText = "Narration stopped.";

  document.querySelectorAll(".panel-display-item").forEach(el => el.classList.remove("active-narrating-panel"));
}

/* ==========================================================================
   14. Live Visual Shaders / Filters
   ========================================================================== */
function initComicShaders() {
  const chips = document.querySelectorAll(".shader-chip");
  const wrapper = document.getElementById("panels-wrapper");
  if (!chips.length || !wrapper) return;

  chips.forEach(chip => {
    chip.addEventListener("click", () => {
      const shader = chip.dataset.shader;
      chips.forEach(c => c.classList.remove("active"));
      chip.classList.add("active");

      wrapper.className = wrapper.className.replace(/\bshader-\w+\b/g, "").trim();
      wrapper.classList.add(`shader-${shader}`);

      showToast(`Applied ${chip.innerText.trim()} visual filter!`);
      playPopSound(480);
    });
  });
}

/* ==========================================================================
   15. Interactive Script & Dialogue Editor
   ========================================================================== */
function initScriptEditor() {
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeScriptEditor();
    }
  });
}

function openScriptEditor(panelNumber) {
  const modal = document.getElementById("script-edit-modal");
  if (!modal) return;

  const titleLabel = document.getElementById("modal-panel-title-label");
  const panelNumInput = document.getElementById("edit-panel-number");
  const speakerInput = document.getElementById("edit-speaker-input");
  const dialogueInput = document.getElementById("edit-dialogue-input");
  const captionInput = document.getElementById("edit-caption-input");
  const sfxInput = document.getElementById("edit-sfx-input");

  if (titleLabel) titleLabel.innerText = `Edit Script for Panel ${panelNumber}`;
  if (panelNumInput) panelNumInput.value = panelNumber;

  const curSpeaker = document.getElementById(`speaker-text-${panelNumber}`)?.innerText.trim() || "";
  const curDialogue = document.getElementById(`dialogue-text-${panelNumber}`)?.innerText.replace(/^"|"$/g, "").trim() || "";
  const curCaption = document.getElementById(`caption-text-${panelNumber}`)?.innerText.trim() || "";
  const curSfx = document.getElementById(`sound-badge-${panelNumber}`)?.querySelector(".sound-text")?.innerText.trim() || "";

  if (speakerInput) speakerInput.value = curSpeaker;
  if (dialogueInput) dialogueInput.value = curDialogue;
  if (captionInput) captionInput.value = curCaption;
  if (sfxInput) sfxInput.value = curSfx;

  modal.classList.add("open");
  if (dialogueInput) dialogueInput.focus();
}

function closeScriptEditor() {
  const modal = document.getElementById("script-edit-modal");
  if (modal) modal.classList.remove("open");
}

async function saveScriptEdit(e) {
  e.preventDefault();
  const comicIdInput = document.getElementById("edit-comic-id");
  const panelNumInput = document.getElementById("edit-panel-number");
  const speakerInput = document.getElementById("edit-speaker-input");
  const dialogueInput = document.getElementById("edit-dialogue-input");
  const captionInput = document.getElementById("edit-caption-input");
  const sfxInput = document.getElementById("edit-sfx-input");
  const submitBtn = document.getElementById("btn-save-script");

  if (!comicIdInput || !panelNumInput) return;

  const comicId = comicIdInput.value;
  const panelNumber = parseInt(panelNumInput.value, 10);
  const speaker = speakerInput?.value.trim() || "";
  const dialogue = dialogueInput?.value.trim() || "";
  const caption = captionInput?.value.trim() || "";
  const soundEffect = sfxInput?.value.trim() || "";

  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerHTML = `<span>⏳</span> Saving...`;
  }

  try {
    const res = await fetch("/api/update-panel-text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        comic_id: comicId,
        panel_number: panelNumber,
        speaker: speaker,
        dialogue: dialogue,
        caption: caption,
        sound_effect: soundEffect
      })
    });

    if (res.ok) {
      const speakerEl = document.getElementById(`speaker-text-${panelNumber}`);
      const dialogueEl = document.getElementById(`dialogue-text-${panelNumber}`);
      const bubbleCard = document.getElementById(`bubble-card-${panelNumber}`);
      const captionEl = document.getElementById(`caption-text-${panelNumber}`);
      const captionCard = document.getElementById(`caption-card-${panelNumber}`);
      const soundBadge = document.getElementById(`sound-badge-${panelNumber}`);

      if (speakerEl) speakerEl.innerText = speaker;
      if (dialogueEl) dialogueEl.innerText = `"${dialogue}"`;
      if (bubbleCard) {
        if (dialogue) bubbleCard.classList.remove("hidden-bubble");
        else bubbleCard.classList.add("hidden-bubble");
      }

      if (captionEl) captionEl.innerText = caption;
      if (captionCard) {
        if (caption) captionCard.classList.remove("hidden-caption");
        else captionCard.classList.add("hidden-caption");
      }

      if (soundBadge) {
        const textSpan = soundBadge.querySelector(".sound-text");
        if (textSpan) textSpan.innerText = soundEffect;
        soundBadge.dataset.sound = soundEffect;
        if (soundEffect) soundBadge.classList.remove("hidden-badge");
        else soundBadge.classList.add("hidden-badge");
      }

      const dataScript = document.getElementById("comic-data-json");
      if (dataScript) {
        try {
          const comicData = JSON.parse(dataScript.textContent);
          const p = comicData.panels.find(x => x.panel_number === panelNumber);
          if (p) {
            p.speaker = speaker;
            p.dialogue_text = dialogue;
            p.dialogue = `${speaker}: '${dialogue}'`;
            p.caption = caption;
            p.sound_effect = soundEffect;
            dataScript.textContent = JSON.stringify(comicData);
          }
        } catch (e) {}
      }

      closeScriptEditor();
      showToast(`💾 Panel ${panelNumber} script updated and PDF refreshed!`);
      playPopSound(560);
    } else {
      showToast("⚠️ Failed to update script.");
    }
  } catch (err) {
    showToast("⚠️ Error: " + err.message);
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = `<span>💾</span> <span>Save Changes & Refresh PDF</span>`;
    }
  }
}

window.openScriptEditor = openScriptEditor;
window.closeScriptEditor = closeScriptEditor;
window.saveScriptEdit = saveScriptEdit;

/* ==========================================================================
   16. Web Audio API Comic Sound Effects Synthesizer
   ========================================================================== */
function playComicSfx(sfxText, event) {
  if (!sfxText) return;

  if (event && event.pageX) {
    const burst = document.createElement("div");
    burst.className = "sfx-particle-blast";
    burst.innerText = sfxText;
    burst.style.left = `${event.pageX}px`;
    burst.style.top = `${event.pageY}px`;
    document.body.appendChild(burst);
    setTimeout(() => burst.remove(), 700);
  }

  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    const now = ctx.currentTime;
    const upper = sfxText.toUpperCase();

    if (upper.includes("BOOM") || upper.includes("POW") || upper.includes("BANG") || upper.includes("CRASH")) {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "sawtooth";
      osc.frequency.setValueAtTime(140, now);
      osc.frequency.exponentialRampToValueAtTime(32, now + 0.35);

      gain.gain.setValueAtTime(0.35, now);
      gain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);

      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.4);
    } else if (upper.includes("BZZT") || upper.includes("ZAP") || upper.includes("CRACKLE")) {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "square";
      osc.frequency.setValueAtTime(750, now);
      osc.frequency.linearRampToValueAtTime(180, now + 0.25);

      gain.gain.setValueAtTime(0.25, now);
      gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);

      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.25);
    } else if (upper.includes("WHOOSH") || upper.includes("SWOOSH") || upper.includes("SHHHK")) {
      const bufferSize = ctx.sampleRate * 0.3;
      const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = Math.random() * 2 - 1;
      }
      const noise = ctx.createBufferSource();
      noise.buffer = buffer;

      const filter = ctx.createBiquadFilter();
      filter.type = "bandpass";
      filter.frequency.setValueAtTime(400, now);
      filter.frequency.exponentialRampToValueAtTime(1800, now + 0.15);
      filter.frequency.exponentialRampToValueAtTime(200, now + 0.3);

      const gain = ctx.createGain();
      gain.gain.setValueAtTime(0.3, now);
      gain.gain.exponentialRampToValueAtTime(0.01, now + 0.3);

      noise.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);
      noise.start(now);
    } else {
      playPopSound(580);
    }
  } catch (err) {
    console.warn("Web audio playback error:", err);
  }
}
window.playComicSfx = playComicSfx;

/* ==========================================================================
   17. High-Res Comic Strip Image Export (HTML5 Canvas Composite)
   ========================================================================== */
function initStripExport() {
  const btn = document.getElementById("btn-export-strip");
  if (!btn) return;

  btn.addEventListener("click", async () => {
    const panels = document.querySelectorAll(".panel-display-item");
    if (!panels.length) return;

    btn.disabled = true;
    const origHtml = btn.innerHTML;
    btn.innerHTML = `<span>⏳</span> Rendering Strip...`;
    showToast("🎨 Compositing continuous comic strip image...");

    try {
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");

      const stripWidth = 900;
      const headerHeight = 160;
      const panelHeight = 700;
      const gap = 30;
      const totalHeight = headerHeight + panels.length * (panelHeight + gap) + 40;

      canvas.width = stripWidth;
      canvas.height = totalHeight;

      ctx.fillStyle = "#0f172a";
      ctx.fillRect(0, 0, stripWidth, totalHeight);

      const titleEl = document.querySelector(".comic-main-title");
      const comicTitle = titleEl ? titleEl.innerText : "ComicCraft Story";
      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 44px Bangers, cursive, sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(comicTitle, stripWidth / 2, 75);

      ctx.fillStyle = "#94a3b8";
      ctx.font = "16px Plus Jakarta Sans, sans-serif";
      ctx.fillText("CREATED WITH COMICCRAFT AI STUDIO", stripWidth / 2, 115);

      for (let i = 0; i < panels.length; i++) {
        const p = panels[i];
        const yTop = headerHeight + i * (panelHeight + gap);

        ctx.fillStyle = "#ffffff";
        ctx.strokeStyle = "#e2e8f0";
        ctx.lineWidth = 4;
        roundRect(ctx, 40, yTop, stripWidth - 80, panelHeight, 16, true, true);

        const imgEl = p.querySelector(".panel-main-img");
        if (imgEl && imgEl.src) {
          const img = new Image();
          img.crossOrigin = "anonymous";
          await new Promise((resolve) => {
            img.onload = () => {
              const imgW = stripWidth - 120;
              const imgH = 460;
              ctx.drawImage(img, 60, yTop + 20, imgW, imgH);
              resolve();
            };
            img.onerror = () => resolve();
            img.src = imgEl.src;
          });
        }

        const caption = p.querySelector(".narration-body")?.innerText || "";
        const speaker = p.querySelector(".speech-speaker span:last-child")?.innerText || "Hero";
        const dialogue = p.querySelector(".speech-text")?.innerText || "";

        ctx.textAlign = "left";
        let textY = yTop + 510;

        if (caption) {
          ctx.fillStyle = "#fef9c3";
          ctx.fillRect(60, textY, stripWidth - 120, 50);
          ctx.fillStyle = "#713f12";
          ctx.font = "italic 15px Comic Neue, cursive, sans-serif";
          ctx.fillText(`NARRATION: ${caption.slice(0, 110)}...`, 75, textY + 30);
          textY += 65;
        }

        if (dialogue) {
          ctx.fillStyle = "#f1f5f9";
          roundRect(ctx, 60, textY, stripWidth - 120, 55, 12, true, false);
          ctx.fillStyle = "#1e293b";
          ctx.font = "bold 15px Plus Jakarta Sans, sans-serif";
          ctx.fillText(`${speaker}: ${dialogue.slice(0, 95)}`, 75, textY + 32);
        }
      }

      const a = document.createElement("a");
      a.download = `comic_strip_${Date.now()}.png`;
      a.href = canvas.toDataURL("image/png");
      a.click();

      showToast("🎉 Comic strip downloaded as high-res PNG!");
      playPopSound(600);
    } catch (err) {
      showToast("⚠️ Could not generate image strip: " + err.message);
    } finally {
      btn.disabled = false;
      btn.innerHTML = origHtml;
    }
  });
}

function roundRect(ctx, x, y, width, height, radius, fill, stroke) {
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.lineTo(x + width - radius, y);
  ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
  ctx.lineTo(x + width, y + height - radius);
  ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
  ctx.lineTo(x + radius, y + height);
  ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
  ctx.lineTo(x, y + radius);
  ctx.quadraticCurveTo(x, y, x + radius, y);
  ctx.closePath();
  if (fill) ctx.fill();
  if (stroke) ctx.stroke();
}

/* ==========================================================================
   18. Google Gemini API Key Management Modal
   ========================================================================== */
function initApiKeyModal() {
  const openBtn = document.getElementById("btn-open-api-modal");
  if (!openBtn) return;

  openBtn.addEventListener("click", () => {
    openApiKeyModal();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeApiKeyModal();
    }
  });
}

async function openApiKeyModal() {
  const modal = document.getElementById("api-key-modal");
  if (!modal) return;

  modal.classList.add("open");
  const banner = document.getElementById("api-key-status-banner");
  const statusIcon = document.getElementById("api-status-icon");
  const statusText = document.getElementById("api-status-text");

  try {
    const res = await fetch("/api/settings/status");
    if (res.ok) {
      const data = await res.json();
      if (data.gemini_api_configured) {
        if (banner) {
          banner.className = "api-key-status-banner active";
        }
        if (statusIcon) statusIcon.innerText = "✅";
        if (statusText) statusText.innerText = `Active: ${data.model} (${data.masked_key})`;
      } else {
        if (banner) {
          banner.className = "api-key-status-banner inactive";
        }
        if (statusIcon) statusIcon.innerText = "⚡";
        if (statusText) statusText.innerText = "No Gemini API key set (Running in creative fallback engine)";
      }
    }
  } catch (err) {}

  const keyInput = document.getElementById("gemini-key-input");
  if (keyInput) keyInput.focus();
}

function closeApiKeyModal() {
  const modal = document.getElementById("api-key-modal");
  if (modal) modal.classList.remove("open");
}

async function saveApiKey(e) {
  e.preventDefault();
  const keyInput = document.getElementById("gemini-key-input");
  const submitBtn = document.getElementById("btn-save-api-key");
  if (!keyInput || !submitBtn) return;

  const candidateKey = keyInput.value.trim();
  if (!candidateKey) return;

  submitBtn.disabled = true;
  const origHtml = submitBtn.innerHTML;
  submitBtn.innerHTML = `<span>⏳</span> Verifying Key...`;

  try {
    const res = await fetch("/api/settings/gemini-key", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ api_key: candidateKey })
    });

    const data = await res.json();
    if (res.ok && data.status === "success") {
      showToast("✨ Gemini API Key verified & activated for peak performance!");
      playPopSound(640);
      keyInput.value = "";
      closeApiKeyModal();

      const badge = document.querySelector(".badge-gemini span:last-child");
      if (badge) badge.innerText = "✨ Gemini 2.5 Flash (Verified)";
    } else {
      showToast(`⚠️ ${data.message || "Failed to verify Gemini API key"}`);
    }
  } catch (err) {
    showToast(`⚠️ Error: ${err.message}`);
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = origHtml;
  }
}

window.openApiKeyModal = openApiKeyModal;
window.closeApiKeyModal = closeApiKeyModal;
window.saveApiKey = saveApiKey;


