

function range(i) {
    return [...Array(8).keys()]
}

function arr_eq(arr1, arr2) {
    return arr1 && arr2 && arr1.length === arr2.length && arr1.every((x, i) => x === arr2[i])
}

function parseMoveString(move_str) {
    const [fx, fy, tx, ty, ex, ey, et] = move_str.split(" ").map(s => parseInt(s));
    return {
        from: [fx, fy],
        to: [tx, ty],
        eaten: [ex, ey],
        end_type: et
    }
}

function unparseMove(move) {
    return [move.from[0], move.from[1], move.to[0], move.to[1], move.eaten[0], move.eaten[1], move.end_type].join(" ");
}

export {
    range,
    arr_eq,
    parseMoveString,
    unparseMove
}
