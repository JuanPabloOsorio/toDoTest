# ToDoTest ✅

Este proyecto está dividido en **backend (FastAPI)** y **frontend (Vue 3 + TypeScript)**.  



## 🚀 Backend (FastAPI)  

### 1. Crear ambiente virtual  
```sh
python -m venv venv
```

### 2. Activar ambiente virtual  
- **Linux / MacOS**:  
```sh
source venv/bin/activate
```  
- **Windows (PowerShell)**:  
```sh
.env\Scriptsctivate
```

### 3. Instalar dependencias  
```sh
pip install -r requirements.txt
```

### 4. Inicializar servidor FastAPI  
Ubicarse en la carpeta del backend:  
```sh
cd toDoTest/backend
uvicorn main:app --reload
```

---

## 💻 Frontend (Vue 3 + TS)

Ubicarse en la carpeta del frontend:  
```sh
cd toDoTest/frontend/vue-toDo
```

### Project Setup
```sh
npm install
```

### Compile and Hot-Reload for Development
```sh
npm run dev
```

### Type-Check, Compile and Minify for Production
```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)
```sh
npm run lint
```
