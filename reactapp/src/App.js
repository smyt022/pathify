import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import MainPage from './MainPage';
import Signup from './Signup';
import Login from './Login';
import CourseDetail from './CourseDetail.js';
import LessonDetail from './LessonDetail.js';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/courses/:courseTitle/lesson/:lessonTitle" element={<LessonDetail />} />
          <Route path="/courses/:courseTitle" element={<CourseDetail />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
