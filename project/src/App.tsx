import React, { useState, useEffect, useCallback } from 'react';
import { ArrowUp, ArrowDown, ArrowLeft, ArrowRight, Gamepad2 } from 'lucide-react';

type Direction = 'UP' | 'DOWN' | 'LEFT' | 'RIGHT';
type Position = { x: number; y: number };

const GRID_SIZE = 20;
const CELL_SIZE = 20;
const INITIAL_SPEED = 150;
const SPEED_INCREASE = 5;

function App() {
  const [snake, setSnake] = useState<Position[]>([{ x: 10, y: 10 }]);
  const [food, setFood] = useState<Position>({ x: 15, y: 15 });
  const [direction, setDirection] = useState<Direction>('RIGHT');
  const [gameOver, setGameOver] = useState(false);
  const [score, setScore] = useState(0);
  const [highScore, setHighScore] = useState(0);
  const [speed, setSpeed] = useState(INITIAL_SPEED);
  const [isPaused, setIsPaused] = useState(false);

  const generateFood = useCallback(() => {
    const newFood = {
      x: Math.floor(Math.random() * GRID_SIZE),
      y: Math.floor(Math.random() * GRID_SIZE),
    };
    return newFood;
  }, []);

  const resetGame = useCallback(() => {
    setSnake([{ x: 10, y: 10 }]);
    setFood(generateFood());
    setDirection('RIGHT');
    setGameOver(false);
    setScore(0);
    setSpeed(INITIAL_SPEED);
    setIsPaused(false);
  }, [generateFood]);

  const checkCollision = useCallback((head: Position) => {
    if (
      head.x < 0 ||
      head.x >= GRID_SIZE ||
      head.y < 0 ||
      head.y >= GRID_SIZE
    ) {
      return true;
    }

    for (let i = 1; i < snake.length; i++) {
      if (head.x === snake[i].x && head.y === snake[i].y) {
        return true;
      }
    }

    return false;
  }, [snake]);

  const moveSnake = useCallback(() => {
    if (gameOver || isPaused) return;

    const head = { ...snake[0] };
    switch (direction) {
      case 'UP':
        head.y -= 1;
        break;
      case 'DOWN':
        head.y += 1;
        break;
      case 'LEFT':
        head.x -= 1;
        break;
      case 'RIGHT':
        head.x += 1;
        break;
    }

    if (checkCollision(head)) {
      setGameOver(true);
      if (score > highScore) {
        setHighScore(score);
      }
      return;
    }

    const newSnake = [head, ...snake];
    if (head.x === food.x && head.y === food.y) {
      setFood(generateFood());
      setScore(prev => prev + 10);
      setSpeed(prev => Math.max(prev - SPEED_INCREASE, 50));
    } else {
      newSnake.pop();
    }

    setSnake(newSnake);
  }, [snake, direction, food, generateFood, gameOver, isPaused, checkCollision, score, highScore]);

  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (e.key === ' ') {
        setIsPaused(prev => !prev);
        return;
      }

      if (gameOver) {
        resetGame();
        return;
      }

      switch (e.key) {
        case 'ArrowUp':
          if (direction !== 'DOWN') setDirection('UP');
          break;
        case 'ArrowDown':
          if (direction !== 'UP') setDirection('DOWN');
          break;
        case 'ArrowLeft':
          if (direction !== 'RIGHT') setDirection('LEFT');
          break;
        case 'ArrowRight':
          if (direction !== 'LEFT') setDirection('RIGHT');
          break;
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [direction, gameOver, resetGame]);

  useEffect(() => {
    const gameLoop = setInterval(moveSnake, speed);
    return () => clearInterval(gameLoop);
  }, [moveSnake, speed]);

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center">
      <div className="mb-4 flex items-center gap-2">
        <Gamepad2 className="w-6 h-6" />
        <h1 className="text-2xl font-bold">Snake Game</h1>
      </div>

      <div className="mb-4 flex gap-8">
        <div className="text-center">
          <p className="text-gray-400">Score</p>
          <p className="text-xl font-bold">{score}</p>
        </div>
        <div className="text-center">
          <p className="text-gray-400">High Score</p>
          <p className="text-xl font-bold">{highScore}</p>
        </div>
      </div>

      <div 
        className="relative bg-gray-800 rounded-lg overflow-hidden"
        style={{
          width: GRID_SIZE * CELL_SIZE,
          height: GRID_SIZE * CELL_SIZE,
        }}
      >
        {snake.map((segment, index) => (
          <div
            key={index}
            className="absolute bg-green-500 rounded-sm"
            style={{
              width: CELL_SIZE - 1,
              height: CELL_SIZE - 1,
              left: segment.x * CELL_SIZE,
              top: segment.y * CELL_SIZE,
              backgroundColor: index === 0 ? '#22c55e' : '#4ade80',
            }}
          />
        ))}
        <div
          className="absolute bg-red-500 rounded-full"
          style={{
            width: CELL_SIZE - 1,
            height: CELL_SIZE - 1,
            left: food.x * CELL_SIZE,
            top: food.y * CELL_SIZE,
          }}
        />
      </div>

      {(gameOver || isPaused) && (
        <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="text-center bg-gray-800 p-8 rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold mb-4">
              {gameOver ? 'Game Over!' : 'Paused'}
            </h2>
            <p className="mb-4">
              {gameOver
                ? `Final Score: ${score}`
                : 'Press SPACE to resume'}
            </p>
            {gameOver && (
              <button
                onClick={resetGame}
                className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded"
              >
                Play Again
              </button>
            )}
          </div>
        </div>
      )}

      <div className="mt-8 text-gray-400 text-center">
        <p className="mb-2">Controls</p>
        <div className="flex gap-2 justify-center">
          <ArrowUp className="w-6 h-6" />
          <ArrowDown className="w-6 h-6" />
          <ArrowLeft className="w-6 h-6" />
          <ArrowRight className="w-6 h-6" />
        </div>
        <p className="mt-2">SPACE to pause</p>
      </div>
    </div>
  );
}

export default App;