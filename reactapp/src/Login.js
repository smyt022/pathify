import React from 'react';
import { Link } from 'react-router-dom';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './neonAesthetic.css'; // css

// login form component
const LoginForm = ({ onSubmitRunThis }) => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmitRunThis(formData);
  }

  return (
    <form onSubmit={handleSubmit} className="formStyle">
      <div>
        <label>
          Username:
        </label>
        <input
          type="text"
          name="username"
          value={formData.username}
          onChange={handleChange}
          className="inputStyle"
        />
      </div>
      <div>
        <label>
          Password:
        </label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          className="inputStyle"
        />
      </div>

      <button type="submit" className="buttonStyle">Log In</button>

      <p>
        Don't have an account? <Link to="/signup/" className="linkStyle">Sign up here</Link>
      </p>
    </form>
  );
};

// login page
const Login = () => {
  const navigate = useNavigate();

  const sendToBackend = (formData) => {
    const csrfToken = String(document.cookie
      .split(';')
      .find((c) => c.trim().startsWith('csrftoken='))
      ?.replace('csrftoken=', ''));

    fetch('/api/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify(formData),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        const message = String(data.message);
        if (message === "login successful") {
          navigate('/');
        }
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
      });
  };


  return (
    <main className="mainStyle">
      <LoginForm onSubmitRunThis={sendToBackend} />
    </main>
  );
};

export default Login;
