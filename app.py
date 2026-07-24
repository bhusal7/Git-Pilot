import streamlit as st
import streamlit.components.v1 as components
import time

from pipeline import run_repo_analyzer



# PAGE CONFIG

st.set_page_config(
    page_title="GitHub AI Repository Analyzer",
    page_icon="🤖",
    layout="wide",
)



# GLOBAL CSS — animated gradient bg, glassmorphism, staggered reveals,
# glow buttons, shimmer progress, animated scrollbar, responsive type

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;900&family=Inter:wght@400;500;600&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

/* ---------- animated aurora background ---------- */
@keyframes auroraShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp {
    background: linear-gradient(120deg, #020617, #0b1224, #1e1b3a, #0b1224, #020617);
    background-size: 400% 400%;
    animation: auroraShift 22s ease infinite;
    color: white;
}

/* floating glow orbs behind content */
.stApp::before {
    content: "";
    position: fixed;
    top: -10%;
    left: -10%;
    width: 45vw;
    height: 45vw;
    background: radial-gradient(circle, rgba(6,182,212,0.20), transparent 70%);
    border-radius: 50%;
    filter: blur(40px);
    animation: floatOrb1 16s ease-in-out infinite;
    z-index: 0;
    pointer-events: none;
}

.stApp::after {
    content: "";
    position: fixed;
    bottom: -15%;
    right: -10%;
    width: 40vw;
    height: 40vw;
    background: radial-gradient(circle, rgba(236,72,153,0.18), transparent 70%);
    border-radius: 50%;
    filter: blur(40px);
    animation: floatOrb2 18s ease-in-out infinite;
    z-index: 0;
    pointer-events: none;
}

@keyframes floatOrb1 {
    0%, 100% { transform: translate(0, 0) scale(1); }
    50%      { transform: translate(6vw, 8vh) scale(1.15); }
}

@keyframes floatOrb2 {
    0%, 100% { transform: translate(0, 0) scale(1); }
    50%      { transform: translate(-6vw, -6vh) scale(1.1); }
}

/* ---------- reveal keyframes ---------- */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(28px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}

@keyframes popIn {
    0%   { opacity: 0; transform: scale(0.9); }
    100% { opacity: 1; transform: scale(1); }
}

@keyframes gradientFlow {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 0px rgba(139,92,246,0.0); }
    50%      { box-shadow: 0 0 22px rgba(139,92,246,0.55); }
}

@keyframes shimmer {
    0%   { background-position: -400px 0; }
    100% { background-position: 400px 0; }
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}

@keyframes bounceDot {
    0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
    40%           { transform: scale(1); opacity: 1; }
}

/* ---------- title ---------- */
.main-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(32px, 5vw, 52px);
    font-weight: 900;
    background: linear-gradient(90deg, #00f5ff, #8b5cf6, #ec4899, #00f5ff);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientFlow 6s ease infinite, fadeInUp 0.9s ease both;
    margin-bottom: 4px;
    position: relative;
    z-index: 1;
}

.subtitle {
    font-size: clamp(14px, 1.6vw, 18px);
    color: #cbd5e1;
    animation: fadeInUp 0.9s ease 0.15s both;
    position: relative;
    z-index: 1;
}

/* ---------- glass cards with stagger ---------- */
.card {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 25px;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(15px);
    margin-bottom: 20px;
    animation: fadeInUp 0.7s ease both;
    transition: transform 0.35s ease, border-color 0.35s ease, box-shadow 0.35s ease;
    position: relative;
    z-index: 1;
}

.card:hover {
    transform: translateY(-4px);
    border-color: rgba(139,92,246,0.5);
    box-shadow: 0 12px 30px rgba(139,92,246,0.18);
}

.card.delay-1 { animation-delay: 0.1s; }
.card.delay-2 { animation-delay: 0.2s; }
.card.delay-3 { animation-delay: 0.3s; }

/* result cards slide in from left/right */
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-30px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(30px); }
    to   { opacity: 1; transform: translateX(0); }
}
.slide-left  { animation: slideInLeft 0.6s ease both; }
.slide-right { animation: slideInRight 0.6s ease both; }

/* ---------- inputs ---------- */
.stTextInput input {
    background: #111827;
    color: white;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    transition: box-shadow 0.3s ease, border-color 0.3s ease, transform 0.2s ease;
}

.stTextInput input:focus {
    border-color: #8b5cf6;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.25);
    transform: translateY(-1px);
}

/* ---------- button ---------- */
.stButton button {
    width: 100%;
    border-radius: 15px;
    height: 52px;
    font-size: 18px;
    font-weight: 700;
    background: linear-gradient(90deg, #06b6d4, #8b5cf6, #ec4899);
    background-size: 200% auto;
    color: white;
    border: none;
    transition: background-position 0.5s ease, transform 0.2s ease, box-shadow 0.3s ease;
    position: relative;
    overflow: hidden;
}

.stButton button:hover {
    background-position: right center;
    transform: translateY(-2px) scale(1.01);
    box-shadow: 0 8px 24px rgba(139,92,246,0.4);
}

.stButton button:active {
    transform: translateY(0) scale(0.98);
}

/* ---------- step tracker ---------- */
.step-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 16px;
    border-radius: 12px;
    margin-bottom: 8px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    transition: all 0.4s ease;
    animation: fadeInUp 0.5s ease both;
}

