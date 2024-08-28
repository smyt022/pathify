import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './neonAesthetic.css'; // Import your CSS file


const BackBtn = () => {
  const navigate = useNavigate();

  const goBack = () => {
    navigate('/');
  }

  return (
    <button className="buttonStyleOrange" onClick={goBack}>back</button>
  );
}


const LogoutBtn = () => {
  const navigate = useNavigate();

  const handleLogOut = (e) => {
    e.preventDefault();

    const csrfToken = String(document.cookie
      .split(';')
      .find((c) => c.trim().startsWith('csrftoken='))
      ?.replace('csrftoken=', ''));

    fetch('/api/logout/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(() => {
      navigate('/login/');
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
  }

  return (
    <form onSubmit={handleLogOut}>
      <button type="submit" className="buttonStyle">Log Out</button>
    </form>
  );
}

const CourseDetail = () => {
  const { courseTitle } = useParams();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [courseState, setCourse] = useState({});

  useEffect(() => {
    fetch('/api/user_info/')
      .then(response => response.json())
      .then(data => {
        if (data.is_authenticated) {
          setIsAuthenticated(true);
          setUsername(data.username);

          const course = data.courses.find(c => c.title === courseTitle);
          if (course) {
            setCourse(course);
          }
        } else {
          navigate('/login/');
        }
      })
      .catch(error => {
        console.error('Error checking user authentication:', error);
      });
  }, [navigate, courseTitle]);

  const toggleUnitDetails = (index) => {
    setCourse(prevState => ({
      ...prevState,
      units: prevState.units.map((unit, i) =>
        i === index ? { ...unit, isOpen: !unit.isOpen } : unit
      )
    }));
  };

  const navigateToLesson = (lessonTitle) => {
    navigate(`/courses/${courseTitle}/lesson/${lessonTitle}`);
  };

  if (!isAuthenticated) {
    return <div>Loading...</div>
  }

  return (
    <main>
      <h1>Welcome {username}!</h1>
      <div> 
        <LogoutBtn />
        <BackBtn />
      </div>
      <h3 className="course-title">Course: {courseState.title}</h3>
      <h6 className="course-description">{courseState.description}</h6>

      <div className="units-container">
        {courseState.units && courseState.units.map((unit, index) => (
          <div key={unit.title} className="unit-dropdown">
            <button className="unit-button" onClick={() => toggleUnitDetails(index)}>
              {unit.title}
            </button>
            {unit.isOpen && (
              <div className="unit-description">
                {unit.description}
                <ul className="lesson-list">
                  {unit.lessons.map(lesson => (
                    <li key={lesson.title} className="lesson-link" onClick={() => navigateToLesson(lesson.title)}>
                      {lesson.title}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </main>
  );
};

export default CourseDetail;
