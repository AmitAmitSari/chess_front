import logo from './logo.svg';
import './App.css';
import Board from './Board.js';
import PromotionOptions from './PromotionOptions.js';
import { useEffect, useState } from 'react';
import socketIOClient from 'socket.io-client';
import { range, arr_eq, parseMoveString, unparseMove } from './utils';

// todo: Use environment variables
const develop = false;
const main_url = develop ? "http://127.0.0.1:5000" : "https://hamitos-chessbot.herokuapp.com";

function App() {
    const [socket, setSocket] = useState(null);
    const [board, setBoard] = useState(range(8).map(_ => range(8).map(_ => "")));
    const [possible_moves, setPossibleMoves] = useState([]);
    const [selected_square, setSelectedSquare] = useState(null);
    const [last_move, setLastMove] = useState(null);
    const [promotion_moves, setPromotionMoves] = useState([]);

    useEffect(() => {
        const socket = socketIOClient(main_url);

        socket.on("connect", (key) => {
            console.log("Connected");
        });

        socket.on("board", new_board => {
            console.log("Got board");
            setBoard(new_board);
        });

        socket.on("possible_moves", possible_moves => {
            console.log("possible_moves");
            setPossibleMoves(possible_moves.map(parseMoveString));
            setLastMove(null);
        });

        console.log("Emitting start_game")
        socket.emit("start_game");

        setSocket(socket);
    }, []);

    function do_move(move) {
        console.log("Doing move, ", move);
        const from_type = board[move.from[0]][move.from[1]];
        if (from_type.toUpperCase() === from_type) {
            board[move.to[0]][move.to[1]] = "PNBRQK"[move.end_type]
        } else {
            board[move.to[0]][move.to[1]] = "pnbrqk"[move.end_type]
        }
        board[move.from[0]][move.from[1]] = "";
        setBoard(board);

        setPossibleMoves([]);
        setSelectedSquare(null);
        setPromotionMoves([]);
        setLastMove(move);
        const move_str = unparseMove(move);
        socket.emit("do_move", { move: move_str });
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

        // todo: on castle the rook only moves after pinging server.
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
        click_square: click_square,
        last_move: last_move,
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
