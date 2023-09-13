import React from 'react';

interface TextInputProps {
    label: string;
    id: string;
    type?: string;
    value: string;
    onChange: (value: string) => void;
    required?: boolean;
}

const TextInput: React.FC<TextInputProps> = ({
    label, id, type = 'text', value, onChange, required = true, }) => {
        
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        onChange(e.target.value);
    };

    return (
        <div>
            <label htmlFor={id}>{label}</label>
            <input
                type={type}
                id={id}
                value={value}
                onChange={handleChange}
                required={required}
            />
        </div>
    );
};

export default TextInput;
