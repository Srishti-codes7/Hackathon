const demoKey = "learnflow-demo-state";

const defaultState = {
  timeSpent: 0,
  rewatches: 0,
  pauses: 0,
  answered: false,
  correct: false,
  mastery: 46,
  difficulty: "Intermediate",
  lastEvent: null
};

function getState() {
  try {
    return {
      ...defaultState,
      ...(JSON.parse(localStorage.getItem(demoKey)) || {})
    };
  } catch {
    return { ...defaultState };
  }
}

function saveState(state) {
  localStorage.setItem(demoKey, JSON.stringify(state));
}

function showToast(message) {
  const toast = document.getElementById("toast");

  if (!toast) return;

  toast.textContent = message;
  toast.classList.add("show");

  setTimeout(() => {
    toast.classList.remove("show");
  }, 2600);
}

function setupMobileMenu() {
  const button = document.getElementById("mobileMenu");
  const sidebar = document.querySelector(".sidebar");

  if (!button || !sidebar) return;

  button.addEventListener("click", () => {
    sidebar.classList.toggle("open");
  });

  document.querySelectorAll(".nav-item").forEach((link) => {
    link.addEventListener("click", () => {
      sidebar.classList.remove("open");
    });
  });
}

/* =========================
   DASHBOARD
========================= */

function setupDashboard() {
  const reset = document.getElementById("resetDemo");

  if (reset) {
    reset.addEventListener("click", () => {
      localStorage.removeItem(demoKey);

      showToast("Demo learner state reset.");

      setTimeout(() => {
        location.reload();
      }, 600);
    });
  }

  const state = getState();

  /*
    If the learner has already answered the quiz
    correctly, update the Binary Search node.
  */

  if (state.correct) {
    const masteryNode = document.querySelector(".node.current");

    if (masteryNode) {
      masteryNode.innerHTML = `
        Binary Search
        <span>61%</span>
      `;

      masteryNode.classList.remove("current");
      masteryNode.classList.add("mastered");
    }
  }
}

/* =========================
   LEARNING PAGE
========================= */

