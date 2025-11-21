import fs from 'fs';
import path from 'path';
import ejs from 'ejs';
import { fileURLToPath } from 'url';

// Helper para obtener __dirname en módulos ES
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Helper para convertir string a PascalCase (ej: 'usuario' -> 'Usuario')
function toPascalCase(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// Mapea los nombres amigables de las plantillas a los nombres de sus directorios
const templateMap = {
    'API REST + mongodb (mongoose)': 'api-rest-mongoose',
    'API REST + mongoDb (Node driver)': 'api-rest-native-driver',
    'API REST con autenticacion': 'api-rest-auth'
};

// Lista de las carpetas que el usuario puede elegir incluir o no.
const optionalFolders = ['controllers/', 'routes/', 'models/', 'helpers/', 'middlewares/', 'config/', 'services/', 'utils/'];

export function scaffoldProject(answers) {
    const { projectName, directory, projectType, resources, dependencies, folders } = answers;

    const projectPath = path.resolve(directory, projectName);
    const templateDirName = templateMap[projectType];
    if (!templateDirName) {
        throw new Error(`Error: Plantilla '${projectType}' no encontrada.`);
    }
    const templatePath = path.join(__dirname, '..', 'templates', templateDirName);

    fs.mkdirSync(projectPath, { recursive: true });
    console.log(`Directorio del proyecto creado en: ${projectPath}`);

    // Pre-procesamos los recursos para tener todos los formatos necesarios
    const processedResources = resources.split(',').map(r => {
        const resource = r.trim().toLowerCase();
        const singular = resource.endsWith('s') ? resource.slice(0, -1) : resource;
        return {
            plural: resource,
            singular: singular,
            pascal: toPascalCase(singular)
        };
    });

    // Creamos un objeto de datos global que estará disponible en TODAS las plantillas
    const globalTemplateData = {
        projectName,
        dependencies: dependencies || [],
        resources: processedResources // ej: [{ singular: 'usuario', plural: 'usuarios', pascal: 'Usuario' }]
    };

    processDirectory(templatePath, projectPath, folders, globalTemplateData);
    
    return projectPath;
}

function processDirectory(sourceDir, destinationDir, userFolders, globalData) {
    const items = fs.readdirSync(sourceDir);
    if(userFolders == 'Todas' || userFolders[0] == 'Todas'){
                userFolders = ['controllers/', 'routes/', 'models/', 'helpers/', 'middlewares/',
                    'config/', 'services/', 'utils/'
                ]
            }
    for (const item of items) {
        const sourceItemPath = path.join(sourceDir, item);
        const stats = fs.statSync(sourceItemPath);

        if (stats.isDirectory()) {
            const itemWithSlash = item + '/';
            if (optionalFolders.includes(itemWithSlash) && !userFolders.includes(itemWithSlash)) {
                continue;
            }
            const newDestDir = path.join(destinationDir, item);
            fs.mkdirSync(newDestDir, { recursive: true });
            processDirectory(sourceItemPath, newDestDir, userFolders, globalData);

        } else if (stats.isFile()) {
            if (item.includes('resource')) {
                // Para cada recurso, creamos una copia del archivo de plantilla
                for (const resource of globalData.resources) {
                    // Combinamos los datos globales con los datos específicos de este recurso
                    const resourceData = {
                        ...globalData,
                        resourceNamePlural: resource.plural,
                        resourceNameSingular: resource.singular,
                        resourceNamePascal: resource.pascal
                    };
                    
                    const finalFileName = item.replace('resource', resource.singular).replace('.ejs', '');
                    const finalDestPath = path.join(destinationDir, finalFileName);
                    renderAndWriteFile(sourceItemPath, finalDestPath, resourceData);
                }
            } else {
                // Para archivos globales, solo pasamos los datos globales
                const finalFileName = item.replace('.ejs', '');
                const finalDestPath = path.join(destinationDir, finalFileName);
                renderAndWriteFile(sourceItemPath, finalDestPath, globalData);
            }
        }
    }
}

function renderAndWriteFile(sourceFile, destinationFile, data) {
    if (path.extname(sourceFile) === '.ejs') {
        const templateContent = fs.readFileSync(sourceFile, 'utf-8');
        const renderedContent = ejs.render(templateContent, data);
        fs.writeFileSync(destinationFile, renderedContent);
        console.log(`-> Archivo creado: ${path.basename(destinationFile)}`);
    } else {
        fs.copyFileSync(sourceFile, destinationFile);
        console.log(`-> Archivo copiado: ${path.basename(destinationFile)}`);
    }
}

