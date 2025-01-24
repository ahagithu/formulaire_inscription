from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI HTML Form Example")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint pour servir la page HTML
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Formulaire d'inscription</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 50px;
                }
                form {
                    max-width: 300px;
                    margin: auto;
                    padding: 20px;
                    border: 1px solid #ccc;
                    border-radius: 10px;
                    background-color: #f9f9f9;
                }
                label {
                    display: block;
                    margin-bottom: 8px;
                    font-weight: bold;
                }
                input {
                    width: 100%;
                    padding: 8px;
                    margin-bottom: 15px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                button {
                    width: 100%;
                    padding: 10px;
                    background-color: #28a745;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #218838;
                }
                #responseMessage {
                    margin-top: 20px;
                    padding: 10px;
                    border-radius: 5px;
                    text-align: center;
                }
                .success {
                    background-color: #d4edda;
                    color: #155724;
                }
                .error {
                    background-color: #f8d7da;
                    color: #721c24;
                }
            </style>
        </head>
        <body>
            <h1>Formulaire d'inscription</h1>
            <form id="registerForm">
                <label for="username">Nom d'utilisateur:</label>
                <input type="text" id="username" name="username" required>
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>
                <label for="password">Mot de passe:</label>
                <input type="password" id="password" name="password" required>
                <button type="submit">S'inscrire</button>
            </form>
            <div id="responseMessage"></div>
            <script>
                document.getElementById('registerForm').addEventListener('submit', async function(event) {
                    event.preventDefault();
                    const formData = {
                        username: document.getElementById('username').value,
                        email: document.getElementById('email').value,
                        password: document.getElementById('password').value
                    };

                    // Validation côté client
                    if (!formData.username || !formData.email || !formData.password) {
                        document.getElementById('responseMessage').innerText = "Tous les champs sont obligatoires.";
                        document.getElementById('responseMessage').className = "error";
                        return;
                    }

                    try {
                        const response = await fetch('/register/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(formData)
                        });

                        if (!response.ok) {
                            const errorData = await response.json();
                            throw new Error(errorData.detail || "Une erreur s'est produite.");
                        }

                        const result = await response.json();
                        document.getElementById('responseMessage').innerText = "Inscription réussie ! Redirection...";
                        document.getElementById('responseMessage').className = "success";

                        // Redirection après 2 secondes
                        setTimeout(() => {
                            window.location.href = `/users/${result.id}`;
                        }, 2000);

                    } catch (error) {
                        document.getElementById('responseMessage').innerText = error.message;
                        document.getElementById('responseMessage').className = "error";
                    }
                });
            </script>
        </body>
    </html>
    """

# Endpoint pour enregistrer un utilisateur
@app.post("/register/", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    db_user = models.User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Endpoint pour lire un utilisateur
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return db_user

# Endpoint pour afficher une page de succès
@app.get("/success", response_class=HTMLResponse)
async def success_page():
    return """
    <html>
        <head>
            <title>Inscription réussie</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 50px;
                    text-align: center;
                }
                .success {
                    background-color: #d4edda;
                    color: #155724;
                    padding: 20px;
                    border-radius: 10px;
                    display: inline-block;
                }
            </style>
        </head>
        <body>
            <div class="success">
                <h1>Inscription réussie !</h1>
                <p>Votre compte a été créé avec succès.</p>
                <a href="/">Retour à l'accueil</a>
            </div>
        </body>
    </html>
    """