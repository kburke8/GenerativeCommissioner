import React, { useState, useEffect } from 'react';
import './App.css';

interface Matchup {
  home_team: string;
  away_team: string;
  home_score: number;
  away_score: number;
  summary: string;
}

const App: React.FC = () => {
  const [matchups, setMatchups] = useState<Matchup[]>([]);

  useEffect(() => {
    try {
      fetch('http://127.0.0.1:5000/last_week_matchups')
        .then(response => response.json())
        .then((data: Matchup[]) => setMatchups(data));
    } catch (error) {
      console.error(error);
    }
  }, []);

  return (
    <div className="App">
      <h1>ESPN Fantasy Matchups</h1>
      <div className="matchup-container"> 
        {matchups.map((matchup, index) => (
          <div key={index} className="matchup-card">
            <div className="matchup-header">
              <div className="team-name">{matchup.home_team}</div>
              <div className="team-name">{matchup.away_team}</div>
            </div>
            <div className="matchup-header">
              <div className="score">Home Score: {matchup.home_score}</div>
              <div className="score">Away Score: {matchup.away_score}</div>
            </div>
            <div className="summary">
              <p>{matchup.summary}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
