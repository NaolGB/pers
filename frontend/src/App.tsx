import React, {useState} from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/user_management/LoginPage';
import Panes from './components/Panes';


function App() {

  const [activeComponent, setActiveComponent] = useState<React.ReactNode | null>(null);

  return (
    <BrowserRouter>
        <Routes>
            <Route path="user/login" element={<LoginPage/>}>
              <Panes
                primaryPane={null}
                secondaryPane={<LoginPage />}
              />
            </Route>
        </Routes>
    </BrowserRouter>
  );
}

export default App;
