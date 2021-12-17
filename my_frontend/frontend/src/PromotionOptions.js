import './PromotionOptions.css';


function option(move, color, onClick) {

    const piece_letter = "pnbrqk"[move.end_type];
    const background = `url(/media/${color}${piece_letter}.png)`;
    const style = {};
    if (color !== "") {
        style["backgroundImage"] = background;
    }

    return (
        <div
            style={style}
            onClick={() => onClick(move)}
            className="option"
        >
            
        </div>
    );
}


function PromotionOptions({promotion_moves, color, onClick}) {

    const rows = promotion_moves.map(move => option(move, color, onClick));

    return (
        <div className="PromotionOptions">{rows}</div>
    );
}


export default PromotionOptions;
