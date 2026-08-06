"""
shared/state.py — Namespaced session state.

All CB-SEM data lives under keys prefixed "cbsem_". All PLS-SEM data lives
under keys prefixed "plssem_". CBSEMState and PLSSEMState are separate,
non-interchangeable accessor objects — cbsem/ modules import ONLY
CBSEMState, plssem/ modules import ONLY PLSSEMState. There is no shared
generic state object read by both sides with conditional branches, which
was the root cause of repeated cross-contamination bugs in earlier
iterations of this project.
"""
import streamlit as st


def init_state():
    if "app_method" not in st.session_state:
        st.session_state["app_method"] = None


def get_method():
    return st.session_state.get("app_method")


def set_method(method: str):
    assert method in ("cbsem", "plssem"), f"Invalid method: {method!r}"
    st.session_state["app_method"] = method


def reset_all():
    keys_to_clear = [
        k for k in list(st.session_state.keys())
        if k.startswith("cbsem_") or k.startswith("plssem_") or k == "app_method"
    ]
    for k in keys_to_clear:
        del st.session_state[k]


class _NamespacedState:
    def __init__(self, prefix: str):
        self._prefix = prefix

    def _key(self, name: str) -> str:
        return f"{self._prefix}{name}"

    def get(self, name: str, default=None):
        return st.session_state.get(self._key(name), default)

    def set(self, name: str, value):
        st.session_state[self._key(name)] = value

    def has(self, name: str) -> bool:
        return self._key(name) in st.session_state

    def delete(self, name: str):
        k = self._key(name)
        if k in st.session_state:
            del st.session_state[k]

    def all_keys(self):
        plen = len(self._prefix)
        return [k[plen:] for k in st.session_state.keys() if k.startswith(self._prefix)]


CBSEMState  = _NamespacedState("cbsem_")
PLSSEMState = _NamespacedState("plssem_")
