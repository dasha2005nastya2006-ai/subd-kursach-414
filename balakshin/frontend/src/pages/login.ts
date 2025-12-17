// frontend/pages login.ts

import { api } from '../api.js';
import { state } from '../state.js';
export function renderLogin() {
const app = document.getElementById('app')!;
app.innerHTML = `<div class="card" style="max-width:400px;margin:100px auto">
<h2>Вход</h2>
<input id="email" placeholder="Email" /><br/><br/>
<input id="pass" type="password" placeholder="Пароль" /><br/><br/>
<button class="btn-primary" id="loginBtn">Войти</button>
</div>`;
document.getElementById('loginBtn')!.onclick = async () => {
const email = (document.getElementById('email') as HTMLInputElement).value;
const pass = (document.getElementById('pass') as HTMLInputElement).value;
const res = await api.login(email, pass);
state.token = res.token;
state.userRole = res.role;
location.hash = '/dashboard';
};
}