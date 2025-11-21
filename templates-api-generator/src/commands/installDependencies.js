import {execSync} from 'child_process'

export async function installDependencies(path, packageManager, dependencies){
    // cwd ejecuta los comandos en la ruta que se le dice
    switch (packageManager){
        case 'npm':
            execSync(`${packageManager} init -y`, { cwd: path, stdio: 'inherit' })
            break
        case 'pnpm':
            execSync(`${packageManager} init`, { cwd: path, stdio: 'inherit' })
            break
        }
    // Instala todas las dependencias en la ruta indicada
    console.log('Instalando dependencias');
    if (dependencies.length > 0) {
        const deps = dependencies.join(' ');
        execSync(`${packageManager} install ${deps.toLowerCase()}`, { cwd: path, stdio: 'inherit' });
    }
}