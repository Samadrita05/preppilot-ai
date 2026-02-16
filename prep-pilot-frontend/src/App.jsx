import { Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import Interviews from "./pages/Interviews";
import Questions from "./pages/Questions";
import Answer from "./pages/Answer";
import Report from "./pages/Report";
import Profile from "./pages/Profile";
import Settings from "./pages/Settings";

export default function App() {
  return (
    <Routes>
      {/* Auth */}
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      
     <Route path="/dashboard" element={<Layout />}>
      <Route index element={<Dashboard />} />
      <Route path="profile" element={<Profile />} />
      <Route path="settings" element={<Settings />} />
    </Route>
      <Route path="/interviews" element={<Interviews />} />
      <Route path="/questions/:interviewId" element={<Questions />} />
      <Route path="/answer/:questionId" element={<Answer />} />
      <Route path="/report/:interviewId" element={<Report />} />
      
       
      {/* Default */}
      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  );
}
