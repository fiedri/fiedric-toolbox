import mongoose from "mongoose";

// Define el esquema para el modelo de mascotas, que valida la estructura de los datos.
const mascotaSchema = new mongoose.Schema({
    nombre: { type: String, required: true },
    especie: {
        type: String,
        required: true,
        // enum asegura que la especie sea una de las opciones permitidas.
        enum: ['perro', 'gato', 'conejo']
    },
    descripcion: { type: String, required: true },
    raza: String,
    edad: {
        type: Number,
        // La edad no puede ser un valor negativo.
        min: [0, 'la edad no puede ser negativa'],
        // Limita la edad a un valor razonable.
        max: [30, 'la edad no parece correcta']
    },
    // Por defecto, una mascota no está adoptada.
    adoptado: { type: Boolean, default: false }
}, {
    // Desactiva la clave de versión (__v) en los documentos.
    versionKey: false,
    // Agrega automáticamente las marcas de tiempo createdAt y updatedAt.
    timestamps: true
});

// Crea el modelo de Mongoose a partir del esquema.
const mascotaModel = mongoose.model('mascota', mascotaSchema);

export default mascotaModel;
