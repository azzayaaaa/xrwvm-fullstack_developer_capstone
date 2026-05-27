import React, { useState } from 'react';
import Header from '../Header/Header';
import './Register.css';

const Register = () => {
  const [form, setForm] = useState({
    userName: '',
    password: '',
    firstName: '',
    lastName: '',
    email: '',
  });

  const update = (key, value) => setForm({ ...form, [key]: value });

  const register = async (event) => {
    event.preventDefault();
    const response = await fetch('/djangoapp/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    });
    const json = await response.json();
    if (json.status === 'Authenticated') {
      sessionStorage.setItem('username', json.userName);
      window.location.href = '/';
    } else {
      alert(json.error || 'Registration failed.');
    }
  };

  return (
    <div>
      <Header />
      <form className="register_container" onSubmit={register}>
        <div className="header">Sign Up</div>
        <div className="inputs">
          <input className="input_field" placeholder="Username" onChange={(e) => update('userName', e.target.value)} />
          <input className="input_field" placeholder="First name" onChange={(e) => update('firstName', e.target.value)} />
          <input className="input_field" placeholder="Last name" onChange={(e) => update('lastName', e.target.value)} />
          <input className="input_field" placeholder="Email" onChange={(e) => update('email', e.target.value)} />
          <input className="input_field" placeholder="Password" type="password" onChange={(e) => update('password', e.target.value)} />
        </div>
        <div className="submit_panel">
          <button className="submit" type="submit">Register</button>
        </div>
      </form>
    </div>
  );
};

export default Register;
