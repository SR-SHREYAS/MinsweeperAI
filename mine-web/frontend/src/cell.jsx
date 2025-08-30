// Cell.jsx
import React, { useState } from 'react';

export default function Cell({ cell, revealed, onClick, onRightClick }) {
  const [isAnimating, setIsAnimating] = useState(false);

  const handleClick = () => {
    if (revealed !== 0) return;
    setIsAnimating(true);
    onClick();
  };

  return (
    <div
      className={`cell 
        ${revealed === 1 ? 'revealed' : ''} 
        ${revealed === 2 ? 'flag' : ''}
        ${isAnimating ? 'pulse' : ''}
        ${cell === -1 && revealed === 1 ? 'mine' : ''}
      `}
      onClick={handleClick}
      onContextMenu={(e) => {
        e.preventDefault();
        onRightClick();
      }}
      onAnimationEnd={() => setIsAnimating(false)}
    >
      {revealed === 1 && cell > 0 && (
        <span className={`number-${cell}`}>{cell}</span>
      )}
      {revealed === 1 && cell === -1 && '💣'}
      {revealed === 2 && '🚩'}
    </div>
  );
}
