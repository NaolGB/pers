import React from 'react';

interface PanesProps {
  primaryPane: React.ReactNode;
  secondaryPane: React.ReactNode;
}

const PanesLayout: React.FC<PanesProps> = ({ primaryPane, secondaryPane }) => {
  return (
    <div>
      <div>{primaryPane}</div>
      <div>{secondaryPane}</div>
    </div>
  );
};

export default PanesLayout;
