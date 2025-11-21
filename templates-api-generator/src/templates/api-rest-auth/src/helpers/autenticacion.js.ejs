import jsonwebtoken from 'jsonwebtoken';
import 'dotenv/config';

// generateToken crea un nuevo token JWT.
export function generateToken(email) {
    // Firma el token con el email y una clave secreta, con una expiración de 1 hora.
    return jsonwebtoken.sign({ email }, process.env.JWT_SECRET, {
        expiresIn: '1h'
    });
}

// verificarToken es un middleware para proteger rutas.
export function verificarToken(req, res, next) {
    // Obtiene el token del encabezado de autorización.
    const token = req.header('Authorization')?.replace('Bearer ', '');
    if (!token) {
        // Si no hay token, devuelve un error de no autorizado.
        return res.status(401).json({ error: 'Token requerido' });
    }
    try {
        // Verifica el token con la clave secreta.
        const data = jsonwebtoken.verify(token, process.env.JWT_SECRET);
        // Añade el email del usuario a la solicitud para su uso posterior.
        req.emailConectado = data.email;
        // Continúa con la siguiente función de middleware.
        next();
    } catch (e) {
        // Si el token no es válido, devuelve un error.
        res.status(401).json({ error: 'Token no válido' });
    }
}
