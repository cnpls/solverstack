import { geoPath } from "d3";


const lineClassName: string = "line";
const lineFill: string = "none";
const lineStroke: string = "#0000ff";
const lineStrokeWidth: number = 2;
const lineOpacity: number = .6;

const MapLine = (props) => {
    const path = geoPath().projection(props.projection);
    const lineStrings = {type: "LineString", coordinates: props.stops};

    return (
        <path 
        className={lineClassName}
        d={path(lineStrings)}
        fill={lineFill}
        stroke={lineStroke}
        strokeWidth={lineStrokeWidth}
        opacity={lineOpacity} />
    );
}

export default MapLine;