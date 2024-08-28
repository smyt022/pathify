import React from 'react';
import { Link } from 'react-router-dom';//to link to other pages on the side easily
//we are using React's 'useState' for cleaner logic for our forms
import { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // for redirecting to other urls
import './neonAesthetic.css'; // css


// Sign up form component
const SignupForm = ({ onSubmitRunThis }) => {
  const [formData, setFormData] = useState({
    email: '',
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
  };

  return (
    <form onSubmit={handleSubmit} className="formStyle">
      <div>
        <label className="labelStyle">
          Email:
        </label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          className="inputStyle"
        />
      </div>
      <div>
        <label className="labelStyle">
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
        <label className="labelStyle">
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
      
      <button type="submit" className="buttonStyle">Create Account</button>

      <p style={{ marginTop: '20px' }}>
        Already have an account? <Link to="/login/" className="linkStyle">Login here</Link>
      </p>
    </form>
  );
};

// Signup page
const Signup = () => {
  const navigate = useNavigate();

  const sendToBackend = (formData) => {
    const csrfToken = String(document.cookie
      .split(';')
      .find((c) => c.trim().startsWith('csrftoken='))
      ?.replace('csrftoken=', ''));

    fetch('/api/signup/', {
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
      console.log(data);
      const message = String(data.message);
      console.log("message: " + message);

      if (message === "user created successfully") {
        navigate('/');
      }
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
  };

  return (
    <main className="mainStyle">
      <SignupForm onSubmitRunThis={sendToBackend} />
    </main>
  );
};

export default Signup;
