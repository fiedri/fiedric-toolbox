import mongoose from "mongoose";

// Define el esquema para el modelo de usuarios.
const userSchema = new mongoose.Schema({
    email: {
        type: String,
        required: true,
        // Asegura que cada email sea único en la colección.
        unique: true,
        // Elimina espacios en blanco al principio y al final.
        trim: true
    },
    nombre: {
        type: String,
        required: true,
        trim: true
    },
    telefono: {
        type: String,
        required: true,
    },
    clave: {
        type: String,
        required: true,
    },
}, {
    // Desactiva la clave de versión (__v) y agrega marcas de tiempo.
    versionKey: false,
    timestamps: true
});

// Crea el modelo de Mongoose a partir del esquema.
const userModel = mongoose.model('user', userSchema);

export default userModel;
