import React, { useState } from 'react';
import TextInput from '../../components/TextInputs';

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleUsernameChange = (value: string) => {
    setUsername(value);
  };

  const handlePasswordChange = (value: string) => {
    setPassword(value);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('hi')
  };

  return (
    <div>
        Login
      <form onSubmit={handleSubmit}>
        <TextInput
          label="Username:"
          id="username"
          value={username}
          onChange={handleUsernameChange}
          required
        />
        <TextInput
          label="Password:"
          id="password"
          type="password"
          value={password}
          onChange={handlePasswordChange}
          required
        />
        <div>
          <button type="submit">Login</button>
        </div>
      </form>
    </div>
  );
};

export default LoginPage;