.step-row.active {
    background: rgba(139,92,246,0.12);
    border-color: rgba(139,92,246,0.45);
    animation: fadeInUp 0.5s ease both, pulseGlow 1.6s ease-in-out infinite;
}

.step-row.done {
    background: rgba(16,185,129,0.08);
    border-color: rgba(16,185,129,0.35);
}

.step-icon {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
    background: rgba(255,255,255,0.08);
}

.step-row.active .step-icon {
    background: conic-gradient(#06b6d4, #8b5cf6, #ec4899, #06b6d4);
    animation: spin 1.2s linear infinite;
}

.step-row.done .step-icon {
    background: #10b981;
}

.step-label {
    font-size: 15px;
    color: #e2e8f0;
    letter-spacing: 0.2px;
}

.step-row.pending .step-label { color: #64748b; }

/* dots loader inline */
.dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #8b5cf6;
    margin-left: 2px;
    animation: bounceDot 1.4s infinite ease-in-out both;
}
.dot:nth-child(2) { animation-delay: 0.16s; }
.dot:nth-child(3) { animation-delay: 0.32s; }

/* ---------- section heading ---------- */
.section-heading {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 26px;
    font-weight: 800;
    background: linear-gradient(90deg, #00f5ff, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: fadeInUp 0.6s ease both;
    margin-top: 6px;
    margin-bottom: 10px;
}

/* ---------- expanders ---------- */
div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.04);
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.08);
    overflow: hidden;
    transition: border-color 0.3s ease, transform 0.3s ease;
    animation: fadeInUp 0.6s ease both;
}

div[data-testid="stExpander"]:hover {
    border-color: rgba(6,182,212,0.4);
}

/* ---------- alerts pop ---------- */
div[data-testid="stAlert"] {
    animation: popIn 0.4s ease both;
    border-radius: 14px;
}

/* ---------- progress bar shimmer ---------- */
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #06b6d4, #8b5cf6, #ec4899, #06b6d4);
    background-size: 800px 100%;
    animation: shimmer 2.2s linear infinite;
    border-radius: 8px;
}

/* ---------- scrollbar ---------- */
::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-track { background: #0b0f19; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #06b6d4, #8b5cf6);
    border-radius: 10px;
}

/* ---------- footer ---------- */
.footer {
    text-align: center;
    color: #94a3b8;
    animation: fadeIn 1.2s ease both;
    padding: 10px 0 30px 0;
    font-size: 14px;
}

.footer .pill {
    display: inline-block;
    padding: 4px 12px;
    margin: 4px;
    border-radius: 999px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    transition: transform 0.25s ease, border-color 0.25s ease;
}

.footer .pill:hover {
    transform: translateY(-2px);
    border-color: #8b5cf6;
}

/* ---------- responsive tweaks ---------- */
@media (max-width: 768px) {
    .card { padding: 18px; }
    .section-heading { font-size: 21px; }
}

</style>
""",
    unsafe_allow_html=True,
)



# HERO — self-contained GSAP-powered animated banner (runs inside an iframe
# via components.html, since Streamlit's markdown does not execute <script>).
# Transparent background so it blends with the aurora gradient behind it.

def render_hero():
    components.html(
        """
        <div id="hero" style="width:100%;height:190px;position:relative;overflow:hidden;
             font-family:'Space Grotesk',sans-serif;background:transparent;">
          <canvas id="orbs" style="position:absolute;inset:0;width:100%;height:100%;"></canvas>
          <div id="heroTitle" style="position:relative;z-index:2;display:flex;justify-content:center;
               align-items:center;height:100%;">
            <span id="letters" style="font-size:44px;font-weight:900;letter-spacing:1px;
                 background:linear-gradient(90deg,#00f5ff,#8b5cf6,#ec4899);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;"></span>
          </div>
        </div>

        <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
        <script>
          const text = "AGENTIC INTELLIGENCE, ANIMATED";
          const el = document.getElementById('letters');
          text.split('').forEach((ch, i) => {
            const span = document.createElement('span');
            span.textContent = ch === ' ' ? '\\u00A0' : ch;
            span.style.display = 'inline-block';
            span.style.opacity = '0';
            el.appendChild(span);
          });

          if (window.gsap) {
            gsap.to("#letters span", {
              opacity: 1,
              y: 0,
              duration: 0.5,
              stagger: 0.03,
              ease: "back.out(2)",
              delay: 0.2
            });
            gsap.set("#letters span", { y: 20 });
            gsap.to("#letters span", {
              y: 0, opacity: 1, duration: 0.5, stagger: 0.03, ease: "back.out(2)", delay: 0.2
            });
          }

          // floating orb particles on canvas
          const canvas = document.getElementById('orbs');
          const ctx = canvas.getContext('2d');
          function resize() {
            canvas.width = canvas.offsetWidth;
            canvas.height = canvas.offsetHeight;
          }
          resize();
          window.addEventListener('resize', resize);

          const colors = ['rgba(6,182,212,0.5)', 'rgba(139,92,246,0.5)', 'rgba(236,72,153,0.5)'];
          const particles = Array.from({length: 26}, () => ({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            r: Math.random() * 2.5 + 1,
            vx: (Math.random() - 0.5) * 0.4,
            vy: (Math.random() - 0.5) * 0.4,
            color: colors[Math.floor(Math.random() * colors.length)]
          }));

          function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(p => {
              p.x += p.vx;
              p.y += p.vy;
              if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
              if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
              ctx.beginPath();
              ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
              ctx.fillStyle = p.color;
              ctx.shadowBlur = 8;
              ctx.shadowColor = p.color;
              ctx.fill();
            });
            requestAnimationFrame(animate);
          }
          animate();
        </script>
        """,
        height=200,
    )


render_hero()



# HEADER TEXT

st.markdown(
    """
