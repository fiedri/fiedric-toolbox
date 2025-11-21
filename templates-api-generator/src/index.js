#!/usr/bin/env node
// si una carpeta no que el usuario introduce no existe, se crea
import inquirer from "inquirer";
import { scaffoldProject} from "./utils/scalffoldProject.js";
import { installDependencies } from "./commands/installDependencies.js";
console.clear
function main() {
    console.log('API-REST Template Generator');
    const prompt = inquirer.createPromptModule();
    prompt([
        {
            type: 'list',
            name: 'projectType',
            message: 'Elige la platilla a crear:',
            choices: ['API REST + mongodb (mongoose)', 'API REST + mongoDb (Node driver)', 'API REST con autenticacion']
        }, {
            type: 'input',
            name: 'projectName',
            message: '¿Cual sera el nombre del proyecto?',
            validate: (answer) => {
                return answer.trim() ? true : false
            }
        }, {
            type: 'input',
            name: 'directory',
            message: '¿Cual sera la ruta del proyecto?',
            default: './',
        },
        {
            type: 'checkbox',
            name: 'folders',
            message: '¿Qué carpetas quieres incluir?',
            choices: ['Todas', 'controllers/', 'routes/', 'models/', 'helpers/', 'middlewares/',
                'config/', 'services/', 'utils/'
            ],
            pageSize: 5,
            default: 'Todas'
        }, {
            type: 'checkbox',
            name: 'dependencies',
            message: '¿Que dependencias quieres incluir automaticamente?',
            choices: ['Express', 'Moongoose', 'dotenv', 'bcrypt', 'jsonwebtoken'],
            default: 'Express'
        }, {
            type: 'rawlist',
            name: 'gestorPaquetes',
            message: '¿Que gestor de paquetes quieres usar?',
            choices: ['npm', 'pnpm'],
            default: 'npm'
        }, {
            type: 'input',
            name: 'resources',
            message: '¿Que recurso deseas menejar en tu API? (separados por coma)?',
            suffix: 'Ejemplo: usuarios, productos, ordenes',
            default: 'usuarios, productos, ordenes' // <-- Esto muestra el ejemplo en el input
        }
    ]).then(answer => {
        const {gestorPaquetes, dependencies} = answer
        const projectPath = scaffoldProject(answer)
        // instalacion de dependencias
        installDependencies(projectPath, gestorPaquetes, dependencies)
        
    });
}



main();
