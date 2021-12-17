import logo from './logo.svg';
import './App.css';
import Board from './Board.js';
import PromotionOptions from './PromotionOptions.js';
import { useEffect, useState } from 'react';
import { range, arr_eq, parseMoveString, unparseMove } from './utils';

// const main_url = "http://192.168.1.19:5000";
const main_url = "https://hamitos-chessbot.herokuapp.com"

function App() {
    const [key, setKey] = useState(null);
    const [board, setBoard] = useState(range(8).map(_ => range(8).map(_ => "")));
    const [possible_moves, setPossibleMoves] = useState([]);
    const [selected_square, setSelectedSquare] = useState(null);
    const [last_move, setLastMove] = useState(null);
    const [promotion_moves, setPromotionMoves] = useState([]);

    useEffect(() => {
        fetch(main_url + "/start_game")
            .then(res => res.json())
            .then(
                (res) => {
                    console.log("Stated game", res)
                    setKey(res.key);
                    setBoard(res.board);
                    setPossibleMoves(res.possible_moves.map(parseMoveString))
                }
            );
    }, []);
    
    useEffect(() => {
        console.log("Doing move, ", last_move);
        fetch(main_url + "/do_move", {
            method: "post",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                key: key,
                move: last_move
            })
        })
            .then(res => res.json(), err => { console.log("ERROR", err) })
            .then((res => {
                console.log("Got back repspose for move, ", last_move, res);
                setBoard(res.board);
                setPossibleMoves(res.possible_moves.map(parseMoveString));
                setSelectedSquare(null);
            }));
    }, [last_move]);

    function do_move(move) {
        const from_type = board[move.from[0]][move.from[1]];
        if (from_type.toUpperCase() == from_type) {
            board[move.to[0]][move.to[1]] = "PNBRQK"[move.end_type]
        } else {
            board[move.to[0]][move.to[1]] = "pnbrqk"[move.end_type]
        }
        board[move.from[0]][move.from[1]] = "";
        setBoard(board);
        setPossibleMoves([]);
        setSelectedSquare(null);
        setPromotionMoves([]);
        const move_str = unparseMove(move);
        setLastMove(move_str);
    }

    function click_square(x, y) {

        setPromotionMoves([]);

        if (selected_square === null) {
            setSelectedSquare([x, y]);
            return;
        }

        const selected_moves = possible_moves.filter(move => arr_eq(move.from, selected_square) && arr_eq(move.to, [x, y]));

        if (selected_moves.length < 1) {
            setSelectedSquare([x, y]);
            return;
        }

        if (selected_moves.length > 1) {
            // pawn promotion
            setPromotionMoves(selected_moves);
            return;
        }

        // todo: on castle the rook only moves after the other players turn.
        // todo: remove en passant pawn.
        const move = selected_moves[0];
        do_move(move);
    }

    function choose_promotion(move) {
        do_move(move);

    }

    let show_moves = possible_moves.slice();
    show_moves = show_moves.filter(move => arr_eq(move.from, selected_square))
    
    if (promotion_moves.length > 0) {
        show_moves = promotion_moves;
    }
    

    const state = {
        board: board,
        possible_moves: show_moves,
        selected_square: selected_square,
        click_square: click_square
    };

    console.log("state", state)

    return (
        <div className="App">
            <header className="App-header">
                <div className="main">
                    <PromotionOptions
                        promotion_moves={promotion_moves}
                        color={'w'}
                        onClick={choose_promotion}/>
                    <Board
                        state={state}
                    />
                </div>
            </header>
        </div>
    );
}

export default App;