<div class="main-title">🤖 GitHub AI Repository Analyzer</div>
<div class="subtitle">Agentic AI + RAG + LangChain powered repository intelligence system.</div>
<br>
""",
    unsafe_allow_html=True,
)



# INTRO CARD

st.markdown(
    """
    <div class="card delay-1">
    🚀 Enter any public GitHub repository URL. The AI will:
    <br><br>
    • Clone repository&nbsp;&nbsp;
    • Build RAG knowledge base&nbsp;&nbsp;
    • Search documentation&nbsp;&nbsp;
    • Analyze architecture&nbsp;&nbsp;
    • Review with critic agent&nbsp;&nbsp;
    • Generate markdown report
    </div>
    """,
    unsafe_allow_html=True,
)



# INPUTS

col1, col2 = st.columns(2)

with col1:
    repo_url = st.text_input(
        "🔗 GitHub Repository URL",
        placeholder="https://github.com/user/project",
    )

with col2:
    query = st.text_input(
        "💬 What do you want to analyze?",
        placeholder="Explain architecture, technologies and improvements",
    )

analyze = st.button("🚀 Analyze Repository")



# ANIMATED STEP TRACKER (custom HTML instead of plain st.info text)

STEPS = [
    ("🔎", "Searching repository..."),
    ("📦", "Loading repository files..."),
    ("🧠", "Building RAG memory..."),
    ("🤖", "Running AI agents..."),
    ("📝", "Generating explanation..."),
    ("🧐", "Running critic review..."),
    ("💾", "Saving report..."),
]


def render_steps(current_index):
    rows = []
    for i, (icon, label) in enumerate(STEPS):
        if i < current_index:
            state = "done"
            icon_html = "✔"
        elif i == current_index:
            state = "active"
            icon_html = icon
        else:
            state = "pending"
            icon_html = icon

        dots = (
            '<span class="dot"></span><span class="dot"></span><span class="dot"></span>'
            if state == "active"
            else ""
        )

        rows.append(
            f"""
            <div class="step-row {state}" style="animation-delay:{i * 0.05}s">
                <div class="step-icon">{icon_html}</div>
                <div class="step-label">{label}{dots}</div>
            </div>
            """
        )
    return "".join(rows)


if analyze:

    if not repo_url:
        st.error("Please provide GitHub repository URL")

    else:
        if not query:
            query = "Analyze this repository completely"

        progress = st.progress(0)
        tracker = st.empty()

        for i in range(len(STEPS)):
            tracker.markdown(render_steps(i), unsafe_allow_html=True)
            progress.progress((i + 1) / len(STEPS))
            time.sleep(0.3)

        tracker.markdown(render_steps(len(STEPS)), unsafe_allow_html=True)

        try:
            result = run_repo_analyzer(
                query=repo_url + "\n" + query,
                repo_path=repo_url,
            )

            st.success("Analysis Completed Successfully 🎉")
            st.divider()

            st.markdown('<div class="section-heading">🧠 AI Final Analysis</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="card slide-left">{result.get("feedback", "No result generated")}</div>',
                unsafe_allow_html=True,
            )

            res_col1, res_col2 = st.columns(2)

            with res_col1:
                with st.expander("🔍 Search Agent Output"):
                    st.write(result.get("search", "No search output"))

            with res_col2:
                with st.expander("📂 Repository Agent Output"):
                    st.write(result.get("repository", "No repository output"))

            with st.expander("📄 Generated Report"):
                st.write(result.get("report", "No report"))

        except Exception as e:
            st.error(f"❌ Error occurred:\n\n{e}")



# FOOTER

st.divider()

st.markdown(
    """
<div class="footer">
Built with ❤️ using
<span class="pill">LangChain</span>
<span class="pill">RAG</span>
<span class="pill">Agents</span>
<span class="pill">Mistral</span>
<span class="pill">Streamlit</span>
</div>
""",
    unsafe_allow_html=True,
)