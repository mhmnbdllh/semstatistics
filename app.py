"""
app.py — SEM Studio root router.

Contains NO CB-SEM or PLS-SEM specific logic, text, or state handling.
Its only job: show the method-selector home page, then hand off
COMPLETELY to cbsem.router.render() or plssem.router.render() — two
independent modules that never import from each other.
"""
import streamlit as st

from shared.state import init_state, get_method, set_method, reset_all
from shared.ui import PAGE_ICON

st.set_page_config(
    page_title="SEM Studio",
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "SEM Studio — CB-SEM (R/lavaan) & PLS-SEM (NIPALS) Suite"},
)


def render_home():
    st.markdown(
        """
        <div style="text-align:center;padding:40px 0 20px">
            <div style="font-size:4rem">🧠</div>
            <h1 style="font-size:2.8rem;font-weight:900;color:#1a6fa8;margin:8px 0">SEM Studio</h1>
            <p style="font-size:1.05rem;color:#555;max-width:680px;margin:0 auto;line-height:1.7">
                Two independent, equally-supported methods:
                <strong style="color:#1a6fa8">CB-SEM (R/lavaan)</strong> and
                <strong style="color:#1a7a4a">PLS-SEM (NIPALS)</strong>.
                Choosing one opens a completely separate workflow.
            </p>
        </div>
        """, unsafe_allow_html=True,
    )
    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            '<div style="background:#eef6fb;border:2px solid #1a6fa8;border-radius:10px;padding:22px">'
            '<h3 style="color:#1a6fa8;margin:0 0 10px">📐 CB-SEM</h3>'
            '<p style="font-size:0.88rem;color:#333;line-height:1.6">'
            '<b>Goal:</b> Theory confirmation<br><b>Sample size:</b> n ≥ 100 (200 recommended)<br>'
            '<b>Data:</b> Requires approx. normality<br><b>Constructs:</b> Reflective only<br>'
            '<b>Engine:</b> R/lavaan (ML/MLR)</p></div>', unsafe_allow_html=True,
        )
        if st.button("Start CB-SEM →", type="primary", use_container_width=True, key="btn_start_cbsem"):
            set_method("cbsem"); st.rerun()
    with col_b:
        st.markdown(
            '<div style="background:#eefbf3;border:2px solid #1a7a4a;border-radius:10px;padding:22px">'
            '<h3 style="color:#1a7a4a;margin:0 0 10px">🔬 PLS-SEM</h3>'
            '<p style="font-size:0.88rem;color:#333;line-height:1.6">'
            '<b>Goal:</b> Prediction / exploratory research<br><b>Sample size:</b> n ≥ 30 (100+ recommended)<br>'
            '<b>Data:</b> Distribution-free<br><b>Constructs:</b> Reflective and formative<br>'
            '<b>Engine:</b> NIPALS (path weighting scheme)</p></div>', unsafe_allow_html=True,
        )
        if st.button("Start PLS-SEM →", type="primary", use_container_width=True, key="btn_start_plssem"):
            set_method("plssem"); st.rerun()

    st.caption(
        "⚠️ CB-SEM and PLS-SEM results are not directly comparable — they use "
        "different estimation logic. Choose based on your research goal."
    )


def main():
    init_state()
    method = get_method()

    with st.sidebar:
        st.markdown("### SEM Studio")
        if method is not None:
            label = "📐 CB-SEM" if method == "cbsem" else "🔬 PLS-SEM"
            st.success(f"Active method: **{label}**")
            if st.button("⬅ Switch method (resets progress)", use_container_width=True):
                reset_all(); st.rerun()
            st.markdown("---")

    if method is None:
        render_home()
    elif method == "cbsem":
        from cbsem.router import render as render_cbsem
        render_cbsem()
    elif method == "plssem":
        from plssem.router import render as render_plssem
        render_plssem()
    else:
        st.error(f"Unknown method state: {method!r}. Resetting.")
        reset_all(); st.rerun()


if __name__ == "__main__":
    main()