function setupLesson() {
  let state = getState();

  const timeEl = document.getElementById("timeSpent");
  const rewatchEl = document.getElementById("rewatchCount");
  const pauseEl = document.getElementById("pauseCount");

  const videoProgress =
    document.getElementById("videoProgress");

  const playButton =
    document.getElementById("playButton");

  const pauseButton =
    document.getElementById("pauseButton");

  const rewatchButton =
    document.getElementById("rewatchButton");

  const videoTime =
    document.getElementById("videoTime");

  const options = [
    ...document.querySelectorAll(".option")
  ];

  const feedback =
    document.getElementById("feedback");

  const nextButton =
    document.getElementById("nextQuestion");

  const score =
    document.getElementById("quizScore");

  const adaptationTitle =
    document.getElementById("adaptationTitle");

  const adaptationText =
    document.getElementById("adaptationText");

  let elapsed = 0;
  let videoPlaying = false;
  let selected = null;

  /* =========================
     Render interaction signals
  ========================= */

  function renderSignals() {
    if (timeEl) {
      timeEl.textContent =
        formatTime(state.timeSpent);
    }

    if (rewatchEl) {
      rewatchEl.textContent =
        state.rewatches;
    }

    if (pauseEl) {
      pauseEl.textContent =
        state.pauses;
    }
  }

  function formatTime(seconds) {
    const minutes = String(
      Math.floor(seconds / 60)
    ).padStart(2, "0");

    const secs = String(
      seconds % 60
    ).padStart(2, "0");

    return `${minutes}:${secs}`;
  }

  renderSignals();

  /* =========================
     Learning timer
  ========================= */

  const timer = setInterval(() => {
    state.timeSpent += 1;
    elapsed += 1;

    renderSignals();

    /*
      Simulated video progress
    */

    if (videoPlaying) {
      const percent = Math.min(
        96,
        35 + elapsed * 1.1
      );

      if (videoProgress) {
        videoProgress.style.width =
          `${percent}%`;
      }

      const seconds = Math.min(
        400,
        138 + elapsed
      );

      const minutes =
        Math.floor(seconds / 60);

      const secs =
        String(seconds % 60).padStart(2, "0");

      if (videoTime) {
        videoTime.textContent =
          `0${minutes}:${secs} / 06:40`;
      }
    }

    /*
      Save learner state every 5 seconds
    */

    if (elapsed % 5 === 0) {
      saveState(state);
    }

  }, 1000);

  window.addEventListener(
    "beforeunload",
    () => {
      clearInterval(timer);
      saveState(state);
    }
  );

  /* =========================
     Video controls
  ========================= */

  function toggleVideo() {
    videoPlaying = !videoPlaying;

    if (playButton) {
      playButton.textContent =
        videoPlaying ? "Ⅱ" : "▶";
    }

    if (pauseButton) {
      pauseButton.textContent =
        videoPlaying ? "Ⅱ" : "▶";
    }

    if (videoPlaying) {

      showToast(
        "Playback started — learning behavior is being tracked."
      );

    } else {

      state.pauses += 1;

      state.lastEvent = "pause";

      saveState(state);

      renderSignals();

      showToast(
        "Pause signal recorded."
      );
    }
  }

  if (playButton) {
    playButton.addEventListener(
      "click",
      toggleVideo
    );
  }

  if (pauseButton) {
    pauseButton.addEventListener(
      "click",
      toggleVideo
    );
  }

  /* =========================
     Rewatch tracking
  ========================= */

  if (rewatchButton) {

    rewatchButton.addEventListener(
      "click",
      () => {

        state.rewatches += 1;

        state.lastEvent = "rewatch";

        saveState(state);

        renderSignals();

        if (videoProgress) {
          videoProgress.style.width = "35%";
        }

        if (videoTime) {
          videoTime.textContent =
            "02:18 / 06:40";
        }

        showToast(
          "Rewatch signal recorded."
        );
      }
    );
  }

  /* =========================
     Quiz option selection
  ========================= */

  options.forEach((option) => {

    option.addEventListener(
      "click",
      () => {

        /*
          Don't allow another answer
          after submission.
        */

        if (state.answered) {
          return;
        }

        options.forEach((item) => {
          item.classList.remove(
            "selected"
          );
        });

        option.classList.add(
          "selected"
        );

        selected = option;

        if (nextButton) {
          nextButton.disabled = false;
        }
      }
    );

  });

  /* =========================
     Quiz submission
  ========================= */

  if (nextButton) {

    nextButton.addEventListener(
      "click",
      () => {

        if (!selected) {
          return;
        }

        /*
          If already answered,
          handle the next action.
        */

        if (state.answered) {

          if (
            nextButton.textContent
              .includes("Continue")
          ) {

            window.location.href =
              "index.html";

            return;
          }

          if (
            nextButton.textContent
              .includes("Review")
          ) {

            feedback.scrollIntoView({
              behavior: "smooth",
              block: "center"
            });

            nextButton.textContent =
              "Continue →";

            state.correct = false;

            saveState(state);

            return;
          }
        }

        /* =========================
           First submission
        ========================= */

        state.answered = true;

        state.correct =
          selected.dataset.correct === "true";

        state.lastEvent =
          "quiz_answer";

        /*
          Disable all options
        */

        options.forEach((option) => {

          option.disabled = true;

          if (
            option.dataset.correct === "true"
          ) {
            option.classList.add(
              "correct"
            );
          }

        });

        /* =========================
           Correct answer
        ========================= */

        if (state.correct) {

          selected.classList.add(
            "correct"
          );

          if (feedback) {

            feedback.textContent =
              "Correct. Your recent accuracy supports moving toward a harder item.";

            feedback.className =
              "feedback good";
          }

          if (score) {
            score.textContent =
              "1 / 1";
          }

          nextButton.textContent =
            "Continue →";

          /*
            Increase mastery
          */

          state.mastery =
            Math.min(
              100,
              state.mastery + 15
            );

          state.difficulty =
            "Advanced";

          if (adaptationTitle) {

            adaptationTitle.textContent =
              "Difficulty can increase";
          }

          if (adaptationText) {

            adaptationText.textContent =
              "Strong accuracy detected. The next item will be slightly more challenging.";
          }

          showToast(
            "Great work — learner state updated."
          );

        }

        /* =========================
           Incorrect answer
        ========================= */

        else {

          selected.classList.add(
            "incorrect"
          );

          if (feedback) {

            feedback.textContent =
              "Not quite. Review the prerequisite concept and try a targeted question.";

            feedback.className =
              "feedback bad";
          }

          if (score) {
            score.textContent =
              "0 / 1";
          }

          nextButton.textContent =
            "Review concept";

          /*
            Decrease mastery
          */

          state.mastery =
            Math.max(
              0,
              state.mastery - 4
            );

          state.difficulty =
            "Easy";

          if (adaptationTitle) {

            adaptationTitle.textContent =
              "Targeted support activated";
          }

          if (adaptationText) {

            adaptationText.textContent =
              "The next recommendation will reinforce this concept before increasing difficulty.";
          }

          showToast(
            "Weakness detected — recommendation adjusted."
          );
        }

        saveState(state);

        nextButton.disabled = false;
      }
    );
  }
}

/* =========================
   APPLICATION STARTUP
========================= */

setupMobileMenu();

if (
  document.body.dataset.page ===
  "dashboard"
) {
  setupDashboard();
}

if (
  document.body.dataset.page ===
  "learn"
) {
  setupLesson();
}