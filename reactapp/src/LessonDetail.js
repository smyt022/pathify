import React from 'react';
import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './neonAesthetic.css'; // css

const BackBtn = ({courseTitle}) => {
  const navigate = useNavigate();

  const goBack = () => {
    navigate(`/courses/${courseTitle}`);
  }

  return (
    <button className="buttonStyleOrange" onClick={goBack}>back</button>
  );
}

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
    fetch('/api/logout/', {
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

const LessonDetails = () => {
    const { courseTitle, lessonTitle } = useParams();

    //CHECKING THAT USER IS AUTHENTICATED
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const navigate = useNavigate();
    const [username, setUsername] = useState(""); //for saving the current logged in user's username
    const [lesson_state, setLesson] = useState({}); //for saving the current logged in user's array of courses
    
    //json format with attributes: title, description

    useEffect(() => {
        fetch('/api/user_info/')
        .then(response => response.json())
        .then(data => {
        if (data.is_authenticated){
            console.log("backend says user is authenticated");
            setIsAuthenticated(true);
            setUsername(data.username);

            //iterate thru courses and lessons to save specific lesson we are looking at
            for (let i=0; i<data.courses.length; i++){

                //iterate thru units 
                for (let j=0; j<data.courses[i].units.length; j++){

                    //iterate thru lessons
                    for (let x=0; x<data.courses[i].units[j].lessons.length; x++){
                        let lesson = {
                            title: data.courses[i].units[j].lessons[x].title,
                            description: data.courses[i].units[j].lessons[x].description,
                            reading_material: data.courses[i].units[j].lessons[x].reading_material,
                            video_link: data.courses[i].units[j].lessons[x].video_link,
                            practice_exercise: data.courses[i].units[j].lessons[x].practice_exercise,
                        }

                        //TESTING
                        //console.log("passing first if statement case: "+String(lesson.title === lessonTitle));
                        //console.log("passing second if statement case: "+String(data.courses[i].title === courseTitle));

                        console.log("lesson.title(backend):"+lesson.title+".");
                        console.log("lessonTitle(url):"+lessonTitle+".");

                        //if lesson found, and is from the course we are looking at, save lesson info
                        if(
                            lesson.title === lessonTitle && 
                            data.courses[i].title === courseTitle
                        ){
                            setLesson(lesson); //save lesson
                            console.log("Found lesson: "+lesson);
                        }
                    }
                }
            }

        } else {
            console.log("backend says user is not authenticated");
            navigate('/login/');
        }
        })
        .catch(error => {
        console.error('Error checking user authentication:', error);
        });
    }, [navigate, courseTitle, lessonTitle]);

    //loading UI
    if(!isAuthenticated){
        return <div>Loading...</div>
    }

    //^^ DONE checking that user is authenticated

    return (
        <main className="lesson-details-container">
            <h1>Welcome {username} !</h1>
              <div>
                <LogoutBtn/>
                <BackBtn courseTitle={courseTitle} />
              </div>
            <h2 className="course-title">Course: {courseTitle}</h2>
            <h3 className="lesson-title">Lesson: { lesson_state.title } </h3>
            <p className="lesson-description">{lesson_state.description}</p>
            <div className="reading-material">
                <h4>Reading Material</h4>
                <p>{lesson_state.reading_material}</p>
            </div>
            <div className="video-link">
                <h4>Video</h4>
                {lesson_state.video_link && (
                    <iframe
                        width="560"
                        height="315"
                        src={lesson_state.video_link.replace('watch?v=', 'embed/')}
                        title={lesson_state.title}
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowFullScreen
                        className="video-frame"
                    ></iframe>
                )}
            </div>
            <div className="practice-exercise">
                <h4>Practice Exercise</h4>
                <p>{lesson_state.practice_exercise}</p>
            </div>
        </main>
    );
};

export default LessonDetails;
