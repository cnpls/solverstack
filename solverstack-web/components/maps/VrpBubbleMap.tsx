import MapAtlas from "./MapAtlas";
import MapLine from "./MapLine";
import MapCircle from "./MapCircle";
import { isNullIsland } from "./MapUtils";
import { geoMercator } from "d3";


const groupClassName: string = "vrp-bubble-map";
const demandCircleSize: number = 3;
const demandCircleClassName: string = "demand";
const originCircleSize: number = 6;
const originCircleClassName: string = "origin";

const VrpBubbleMap = (props) => {
    const projection = geoMercator()
        .center([props.originLon, props.originLat])
        .scale(isNullIsland(props.originLat, props.originLon) ? 100 : 600)
        .translate([ props.width / 2, props.height / 2 ]);
    
    if (!props.atlasJson) {
        return <pre>Loading...</pre>;
    }
    
    return (
        <svg
        height={props.height}
        width={props.width}>
            <g className={groupClassName}>
                <MapAtlas 
                atlasJson={props.atlasJson} 
                projection={projection} />
                {props.routes.map(r => (
                    <MapLine 
                    stops={r.stops} 
                    projection={projection} />
                ))}
                {props.demand.map(d => (
                    <MapCircle 
                    name={demandCircleClassName} 
                    lat={d.latitude} 
                    lon={d.longitude} 
                    projection={projection}
                    size={demandCircleSize} />
                ))}
                {!isNullIsland(props.originLat, props.originLon) &&
                    <MapCircle 
                    name={originCircleClassName} 
                    lat={props.originLat} 
                    lon={props.originLon} 
                    projection={projection}
                    size={originCircleSize} />
                }
            </g>
        </svg>
    );
}

export default VrpBubbleMap;