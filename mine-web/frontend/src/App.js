import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import Confetti from 'react-confetti';

function App() {
  const [gameState, setGameState] = useState(null);
  const [difficulty, setDifficulty] = useState('medium');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showConfetti, setShowConfetti] = useState(false);
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  const difficulties = {
    easy: { rows: 9, cols: 9, mines: 10 },
    medium: { rows: 16, cols: 16, mines: 40 },
    hard: { rows: 16, cols: 30, mines: 99 }
  };

  // Handle window resize for confetti
  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const startGame = async () => {
    setLoading(true);
    setError(null);
    setShowConfetti(false);
    try {
      const config = difficulties[difficulty];
      const response = await axios.post('/start', config);
      setGameState(response.data);
    } catch (err) {
      setError('Failed to start game. Is the backend running?');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const revealCell = async (x, y) => {
    if (!gameState || gameState.game_over || gameState.revealed[x][y]) return;
    
    try {
      const response = await axios.post('/reveal', { x, y });
      setGameState(response.data);

      if (response.data.result === "win") {
        setShowConfetti(true);
      } else if (response.data.result === "mine") {
        revealAllMines();
      }
    } catch (err) {
      console.error('Error revealing cell:', err);
    }
  };

  const flagCell = async (e, x, y) => {
    e.preventDefault();
    if (!gameState || gameState.game_over) return;
    
    try {
      const response = await axios.post('/flag', { x, y });
      setGameState(response.data);
    } catch (err) {
      console.error('Error flagging cell:', err);
    }
  };

  const revealAllMines = () => {
    const updatedGame = { ...gameState };
    updatedGame.grid.forEach((row, x) => {
      row.forEach((cell, y) => {
        if (cell === -1) updatedGame.revealed[x][y] = 1;
      });
    });
    setGameState(updatedGame);
  };

  const getCellColor = (value) => {
    const colors = ['', 'blue', 'green', 'red', 'darkblue', 'brown', 'teal', 'black', 'gray'];
    return value === -1 ? 'red' : colors[value] || 'white';
  };

  const getCellContent = (cell, revealed) => {
    if (revealed === 1) {
      return cell === -1 ? '💣' : cell > 0 ? cell : '';
    } else if (revealed === 2) {
      return '🚩';
    }
    return '';
  };

  return (
    <div className="App">
      {showConfetti && (
        <Confetti
          width={windowSize.width}
          height={windowSize.height}
          recycle={false}
          numberOfPieces={500}
        />
      )}

      <h1>Minesweeper</h1>
      
      <div className="controls">
        <select 
          value={difficulty} 
          onChange={(e) => setDifficulty(e.target.value)}
          disabled={loading}
        >
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
        <button onClick={startGame} disabled={loading}>
          {loading ? 'Starting...' : 'New Game'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {gameState?.grid ? (
        <div className="board" style={{
          gridTemplateColumns: `repeat(${gameState.cols}, 30px)`
        }}>
          {gameState.grid.map((row, x) =>
            row.map((cell, y) => (
              <div
                key={`${x}-${y}`}
                className={`cell ${gameState.revealed[x][y] ? 'revealed' : ''} ${
                  gameState.revealed[x][y] === 2 ? 'flagged' : ''
                }`}
                style={{
                  backgroundColor: gameState.revealed[x][y] === 1
                    ? getCellColor(cell)
                    : gameState.revealed[x][y] === 2
                    ? 'lightgreen'
                    : '#ccc',
                  color: cell > 0 ? 'white' : 'black'
                }}
                onClick={() => revealCell(x, y)}
                onContextMenu={(e) => flagCell(e, x, y)}
              >
                {getCellContent(cell, gameState.revealed[x][y])}
              </div>
            ))
          )}
        </div>
      ) : (
        !loading && <div className="message">Click "New Game" to start</div>
      )}

      {gameState?.game_over && (
        <div className={`game-message ${gameState.win ? 'victory' : 'defeat'}`}>
          {gameState.win ? '🎉 You Won!' : '💥 Game Over!'}
        </div>
      )}
    </div>
  );
}

export default App;
