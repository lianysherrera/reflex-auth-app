# Reflex Auth App

Sistema de autenticación construido con [Reflex](https://reflex.dev) (Python → React): registro, login, verificación de email, sesiones con expiración, perfil de usuario y notas personales.

## Funcionalidades

- Registro e inicio de sesión con contraseñas hasheadas (bcrypt)
- Verificación de cuenta por correo electrónico (SMTP vía Mailtrap)
- Sesiones con expiración automática a los 7 días
- Rutas protegidas (dashboard, perfil)
- Perfil de usuario: editar nombre/bio y cambiar contraseña
- Notas personales (crear/eliminar) con estado vacío ilustrado
- Avatar único generado automáticamente por usuario ([boring-avatars](https://github.com/boringdesigners/boring-avatars))
- Saludo según la hora del día en el dashboard
- Fondo animado con [particles.js](https://vincentgarreau.com/particles.js/) en la pantalla de inicio
- Página 404 personalizada

## Stack

- [Reflex](https://reflex.dev) (Python, compila a React)
- SQLModel + SQLite (`auth.db`)
- Alembic para migraciones de base de datos
- bcrypt para hashing de contraseñas
- Mailtrap (SMTP) para envío de correos

## Estructura del proyecto

```
reflex_auth_app/
├── components/     # Navbar, avatar
├── models/         # User, Session, Note (SQLModel)
├── pages/          # Registro, login, dashboard, perfil, verificación, 404
├── state/          # AuthState (lógica de autenticación y notas)
└── utils/          # Seguridad (hash/verify), email, conexión a DB
```

## Instalación

1. Clona el repositorio y entra a la carpeta del proyecto.

2. Crea y activa el entorno virtual:

   ```
   python -m venv venv
   ```


3. Instala las dependencias:

   ```
   pip install -r requirements.txt
   ```

4. Copia `.env.example` a `.env` y completa las credenciales SMTP:

   ```
   MAILTRAP_HOST=sandbox.smtp.mailtrap.io
   MAILTRAP_PORT=2525
   MAILTRAP_USERNAME=
   MAILTRAP_PASSWORD=
   ```

5. Aplica las migraciones de base de datos:

   ```
   reflex db migrate
   ```

6. Levanta la app:

   ```
   reflex run
   ```

La app quedará disponible en `http://localhost:3000`.
