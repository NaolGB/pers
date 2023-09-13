// src/components/AppRouter.tsx
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginPage from '../pages/user_management/LoginPage';

const AppRouter: React.FC = () => {
  return (
    <BrowserRouter>
        <Routes>
            <Route path="user/login" element={<LoginPage/>} />
        </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;
