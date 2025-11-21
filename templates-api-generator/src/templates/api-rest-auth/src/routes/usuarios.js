import express from 'express';
import usuario from '../controllers/usuario.js';
import { verificarToken } from '../helpers/autenticacion.js';

const routerUser = express.Router();

// Define las rutas para la autenticación y el perfil de usuario.

// Ruta para registrar un nuevo usuario.
routerUser.post('/register', usuario.register);

// Ruta para iniciar sesión.
routerUser.post('/login', usuario.login);

// Ruta para obtener el perfil del usuario (protegida).
routerUser.get('/profile', verificarToken, usuario.getProfile);

export default routerUser;
