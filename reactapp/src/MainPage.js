import React from 'react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './neonAesthetic.css'; // css


const LogoutBtn = () => {
  const navigate = useNavigate();

  const handleLogOut = (e) => {
    e.preventDefault();//prevent default behaviour of refreshing the page

    //get CSRF from cookies
    const csrfToken = String(document.cookie
      .split(';')
      .find((c) => c.trim().startsWith('csrftoken='))
      ?.replace('csrftoken=', ''));
    
    //tell backend to logout user (just by getting the endpoint)
    fetch('api/logout/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
    })
    .then(response => {
      if(!response.ok){//didnt return a 200 http response
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log(data);//data 
    })
    .then( () => {
      //redirect client to login page
      navigate('/login/');
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
    
  }

  return (
    <form onSubmit={handleLogOut}>
        <button type="submit" className="logout-button">Log Out</button>
    </form>
  );
}

const CreateCourseForm = () => {
  const [skill, setSkill] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!/^[a-zA-Z]+$/.test(skill)) {
      alert("Please enter a single word made of alphabet letters only.");
      return;
    }

    setIsSubmitting(true); // Set loading state to true when form is submitted

    const csrfToken = String(document.cookie
      .split(';')
      .find((c) => c.trim().startsWith('csrftoken='))
      ?.replace('csrftoken=', ''));

    fetch('/api/create_course/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({ skill }),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log(data.message);
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    })
    .finally(() => {
      setIsSubmitting(false); // Set loading state to false after the request completes

      //refresh the page
      window.location.reload();
    });
  };

  return (
    <div>
      {isSubmitting ? (
        <p>One moment, new course creation in progress...</p>
      ) : (
        <form onSubmit={handleSubmit} className="formStyle">
          <label htmlFor="skill" className="labelStyle">Enter a skill you would like to learn:</label>
          <input 
            type="text" 
            id="skill" 
            name="skill" 
            value={skill} 
            onChange={(e) => setSkill(e.target.value)} 
            className="inputStyle"
          />
          <button type="submit" className="buttonStyle">Submit</button>
        </form>
      )}
    </div>
  );
};



const Body = () => {
  //CHECKING THAT USER IS AUTHENTICATED
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();
  const [username, setUsername] = useState(""); //for saving the current logged in user's username
  const [courses, setCourses] = useState([]); //for saving the current logged in user's array of courses
  //json format with attributes: title, description
  let coursesArray = []; //
  
  useEffect(() => {
    fetch('/api/user_info/')
    .then(response => response.json())
    .then(data => {
      if (data.is_authenticated){
        console.log("backend says user is authenticated");
        setIsAuthenticated(true);
        setUsername(data.username);

        //get "courses" array in json form
        for (let i=0; i<data.courses.length; i++){
          let course = {
            title: data.courses[i].title,
            description: data.courses[i].description,
            units: []
          };

          //get "units" array into course json
          for (let j=0; j<data.courses[i].units.length; j++){
            let unit = {
              title: data.courses[i].units[j].title,
              description: data.courses[i].units[j].description,
              lessons: []
            }

            //get "lessons" array into unit json
            for (let x=0; x<data.courses[i].units[j].lessons.length; x++){
              let lesson = {
                title: data.courses[i].units[j].lessons[x].title,
                description: data.courses[i].units[j].lessons[x].description,
                reading_material: data.courses[i].units[j].lessons[x].reading_material,
                video_link: data.courses[i].units[j].lessons[x].video_link,
                practice_exercise: data.courses[i].units[j].lessons[x].practice_exercise,
              }

              //add lesson into unit "lessons" 
              unit.lessons.push(lesson);
            }

            //add unit into course "units"
            course.units.push(unit);
          }

          //add course to courses
          coursesArray.push(course);
        }
        setCourses(coursesArray);

      } else {
        console.log("backend says user is not authenticated");
        navigate('/login/');
      }
    })
    .catch(error => {
      console.error('Error checking user authentication:', error);
    });
  }, [navigate]);

   // Use an effect to log the updated values of username and courses
   useEffect(() => {
    console.log("username:", username);
    //courses
    for(let i=0; i<courses.length; i++){
      console.log("course: ", courses[i]);
      //units
      for(let j=0; j<courses[i].units.length; j++){
        console.log("unit: ", courses[i].units[j]);

        //lessons
        for(let k=0; k<courses[i].units[j].lessons.length; k++){
          console.log("lesson: ", courses[i].units[j].lessons[k]);
        }
      }
    }
    
  }, [username, courses]);

  //loading UI
  if(!isAuthenticated){
    return <div>Loading...</div>
  }

  //^^ DONE checking that user is authenticated



  const handleCourseClick = (courseTitle) => {
    navigate(`/courses/${courseTitle}`);
  };

  return (
    <main>
      <h1>Welcome {username} !</h1>
      <LogoutBtn/>
      <CreateCourseForm/>
      <h3>Courses you are taking:</h3>
      <div className="courses-container">
        {courses.map(course => (
          <div 
            key={course} 
            className="course-card" 
            onClick={() => handleCourseClick(course.title)}>
            <h4>{course.title}</h4>
            <p>{course.description}</p>
          </div>
        ))}
      </div>
    </main>
  );
};

export default Body;
