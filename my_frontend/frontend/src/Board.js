
import './Board.css';
import { arr_eq } from "./utils";


function square(x, y, state) {
    const classes = [""];
    const at_square = state.board[x][y];
    if (arr_eq([x, y], state.selected_square)) {
        classes.push("selected");
    }
    if (x % 2 === y % 2) {
        classes.push("black-square");
    } else {
        classes.push("white-square");
    }

    let color = "";
    if (at_square !== "") {
        if (at_square === at_square.toUpperCase()) {
            color = "w";
        } else {
            color = "b";
        }
    }
    const piece_letter = at_square.toLowerCase();
    const background = `url(/media/${color}${piece_letter}.png)`;
    const style = {};
    if (color !== "") {
        style["backgroundImage"] = background;
    }

    const inner_classes = [];
    if (state.possible_moves.filter(m => arr_eq(m.to, [x, y])).length > 0) {
        inner_classes.push("move-to");
    }
    if (color !== "") {
        inner_classes.push("piece-here");
    }

    const piece = <div className={inner_classes.join(" ")} style={style}></div>;
    
    return (
    <div id={"square-" + x + "-" + y }
        className={classes.join(" ")}
        onClick={() => state.click_square(x, y)}>
        {piece}
    </div>);
}

function row(y, state) {
    return [...Array(8).keys()].map(x => <td key={"col-" + x}>{square(x, y, state)}</td>);
}


function Board({state}) {

    const rows = [...Array(8).keys()].map(y => <tr key={"row-" + y}>{row(y, state)}</tr>);

    return (
        <table border="1" className="board-table">
            <tbody>
                {rows}
            </tbody>
        </table>
    );
}


export default Board;
