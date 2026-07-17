import json

import reflex as rx
from reflex_auth_app.pages.register import register_page
from reflex_auth_app.pages.login import login_page
from reflex_auth_app.pages.dashboard import dashboard_page
from reflex_auth_app.pages.verify import verify_page
from reflex_auth_app.state.auth_state import AuthState
from reflex_auth_app.utils.db import init_db
from reflex_auth_app.components.navbar import navbar
from reflex_auth_app.pages.profile import profile_page
from reflex_auth_app.pages.not_found import not_found_page

PARTICLES_CONFIG = {
    "particles": {
        "number": {"value": 140, "density": {"enable": True, "value_area": 800}},
        "color": {"value": "#ffffff"},
        "shape": {"type": "circle"},
        "opacity": {"value": 0.6, "random": False},
        "size": {"value": 3, "random": True},
        "line_linked": {
            "enable": True,
            "distance": 150,
            "color": "#ffffff",
            "opacity": 0.3,
            "width": 1,
        },
        "move": {
            "enable": True,
            "speed": 4,
            "direction": "none",
            "random": True,
            "straight": False,
            "out_mode": "out",
        },
    },
    "interactivity": {
        "detect_on": "canvas",
        "events": {
            "onhover": {"enable": True, "mode": "repulse"},
            "onclick": {"enable": False, "mode": "push"},
            "resize": True,
        },
        "modes": {"repulse": {"distance": 150, "duration": 0.4}},
    },
    "retina_detect": True,
}


def particles_background() -> rx.Component:
    init_script = f"""
    (function() {{
        function initParticles() {{
            particlesJS('particles-js', {json.dumps(PARTICLES_CONFIG)});
        }}
        if (window.particlesJS) {{
            initParticles();
        }} else {{
            var script = document.createElement('script');
            script.src = "https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js";
            script.onload = initParticles;
            document.body.appendChild(script);
        }}
    }})();
    """
    return rx.box(
        id="particles-js",
        position="fixed",
        top="0",
        left="0",
        width="100vw",
        height="100vh",
        z_index="0",
        on_mount=rx.call_script(init_script),
    )


def index() -> rx.Component:
    return rx.fragment(
        particles_background(),
        rx.box(
            rx.box(navbar(), pointer_events="auto"),
            rx.center(
                rx.vstack(
                    rx.heading(
                        "Sistema de autenticación con Reflex",
                        size="9",
                        text_align="center",
                        weight="bold",
                    ),
                    rx.text(
                        "Gestiona tus usuarios de forma segura y sencilla.",
                        size="4",
                        color_scheme="gray",
                        text_align="center",
                    ),
                    spacing="6",
                    align="center",
                ),
                min_height="100vh",
                pointer_events="none",
            ),
            position="relative",
            z_index="1",
            pointer_events="none",
        ),
    )


init_db()

app = rx.App()
app.add_page(index)
app.add_page(register_page, route="/register", on_load=[AuthState.redirect_if_logged_in, AuthState.reset_register_messages])
app.add_page(login_page, route="/login", on_load=[AuthState.redirect_if_logged_in, AuthState.reset_login_error])
app.add_page(dashboard_page, route="/dashboard", on_load=[AuthState.require_login, AuthState.load_notes])
app.add_page(verify_page, route="/verify", on_load=AuthState.handle_verify)
app.add_page(profile_page, route="/profile", on_load=AuthState.require_login)
app.add_page(not_found_page, route="404")